from app.allImports import *
from flask import render_template
from app.logic.redirectBack import redirect_url
from app import app

@app.route("/roomPreference", methods = ["GET"])

# @save_last_visited
# @can_modify

def roomPreference():
    page="Room Preference"
    # users = User.select().order_by(User.lastName)
    # rooms = Rooms.select().order_by(Rooms.building)
   
    
    return render_template("roomPreference.html")
    