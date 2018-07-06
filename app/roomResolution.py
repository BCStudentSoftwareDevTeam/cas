from allImports import *
from app import app
from app.logic.authorization import must_be_admin

@app.route("/roomResolution", methods=["GET"])
@must_be_admin

def roomResolution():
    # Creating the UI
    course = Course.select()

    return render_template("roomResolution.html",  isAdmin=g.user.isAdmin, courses=course)
      
      
@app.route("/roomResolutionView/<rpid>", methods=["GET"])


def roomResolutionView(rpid):
       # Creating the UI
    roompreference = RoomPreferences.get(RoomPreferences.rpID==rpid)
    buildings = Building.select()
    instructor = InstructorCourse.get()
    bannercourses = BannerCourses.select()
    course = Course.get()
    rooms = Rooms.select() #Has to be a select() of available rooms
    educationtech = EducationTech.select()
    return render_template("roomResolutionView.html", 
                            roompreference=roompreference, 
                            available_rooms=rooms, 
                            buildings=buildings, 
                            instructor = instructor, 
                            courses=course, 
                            bannercourses=bannercourses,
                            educationtech=educationtech,
                        )