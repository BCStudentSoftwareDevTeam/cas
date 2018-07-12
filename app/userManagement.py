#Controller that talks to model for userManagement html file
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
def user_insert(): # this function is used to update and delete data from the user input
   
    programchairs = ProgramChair.select()
    
    # request.form requests data from the front end on what the user has entered
    # for the adding users
    if request.form.get('adduser') == 'adduser' : 
        if request.form.get('access') == "program_chair":
            pch = ProgramChair.create(username = request.form.get("userToAdd"), pid =request.form.get("program"))
            pch.save()
            flash("Your changes have been successfully saved!")
           
        elif request.form.get('access') == 'division_chair':
            dc = DivisionChair.create(username = request.form.get("userToAdd"), did = request.form.get("division"))
            dc.save()
            flash("Your changes have been successfully saved!")
        elif request.form.get('access') == 'building_manager':
            bm = BuildingManager.create(username = request.form.get("userToAdd"), bmid = request.form.get("building"))
            bm.save()
            flash("Your changes have been successfully saved!")
        elif request.form.get('access') == 'administrator' :
            pass
            # data = request.form

            # if data['admin'] != "None":
            #     # get the user
            # user = User.create(User.username = request.form['admin'])
    
            # # toggle admin status
            # user.isAdmin = not user.isAdmin
            # user.save()
            
    #for the removing users        
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

    return redirect(url_for("userManagement"))
    
if __name__ == '__main__':
    app.run()
    
    
