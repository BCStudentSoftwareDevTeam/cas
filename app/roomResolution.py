from allImports import *
from models import *
from peewee import *
from app import app
from app.logic.authorization import must_be_admin
from app.logic import functions
from app.logic.functions import get_unavailable_rooms
import json

#Term modal
@app.route("/roomResolutionTerm", methods=["GET"])
@must_be_admin
def roomResolutionTerm():
    terms = Term.select()
    dummy = True
    return render_template("selectTerm.html", allTerms=terms, dummy=dummy)
    
    
#Room Resolution Page  
@app.route("/roomResolution/<termCode>", methods=["GET"])
@must_be_admin
def roomResolution(termCode):
    # Creating the UI
    courses = Course.select().where(Course.rid == None, Course.term==termCode, Course.schedule.is_null(False))
    return render_template("roomResolution.html",  isAdmin=g.user.isAdmin, courses=courses, termcode=termCode)
    
    
#Room Resolution View
@app.route("/roomResolutionView/<termCode>/<cid>", methods=["GET"])
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
    courses = Course.get(Course.cId==cid) #Course A
    print(cid)
    print("SSS:", courses.prefix.prefix)
    #will give an error if schedule.sid is None
    schedule = courses.schedule.sid
    print(schedule)
    #days = ScheduleDays.get(ScheduleDays.schedule==schedule)
    daysQuery = ScheduleDays.select().where(ScheduleDays.schedule==schedule)
    days = [i for i in daysQuery]
    #print(days.id, days.schedule.sid)
    course_capacity = 1 if not courses.capacity  else courses.capacity 
    #this query gets all the room ids for the course if the room is free during a course schedule
    # print("Is it this query breaking?")
    daysCache = {}
    daysQuery = ScheduleDays.select()
    for days1 in daysQuery:
        if(days1.schedule_id in daysCache):
            daysCache[days1.schedule_id].append(days1.day)
        else:
            daysCache[days1.schedule_id] = [days1.day]
    print("Days cache:", daysCache)
    
    availablerooms1 = [] 
    #query 1 get all the rooms that are not assigned
    unassignedRooms = (Rooms
         .select()
         .join(Course, JOIN.LEFT_OUTER).where(Course.rid == None))
    
    for room in unassignedRooms:
        availablerooms1.append(room.rID)
        
    countme=0
    for i in unassignedRooms:
        countme+=1
    print(countme)
    
    #query 2 get all the rooms that are assigned
    counter=0
    print(courses.term.termCode)
    assignedRooms = (Rooms.select(Rooms, Course.schedule).join(Course).where(Course.term == courses.term.termCode & Course.rid.is_null(False))
                    ).distinct() #& Course.term == courses.term
                    
    assignedQuery = "SELECT DISTINCT t1.rID, t2.schedule_id FROM rooms AS t1 INNER JOIN course AS t2 ON (t1.rID = t2.rid_id) WHERE (t2.term_id = {0}  AND t2.rid_id IS NOT NULL)".format("201812")
    print(assignedQuery)
    cursor = mainDB.execute_sql(assignedQuery)
    cursorCounter = 0
    for i in cursor:

        cursorCounter += 1
    print("Count: ",  cursorCounter)
    
    
    #& Course.term == courses.term).distinct()
    print("assigned ",assignedRooms )
    rooms_cache = {}  #room and courses_schedule_id mapping 
    
    for room in cursor:
            
        if int(room[0]) in rooms_cache:
            rooms_cache[int(room[0])].append(room[1])
        else:
            rooms_cache[int(room[0])] = [room[1]]
        counter+=1
    print(rooms_cache)
    
    """
    for room in assignedRooms.naive():
        if room in rooms_cache:
            rooms_cache[room].append(room.schedule)
        else:
            rooms_cache[room] = [room.schedule]
        counter+=1
    print(rooms_cache)
    """
    #print("Hello ", courses.schedule_id)
    #print(cfg['conflicts'][courses.schedule_id])
    #if room is not conflicting, add it to available rooms
    print("Original: ", len(rooms_cache) )
    print("Before: ", len(availablerooms1))
    a_set = set(cfg['conflicts'][courses.schedule_id])
    for key in rooms_cache:
        b_set = set(rooms_cache[key]) 
        if (not a_set & b_set):
            #print("1:", a_set)
            #print("2: ", b_set)
            availablerooms1.append(key)
        else:
            if key == 66:
                print("first: ", a_set)
                print("second: ", b_set)
    print(len(availablerooms1))        
    
    
        
    #query 3 if: else conditions on the room that are assigned
    
    sql_query = """
                   SELECT r1.rID, building_id
                   FROM rooms as r1
                   LEFT OUTER JOIN (
                     SELECT c1.rid_id as r2
                     FROM course as c1
                     JOIN (
                       SELECT sid
                       FROM bannerschedule as bs
                       WHERE CAST("{0}" as TIME) < CAST(bs.endTime as TIME) 
                       AND CAST("{1}" as TIME) > CAST(bs.startTime AS TIME)) as bs1 
                     ON c1.schedule_id = bs1.sid 
                     WHERE c1.rid_id IS NOT NULL
                     AND c1.term_id = {2}) as x
                   ON r1.rID = r2
                   INNER JOIN building as b ON r1.building_id = b.bID
                   WHERE r2 IS NULL
                   AND r1.maxCapacity >= {3}
                   ORDER BY b.name;
                """.format(courses.schedule.startTime, courses.schedule.endTime,
                courses.term.termCode, course_capacity)
    print(sql_query)
    cursor = mainDB.execute_sql(sql_query)
    availablerooms = [] 
    for room in cursor:
        availablerooms.append(room[0])
    rooms=Rooms.select().where(Rooms.rID << availablerooms1)
    curr_course=courses       
    
    #unavailable rooms mapped with their courses
    unavailable_to_course=get_unavailable_rooms(curr_course, availablerooms1)
    
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
    print(courses)
    #Actual conflicting course(S) {'pref1': {'instructor': u'Scott Heggen', 'course_name': 'CSC 236 Data Structures', 'cid': 1}}
    return render_template("roomResolutionView.html", 
                            roompreference=roompreference, 
                            available_rooms=rooms,
                            unavailable_to_course =unavailable_to_course,
                            buildings=buildings, 
                            instructors = instructors, 
                            courses=courses, 
                            bannercourses=bannercourses,
                            preferences=preferences,
                            termcode=termCode,
                            days=days
                        )
                        

#Controller for Assign button (roomResolutionView) sending the assignment of a course to a room to database
#Assign to AVAILABLE ROOMS ONLY
@app.route("/assignRoom/<cid>", methods=["POST"])

def assignRoom(cid):
    '''
    Assign General Available room to a course
    params:
       int: cid: Course_Id

    '''
    try:
        data = request.form
        course=Course.get(Course.cId==cid)
        #already has a room
        if course.rid:
            course.rid = data['roomID']
            course.save()
            flash("Your changes have been saved!") 
            return json.dumps({"success": 1})
        else:
            #If the course doesn't have a room
            course.rid = data['roomID']
            course.save()
            flash("Your changes have been saved!") 
            return json.dumps({"success": 1})
    except:
        flash("An error has occurred. Please try again.","error")
        return json.dumps({"success":0})
    
    
#Assign to an OCCUPIED room, remove current occupant: Save and go to displayed course 
@app.route("/updateRoom/<cid>", methods=["POST"])

def updateRoom(cid):
    '''Assign preference room to a course. 
       Update the room id of previous course (i.e. conflict_course) to None.
       
       params:
         int: cid: Course_Id
    '''
    try:
        course = Course.get(Course.cId==cid)
        data = request.form
        course.rid = data['roomID']
        course.save()
        conflict_course = Course.get(Course.cId == data['ogCourse'])
        conflict_course.rid=None
        conflict_course.save()
        response={"url":conflict_course.cId}
        return json.dumps(response)
    except:
        flash("An error has occurred. Please try again.","error")
        return json.dumps({"error":0})
            


@app.route("/addSecond/<cid>", methods=["POST"])
def addSecond(cid):
    '''
    Assign Course to a room that already has courses in it. 
    params:
       int: cid: Course_Id

    '''
    try:
        course = Course.get(Course.cId==cid)
        data = request.form
        course.rid = data['roomID']
        course.save()
        response={"success":1}
        flash("Your changes have been saved!") 
        return json.dumps({"success": 1})
    except:
        flash("An error has occurred. Please try again.","error")
        return json.dumps({"error":0})
        
    
