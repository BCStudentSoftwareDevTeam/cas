from app.controllers.admin_routes import *
# from app.controllers.admin_routes.admin_routes import *

from app.allImports import *
from app.updateCourse import DataUpdate
from app.models.models import User, Division, DivisionChair
from app.logic.authorizedUser import AuthorizedUser, must_be_admin


@admin_bp.route("/admin/divisionManagement/<did>", methods=["GET"])
@must_be_admin
def adminDivisionManagement(did):

   users = User.select().order_by(User.lastName)
   divisions = Division.select()
   division = Division.get(Division.dID == did)
   divisionChairs = {}
   divisionChairs[division.dID] = DivisionChair.select().where(DivisionChair.did == division.dID)

   cfg = load_config()
   return render_template("editDivision.html",
                           division      = division,
                           divisionChairs = divisionChairs,
                           users         = users,
                           divisions     = divisions,
                           cfg           = cfg
                           )
