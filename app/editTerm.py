from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
@app.route("/editTerm/<state>", methods=["POST"])
def editterm(state):
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
      page =  "/" + request.url.split("/")[-1]
      data = request.form
      term = Term.get(Term.termCode == data['termCode'])
      if state == "locked":
        term.editable = False
        term.locked = True
      elif state == "tracking":
        term.editable = False
        term.locked = False
      elif state == "open":
        term.editable = True
        term.locked = False
      else:
        return jsonify({"Error": "Invalid State"})
        
      term.save()
      message = "Term: term {0} is now in {1} mode".format(data['termCode'], state)
      log.writer("INFO", page, message)
      return redirect(redirect_url())