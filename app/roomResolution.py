from allImports import *
from models import *
from peewee import *
from app import app
from app.logic.authorization import must_be_admin
from app.logic import functions

@app.route("/roomResolution", methods=["GET"])
@must_be_admin

def roomResolution():
    # Creating the UI
    courses = Course.select().where(Course.rid == None)
    flash("Your changes have been saved!") #Needs to be on change after room is assigned in View
    return render_template("roomResolution.html",  isAdmin=g.user.isAdmin, courses=courses)
      
      

@app.route("/roomResolutionView/<cid>", methods=["GET"])

def roomResolutionView(cid):
       # Creating the UI
    roompreference = RoomPreferences.get(RoomPreferences.course==cid)
    buildings = Building.select()
    instructor = InstructorCourse.select().where(InstructorCourse.course==cid)
    bannercourses = BannerCourses.select()
    course = Course.get(Course.cId==cid)
    educationtech = EducationTech.select()
    sql_query = 'SELECT r1.rID FROM rooms as r1 LEFT OUTER JOIN (SELECT c1.rid_id as r2 FROM course c1 JOIN (SELECT sid FROM bannerschedule WHERE CAST("{0}" as TIME) < CAST(bannerschedule.endTime as TIME) AND CAST("{1}" as TIME)  > CAST(bannerschedule.startTime AS TIME)) bs1 ON c1.schedule_id = bs1.sid WHERE c1.rid_id IS NOT NULL AND c1.term_id = {2}) ON r1.rID = r2 WHERE r2 IS NULL;'.format(course.schedule.startTime, course.schedule.endTime, course.term.termCode)
    cursor = mainDB.execute_sql(sql_query)
    availablerooms = []
    for room in cursor:
        availablerooms.append(room[0])
    
    rooms = []
    for rid in availablerooms: 
        room = Rooms.get(Rooms.rID==rid)
        rooms.append(room)
        print rid
    
    return render_template("roomResolutionView.html", 
                            roompreference=roompreference, 
                            available_rooms=rooms, 
                            buildings=buildings, 
                            instructor = instructor, 
                            courses=course, 
                            bannercourses=bannercourses,
                            educationtech=educationtech
                        )
                        


