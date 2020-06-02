from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.allImports import *
from app.updateCourse import DataUpdate
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic import functions
from app.logic.authorizedUser import AuthorizedUser
from app.loadConfig import load_config

@main_bp.route("/selectTermRP", methods=["GET"])
def selectTermRP():
    cfg = load_config()
    terms = Term.select().order_by(Term.termCode.desc())
    return render_template("selectTermForRoomPreferences.html",
                            allTerms=terms,
                            cfg = cfg)
