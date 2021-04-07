from app import app
from app.allImports import *
from app.logic.redirectBack import redirect_url
from flask import session
from app.models.models import User
from app import login_manager
from app.login_manager import require_login
from  app.logic.authorizedUser import authUser


@login_manager.user_loader
def user_loader(user_id):
    print("This is the userID.....",user_id)
    return User.get(User.username == user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    # get the user from shibboleth
    system_user = authUser(request.environ)
    print("This is the system user",system_user)
    print("This is the user", User.username)
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
    print(User.username)
    # user_id = session["user_id"]
    # print(user_id)
    logout_user()
    print("After Logout", User.username)

    currentUser = require_login()
    if not currentUser:
        print("There is no User logged in")
    else:
        print(User.username)
    return redirect('https://login.berea.edu/idp/profile/Logout')
