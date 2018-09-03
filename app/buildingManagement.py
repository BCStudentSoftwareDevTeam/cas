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
@must_be_admin #Should be a requirement for a building manager, not admin!

def buildingManagement():
    building = Building.select()
    user = User.select()
    room = Rooms.select()
    
    
   #TODO:Need for loop to generate buildings
   
   #TODO: Need for loop to pull rooms
   
    return render_template("buildingManagement.html",
    building = building,
    room = room,
    user = user
    )
    
    
    
    