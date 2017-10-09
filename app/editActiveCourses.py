from allImports import *
from app.logic.getAuthUser import AuthorizedUser

@app.route("/edit/active/courses", methods=['GET'])
def editAcitveCourses():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
        activeCourses   = BannerCourses.select().where(BannerCourses.is_active == True)
        deactiveCourses = BannerCourses.select().where(BannerCourses.is_active == False)
        return render_template("editActiveCourses.html",
                                cfg             = cfg,
                                activeCourses   = activeCourses,
                                deactiveCourses = deactiveCourses
                               )
    else:
        abort(403)