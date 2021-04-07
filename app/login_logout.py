from app import app
from app.allImports import *
from app.logic.redirectBack import redirect_url
from flask import session

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route("/login", methods=["GET"])
def login():
    # get the user from shibboleth
    system_user = authUser(request.environ)
    # look for user in our database
    try:
        user = User.get(User.username == system_user)
        print(user.username)
        login_user(user)
        return redirect(redirect_url())
    except Exception as e:
        abort(401)
    abort(401)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect('https://login.berea.edu/idp/profile/Logout')
