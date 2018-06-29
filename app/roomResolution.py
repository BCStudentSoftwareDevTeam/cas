from allImports import *
from app import app

@app.route("/roomResolution", methods=["GET"])

def roomResolution():
    # Creating the UI
    course = Course.select()
    bannercourses = BannerCourses.select()
    return render_template("roomResolution.html", courses=course, bannercourses=bannercourses)
      
      
@app.route("/roomResolutionView", methods=["GET"])

def roomResolutionView():
       # Creating the UI
      return render_template("roomResolutionView.html")
      
    