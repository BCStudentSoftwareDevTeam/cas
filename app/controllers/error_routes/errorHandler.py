from app.controllers.error_routes import *
from app import *
# from app.controllers.admin_routes import *

from app.allImports import *

@app.errorhandler(403)
def unauthenticated(e):
    return render_template('/snips/errors/403.html', cfg = cfg), 403

@app.errorhandler(404)
def pageNotFound(e):
    return render_template('/snips/errors/404.html', cfg = cfg), 404

@app.errorhandler(500)
def internalError(e):
    return render_template('/snips/errors/500.html', cfg = cfg), 500
