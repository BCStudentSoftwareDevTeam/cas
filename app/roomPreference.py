from app.allImports import *
from flask import render_template
from app.logic.redirectBack import redirect_url
from app import app

@app.route("/roomPreference", methods = ["GET"])
def roomPreference():
    return render_template("roomPreference.html")
    