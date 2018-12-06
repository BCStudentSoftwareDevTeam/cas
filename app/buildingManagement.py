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
    #Gathering of appropriate data to send to html
    building = Building.select()
    user = User.select()
    rooms = Rooms.select()
    

    return render_template("buildingManagement.html",
                            building = building,
                            rooms = rooms,
                            user = user
                            )
                         
 
@app.route('/getRoomData/<rID>', methods=["GET"]) 
# connected to ajax calls in the javascript file to populate the room data
def getRoomData(rID):
    room = Rooms.get(Rooms.rID == rID)
    room_details={}
    room_details["number"] = room.number
    room_details["capacity"] = room.maxCapacity
    room_details["type"] = room.roomType
    room_details["specializedEq"] = room.specializedEq
    room_details["specialFeatures"] = room.specialFeatures
    room_details["movableFurniture"] = room.movableFurniture
    room_details["visualAcc"] = room.visualAcc
    room_details["audioAcc"] = room.audioAcc
    room_details["physicalAcc"] = room.physicalAcc
    # print ("python" ,rID)
    # print(room_details["number"])     #Use to make sure all above attributes are correct?
    return json.dumps(room_details)
    
@app.route("/saveChanges/<rID>", methods=["POST"])
def saveChanges(rID):
#updates room data in database after clicking save changes.
#   print("Here I am, rock yhou like a hurricane")
   try:
        room = Rooms.get(Rooms.rID==rID)
        data = request.form
        room.maxCapacity = (data['roomCapacity'])
        room.roomType = (data['roomType'])
        room.specializedEq = (data['specializedEq'])
        room.specialFeatures = (data['specialFeatures'])
        room.movableFurniture = (data['movableFurniture'])
        room.visualAcc = (data['visualAcc'])
        room.audioAcc = (data['audioAcc'])
        room.physicalAcc = (data['physicalAcc'])
        # print("it is saved", room)
        room.save()
        return json.dumps({"success":1})
   except:
       flash("An error has occurred, your changes were NOT saved. Please try again.","error")
       return json.dumps({"error":0})
 
@app.route('/getEducationData/<rid>', methods = ["GET"])
def getEducationData(rid):
    # print("hello")
  
    room = Rooms.get(Rooms.rID == rid)
    tech_details = room.educationTech
    education_materials={}
    education_materials["projector"] = tech_details.projector
    education_materials["smartboards"] = tech_details.smartboards
    education_materials["instructor_computers"] = tech_details.instructor_computers
    education_materials["podium"] = tech_details.podium
    education_materials["student_workspace"] = tech_details.student_workspace
    education_materials["chalkboards"] = tech_details.chalkboards
    education_materials["whiteboards"] = tech_details.whiteboards
    education_materials["dvd"]=tech_details.dvd 
    education_materials["blu_ray"]= tech_details.blu_ray 
    education_materials["audio"]= tech_details.audio
    education_materials["extro"]=tech_details.extro  
    education_materials["doc_cam"]=tech_details.doc_cam
    education_materials["vhs"]= tech_details.vhs
    education_materials["mondopad"]=tech_details.mondopad
    education_materials["tech_chart"]=tech_details.tech_chart
    # print("Sending response to front end", education_materials)
    # print("Sending response to front end", education_materials)
    return json.dumps(education_materials)
    
    
    
@app.route("/saveEdTechChanges/<rID>", methods=["POST"])
def saveEdTechChanges(rID):
#updates room data in database after clicking save changes.
  try:
      room = Rooms.get(Rooms.rID==rID)
      edtech_update = room.educationTech
      data = request.form
    #   print("data", data)
      edtech_update.projector = data['projector']
     
      edtech_update.smartboards = data['smartboards']
      
      edtech_update.instructor_computers = data['instructor_computers']
      
      edtech_update.podium= data['podium']
      
      edtech_update.student_workspace = data['student_workspace']
      
      edtech_update.chalkboards= data['chalkboards']
      
      edtech_update.whiteboards= data['whiteboards']
        #start from here you need to save to the database everything else already saved. You just need to save from dvd to tech_chart
      edtech_update.dvd = data['dvd']
      edtech_update.blu_ray= data["blu_ray"]
      edtech_update.extro= (data['extro'])
      edtech_update.doc_cam= (data['doc_cam'])
      edtech_update.vhs= (data['vhs'])
      edtech_update.mondopad=str(data['mondopad'])
      edtech_update.tech_chart=(data['tech_chart'])
      edtech_update.save()
    #   print("data", edtech_update)
      
    #   print("after")
      flash("Your changes have been saved!")
      return json.dumps({"success":1})
  except:
      flash("An error has occurred, your changes were NOT saved. Please try again.","error")
      return json.dumps({"error":0})