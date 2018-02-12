from allImports import *
from updateCourse import DataUpdate
import datetime
from app.logic.redirectBack import redirect_url
from app.logic.authorization import can_modify
from app.logic.authorization import must_be_admin
from flask import session

@app.route("/", methods=["GET"])
@can_modify
def deadlineDisplay(can_edit):
    print session.keys()
    for key in session.keys():
        session.pop(key)
    dates=Deadline.select()   
    return render_template("deadline.html",
                           can_edit=g.user.isAdmin,
                           deadlines=dates)

@app.route("/deadline/edit", methods=["POST"])
def deadlineEdit():
    try: 
        data = request.form
        deadline = Deadline.get(Deadline.id == data['id'])
        deadline.description = data['deadlineDescription']
        deadline.save()

        message = "Deadline: has been edited to {0}".format(
        deadline.description)
        log.writer("INFO", "/", message)
        flash("Your Deadline has been edited")
    except Exception as e:
        flash('Error while trying to edit your deadline.')
        print e
    return redirect(redirect_url('/'))