from app.allImports import *
from flask import render_template
from app.logic.redirectBack import redirect_url
from app import app
from app.logic import course


@app.route("/roomPreference/<rid>", methods = ["GET"])
def roomPreference(rid, prefix):
    page="Room Preference"
    room = Rooms.select().where(Rooms.rID ==rid).get()
   


    # course= Course.select().where(Course.cId).get()
    user= User.select().get()
    
   
    
    return render_template("roomPreference.html",
    room= room,
    user=user,
    courses=courses)