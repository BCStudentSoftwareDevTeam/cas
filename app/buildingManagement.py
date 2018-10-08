#Controllger for Building Management page
from allImports import *
from app.logic.authorization import must_be_admin
from flask import render_template,flash
from app.logic.redirectBack import redirect_url
from app import app
import json
from app.logic import course
from app.logic import functions
from app.logic.getAuthUser import AuthorizedUser

@app.route("/buildingManagement", methods=["GET"])
@must_be_admin #TODO:Should be a requirement for a building manager, not admin!

#TODO: Should only pull rooms from a cetain building associated with user's login

def buildingManagement():
    building = Building.select()
    user = User.select()
    rooms = Rooms.select()
    
    #jsondumps if success
    #function to fill html
    
   
    return render_template("buildingManagement.html",
    building = building,
    rooms = rooms,
    user = user
    )
 
 
@app.route("/getRoomData/<rID>", methods=["GET"])    
def getRoomData(rID):
    
    room = Rooms.get(Rooms.rID == rID)
    room_details={}
    room_details["number"] = room.number
    room_details["capacity"] = room.maxCapacity
    room_details["type"] = room.roomType
    room_details["specializedEq"] = room.specializedEq
    room_details["specialFeatures"] = room.specialFeatures
    room_details["movableFurniture"] = room.movableFurniture
    #room_details["educationTech"] = room.movableFurniture #TODO: Fix, it is looped through in RoomPreferences controller i think -kat
    room_details["visualAcc"] = room.visualAcc
    room_details["audioAcc"] = room.audioAcc
    room_details["physicalAcc"] = room.physicalAcc
    
    return json.dumps(room_details)
    
    
    
    