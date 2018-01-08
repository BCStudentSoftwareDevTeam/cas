from allImports import *
from updateCourse import DataUpdate
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic import functions
from app.logic.authorization import require_authorization

@app.route("/selectTerm", methods=["GET"])
@require_authorization
def selectTerm():
    terms = Term.select().order_by(Term.termCode.desc())
    user = g.user
    if user.lastVisited is not None:
        prefix = user.lastVisited.prefix
    else:
        prefix = "MAT"
    return render_template("selectTerm.html", allTerms=terms, prefix=prefix)



 