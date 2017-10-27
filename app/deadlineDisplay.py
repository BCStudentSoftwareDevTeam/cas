from allImports import *
from updateCourse import DataUpdate
import datetime
from app.logic.authorization import can_modify


@app.route("/", methods=["GET"])
@can_modify
def deadlineDisplay(can_edit):
    today = datetime.date.today()
    dates=Deadline.select().where(Deadline.date > today).distinct().order_by(
        Deadline.date)
        
    return render_template("deadline.html",
                           can_edit=can_edit,
                           deadlines=dates,
                           today=today)
