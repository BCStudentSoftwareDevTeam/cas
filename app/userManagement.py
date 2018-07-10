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
                           
                           
@app.route("/admin/userInsert", methods = ["POST"])                           
def user_insert(): # this function is used to update and delet data from the user input
    print(request.form)
    # Conditional for type of action (Remove or add)
    if request.form.get('removeuser') == 'removeuser':
        # print ("remove")i
        pc = ProgramChair.get(ProgramChair.username == request.form.get("userToRemove"), ProgramChair.pid == request.form.get("program"))
        pc.delete_instance()
        # bm = BuildingManager.get(BuildingManager.username == request.form.get("userToRemove"), BuildingManager.bmid == request.form.get("building"))
        # bm.delete_instance()
        # dc = DivisionChair.get(DivisionChair.username == request.form.get("userToRemove"), DivisionChair.did== request.form.get("division"))
        # dc.delete_instance()

    elif request.form.get('adduser') == 'adduser' :
        # print ("adduser")
        pass
   
    return redirect(url_for("userManagement"))
    
if __name__ == '__main__':
    app.run()