from allImports import *
from flask import render_template,flash
from app.logic.redirectBack import redirect_url
from app import app
import json
from app.logic import course
from app.logic import functions
from app.logic.getAuthUser import AuthorizedUser
from app.models import InstructorCourse, Course
from string import strip

@app.route("/roomPreference/<term>", methods = ["GET"])
def roomPreference(term):
    # FIXME bring current_term in via URL, and add the modal to select current term used on courses.html
    # print(term)
    current_term = term
    current_user = AuthorizedUser().getUsername()

    # Used to populate dropdowns and stuff
    room = Rooms.select().join(Building, on = (Building.bID == Rooms.building)).order_by(Building.bID.desc(), Rooms.number.desc())
    users= User.select()
    instructors = InstructorCourse.select()
    # educationTech= EducationTech.select()

    # FIXME used for conflicting courses UI, which is hidden
    # print(current_user)
    # print(current_term)
    #Select * from (course) join instructorcourse on instructorcourse.course_id == course.cId and instructorcourse.username_id== 'heggens'  
    term = Term.get(Term.termCode == current_term)
    # print(term)
    courses = ( Course.select()
                    .join(InstructorCourse, on= (InstructorCourse.course == Course.cId))
                    .join(Term, on=(Term.termCode == Course.term))
                    .where(InstructorCourse.username == current_user)
                    .where(Course.term == int(current_term))
                )
    #courses = InstructorCourse.select().where(InstructorCourse.username == current_user).where(InstructorCourse.course_id.term.termCode == int(current_term))
    # for course in courses:
    #     print("Hi Sher")
    #     print(course.cId)
    # # for rp in roompreferences:
    #     print(rp.course.cId)
    # roomPreferences = {}
    
    
    # Constructs RoomPreferences if they don't exist
    for course in courses:
        # print("adding ", course.cId, "to ", current_user)
        (rp, c) = RoomPreferences.get_or_create(course = course.cId)
        # print(rp.course.term.termCode)
    
    roompreferences= (  RoomPreferences.select()
                                    .join(InstructorCourse, 
                                        on = (InstructorCourse.course == RoomPreferences.course))
                                    .join(Course, on = (RoomPreferences.course == Course.cId))
                                    .join(Term, on = (Course.term == Term.termCode))
                                    .where(RoomPreferences.course == InstructorCourse.course 
                                            and InstructorCourse.username == current_user)
                                    .where(Course.term == current_term)
                                    .distinct()
                        )
    # roompreferences = RoomPreferences.select().join(Course, on = (RoomPreferences.course == Course.cId)).join(InstructorCourse, on=(Course.cId == InstructorCourse.course)).where(InstructorCourse.username == current_user and Course.term == current_term).distinct()
  
    return render_template(
        "roomPreference.html",
        roompreferences= roompreferences,
        room=room,
        users=users,
        course=courses,
        # educationTech=educationTech,
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

@app.route('/education_Tech/<rid>', methods = ["GET"])
def education_Tech(rid):
  
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
    return json.dumps(education_materials)
    
# We will add this on monday based on the room_details ^^^^
    
        #Assign to an occupied room, remove current occupant
@app.route("/postPreference", methods=["POST"]) # This method serves to post data from the user input and dumps into the database
def postPreference():
    data = request.form #data coming from POST
    
    pref = int(data["pref_id"]) # Preference to be updated for a course
    
    room = int(data["roomID"]) # ID of the room to update a course's room preference with. 
    
    rp = RoomPreferences.get(RoomPreferences.course== data["ogCourse"])
    
    rp.initial_Preference = 0 # Just something we're not sure what to do with. 
    
    if room > 0: #If a room was selected
        
        if (pref == 1): # for preference 1
        
            rp.pref_1      = data["roomID"] # grab selected roomID
        
            rp.any_Choice  = 2 # Set all succeeding preferences to any room works
        
            rp.none_Choice = None # update database to reflect that 'This course does not require a room/No other room works' was not selected
        
        elif (pref == 2): # preference 2
            
            rp.pref_2      = data["roomID"] 
            
            if rp.any_Choice >= 2:
                rp.any_Choice  = 3
            else:
                rp.any_Choice = None
                
            if rp.none_Choice >= 2:
                print("none on three")
                rp.none_Choice = 3
            else:
                rp.none_Choice = None
        
        elif(pref == 3): # preference 3
        
            rp.pref_3      = data["roomID"]
        
            rp.none_Choice = None
        
        else:
        
            flash("You tried to select a preference that doesn't exist!","ERROR!!! :(")
        
            return json.dumps({"success  ": 0}) # Picked a preference outside of 1,2,or 3
    
    elif room == 0:# if 'Any room works' was selected
        
        if (pref == 1): # for preference 1
        
            rp.pref_1      = None # Set preference 1 of the specific course to none to indicate that a room was not selected for that particular preference
        
            rp.pref_2      = None # Same for preference 2
        
            rp.pref_3      = None # Same for preference 3 
        
            rp.any_Choice  = 1 # Set the column 'any_choice' to the preference ID to indicate that 'Any room was selected'
        
            rp.none_Choice = None # update database to reflect that 'This course does not require a room/No other room works' was not selected
        
        elif (pref == 2): # preference 2
        
            rp.pref_2      = None
        
            rp.pref_3      = None
        
            rp.any_Choice  = 2
        
            rp.none_Choice = None 
        
        elif(pref == 3): # preference 3
            
            rp.pref_3      = None
            
            rp.any_Choice  = 3
            
            rp.none_Choice = None
    
    elif room == -1:  # If 'No other rooms work' or 'This course does not require a room' was selected
    
        # if(rp.any_Choice == str(pref).decode("utf-8")): rp.any_Choice = None // FIXME: WHAT DOES THIS DO???>????
        
        if (pref == 1): # for preference 1
    
            rp.any_Choice  = None # Set the 'any_choice' column of a course to none to indicate that 'Any room works' was not selected
    
            rp.pref_1      = None # Set preference 1 for the course to none to indicate that a room was not selected as preference 
    
            rp.none_Choice = 1 # Set the none_choice column to the preference ID to indicate that 'No other rooms work' or 'This course does not require a room' was selected for the course
    
            rp.pref_2      = None # Set preference 2 for the course to none to indicate that a room was not selected as preference 
    
            rp.pref_3      = None # Set preference 3 for the course to none to indicate that a room was not selected as preference 
    
            flash("WARNING: This indicates to the registrar that this course does not need a room","error")
    
        elif (pref == 2):
            
            rp.pref_2 = None
            
            rp.none_Choice = 2
            
            rp.pref_3 = None
            
            rp.any_Choice = None
        
        elif(pref == 3):
        
            rp.pref_3 = None
        
            rp.none_Choice = 3
        
            rp.any_Choice = None
    
    print("Time to save ", rp.none_Choice)  
    print("Time to save ", rp.any_Choice)  
    rp.save() # Save the room preference in the database for the course
   
    # print('RP_any', rp.any_Choice)
    # print("RP_None", rp.none_Choice )
    # print("RP-Pref1", rp.pref_1)
    # print("RP-Pref2", rp.pref_2)
    # print("RP-Pref3", rp.pref_3)
   
    return json.dumps({"success": 1}) 

@app.route("/getNotes/<cid>", methods=["GET"])
def getNotes(cid):
    
    print (RoomPreferences.get(RoomPreferences.notes).where(RoomPreferences.course == cid))
    return json.dumps({"notes": RoomPreferences.get(RoomPreferences.notes).where(RoomPreferences.course == cid)})
    
@app.route("/postNotes", methods=["POST"]) # This method serves to post data from the user input and dumps into the database
def postNotes():
    
    data = request.form
    
    # key = 'pref_'+str(data['pref_id'])
    
    # try:
    
    room_preference = RoomPreferences.get(RoomPreferences.course == data['cid'])
    room_preference.notes = data['note']
    room_preference.save()
    
        # old_notes = room_preference.notes
    
    #     # if room_preference.notes:
    #     #     note_dict = eval(old_notes)
    #     #     note_dict[key]=str(data['note'])
    #     # else:
    #     #     note_dict = dict()
    #     #     note_dict[key] = str(data['note'])
    #     # room_preference.notes = str(note_dict)
    #     # room_preference.save()
    #     # print("flash")
    #     return json.dumps({"success":1})
    #     # for the get you would return json.dumps(eval(old_notes)) if room_preference.notes:
    # except Exception as e:
    #     print (e)
    #     flash("your message has been saved!")
    #     return json.dumps({"error":1})
    
    flash("your notes has been saved")
    return data 
    
    
    
