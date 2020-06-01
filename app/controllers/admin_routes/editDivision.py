from app.controllers.admin_routes import *
# from app.controllers.admin_routes.admin_routes import *

from app.allImports import *
from app.logic.redirectBack import redirect_url
from app.logic.authorizedUser import AuthorizedUser, must_be_admin
from app.models.models import DivisionChair

@admin_bp.route("/editDivision", methods=["POST"])
@must_be_admin
def editDivision():

    page        = "/" + request.url.split("/")[-1]
    data        = request.form
    newChairs   = request.form.getlist('professors[]')
    did         = data['dID']
    #SELECT ALL OF THE CURRENT CHAIRS OF THE DIVISION
    currentChairs = DivisionChair.select().where(DivisionChair.did == did)
    #LOOP THROUGH ALL OF THE CURRENT CHAIRS
    for currentChair in currentChairs:
      #IF A USER'S NAME IS NOT PART OF THE NEWCHAIR LIST THEN DELETE THEM
      if currentChair.username.username not in newChairs:
        message = "USER: {0} has been removed as a Division chair for did: {1}".format(currentChair.username.username,did)
        # log.writer("INFO", page, message)
        currentChair.delete_instance()
      else:
        #HOWEVER IF THEY ARE PART OF THE LIST, DELETE THEM FROM THE LIST
        newChairs.remove(currentChair.username.username)
    #LOOK THROUGH THE NEW CHAIR LIST
    for user_name in newChairs:
      #ADD THE USERNAMES TO THE Division CHAIR LIST
      newChair  = DivisionChair(username = user_name, did = did)
      newChair.save()
      message = "USER: {0} has been added as a Division chair for did: {1}".format(user_name,did)
      # log.writer("INFO", page, message)

    flash("Division succesfully changed")
    return redirect(redirect_url())
