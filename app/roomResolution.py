from allImports import *
from app import app

@app.route("/roomResolution", methods=["GET"])

def roomResolution():
    # Creating the UI
      return render_template("roomResolution.html")
      
@app.route("/roomResolutionView", methods=["GET"])

def roomResolutionView():
       # Creating the UI
      return render_template("roomResolutionView.html")