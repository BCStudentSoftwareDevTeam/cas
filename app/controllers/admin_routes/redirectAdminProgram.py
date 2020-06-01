from app.controllers.admin_routes import *
from app.models.models import Program, Division

from app.allImports import *

# No idea why these exist -SH

@admin_bp.route("/redirect/program_management", methods=["GET"])
def redirectProgramManagement():
   program = Program.get()

   return redirect(url_for("admin.adminProgramManagement",
                           pid = program.pID, ))

@admin_bp.route("/redirect/division_management", methods=["GET"])
def redirectDivisionManagement():
   division = Division.get()

   return redirect(url_for("admin.adminDivisionManagement",
                           did = division.dID, ))
