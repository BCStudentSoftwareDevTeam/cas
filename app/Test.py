from allImports import *
@app.route("/example", methods = ["GET"])
def example():
    return render_template("example.html", cfg = cfg)