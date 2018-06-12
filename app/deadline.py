from allImports import *
from updateCourse import DataUpdate
import datetime
from app.logic.redirectBack import redirect_url
from app.logic.authorization import can_modify
from flask import session
import datetime

@app.route("/", methods=["GET"])
@can_modify
def deadlineDisplay(can_edit):
    today = datetime.date.today()
    for key in session.keys():
        session.pop(key)
    terms = Term.select().order_by(-Term.termCode)
    tid = terms[0].termCode
    dates=Deadline.select()
    return render_template("deadline.html",
                           allTerms = terms,
                           can_edit=g.user.isAdmin,
                           currentTerm=int(tid),
                           deadlines=dates,
                           today = today)

@app.route("/deadline/create", methods=["POST"])
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