from allImports import *
from updateCourse import DataUpdate
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic import functions
from app.logic.authorization import require_authorization

@app.route("/selectTermRP", methods=["GET"])
@require_authorization
def selectTermRP():
    terms = Term.select().order_by(Term.termCode.desc())
    user = g.user
    return render_template("selectTermForRoomPreferences.html", allTerms=terms)



 