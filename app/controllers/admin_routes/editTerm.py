from app.controllers.admin_routes import *

from app.allImports import *
from app.logic.redirectBack import redirect_url
from app.logic.authorizedUser import AuthorizedUser, must_be_admin


@admin_bp.route("/editTerm/<state>", methods=["POST"])
@must_be_admin
def editterm(state):
    page =  "/" + request.url.split("/")[-1]
    data = request.form
    term = Term.get(Term.termCode == data['termCode'])
    if state == "locked":
      term.state = 2
    elif state == "tracking":
      term.state = 1
    elif state == "open":
      term.state = 0
    else:
      return jsonify({"Error": "Invalid State"})

    term.save()
    message = "Term: term {0} is now in {1} mode".format(data['termCode'], state)
    log.writer("INFO", page, message)
    return redirect(redirect_url())
