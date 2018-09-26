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
    
   
    return render_template("buildingManagement.html",
    building = building,
    rooms = rooms,
    user = user
    )
    
    
    
    