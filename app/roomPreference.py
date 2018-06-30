from app.allImports import *
from flask import render_template
from app.logic.redirectBack import redirect_url
from app import app
from app.logic import course


# @app.route("/roomPreference/<rid>", methods = ["GET"])
@app.route("/roomPreference/", methods = ["GET"])
# def roomPreference(rid = 1):
def roomPreference():
    page="Room Preference"
    roompreference = RoomPreferences.select()
    # room = Room.select().where(Room.rID = rid)
    print(roompreference)
    user= User.select()
    return render_template("roomPreference.html",
    roompreference= roompreference,
    user=user,
   
    )