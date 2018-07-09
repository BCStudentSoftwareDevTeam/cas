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
    
    
@app.route('/room_details/<id>', methods = ["GET"])
def room_details(rid):
    details = Rooms.select().where(Rooms.rID==rid)
    room_materials={}
    for items in details:
        room_materials[room_capacity]= items.room_capacity
        room_materials[visualAcc]= items.visualAcc
        room_details[audioAcc]= items.audioAcc
        room_materials[physicalAcc]=items.physicalAcc
        room_materials[educationTech]=items.educationTech
        room_materials[specialEqu]= items.specialEqu
        room_materials[specailFeatures]=items.specailFeatures
        room_materials[moveableFurnitures]=items.moveableFurnitures
        
        
    return json.dumps(room_materials)
    
    
# New controller for ajax request
# Query DB for data about specific room
# construct all the data to send to front end (build dictionary)
# return a json object (return (json.dumps(<data>))
# ---> back to javascript



@app.route('/roomDetails', methods=['GET'])
def roomDetails():
    

        
    }
    return json.dumps({'status':'OK','user':user,'pass':password}); 