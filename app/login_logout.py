from allImports import *
from app.logic.redirectBack import redirect_url
from flask import session

@app.route("/login", methods=["GET"])
def login():
    # get the user from shibboleth
    system_user = authUser(request.environ)
    # look for user in our database
    try:
        user = User.get(User.username == system_user)
        print user.username
        login_user(user)
        return redirect(redirect_url())
    except Exception as e:
        abort(401)
    abort(401)