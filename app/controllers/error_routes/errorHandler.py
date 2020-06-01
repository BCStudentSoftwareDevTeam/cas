from app.controllers.error_routes import *
# from app.controllers.admin_routes import *

from app.allImports import *

@error_bp.errorhandler(401)
def unauthorized(e):
    return render_template('/snips/errors/401.html'), 401

@error_bp.errorhandler(403)
def unauthenticated(e):
    return render_template('/snips/errors/403.html'), 403

@error_bp.errorhandler(404)
def pageNotFound(e):
    return render_template('/snips/errors/404.html'), 404
