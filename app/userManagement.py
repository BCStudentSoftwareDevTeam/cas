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
    programchairs = ProgramChair.select()
    buildings = Building.select()
    divisions = Division.select()
    
    return render_template("userManagement.html",
                           programchairs = programchairs, #passing of the variable to html,
                           programs = programs,
                           buildings = buildings,
                           divisions = divisions,
                           users = users
                           
                           )
         
 




