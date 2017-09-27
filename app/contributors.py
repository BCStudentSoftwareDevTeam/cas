from app.allImports import *

@app.route("/contributors/", methods = ["GET"])
def contributors():
    return render_template("contributors.html",
                        cfg = cfg,
                        )