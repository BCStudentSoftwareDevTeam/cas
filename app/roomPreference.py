from allImports import *
from flask import render_template,flash
from app.logic.redirectBack import redirect_url
from app import app
import json
from app.logic import course
from app.logic import functions
from app.logic.getAuthUser import AuthorizedUser
from app.models import InstructorCourse, Course

@app.route("/roomPreference/<term>", methods = ["GET"])
def roomPreference(term):
    # FIXME bring current_term in via URL, and add the modal to select current term used on courses.html
    # print(term)
    current_term = term
    current_user = AuthorizedUser().getUsername()

    # Used to populate dropdowns and stuff
    room = Rooms.select().join(Building, on = (Building.bID == Rooms.building))
    users= User.select()
    instructors = InstructorCourse.select()
    educationTech= EducationTech.select()

    # FIXME used for conflicting courses UI, which is hidden
    courses = Course.select().join(InstructorCourse, on=(InstructorCourse.course == Course.cId)).where(InstructorCourse.username == current_user and Course.term == current_term)
    # for course in courses:
        # print("Hi Sher")
        # print(course.term)
    roompreferences = RoomPreferences.select().join(Course, on = (InstructorCourse.course == Course.cId)).join(InstructorCourse, on=(RoomPreferences.course == InstructorCourse.course)).where(InstructorCourse.username == current_user and Course.term == current_term).distinct()
    # for rp in roompreferences:
    #     print(rp.course.cId)
    # roomPreferences = {}
    
    
    # Constructs RoomPreferences if they don't exist
    for course in courses:
        RoomPreferences.get_or_create(course = course.cId)
    
  
    return render_template(
        "roomPreference.html",
        roompreferences= roompreferences,
        room=room,
        users=users,
        course=courses,
        educationTech=educationTech,
        instructors=instructors
    )



@app.route('/room_details/<rid>', methods = ["GET"])
def room_details(rid):
    room_materials={}
    if int(rid) > 0:
        
        details = Rooms.get(Rooms.rID == rid)
        room_materials["number"]=details.number 
        room_materials['maxCapacity']= details.maxCapacity
        room_materials['visualAcc']= details.visualAcc
        room_materials['audioAcc']= details.audioAcc
        room_materials['physicalAcc']=details.physicalAcc
        room_materials['specializedEq']= details.specializedEq
        room_materials['movableFurniture']=details.movableFurniture
        room_materials['specialFeatures']=details.specialFeatures
        room_materials['educationTech']=education_Tech(rid)
    
   
    return json.dumps(room_materials)
    
    

# We will add this on monday based on the room_details 

@app.route('/education_Tech', methods = ["GET"])
def education_Tech(rid):
  
    room = Rooms.get(Rooms.rID == rid)
    tech_details = room.educationTech
    education_materials={}

    education_materials["dvd"]=tech_details.dvd 
    education_materials["blu_ray"]= tech_details.blu_ray 
    education_materials["audio"]= tech_details.audio
    education_materials["extro"]=tech_details.extro  
    education_materials["doc_cam"]=tech_details.doc_cam
    education_materials["vhs"]= tech_details.vhs
    education_materials["mondopad"]=tech_details.mondopad
    education_materials["tech_chart"]=tech_details.tech_chart
    
    
   
   
    return education_materials
    
# We will add this on monday based on the room_details ^^^^
    
        #Assign to an occupied room, remove current occupant
@app.route("/postPreference", methods=["POST"]) # This method serves to post data from the user input and dumps into the database
def postPreference():
    data = request.form #data coming from POST
    pref = int(data["pref_id"])
    room = int(data["roomID"])
    rp = RoomPreferences.get(RoomPreferences.course== data["ogCourse"])
    rp.initial_Preference = 0
    
    if room > 0: #If there is a room id
        if (pref == 1):
            rp.pref_1 = data["roomID"]
            rp.any_Choice = 2
        elif (pref == 2):
            rp.pref_2 = data["roomID"]
            rp.any_Choice = 3
        elif(pref == 3):
            rp.pref_3 = data["roomID"]
        else:
            flash("You tried to select a preference that doesn't exist!","error")
            return json.dumps({"success  ": 0}) #Picked a preference outside of 1,2,or 3
    
    elif room == 0:#Any case
        if(rp.none_Choice == pref): rp.none_Choice = None 
        
        if (pref == 1): 
            rp.pref_1 = None
            rp.any_Choice = 1
        elif (pref == 2):
            rp.pref_2 = None
            rp.any_Choice = 2
        elif(pref == 3):
            rp.pref_3 = None
            rp.any_Choice = 3
        
    elif room == -1:  #No other rooms work case
        if(rp.any_Choice == pref): rp.any_Choice = None
        
        if (pref == 1): 
            rp.pref_1 = None
            rp.none_Choice = 1
            flash("WARNING: This indicates to the registrar that this course does not need a room","error")
        elif (pref == 2):
            rp.pref_2 = None
            rp.none_Choice = 2
        elif(pref == 3):
            rp.pref_3 = None
            rp.none_Choice = 3
      
    rp.save()
    print("RP", rp.any_Choice)
    return json.dumps({"success": 1})

    
@app.route("/postNotes", methods=["POST"]) # This method serves to post data from the user input and dumps into the database
def postNotes():
    data = request.form
    key = 'pref_'+str(data['pref_id'])
    try:
        room_preference = RoomPreferences.get(RoomPreferences.course == data['cid'])
        old_notes = room_preference.notes
        if room_preference.notes:
            note_dict = eval(old_notes)
            note_dict[key]=str(data['note'])
        else:
            note_dict = dict()
            note_dict[key] = str(data['note'])
        room_preference.notes = str(note_dict)
        room_preference.save()
        print("flash")
        return json.dumps({"success":1})
        # for the get you would return json.dumps(eval(old_notes)) if room_preference.notes:
    except Exception as e:
        print (e)
        flash("your message has been saved!")
        return json.dumps({"error":1})
    flash("your notes has been saved")
    return data 
    
    
    