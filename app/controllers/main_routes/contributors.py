from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.allImports import *
from app.loadConfig import load_config

@main_bp.route("/contributors/", methods = ["GET"])
def contributors():
    cfg = load_config()
    return render_template("contributors.html", cfg = cfg)
