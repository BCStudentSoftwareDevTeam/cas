from allImports import *
from app import app

@app.route("/roomResolution", methods=["GET"])

def roomResolution():
    # Creating the UI
    course = Course.select()
    bannercourses = BannerCourses.select()
    return render_template("roomResolution.html", courses=course, bannercourses=bannercourses)
      
      
@app.route("/roomResolutionView/<rpid>", methods=["GET"])

def roomResolutionView(rpid):
       # Creating the UI
    roompreference = RoomPreferences.get(RoomPreferences.rpID==rpid)
    buildings = Building.select()
    return render_template("roomResolutionView.html", roompreference=roompreference, buildings=buildings)