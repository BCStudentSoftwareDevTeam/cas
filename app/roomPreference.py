from app.allImports import *
from flask import render_template
from app.logic.redirectBack import redirect_url
from app import app
from app.logic import course
# @app.route("/roomPreference/", methods = ["GET"])
@app.route("/roomPreference/<rid>", methods = ["GET"])
def roomPreference(rid=1):
    page="Room Preference"
    # courses = (Course.select(Course, Ban).join(BannerCourses)
    #                  .where(Course.prefix == prefix)
    #                  .where(Course.term == tID))
    roompreferences = RoomPreferences.select()
      
        
        
    room = Rooms.select().where(Rooms.rID == rid).get()
    users= User.select().get()
    course= Course.select().get()
   
    
  
    return render_template(
        "roomPreference.html",
        roompreferences= roompreferences,
        room=room,
        users=users,
        course=course 
        
    )