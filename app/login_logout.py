from allImports import *

from app.logic.redirectBack import redirect_url
@app.route("/login", methods=["GET"])
def login():
    # get the user from shibboleth
        system_user = authUser(request.environ)
        
        # look for user in our database
        user = User.get(User.username == system_user)
        if user is None:
            abort(403)
        else:
            login_user(user)
            print user.username
        return redirect(redirect_url())