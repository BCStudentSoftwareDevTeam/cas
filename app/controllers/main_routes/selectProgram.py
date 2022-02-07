from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.allImports import *
from app.updateCourse import DataUpdate
from app.logic.authorizedUser import AuthorizedUser
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic import functions
from app.loadConfig import load_config

from app.models.models import Program, Subject

@main_bp.route("/selectProgram", methods=["GET", "POST"])
#FIXME: @require_authorization
def selectProgram():
    cfg = load_config()
    programs = Program.select().order_by(Program.name)
    subjects = Subject.select()
    return render_template("selectProgram.html",
                            allPrograms=programs,
                            subjects = subjects,
                            cfg=cfg)
