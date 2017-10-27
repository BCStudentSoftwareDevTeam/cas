from allImports import *
from updateCourse import DataUpdate
from app.logic.redirectBack import redirect_url
import datetime
from app.logic.authorization import must_be_admin


@app.route("/deadline/create", methods=["POST"])
@must_be_admin
def deadlineCreate():
    page = "/" + request.url.split("/")[-1]
    
    data = request.form
    
    date = datetime.datetime.strptime(data['deadlineDate'],"%m/%d/%Y").date()
    deadline = Deadline.create(
        description=data['deadlineDescription'],
        date=date)
    deadline.save()

    message = "Deadline: {0} has been added".format(deadline.description)
    log.writer("INFO", page, message)
    flash("Your Deadline has been created")
    return redirect(redirect_url())


@app.route("/deadline/edit", methods=["POST"])
@must_be_admin
def deadlineEdit():
    page = "/" + request.url.split("/")[-1]

    data = request.form

    deadline = Deadline.get(Deadline.id == data['id'])
    deadline.description = data['deadlineDescription']
    deadline.save()

    message = "Deadline: has been edited to {0}".format(
        deadline.description)
    log.writer("INFO", page, message)
    flash("Your Deadline has been edited")
    return redirect(redirect_url())


@app.route("/deleteDeadline", methods=["POST"])
@must_be_admin
def deleteDeadline():
    page = r"/" + request.url.split("/")[-1]

    data = request.form

    deadline = Deadline.get(Deadline.id == int(data['id']))
    deadline.delete_instance()

    message = "Deadline: {0} has been deleted".format(deadline.description)
    log.writer("INFO", page, message)
    flash("Your Deadline has been deleted")
    return redirect(redirect_url())
