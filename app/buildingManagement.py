#Controllger for Building Management page
from allImports import *
from app.logic.authorization import must_be_admin

@app.route("/buildingManagement", methods=["GET"])
@must_be_admin #Should be a requirement for a building manager, not admin!

def buildingManagement():
    
   #TODO:Need for loop to generate buildings
   
   #TODO: Need for loop to pull rooms
   
    return render_template("buildingManagement.html")