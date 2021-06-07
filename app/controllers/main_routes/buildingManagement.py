from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.allImports import *
from flask import render_template,flash
from app.logic.redirectBack import redirect_url
import json
from app.logic import courseLogic
from app.logic import functions
from app.models.models import Building, Rooms, BuildingManager
from app.loadConfig import load_config
from datetime import datetime

from werkzeug.utils import secure_filename

#Running page
@main_bp.route("/buildingManagement", methods=["GET"])
def buildingManagement():                                   #Gathering of appropriate data to send to html
    au = AuthorizedUser()
    cfg = load_config()
    if au.user.isAdmin:
        building = Building.select()
    else:
        building = (Building.select()
                    .join(BuildingManager)
                    .where(BuildingManager.username == au.username)
                    )
    le_rooms = []                                           #Scott LITERALLY created this variable with a terrible name
    if len(building) == 0:
        abort(403)
    else:
        for b in building:
            rooms = Rooms.select().where(Rooms.building == b.bID)
            for room in rooms:
                le_rooms.append(room)
        user = User.select()
        return render_template("buildingManagement.html",
                                building = building,
                                rooms = le_rooms,
                                user = user,
                                cfg = cfg,
                                isAdmin = au.user.isAdmin
                                )

@main_bp.route('/getRoomData/<rID>', methods=["GET"])
# connected to ajax calls in the javascript file to populate the room data into panel
def getRoomData(rID):
    room = Rooms.get(Rooms.rID == rID)                          #Sets room variable to room object where the rID's are the same
    room_details={}                                             #Empty dictionare to hold all room attributes
    room_details["number"] = room.number                        #Begin setting room attributes to their appropriate keys
    room_details["building"] = room.building.shortName
    room_details["capacity"] = room.maxCapacity
    room_details["type"] = room.roomType
    room_details["specializedEq"] = room.specializedEq
    room_details["specialFeatures"] = room.specialFeatures
    room_details["movableFurniture"] = room.movableFurniture    #Use to make sure all above attributes are correct?
    room_details["visualAcc"] = room.visualAcc
    room_details["audioAcc"] = room.audioAcc
    room_details["physicalAcc"] = room.physicalAcc
    return json.dumps(room_details)

@main_bp.route("/imageUpload/<rid>", methods=["POST"])
def imageUpload(rid):
    print("RID: ", rid)
    # try:
        # Save the files
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join('app/static/images/', filename))
    # except Exception as e:
    #     print(e)
    #     return ("Image failed to upload to the server", 500)

    # Update the DB
    room = Rooms.get(Rooms.rID == rid)
    if not room.roomImageURL:
        room.roomImageURL = filename
    elif len(room.roomImageURL) == 0:
        room.roomImageURL = filename
    else:
        room.roomImageURL += "," + filename
    room.save()
    print("Room image saved", room.roomImageURL)
    return ("Success", 200)

@main_bp.route("/getImages/<rid>", methods=["GET"])
def getImages(rid):
    images = Rooms.get(Rooms.rID == rid)
    imageSet = []
    if not images.roomImageURL:
        return json.dumps(imageSet)
    if len(images.roomImageURL) == 0:
        return json.dumps(imageSet)
    for img in images.roomImageURL.split(","):
        try:
            fileSize = os.path.getsize("app/static/images/" + img);
            imageSet.append({"name": img, "size": fileSize})
        except:
            images.roomImageURL.replace(img, "")
            images.save()
    return json.dumps(imageSet)

@main_bp.route("/removeImage", methods=["POST"])
def removeImage():
    room = Rooms.get(Rooms.rID == request.form["rid"])
    if not len(room.roomImageURL) == 0:
        os.remove("app/static/images/" + room.roomImageURL)
        room.roomImageURL = None
    room.save()
    return json.dumps({"success":1})

@main_bp.route("/saveChanges/<rID>", methods=["POST"])
def saveChanges(rID):
#Saves all room data EXCLUDING ed tech
   try:
        room = Rooms.get(Rooms.rID==rID)                        #Sets room variable to room object where the rID's are the same
        data = request.form
        room.maxCapacity = (data['roomCapacity'])               #Begin setting room attributes to their keys in js (Inside saveChanges)
        room.roomType = (data['roomType'])
        room.specializedEq = (data['specializedEq'])
        room.specialFeatures = (data['specialFeatures'])
        if data['movableFurniture'] == 'false':                 #If movable furniture reads false from js
            room.movableFurniture = 0                           #Set to false in sqlite
        else:
            room.movableFurniture = 1                           #Else: its set to true in sqlite
        room.visualAcc = (data['visualAcc'])
        room.audioAcc = (data['audioAcc'])
        room.physicalAcc = (data['physicalAcc'])
        # e.g., 06/02/2020 11:28:36 PM
        room.lastModified = (datetime.now().strftime("%m/%d/%Y %I:%M %p"))
        room.save()                                             #Save data
        return json.dumps({"success":1})
   except:
       flash("An error has occurred, your changes were NOT saved. Please try again.","error")
       return json.dumps({"error":0})

#Education tech pull
@main_bp.route('/getEducationData/<rid>', methods = ["GET"])
def getEducationData(rid):
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
    return json.dumps(education_materials)

#Education tech save to DB
@main_bp.route("/saveEdTechChanges/<rid>", methods=["POST"])
def saveEdTechChanges(rid):
  try:
    room = Rooms.get(Rooms.rID==rid)
    edtech_update = room.educationTech
    data = request.form
    edtech_update.projector = data['projector']
    edtech_update.smartboards = data['smartboards']
    edtech_update.instructor_computers = data['instructor_computers']
    edtech_update.podium= data['podium']
    edtech_update.student_workspace = data['student_workspace']
    edtech_update.chalkboards= data['chalkboards']
    edtech_update.whiteboards= data['whiteboards']
    if data['vhs'] == 'false':                                  #this checks the booleans and set them to correct values.
                                                                #If they are checked thier values set to 1s an if they are unchecked thier values sets to 1s
        edtech_update.vhs = 0
    else:
        edtech_update.vhs = 1
    if data['dvd'] == 'false':
        edtech_update.dvd= 0
    else:
        edtech_update.dvd = 1
    if data['blu_ray']=='false':
        edtech_update.blu_ray=0
    else:
        edtech_update.blu_ray=1
    if data['audio']=='true':
        edtech_update.audio=1
    else:
        edtech_update.audio=0
    if data['mondopad']=='true':
        edtech_update.mondopad=1
    else:
        edtech_update.mondopad=0
    if data['doc_cam']=='true':
        edtech_update.doc_cam=1
    else:
        edtech_update.doc_cam=0
    if data['tech_chart']=='true':
        edtech_update.tech_chart=1
    else:
        edtech_update.tech_chart=0
    if data['extro']=='false':
        edtech_update.extro=0
    else:
        edtech_update.extro=1
    edtech_update.save()
    flash("Your changes have been saved!")
    return json.dumps({"success":1})
  except:
      flash("An error has occurred, your changes were NOT saved. Please try again.","error")
      return json.dumps({"error":0})
