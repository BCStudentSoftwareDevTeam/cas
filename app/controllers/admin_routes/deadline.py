from app.controllers.admin_routes import *
# from app.controllers.admin_routes.admin_routes import *

from app.allImports import *
from app.updateCourse import DataUpdate
import datetime
from app.logic.redirectBack import redirect_url
from app.logic.authorizedUser import AuthorizedUser, must_be_admin
from flask import session
import datetime

from app.models import *


@admin_bp.route("/", methods=["GET"])
#FIXME: @can_modify
def deadlineDisplay():

    today = datetime.date.today()

    for key in session.keys():
        session.pop(key)
    terms = Term.select().order_by(-Term.termCode)

    tid = terms[0].termCode

    dates=Deadline.select()
    return render_template("deadline.html",
                           allTerms = terms,
                           cfg = cfg,
                           can_edit=True,             #FIXME: can_edit,  #g.user.isAdmin,
                           currentTerm=int(tid),
                           deadlines=dates,
                           today = today)

@admin_bp.route("/deadline/create", methods=["POST"])
def deadlineCreate():
    # page = "/" + request.url.split("/")[-1]

    data = request.form

    # date = datetime.datetime.strptime(data['deadlineDate'],"%m/%d/%Y").date()
    date = datetime.date.today()

    deadline = Deadline.create(
        description=data['deadlineDescription'],
        date=date)
    deadline.save()

    message = "Deadline: {0} has been added".format(deadline.description)
    # log.writer("INFO", page, message)
    flash("Your Deadline has been created")
    return redirect(redirect_url('/'))


@admin_bp.route("/deadline/edit", methods=["POST"])
@must_be_admin
def deadlineEdit():

    try:
        data = request.form

        deadline = Deadline.get(Deadline.id == data['id'])
        # this condition checks to see if the deadline box is empty and prints a message.
        if data['deadlineDescription'] == "":
            deadline.description = "Upcoming deadlines will be posted here."
        else:
            deadline.description = data['deadlineDescription']
        deadline.save()


        message = "Deadline: has been edited to {0}".format(
        deadline.description)
        log.writer("INFO", "/", message)
        flash("Your Deadline has been edited")
    except Exception as e:
        flash('Error while trying to edit your deadline.')
        print(e)
    return redirect(redirect_url('/'))
