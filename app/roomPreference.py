from app.allImports import *
from flask import render_template
from app.logic.redirectBack import redirect_url
from app import app
from app.logic import course
@app.route("/roomPreference/", methods = ["GET"])
@app.route("/roomPreference/<rid>", methods = ["GET"])
def roomPreference(rid):
    page="Room Preference"
    roompreferences = RoomPreferences.select()
    room = Rooms.select().where(Rooms.rID==rid)
    users= User.select().get()
    course= Course.select().get()
    educationTech= EducationTech.select()
    return render_template(
        "roomPreference.html",
        roompreferences= roompreferences,
        room=room,
        users=users,
        course=course,
        educationTech=educationTech
    )
    
    
# New controller for ajax request
# Query DB for data about specific room
# construct all the data to send to front end (build dictionary)
# return a json object (return (json.dumps(<data>))
# ---> back to javascript



@app.route('/roomDetails', methods=['GET'])
def roomDetails():
    

        
    }
    return json.dumps({'status':'OK','user':user,'pass':password}); 