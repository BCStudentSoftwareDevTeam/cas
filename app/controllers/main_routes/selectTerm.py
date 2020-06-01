from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.allImports import *
from app.updateCourse import DataUpdate
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic import functions
from app.models.models import Term, User
from app.logic.authorizedUser import *
from app.loadConfig import load_config

cfg = load_config()

@main_bp.route("/selectTerm", methods=["GET"])
def selectTerm():
    terms = Term.select().order_by(Term.termCode.desc())
    au = AuthorizedUser()
    prefix = au.getSubject()

    if au.getSubject() is not None:
        prefix = au.getSubject()
    else:
        prefix = "MAT"          # Arbitrarily send them to MAT because whatev.

    return render_template("selectTerm.html",
                            allTerms=terms,
                            prefix=prefix,
                            cfg = cfg)
