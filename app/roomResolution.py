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
    flash("Your changes have been saved!") #Needs to be on change after room is assigned in View
    return render_template("roomResolution.html",  isAdmin=g.user.isAdmin, courses=courses, termcode=termCode)
      
      

@app.route("/roomResolutionView/<termCode>/<cid>", methods=["GET"])
def roomResolutionView(termCode,cid):
       # Creating the UI
    try:
        roompreference = RoomPreferences.get(RoomPreferences.course==cid)
    except Exception as e:
        roompreference= RoomPreferences(course=cid, any_Choice = "any").save()
        roompreference = RoomPreferences.get(RoomPreferences.course==cid)
        

        flash("Course has no preferences assinged.")
    buildings = Building.select()
    instructors = InstructorCourse.select().where(InstructorCourse.course==cid)
    print instructors
    bannercourses = BannerCourses.select()
    courses = Course.get(Course.cId==cid)
    educationtech = EducationTech.select()
    sql_query = 'SELECT r1.rID FROM rooms as r1 LEFT OUTER JOIN (SELECT c1.rid_id as r2 FROM course c1 JOIN (SELECT sid FROM bannerschedule WHERE CAST("{0}" as TIME) < CAST(bannerschedule.endTime as TIME) AND CAST("{1}" as TIME)  > CAST(bannerschedule.startTime AS TIME)) bs1 ON c1.schedule_id = bs1.sid WHERE c1.rid_id IS NOT NULL AND c1.term_id = {2}) ON r1.rID = r2 WHERE r2 IS NULL;'.format(courses.schedule.startTime, courses.schedule.endTime, courses.term.termCode)#Query of death
    cursor = mainDB.execute_sql(sql_query)
    availablerooms = []
    for room in cursor:
        availablerooms.append(room[0])
    
    rooms = []
    for rid in availablerooms: 
        room = Rooms.get(Rooms.rID==rid)
        rooms.append(room)
        print rid


    #For populating current occupant in course's preferences
    #For current course
    confcourse = RoomPreferences.get(RoomPreferences.course == cid)
    sch1startTime = confcourse.course.schedule.startTime
    # print sch1startTime
    sch1endTime = confcourse.course.schedule.endTime
    # print sch1endTime
    rp = RoomPreferences.get(RoomPreferences.course == cid)
    #This gets all conflicting courses
    conflicts_query = "SELECT cid FROM `course` INNER JOIN `bannerschedule` ON `bannerschedule`.sid = `course`.schedule_id WHERE `course`.rid_id = {0} AND `bannerschedule`.endTime <= \"{1}\" OR `bannerschedule`.startTime >= \"{2}\";"
    cclist = []
    if rp.pref_1:
        cclist.append(conflicts_query.format(rp.pref_1.rID,sch1startTime,sch1endTime))
    elif rp.pref_2:
        cclist.append(conflicts_query.format(rp.pref_2.rID,sch1startTime,sch1endTime))
    elif rp.pref_3:
        cclist.append(conflicts_query.format(rp.pref_3.rID,sch1startTime,sch1endTime))
    print (cclist , "This is the cc list")
    
    
    conflictingroomdata = []
    preferences = dict()
    
    if cclist != []:
    #cclist = [conflictingcourse1, conflictingcourse2, conflictingcourse3]
        for cc in cclist:
            cursor = mainDB.execute_sql(cc)
            print ("This is cursor", cursor)
            for conflict in cursor:
                conflictingroomdata.append(conflict[0])
    
        print ("This is the conflictingroomdata" ,conflictingroomdata)
        
    
        
        for idx in range(len(conflictingroomdata)): 
            pref_info = dict()
            cc = Course.get(Course.cId == conflictingroomdata[idx])
            pref_inst = InstructorCourse.select().where(InstructorCourse.course==conflictingroomdata[idx])
            full_name = None
            for inst in pref_inst:
                full_name = inst.username.firstName + " " +inst.username.lastName
                
            pref = 'pref'+ str(idx + 1)
            print ("This is cc", cc)
            current_course = str(cc.prefix.prefix) + " " + str(cc.bannerRef.number) + " " + str(cc.bannerRef.ctitle) 
            pref_info['course_name']=current_course
            pref_info['instructor']=full_name
            pref_info['cid']=cc.cId
            preferences[pref] = pref_info
            
            
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
def assignRoom(cid=0):
    data = request.form
    # print("ROOM ID: ", data['roomID'])
    # room = data["assignroombutton"]
    course = Course.get(Course.cId == cid) #Gets course ID from database
    course.rid = data['roomID']
    course.save()
    # print course.rid
    return json.dumps({"success": 1})
    
    
#Assign to an occupied room, remove current occupant
@app.route("/updateRoom/<cid>", methods=["POST"])
def updateRoom(cid=0):
    data = request.form #data coming from POST
    print("Room ID: ", data['roomID'])
    course = Course.get(Course.cId == cid) #Gets original course ID from database
    course.rid = data['roomID']
    course.save()
    course = Course.get(Course.cId == data['ogCourse']) #Gets conflicting course ID from database
    print("course rid:", course.rid)
    course.rid = None  #Sets room to None
    course.save()
    return json.dumps({"success": 1})


    
    
