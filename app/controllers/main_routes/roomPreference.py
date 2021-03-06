from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.allImports import *
from flask import render_template,flash, jsonify
from playhouse.shortcuts import model_to_dict
from app.logic.redirectBack import redirect_url
# from app import app
import json
from app.logic import courseLogic
from app.logic import functions
from app.logic.authorizedUser import AuthorizedUser
from app.models.models import *
from app.loadConfig import load_config

@main_bp.route("/roomPreference/<term>", methods = ["GET"])
def roomPreference(term):
    cfg = load_config()
    current_term = term
    term = Term.get(Term.termCode == current_term)
    au = AuthorizedUser()
    current_user = au.username

    # Used to populate dropdowns and stuff
    room = Rooms.select().join(Building, on = (Building.bID == Rooms.building)).order_by(Building.name.asc(), Rooms.number.asc())

    users= User.select()
    educationTech= EducationTech.select()

    courses = ( Course.select()
                    .join(InstructorCourse, on= (InstructorCourse.course == Course.cId))
                    .join(Term, on=(Term.termCode == Course.term))
                    .where(Course.term == int(current_term))
                    .where(Course.offCampusFlag == False))

    # Constructs RoomPreferences if they don't exist
    for course in courses:
        (rp, c) = RoomPreferences.get_or_create(course = course.cId)

    roompreferences= (  RoomPreferences.select()
                                    .join(InstructorCourse, on = (InstructorCourse.course == RoomPreferences.course))
                                    .join(Course, on = (RoomPreferences.course == Course.cId))
                                    .join(Term, on = (Course.term == Term.termCode))
                                    .where(RoomPreferences.course == InstructorCourse.course)
                                    .where(Course.term == current_term)
                                    .where(Course.offCampusFlag == False)
                                    .distinct().where(Course.parentCourse == None))

    if au.user.isAdmin == False:
        roompreferences = roompreferences.where(InstructorCourse.username == current_user)
        courses = courses.where(InstructorCourse.username == current_user)

    if term.term_state.number != 3:
        return render_template("roomPreferencesLocked.html",
                                cfg = cfg,
                                isAdmin = au.user.isAdmin)

    instructor_query = InstructorCourse.select(InstructorCourse, User).join(User)
    instructors = {}
    for instructor in instructor_query.objects():
        name = f"{instructor.firstName} {instructor.lastName}"
        instructors.setdefault(instructor.course_id, []).append(name)


    return render_template(
            "roomPreference.html",
            roompreferences= roompreferences,
            room=room,
            users=users,
            course=courses,
            educationTech=educationTech,
            instructors=instructors,
            cfg = cfg,
            isAdmin = au.user.isAdmin
        )

@main_bp.route('/room_details/<rid>', methods = ["GET"])
def room_details(rid):
    room_materials={}
    if int(rid) > 0:

        details = Rooms.get(Rooms.rID == rid)
        room_materials["roomType"]=details.roomType
        room_materials["building"]=details.building.name
        room_materials["number"]=details.number
        room_materials['maxCapacity']= details.maxCapacity
        room_materials['visualAcc']= details.visualAcc
        room_materials['audioAcc']= details.audioAcc
        room_materials['physicalAcc']=details.physicalAcc
        room_materials['specializedEq']= details.specializedEq
        room_materials['movableFurniture']=details.movableFurniture
        room_materials['specialFeatures']=details.specialFeatures
        room_materials['roomImgURL']=details.roomImageURL
        room_materials['educationTech']=education_Tech(rid)


    return json.dumps(room_materials)


@main_bp.route('/education_Tech/<rid>', methods = ["GET"])
def education_Tech(rid):

    educationTech = Rooms.get(Rooms.rID == rid).educationTech
    return json.dumps(model_to_dict(educationTech))


@main_bp.route("/postPreference", methods=["POST"]) # This method serves to post data from the user input and dumps into the database
def postPreference():
    """
    State handler for adding preferences, updating any_Choice, and none_Choice

    """
    data = request.form #data coming from POST

    pref = int(data["pref_id"]) # Preference to be updated for a course

    room = int(data["roomID"]) # ID of the room to update a course's room preference with.

    rp = RoomPreferences.get(RoomPreferences.course == data["ogCourse"])
    rp.initial_Preference = 0 # Just something we're not sure what to do with.
    any_choice = None
    none_choice = None
    print("Room {} pref {} ".format(room,pref))
    if room > 0: #If a room was selected

        if (pref == 1): # for preference 1

            rp.pref_1      = int(data["roomID"]) # grab selected roomID

            rp.any_Choice  = 2 # Set all succeeding preferences to any room works

            rp.none_Choice = None # update database to reflect that 'This course does not require a room/No other room works' was not selected

            any_choice = 2

        elif (pref == 2): # preference 2
            rp.pref_2      = int(data["roomID"])
            if rp.any_Choice is not None and int(rp.any_Choice) >= 2:
                any_choice  = 3
            else:
                any_choice = None

            if rp.none_Choice is not None and int(rp.none_Choice) >= 2:
                none_choice = 3
            else:
                none_choice = None

            rp.any_Choice = any_choice
            rp.none_Choice = none_choice


        elif(pref == 3): # preference 3
            rp.pref_3      = int(data["roomID"])
            rp.none_Choice = None

        else:

            flash("You tried to select a preference that doesn't exist!","ERROR!!! :(")

            return json.dumps({"success  ": 0}) # Picked a preference outside of 1,2,or 3

    elif room == 0:# if 'Any room works' was selected

        if (pref == 1): # for preference 1
            # Was 100. Why? (Caused foreign key errors since no room 100 existed)
            rp.pref_1      = None # Set preference 1 of the specific course to None to indicate that a room was not selected for that particular preference
            rp.pref_2      = None # Same for preference 2
            rp.pref_3      = None # Same for preference 3
            rp.any_Choice  = 1 # Set the column 'any_choice' to the preference ID to indicate that 'Any room was selected'
            rp.none_Choice = None # update database to reflect that 'This course does not require a room/No other room works' was not selected

            any_choice = 1


        elif (pref == 2): # preference 2
            rp.pref_2      = None
            rp.pref_3      = None
            rp.any_Choice  = 2
            rp.none_Choice = None

            any_choice = 2

        elif(pref == 3): # preference 3
            rp.pref_3      = None
            rp.any_Choice  = 3
            rp.none_Choice = None
            any_choice = 3

    elif room == -1:  # If 'No other rooms work' or 'This course does not require a room' was selected
        # if(rp.any_Choice == str(pref).decode("utf-8")): rp.any_Choice = None // FIXME: WHAT DOES THIS DO???>????
        if (pref == 1): # for preference 1
            rp.any_Choice  = None # Set the 'any_choice' column of a course to none to indicate that 'Any room works' was not selected
            rp.pref_1      = None # Set preference 1 for the course to None to indicate that a room was not selected as preference
            rp.none_Choice = 1 # Set the none_choice column to the preference ID to indicate that 'No other rooms work' or 'This course does not require a room' was selected for the course

            rp.pref_2      = None # Set preference 2 for the course to 100 to indicate that a room was not selected as preference

            none_choice = 1

            rp.pref_3      = None # Set preference 3 for the course to 100 to indicate that a room was not selected as preference

            flash("WARNING: This indicates to the registrar that this course does not need a room","error")

        elif (pref == 2):
            rp.pref_2 = None
            rp.none_Choice = 2
            rp.pref_3 = None
            rp.any_Choice = None

            none_choice = 2

        elif(pref == 3):

            rp.pref_3 = None

            rp.none_Choice = 3

            rp.any_Choice = None

            none_choice = 3




    rp.save() # Save the room preference in the database for the course

    #if room has crosslisted courses, update CC roompreferences to0
    if rp.course.crossListed:
        rm = RoomPreferences()
        rm.update_cc_child(room, pref, data["ogCourse"], none_choice, any_choice)

    # print('RP_any', rp.any_Choice)
    # print("RP_None", rp.none_Choice )
    # print("RP-Pref1", rp.pref_1)
    # print("RP-Pref2", rp.pref_2)
    # print("RP-Pref3", rp.pref_3)
    postNotes(data["ogCourse"], data['note'])
    return json.dumps({"success": 1})


@main_bp.route("/getNotes/<cid>", methods=["GET"])
def getNotes(cid):
    """
    Gets the notes for a course, to add into the UI textarea in the modal
    """
    # print ("Getted", RoomPreferences.get(RoomPreferences.course == cid).notes)
    return json.dumps({"notes": RoomPreferences.get(RoomPreferences.course == cid).notes})


def postNotes(cid, note):
    # Disabled all ability to track notes per preference; now all notes are just one thing everywhere (for a course)

    room_preference = RoomPreferences.get(RoomPreferences.course == cid)
    room_preference.notes = note
    room_preference.save()
    if room_preference.course.crossListed:
        qs = CrossListed.select().where(CrossListed.courseId == cid).where(CrossListed.crosslistedCourse !=  cid)
        if qs.exists():
            for obj in qs:
                child = RoomPreferences.get(RoomPreferences.course==obj.crosslistedCourse.cId)
                child.notes = note
                child.save()
