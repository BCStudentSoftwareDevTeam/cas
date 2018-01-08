from allImports import *
from updateCourse import DataUpdate
import datetime
from app.logic.authorization import must_be_authorized
from app.logic.authorization import can_modify
from flask import session

@app.route("/", methods=["GET"])
@can_modify
def deadlineDisplay(can_edit):
    print session.keys()
    for key in session.keys():
        session.pop(key)
    today = datetime.date.today()
    dates=Deadline.select().where(Deadline.date > today).distinct().order_by(
        Deadline.date)
        
    return render_template("deadline.html",
                           can_edit=can_edit,
                           deadlines=dates,
                           today=today)
