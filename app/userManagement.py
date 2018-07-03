#Controller that talks to model for userManagement html file
from allImports import *
from app.logic.authorization import must_be_admin
from programManagement import *

@app.route("/admin/userManagement", methods=["GET"])
@must_be_admin
  
 
def userManagement0():
    page        = "/" + request.url.split("/")[-1]
    users = User.select()
    programs = Program.select()
    buildings = Building.select()
    divisions = Division.select()
    admins = User.select().where(User.isAdmin== 1)
    programchairs = ProgramChair.select().where(User.ProgramChair == 1)
    divisionchairs = DivisionChair.select().where(User.DivisionChair == 1)
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
                           buildingmanagers = buildingmanagers,
                          
                           )
         
 




