from app.controllers.admin_routes import *
# from app.controllers.admin_routes.admin_routes import *

from app.allImports import *
from app.models.models import *
from peewee import *
# from app import app
from app.logic.authorizedUser import AuthorizedUser
from app.logic import functions
from app.logic.functions import map_unavailable_rooms, find_avail_unavailable_rooms
from app.logic.courseLogic import find_crosslist_via_id
import json
from functools import wraps
from app import load_config
from app.logic.authorizedUser import AuthorizedUser, must_be_admin


#Term modal
@admin_bp.route("/roomResolutionTerm", methods=["GET"])
@must_be_admin
def roomResolutionTerm():
    terms = Term.select()
    dummy = True
    cfg = load_config()
    return render_template("selectTerm.html", allTerms=terms, dummy=dummy, cfg = cfg)


#Room Resolution Page
@admin_bp.route("/roomResolution/<termCode>", methods=["GET"])
@must_be_admin
def roomResolution(termCode):
    # Creating the UI
    courses = Course.select().where(Course.rid == None, Course.term==termCode, Course.schedule.is_null(False))
    cfg = load_config()
    au = AuthorizedUser()
    return render_template("roomResolution.html",  isAdmin=au.user.isAdmin, courses=courses, termcode=termCode, cfg = cfg)


#Room Resolution View
@admin_bp.route("/roomResolutionView/<termCode>/<cid>", methods=["GET"])
@must_be_admin
def roomResolutionView(termCode,cid):
    # print("Starting Room Resolution edits")
    try:
        roompreference = RoomPreferences.get(RoomPreferences.course==cid)  #cid==5
        if (roompreference.pref_1 == None):
            flash("Course has no preferences assigned.") #If course has no preferences indicated
    except Exception as e:
        roompreference = RoomPreferences(course=cid, any_Choice = "any").save()
        roompreference = RoomPreferences.get(RoomPreferences.course==cid)
        flash("Course has no preferences assigned.")
    #Pulling data
    buildings = Building.select()
    instructors = InstructorCourse.select().where(InstructorCourse.course==cid)
    bannercourses = BannerCourses.select()
    curr_course = Course.get(Course.cId==cid)
    #will give an error if schedule.sid is None
    schedule = curr_course.schedule.sid

    daysQuery = ScheduleDays.select().where(ScheduleDays.schedule==schedule)
    days = [i for i in daysQuery]

    course_capacity = 1 if not curr_course.capacity  else curr_course.capacity

    #find all rooms that are free during course schedule AND find rooms that are not free during a course schedule
    availablerooms, unavailablerooms = find_avail_unavailable_rooms(curr_course)
    rooms=Rooms.select().where(Rooms.rID << availablerooms)
    #map unavaile rooms to their courses
    unavailable_to_course = map_unavailable_rooms(curr_course, unavailablerooms)

    #For populating current occupant in course's preferences aka Course B aka Conflicting Course!
    confcourse = RoomPreferences.get(RoomPreferences.course == cid) # grab the A course's preferences
    sch1startTime = confcourse.course.schedule.startTime            # grab the A course's schedule start time
    sch1endTime = confcourse.course.schedule.endTime                # grab the A course's schedule end time
    rp = RoomPreferences.get(RoomPreferences.course == cid)         # get the A course's room preferences again (not needed, but used both variables)
    scheduleDays = ScheduleDays.get(ScheduleDays.schedule == confcourse.course.schedule.sid)

    conflicts_query = """
			SELECT
			  cid
			FROM
			  course as c
			  INNER JOIN bannerschedule as bs ON bs.sid = c.schedule_id
			WHERE
			  c.rid_id = {0}
			  AND bs.endTime > \"{1}\" AND bs.startTime < \"{2}\";
			      """  #For course B


    '''    conflicts_query = """   SELECT cid
                            FROM `course` as c
                            INNER JOIN `bannerschedule` as bs
                            ON `bannerschedule`.sid = `course`.schedule_id
                            WHERE `course`.rid_id = {0} AND `bannerschedule`.endTime > \"{1}\" AND `bannerschedule`.startTime < \"{2}\";"""  #For course B
    '''
    cclist = []  # holds all conflicting courses queries to be executed later

    # "A" course's schedule
    aCourseSchedule = scheduleDays.day
    #check which preference we're on, and append to cclist
    if rp.pref_1:
        cclist.append(conflicts_query.format(rp.pref_1.rID,sch1startTime,sch1endTime)) #comparing course A to B
        if rp.pref_2:
            cclist.append(conflicts_query.format(rp.pref_2.rID,sch1startTime,sch1endTime))
            if rp.pref_3:
                cclist.append(conflicts_query.format(rp.pref_3.rID,sch1startTime,sch1endTime))

    conflictingroomdata = []        # data about one B Course
    preferences = dict()            # dictionary to hold all B courses


    if cclist:                                        #if there are conflicting courses
        # cclist = [conflictingcoursequery1, conflictingcoursequery2, conflictingcoursequery3]
        for cc in cclist:
            cursor = mainDB.execute_sql(cc)                 # execute each query
            for conflict in cursor:
                conflictingroomdata.append(conflict[0])     # append results of query to list of actual B courses
        #pulling specific data from conflicting course to populate preference tabs
        for idx in range(len(conflictingroomdata)):
            pref_info = dict()                                          # to hold course info
            cc = Course.get(Course.cId == conflictingroomdata[idx])     # get all data baout the course
            bScheduleDays = ScheduleDays.get(ScheduleDays.schedule == cc.schedule)
            for letter in aCourseSchedule:
                if letter in bScheduleDays.day:
                    pref_inst = InstructorCourse.select().where(InstructorCourse.course==conflictingroomdata[idx])  # get instructor information
                    full_name = None

                    for inst in pref_inst:
                        full_name = inst.username.firstName + " " +inst.username.lastName       # if there's an instructor, add name to full_name

                    pref = 'pref'+ str(idx + 1)         # which pref?
                    current_course = str(cc.prefix.prefix) + " " + str(cc.bannerRef.number) + " " + str(cc.bannerRef.ctitle) # String of info about B course
                    pref_info['course_name']=current_course         # add to pref_info
                    pref_info['instructor']=full_name               # add instructor to pref info
                    pref_info['cid']=cc.cId                         # add cId to pref_info
                    pref_info["course_notes"]=cc.notes if cc.notes else None              # course notes
                    pref_info['startTime']=cc.schedule.startTime    #adds course B's times and days to pref_info
                    pref_info['endTime']=cc.schedule.endTime
                    pref_info['days']= bScheduleDays.day

                    (rp1, created) = RoomPreferences.get_or_create(course = cc.cId)
                    pref_info['notes']=rp1.notes
                    preferences[pref] = pref_info
                    break
    course_to_crosslist=find_crosslist_via_id(cid)
    #Actual conflicting course(S) {'pref1': {'instructor': u'Scott Heggen', 'course_name': 'CSC 236 Data Structures', 'cid': 1}}
    cfg = load_config()
    return render_template("roomResolutionView.html",
                            roompreference=roompreference,
                            available_rooms=rooms,
                            course_to_crosslist = course_to_crosslist,
                            unavailable_to_course =unavailable_to_course,
                            buildings=buildings,
                            instructors = instructors,
                            courses=curr_course,
                            bannercourses=bannercourses,
                            preferences=preferences,
                            termcode=termCode,
                            days=days,
                            cfg = cfg
                        )



def decorator(func):
    @wraps(func)
    def wrapper(cid, *args, **kwargs):
        try:
            course = Course.get(Course.cId==cid)
            data = request.form
            response = func(course, data)
            if course.crossListed:
                assign_or_unassign_cc(course, data['roomID'])
            #if response is not None, updateRoom function was passed as callback, thus redirect user
            if response:
                return json.dumps(response)
            flash("Your changes have been saved!")
            return json.dumps({"success": 1})
        except:
            flash("An error has occurred. Please try again.","error")
            return json.dumps({"error":0})
    return wrapper

#Controller for Assign button (roomResolutionView) sending the assignment of a course to a room to database
#Assign to AVAILABLE ROOMS ONLY
@admin_bp.route("/assignRoom/<cid>", methods=["POST"])
@decorator
@must_be_admin
def assignRoom(course, data):
    '''
    Assign Available/Unavailable room to a course

    params:
      course: new_course
      data: form data
    '''
    course.rid = data["roomID"]
    course.save()

#Assign to an OCCUPIED room, remove current occupant: Save and go to displayed course
@admin_bp.route("/updateRoom/<cid>", methods=["POST"])
@decorator
@must_be_admin
def updateRoom(course, data):
    '''Reassign room to a different course. Remove the current one

       params:
         course: new_course
         data: form data
    '''
    course.rid = data["roomID"]
    course.save()
    conflict_course = Course.get(Course.cId == data['ogCourse'])
    conflict_course.rid=None
    conflict_course.save()
    if(conflict_course.crossListed):
        assign_or_unassign_cc(conflict_course, None)
    return {"url":conflict_course.cId}


def assign_or_unassign_cc(course, roomId):
    '''Unassign remove from the children of Crosslisted Course

       params:
         course: crosslisted course
         roomId: room
    '''
    qs = CrossListed.select().where(CrossListed.courseId == course.cId)
    if qs.exists:
        for cross_course in qs:
            #skip the parent itself
            if cross_course.crosslistedCourse.cId != course.cId:
                cross_course.crosslistedCourse.rid = roomId
                cross_course.crosslistedCourse.save()
