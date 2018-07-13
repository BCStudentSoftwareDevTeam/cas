from app.allImports import *
from flask import render_template
from app.logic.redirectBack import redirect_url
from app import app
import json
from app.logic import course
@app.route("/roomPreference/", methods = ["GET"])
@app.route("/roomPreference/<rid>", methods = ["GET"])


def roomPreference(rid=1):
    page="Room Preference"
    roompreferences = RoomPreferences.select()
    room = Rooms.select()
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
    
    


@app.route('/room_details/<rid>', methods = ["GET"])
def room_details(rid):
    details = Rooms.get(Rooms.rID == rid)
    room_materials={}

    room_materials["number"]=details.number 
    room_materials['maxCapacity']= details.maxCapacity
    room_materials['visualAcc']= details.visualAcc
    room_materials['audioAcc']= details.audioAcc
    room_materials['physicalAcc']=details.physicalAcc
    room_materials['specializedEq']= details.specializedEq
    room_materials['movableFurniture']=details.movableFurniture
    room_materials['specialFeatures']=details.specialFeatures
   
    

    return json.dumps(room_materials)
    
    

# New controller for ajax request
# Query DB for data about specific room
# construct all the data to send to front end (build dictionary)
# return a json object (return (json.dumps(<data>))
# ---> back to javascript


# #hamza added this for posting data to room
@app.route("/setPreference/<cid>")
def setPreference(cid=1):
    if cid != 0:
        data = request.form
        roomPicked = data['roomPicked']
        rp = roompreferences.get_or_create(roomPreferences.course.cid==cid)
        rp.pref_1=roomPicked