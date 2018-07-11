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
    rooms = Rooms.select() #Has to be a select() of available rooms
    educationtech = EducationTech.select()
    query = "SELECT * FROM rooms INNERJOIN course INNERJOIN bannerschedule"

    return render_template("roomResolutionView.html", 
                            roompreference=roompreference, 
                            available_rooms=rooms, 
                            buildings=buildings, 
                            instructor = instructor, 
                            courses=course, 
                            bannercourses=bannercourses,
                            educationtech=educationtech
                        )
