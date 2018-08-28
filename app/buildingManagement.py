#Controllger for Building Management page
from allImports import *
from app.logic.authorization import must_be_admin

@app.route("/admin/buildingManagement", methods=["GET"])
@must_be_admin #Should be a requirement for a building manager, not admin

def buildingManagement():

    return render_template("buildingManagement.html")