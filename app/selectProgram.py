from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic import functions

@app.route("/selectProgram", methods=["GET", "POST"])
def selectProgram():
    programs = Program.select()
    authorizedUser = AuthorizedUser()
    subjects = Subject.select()
    return render_template("selectProgram.html", allPrograms=programs, subjects = subjects, cfg=cfg)


 