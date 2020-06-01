from app.controllers.admin_routes import *
# from app.controllers.admin_routes.admin_routes import *

from app.allImports import *
from app.logic.redirectBack import redirect_url
from app.logic.authorizedUser import AuthorizedUser, must_be_admin
from app.models.models import ProgramChair

@admin_bp.route("/editProgram", methods=["POST"])
@must_be_admin
def editProgram():
    page        = "/" + request.url.split("/")[-1]
    data        = request.form
    newChairs   = request.form.getlist('professors[]')
    pid         = data['pID']

    #SELECT ALL OF THE CURRENT CHAIRS OF THE PROGRAM
    currentChairs = ProgramChair.select().where(ProgramChair.pid == pid)
    #LOOP THROUGH ALL OF THE CURRENT CHAIRS
    for currentChair in currentChairs:
      #IF A USER'S NAME IS NOT PART OF THE NEWCHAIR LIST THEN DELETE THEM
      if currentChair.username.username not in newChairs:
        message = "USER: {0} has been removed as a program chair for pid: {1}".format(currentChair.username.username,pid)
        # log.writer("INFO", page, message)
        currentChair.delete_instance()
      else:
        #HOWEVER IF THEY ARE PART OF THE LIST, DELETE THEM FROM THE LIST
        newChairs.remove(currentChair.username.username)
    #LOOK THROUGH THE NEW CHAIR LIST
    for user_name in newChairs:
      #ADD THE USERNAMES TO THE PROGRAM CHAIR LIST
      newChair  = ProgramChair(username = user_name, pid = pid)
      newChair.save()
      message = "USER: {0} has been added as a program chair for pid: {1}".format(user_name,pid)
      # log.writer("INFO", page, message)

    flash("Program succesfully changed")
    return redirect(redirect_url())
