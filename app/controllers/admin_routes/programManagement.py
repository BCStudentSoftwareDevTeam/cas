from app.controllers.admin_routes import *

from app.allImports import *
from app.updateCourse import DataUpdate
from app.logic.authorizedUser import AuthorizedUser, must_be_admin
from app.models.models import User, Division, Program, ProgramChair
from app.loadConfig import load_config

@admin_bp.route("/admin/programManagement/<pid>", methods=["GET"])
@must_be_admin
def adminProgramManagement(pid):

    users = User.select().order_by(User.lastName)

    divisions = Division.select()
    programs  = Program.select()
    program = Program.get(Program.pID == pid)
    programChairs = {}
    programChairs[program.pID] = ProgramChair.select().where(ProgramChair.pid == program.pID)
    cfg = load_config()

    return render_template("editProgram.html",
                            program       = program,
                            programChairs = programChairs,
                            users         = users,
                            divisions     = divisions,
                            programs      = programs,
                            cfg           = cfg
                            )
