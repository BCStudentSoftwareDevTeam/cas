from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url

@app.route("/edit/active/courses", methods=['GET'])
def editAcitveCourses():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
        activeCourses   = BannerCourses.select().where(BannerCourses.is_active == True)
        deactiveCourses = BannerCourses.select().where(BannerCourses.is_active == False)
        return render_template("editActiveCourses.html",
                                cfg             = cfg,
                                isAdmin=authorizedUser.isAdmin(),
                                activeCourses   = activeCourses,
                                deactiveCourses = deactiveCourses
                               )
    else:
        abort(403)
        
@app.route("/deactivate/course", methods=['POST'])
def deactivateCourse():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
        data = request.form
        Course = BannerCourses.get(BannerCourses.reFID == data['deactivate'])
        Course.is_active = False
        message = Course.subject.prefix + ' ' + Course.number + ' ' + Course.ctitle + ' has been deactivated'
        Course.save()
        flash(message)
        return redirect(redirect_url())
    else:
        abort(403)
        
@app.route("/activate/course", methods=['POST'])
def activateCourse():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
        data = request.form
        Course = BannerCourses.get(BannerCourses.reFID == data['activate'])
        Course.is_active = True
        message = Course.subject.prefix + ' ' + Course.number + ' ' + Course.ctitle + ' has been activated'
        Course.save()
        flash(message)
        return redirect(redirect_url())
    else:
        abort(403)