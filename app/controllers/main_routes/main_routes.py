from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.login_manager import *
import datetime

from app.allImports import *
from app.models.models import Term, Deadline
from app.loadConfig import load_config
from app.logic.authorizedUser import AuthorizedUser, can_modify, must_be_admin

@main_bp.before_app_request
def before_request():
    pass # TODO Do we need to do anything here? User stuff?

@main_bp.route("/", methods=["GET"])
@can_modify
def deadlineDisplay(can_edit):

    today = datetime.date.today()

    for key in list(session.keys()):
    # for key in session.keys():
        session.pop(key)
    terms = Term.select().order_by(-Term.termCode)

    tid = terms[0].termCode

    dates=Deadline.select()

    cfg = load_config()
    au = AuthorizedUser()
    return render_template("deadline.html",
                           allTerms = terms,
                           cfg = cfg,
                           can_edit = can_edit,  #g.user.isAdmin,
                           currentTerm=int(tid),
                           deadlines=dates,
                           today = today,
                           isAdmin = au.user.isAdmin)

@main_bp.route("/deadline/create", methods=["POST"])
@must_be_admin
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
    return redirect(url_for('main.deadlineDisplay'))


@main_bp.route("/deadline/edit", methods=["POST"])
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
    return redirect(url_for('main.deadlineDisplay'))
