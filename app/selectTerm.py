from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic import functions

@app.route("/selectTerm", methods=["GET", "POST"])
def selectTerm():
    terms = Term.select().order_by(Term.termCode.desc())
    authorizedUser = AuthorizedUser()
    username = authorizedUser.getUsername()
    user = User.get(User.username == username)
    print(user)
    if user.lastVisited is not None:
        prefix = user.lastVisited.prefix
    else:
        prefix = "MAT"

    return render_template("selectTerm.html", allTerms=terms, prefix=prefix, cfg=cfg)


 