from allImports import *
from models import *
from peewee import *
from app import app
from app.logic.authorization import must_be_admin
from app.logic import functions
import json

# Term modal


@app.route("/roomResolutionTerm", methods=["GET"])
@must_be_admin
def roomResolutionTerm():
    terms = Term.select()
    dummy = True
    return render_template("selectTerm.html", allTerms=terms, dummy=dummy)


# Room Resolution Page
@app.route("/roomResolution/<termCode>", methods=["GET"])
@must_be_admin
def roomResolution(termCode):
    # Creating the UI
    courses = Course.select().where(
        Course.rid is None,
        Course.term == termCode,
        Course.schedule.is_null(False))
    return render_template(
        "roomResolution.html",
        isAdmin=g.user.isAdmin,
        courses=courses,
        termcode=termCode)


# Room Resolution View
@app.route("/roomResolutionView/<termCode>/<cid>", methods=["GET"])
def roomResolutionView(termCode, cid):
    try:
        roompreference = RoomPreferences.get(
            RoomPreferences.course == cid)  # cid==5
        if (roompreference.pref_1 is None):
            # If course has no preferences indicated
            flash("Course has no preferences assigned.")
    except Exception as e:
        roompreference = RoomPreferences(course=cid, any_Choice="any").save()
        roompreference = RoomPreferences.get(RoomPreferences.course == cid)
        flash("Course has no preferences assigned.")
    # Pulling data
    buildings = Building.select()
    instructors = InstructorCourse.select().where(InstructorCourse.course == cid)
    bannercourses = BannerCourses.select()
    courses = Course.get(Course.cId == cid)  # Course A
    # will give an error if schedule.sid is None
    schedule = courses.schedule.sid
    days = ScheduleDays.get(ScheduleDays.schedule == schedule)
    course_capacity = 1 if not courses.capacity else courses.capacity
    # this query gets all the room ids for the course if the room is free
    # during a course schedule
    sql_query = """SELECT r1.rID, building_id FROM rooms as r1
                LEFT OUTER JOIN (SELECT c1.rid_id as r2
                FROM course c1 JOIN (SELECT sid FROM bannerschedule WHERE CAST("{0}" as TIME)
                < CAST(bannerschedule.endTime as TIME)
                AND CAST("{1}" as TIME)  > CAST(bannerschedule.startTime AS TIME)) bs1 ON c1.schedule_id = bs1.sid
                WHERE c1.rid_id IS NOT NULL AND c1.term_id = {2}) ON r1.rID = r2
                INNER JOIN building ON r1.building_id = building.bID
                WHERE r2 IS NULL AND r1.maxCapacity >= {3}
                ORDER BY building.name;""".format(
        courses.schedule.startTime, courses.schedule.endTime, courses.term.termCode, course_capacity)
    cursor = mainDB.execute_sql(sql_query)
    availablerooms = []
    for room in cursor:
        availablerooms.append(room[0])
    rooms = Rooms.select().where(Rooms.rID << availablerooms)
    # For populating current occupant in course's preferences aka Course B aka
    # Conflicting Course!
    # grab the A course's preferences
    confcourse = RoomPreferences.get(RoomPreferences.course == cid)
    # grab the A course's schedule start time
    sch1startTime = confcourse.course.schedule.startTime
    # grab the A course's schedule end time
    sch1endTime = confcourse.course.schedule.endTime
    # get the A course's room preferences again (not needed, but used both
    # variables)
    rp = RoomPreferences.get(RoomPreferences.course == cid)
    scheduleDays = ScheduleDays.get(
        ScheduleDays.schedule == confcourse.course.schedule.sid)

    conflicts_query = """   SELECT cid
                            FROM `course`
                            INNER JOIN `bannerschedule`
                            ON `bannerschedule`.sid = `course`.schedule_id
                            WHERE `course`.rid_id = {0} AND `bannerschedule`.endTime > \"{1}\" AND `bannerschedule`.startTime < \"{2}\";"""  # For course B
    cclist = []  # holds all conflicting courses queries to be executed later

    # "A" course's schedule
    aCourseSchedule = scheduleDays.day
    # check which preference we're on, and append to cclist
    if rp.pref_1:
        cclist.append(
            conflicts_query.format(
                rp.pref_1.rID,
                sch1startTime,
                sch1endTime))  # comparing course A to B
        if rp.pref_2:
            cclist.append(
                conflicts_query.format(
                    rp.pref_2.rID,
                    sch1startTime,
                    sch1endTime))
            if rp.pref_3:
                cclist.append(
                    conflicts_query.format(
                        rp.pref_3.rID,
                        sch1startTime,
                        sch1endTime))

    conflictingroomdata = []        # data about one B Course
    preferences = dict()            # dictionary to hold all B courses

    if cclist:  # if there are conflicting courses
        # cclist = [conflictingcoursequery1, conflictingcoursequery2, conflictingcoursequery3]
        for cc in cclist:
            # execute each query
            cursor = mainDB.execute_sql(cc)
            for conflict in cursor:
                # append results of query to list of actual B courses
                conflictingroomdata.append(conflict[0])
        # pulling specific data from conflicting course to populate preference
        # tabs
        for idx in range(len(conflictingroomdata)):
            # to hold course info
            pref_info = dict()
            # get all data baout the course
            cc = Course.get(Course.cId == conflictingroomdata[idx])
            bScheduleDays = ScheduleDays.get(
                ScheduleDays.schedule == cc.schedule)
            for letter in aCourseSchedule:
                if letter in bScheduleDays.day:
                    print(
                        "A course day: {0} conflicted with B course day: {1}".format(
                            letter, bScheduleDays.day))
                    pref_inst = InstructorCourse.select().where(
                        InstructorCourse.course == conflictingroomdata[idx])  # get instructor information
                    full_name = None

                    for inst in pref_inst:
                        # if there's an instructor, add name to full_name
                        full_name = inst.username.firstName + " " + inst.username.lastName

                    pref = 'pref' + str(idx + 1)         # which pref?
                    current_course = str(cc.prefix.prefix) + " " + str(cc.bannerRef.number) + " " + str(
                        cc.bannerRef.ctitle)  # String of info about B course
                    # add to pref_info
                    pref_info['course_name'] = current_course
                    # add instructor to pref info
                    pref_info['instructor'] = full_name
                    # add cId to pref_info
                    pref_info['cid'] = cc.cId

                    # adds course B's times and days to pref_info
                    pref_info['startTime'] = cc.schedule.startTime
                    pref_info['endTime'] = cc.schedule.endTime
                    pref_info['days'] = bScheduleDays.day

                    (rp1, created) = RoomPreferences.get_or_create(course=cc.cId)
                    pref_info['notes'] = rp1.notes
                    preferences[pref] = pref_info
                    break

    # Actual conflicting course(S) {'pref1': {'instructor': u'Scott Heggen',
    # 'course_name': 'CSC 236 Data Structures', 'cid': 1}}

    return render_template("roomResolutionView.html",
                           roompreference=roompreference,
                           available_rooms=rooms,
                           buildings=buildings,
                           instructors=instructors,
                           courses=courses,
                           bannercourses=bannercourses,
                           preferences=preferences,
                           termcode=termCode,
                           days=days
                           )


# Controller for Assign button (roomResolutionView) sending the assignment of a course to a room to database
# Assign to AVAILABLE ROOMS ONLY
@app.route("/assignRoom/<cid>", methods=["POST"])
def assignRoom(cid):
    '''
    Assign General Available room to a course
    params:
       int: cid: Course_Id

    '''
    try:
        data = request.form
        course = Course.get(Course.cId == cid)
        # already has a room
        if course.rid:
            course.rid = data['roomID']
            course.save()
            # print course.rid
            flash("Your changes have been saved!")
            return json.dumps({"success": 1})
        else:
            # If the course doesn't have a room
            course.rid = data['roomID']
            course.save()
            flash("Your changes have been saved!")
            return json.dumps({"success": 1})
    except BaseException:
        flash("An error has occurred. Please try again.", "error")
        return json.dumps({"success": 0})


# Assign to an OCCUPIED room, remove current occupant: Save and go to
# displayed course
@app.route("/updateRoom/<cid>", methods=["POST"])
def updateRoom(cid):
    '''Assign preference room to a course.
       Update the room id of previous course (i.e. conflict_course) to None.

       params:
         int: cid: Course_Id
    '''
    try:
        course = Course.get(Course.cId == cid)
        data = request.form
        course.rid = data['roomID']
        course.save()
        conflict_course = Course.get(Course.cId == data['ogCourse'])
        conflict_course.rid = None
        conflict_course.save()
        response = {"url": conflict_course.cId}
        return json.dumps(response)
    except BaseException:
        flash("An error has occurred. Please try again.", "error")
        return json.dumps({"error": 0})
