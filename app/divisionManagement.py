from allImports import *
from updateCourse import DataUpdate
from app.logic.authorization import must_be_admin


@app.route("/admin/divisionManagement/<did>", methods=["GET"])
@must_be_admin
def adminDivisionManagement(did):
      
   users = User.select().order_by(User.lastName)
   divisions = Division.select()
   division = Division.get(Division.dID == did)
   divisionChairs = {}
   divisionChairs[division.dID] = DivisionChair.select().where(DivisionChair.did == division.dID)
   
   return render_template("editDivision.html",
                           division      = division,
                           divisionChairs = divisionChairs,
                           users         = users,
                           divisions     = divisions)