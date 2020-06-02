from app.controllers.admin_routes import *
# from app.controllers.admin_routes.admin_routes import *

from app.allImports import *
from app.logic.authorizedUser import AuthorizedUser, must_be_admin
from app.logic.redirectBack import redirect_url
from app.loadConfig import load_config

from app.models.models import BannerCourses
@admin_bp.route("/edit/active/courses", methods=['GET'])
@must_be_admin
def editActiveCourses():
    authorizedUser = AuthorizedUser()
    activeCourses   = BannerCourses.select().where(BannerCourses.is_active == True)
    deactiveCourses = BannerCourses.select().where(BannerCourses.is_active == False)
    cfg = load_config()
    return render_template("editActiveCourses.html",
                            cfg             = cfg,
                            isAdmin=authorizedUser.user.isAdmin,
                            activeCourses   = activeCourses,
                            deactiveCourses = deactiveCourses
                           )

@admin_bp.route("/deactivate/course", methods=['POST'])
@must_be_admin
def deactivateCourse():
    authorizedUser = AuthorizedUser()

    data = request.form
    Course = BannerCourses.get(BannerCourses.reFID == data['deactivate'])
    Course.is_active = False
    message = Course.subject.prefix + ' ' + Course.number + ' ' + Course.ctitle + ' has been deactivated'
    Course.save()
    flash(message)
    return redirect(redirect_url())

@admin_bp.route("/activate/course", methods=['POST'])
@must_be_admin
def activateCourse():
    authorizedUser = AuthorizedUser()

    data = request.form
    Course = BannerCourses.get(BannerCourses.reFID == data['activate'])
    Course.is_active = True
    message = Course.subject.prefix + ' ' + Course.number + ' ' + Course.ctitle + ' has been activated'
    Course.save()
    flash(message)
    return redirect(redirect_url())
