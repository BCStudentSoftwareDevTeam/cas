from allImports import *
@app.route("/newviews", methods = ["GET"])
def show():
    return render_template("newview.html", cfg = cfg)


    