from allImports import *

@app.errorhandler(401)
def unauthorized(e):
    return render_template('/snips/errors/401.html'), 401

@app.errorhandler(403)
def unauthenticated(e):
    return render_template('/snips/errors/403.html'), 403
    
@app.errorhandler(404)
def pageNotFound(e):
    return render_template('/snips/errors/404.html'), 404