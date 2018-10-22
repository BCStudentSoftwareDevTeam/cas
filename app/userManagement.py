#Controller that talks to model for userManagement html file

#THERE IS MORE OF THE CODE IN THE REMOVE USER PYTHON FILE AND REMOVE USER JS FILE
from allImports import *
from app.logic.authorization import must_be_admin
from programManagement import *
from flask import Flask, render_template, request

@app.route("/admin/userManagement", methods=["GET"])
@must_be_admin
def userManagement():
    page        = "/" + request.url.split("/")[-1]
    users = User.select()
    programs = Program.select()
    buildings = Building.select()
    divisions = Division.select()
    admins = User.select().where(User.isAdmin == 1)
    programchairs = ProgramChair.select()
    divisionchairs = DivisionChair.select()
    buildingmanagers = BuildingManager.select()
    
    return render_template("userManagement.html",
                        #passing of the variable to html,
                           programs = programs,
                           buildings = buildings,
                           divisions = divisions,
                           users = users,
                           admins = admins,
                           divisionchairs = divisionchairs,
                           programchairs = programchairs,
                           buildingmanagers = buildingmanagers
                           )

                           
                           
@app.route("/admin/userInsert", methods = ["POST"]) #'admin/userInsert points to the URL for the form in html file'                          
def user_insert():
    '''
    this function is used to update and delete data from the user input
    request.form requests data from the front end on what the user has entered
    for updating added users, we use get_or_create to prevent duplication of data in the database when a user is added more than once
    '''
    if request.form.get('adduser') == 'adduser' : 
        if request.form.get('access') == "program_chair":                     
            pch = ProgramChair.get_or_create(username = request.form.get("userToAdd"), pid =request.form.get("program"))
            flash("Your changes have been successfully saved!")
        elif request.form.get('access') == 'division_chair':
            dc = DivisionChair.get_or_create(username = request.form.get("userToAdd"), did = request.form.get("division"))
            flash("Your changes have been successfully saved!")
        elif request.form.get('access') == 'building_manager':
            bm = BuildingManager.get_or_create(username = request.form.get("userToAdd"), bmid = request.form.get("building"))
            flash("Your changes have been successfully saved!")
        elif request.form.get('access') == 'administrator' :
            user = User.get(username = request.form.get("userToAdd"))  
            user.isAdmin = 1
            user.save() # We add save() for admin because it is not adding a new record
            
            
    #for updating removed users       
    elif request.form.get('removeuser') == 'removeuser':  
        if request.form.get('access') == "program_chair":
            pc = ProgramChair.get(ProgramChair.username == request.form.get("userToRemove"), ProgramChair.pid == request.form.get("program"))
            pc.delete_instance()
            flash("Your changes have been successfully saved!")
        elif request.form.get('access') == 'division_chair':
            dc = DivisionChair.get(DivisionChair.username == request.form.get("userToRemove"), DivisionChair.did== request.form.get("division"))
            dc.delete_instance()
            flash("Your changes have been successfully saved!")
        elif request.form.get('access') == 'building_manager':
            bm = BuildingManager.get(BuildingManager.username == request.form.get("userToRemove"), BuildingManager.bmid == request.form.get("building"))
            bm.delete_instance()
            flash("Your changes have been successfully saved!")
        elif request.form.get('access') == 'administrator' :
            user = User.get(User.username == request.form.get("userToRemove"))
            user.isAdmin = 0
            user.save()

    return redirect(url_for("userManagement"))
    
if __name__ == '__main__':
    app.run()
    
    
