from allImports import *
from models import *
from peewee import *
from app import app
from app.logic.authorization import must_be_admin
from app.logic import functions
import json

@app.route("/roomResolutionTerm", methods=["GET"])
@must_be_admin
def roomResolutionTerm():
    #Brings up term modal
    terms = Term.select()
    dummy = True
    
    return render_template("selectTerm.html", allTerms=terms, dummy=dummy)
    
@app.route("/roomResolution/<termCode>", methods=["GET"])
@must_be_admin
def roomResolution(termCode):
    # Creating the UI
    courses = Course.select().where(Course.rid == None, Course.term==termCode)
    return render_template("roomResolution.html",  isAdmin=g.user.isAdmin, courses=courses, termcode=termCode)
      
      

@app.route("/roomResolutionView/<termCode>/<cid>", methods=["GET"])
def roomResolutionView(termCode,cid):
       # Creating the UI
    try:
        roompreference = RoomPreferences.get(RoomPreferences.course==cid)
    except Exception as e:
        roompreference = RoomPreferences(course=cid, any_Choice = "any").save()
        roompreference = RoomPreferences.get(RoomPreferences.course==cid)
        

        flash("Course has no preferences assigned.")
    buildings = Building.select()
    instructors = InstructorCourse.select().where(InstructorCourse.course==cid)
    print instructors
    bannercourses = BannerCourses.select()
    courses = Course.get(Course.cId==cid)
    educationtech = EducationTech.select()
    
    # Getting all available rooms for the first tab
    sql_query = """ SELECT r1.rID FROM rooms as r1 
                    LEFT OUTER JOIN 
                    (SELECT c1.rid_id as r2 FROM course c1 JOIN (SELECT sid FROM bannerschedule 
                    WHERE CAST("{0}" as TIME) < CAST(bannerschedule.endTime as TIME) AND CAST("{1}" as TIME)  > CAST(bannerschedule.startTime AS TIME)) bs1 
                    ON c1.schedule_id = bs1.sid WHERE c1.rid_id IS NOT NULL AND c1.term_id = {2}) ON r1.rID = r2 WHERE r2 IS NULL AND r1.maxCapacity >= {3};""".format(courses.schedule.startTime, courses.schedule.endTime, courses.term.termCode, courses.capacity)
    cursor = mainDB.execute_sql(sql_query)
    print(sql_query)
    
    # if cursor:
    #     print("Cursor worked: ", cursor)
    availablerooms = []
    for room in cursor:
        availablerooms.append(room[0])
        print("The room is: ", room[0])
    
    rooms = []
    for rid in availablerooms: 
        room = Rooms.get(Rooms.rID==rid)
        rooms.append(room)
        print rid


    #For populating current occupant in course's preferences
    
    confcourse = RoomPreferences.get(RoomPreferences.course == cid) # grab the A course's preferences
    sch1startTime = confcourse.course.schedule.startTime            # grab the A course's schedule start time
    # print sch1startTime
    sch1endTime = confcourse.course.schedule.endTime                # grab the A course's schedule end time
    # print sch1endTime
    rp = RoomPreferences.get(RoomPreferences.course == cid)         # get the A course's room preferences again (not needed, but used both variables)
    
    print("this is confcourse", confcourse.course.cId)
    print("This is ssch1starttime", sch1startTime)
    print("this is sch1endTime", sch1endTime)
    
    #This gets all conflicting courses
    print("What is this schedule you speak of: ", confcourse.course.schedule.sid)
    scheduleDays = ScheduleDays.get(ScheduleDays.schedule == confcourse.course.schedule.sid)
    
    
    conflicts_query = """   SELECT cid 
                            FROM `course` 
                            INNER JOIN `bannerschedule` 
                            ON `bannerschedule`.sid = `course`.schedule_id 
                            WHERE `course`.rid_id = {0} AND `bannerschedule`.endTime > \"{1}\" AND `bannerschedule`.startTime < \"{2}\";"""  #For course B
    cclist = []  # holds all conflicting courses queries to be executed later
    
    # "A" course schedule
    aCourseSchedule = scheduleDays.day
    
    # check which preference we're on, and append to cclist
    if rp.pref_1:
        cclist.append(conflicts_query.format(rp.pref_1.rID,sch1startTime,sch1endTime)) #comparing course A to B
    if rp.pref_2:
        cclist.append(conflicts_query.format(rp.pref_2.rID,sch1startTime,sch1endTime))
    if rp.pref_3:
        cclist.append(conflicts_query.format(rp.pref_3.rID,sch1startTime,sch1endTime))
    print (cclist , "This is the cc list")
    
    conflictingroomdata = []        # data about one B Course
    preferences = dict()            # dictionary to hold all B courses
    
    #if there are conflicting courses
    if cclist != []:                
        # cclist = [conflictingcoursequery1, conflictingcoursequery2, conflictingcoursequery3]
        for cc in cclist:
            cursor = mainDB.execute_sql(cc)             # execute each query
            print ("This is cursor", cursor)
            for conflict in cursor:
                print("Conflict[0] is: ", conflict[0])      # conflict[0] is the B course ID (cId)
                conflictingroomdata.append(conflict[0])     # appends results of query to list of actual B courses 
    
        print ("This is the conflictingroomdata" ,conflictingroomdata)
        
        #pulling specific data from conflicting course
        for idx in range(len(conflictingroomdata)):
            pref_info = dict()          # to hold course info
            cc = Course.get(Course.cId == conflictingroomdata[idx])     # get all data baout the course
            bScheduleDays = ScheduleDays.get(ScheduleDays.schedule == cc.schedule)
            for letter in aCourseSchedule:
                if letter in bScheduleDays.day:
                    print("A course day: {0} conflicted with B course day: {1}".format(letter, bScheduleDays.day))
                    pref_inst = InstructorCourse.select().where(InstructorCourse.course==conflictingroomdata[idx])  # get instructor information
                    full_name = None
                    
                    for inst in pref_inst:
                        full_name = inst.username.firstName + " " +inst.username.lastName       # if there's an instructor, add name to full_name
                        
                    pref = 'pref'+ str(idx + 1)         # which pref?
                    print ("This is cc", cc)            
                    current_course = str(cc.prefix.prefix) + " " + str(cc.bannerRef.number) + " " + str(cc.bannerRef.ctitle) # String of info about B course
                    pref_info['course_name']=current_course         # add to pref_info
                    pref_info['instructor']=full_name               # add instructor to pref info
                    pref_info['cid']=cc.cId                         # add cId to pref_info
                    
                    print ("Conflicting course's preference notes",cc.cId)
                    (rp1, created) = RoomPreferences.get_or_create(course = cc.cId)
                    print(rp1.notes)
                    pref_info['notes']=rp1.notes
                    
                    preferences[pref] = pref_info
                    break
            
           
            
            
            
        print ("This is the conflicting course",preferences) #Actual conflicting course(S) {'pref1': {'instructor': u'Scott Heggen', 'course_name': 'CSC 236 Data Structures', 'cid': 1}}
        
   
    
    return render_template("roomResolutionView.html", 
                            roompreference=roompreference, 
                            available_rooms=rooms, 
                            buildings=buildings, 
                            instructors = instructors, 
                            courses=courses, 
                            bannercourses=bannercourses,
                            educationtech=educationtech,
                            preferences=preferences,
                            termcode=termCode
                            
                            
                        )
                        

#Controller for Assign button (roomResolutionView) sending the assignment of a course to a room to database
#Available rooms
@app.route("/assignRoom/<cid>", methods=["POST"])

#Add functionality that checks if room is still empty before the insert#
def assignRoom(cid=0):
    if Course.get(Course.cId==cid).rid == None: 
        if assignRoom:
            data = request.form
            print("ROOM ID: ", data['roomID'])
            # room = data["assignroombutton"]
            course = Course.get(Course.cId == cid) #Gets course ID from database
            course.rid = data['roomID']
            course.save()
            # print course.rid
            flash("Your changes have been saved!") 
            return json.dumps({"success": 1})
        
    else:
        flash("An error has occurred. Please try again.","error")
        return json.dumps({"success":0})
    
    
#Assign to an occupied room, remove current occupant
@app.route("/updateRoom/<cid>", methods=["POST"])
#TO DO: Add check for if Course has already been resolved (has an rid)
def updateRoom(cid=0):
    print("YOOOOOOOOOOOOOOOOOOOOO",Course.get(Course.cId==cid).rid)
    if Course.get(Course.cId==cid).rid == None:
        if updateRoom:
            data = request.form #data coming from POST
            print("Room ID: ", data['roomID'])
            course = Course.get(Course.cId == cid) #Gets original course ID from database
            course.rid = data['roomID']
            course.save()
            course = Course.get(Course.cId == data['ogCourse']) #Gets conflicting course ID from database
            print("course rid:", course.rid)
            course.rid = None  #Sets room to None
            course.save()
            flash("Your changes have been saved!") 
            return json.dumps({"success": 1})
            
    else:
        flash("An error has occurred. Please try again.","error")
        return json.dumps({"success":0})
        


    
    
