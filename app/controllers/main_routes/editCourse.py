from collections import defaultdict

from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.allImports import *
from app.updateCourse import DataUpdate
from app.logic.TrackerEdit import TrackerEdit
from app.logic import databaseInterface
from app.logic.courseLogic import find_crosslist_via_id
from app.loadConfig import load_config
from app.models.models import *
from app.logic.authorizedUser import can_modify


@main_bp.route("/editCourseModal/<tid>/<prefix>/<cid>/<page>", methods=["GET"])
def editCourseModal(tid, prefix, cid, page):

    # Select all schedules
    schedules = BannerSchedule.select().order_by(BannerSchedule.order)
    # Select all terms
    terms = Term.select()
    # Select the course informations
    course = Course.get(Course.cId == cid)
    # Select all users
    users = User.select().order_by(User.lastName)
    # Select instructors for the course
    instructors = {}
    instructors[course.cId] = InstructorCourse.select().where(InstructorCourse.course == course.cId)
    print("Instructors: ", instructors[course.cId])
    # SELECT ALL ROOMS
    rooms     = Rooms.select()

    getCrosslistedCourses = find_crosslist_via_id(cid)
    allCourses = BannerCourses.select().order_by(BannerCourses.reFID)
    currentCrosslistedCourse = None
    if(getCrosslistedCourses):
      for c in getCrosslistedCourses:
        currentCrosslistedCourse = list(getCrosslistedCourses[c])
    cfg = load_config()
    return render_template("snips/courseElements/editCourse.html",
                            schedules = schedules,
                            terms     = terms,
                            allCourses=allCourses,
                            currentCrosslistedCourse=currentCrosslistedCourse,
                            course    = course,
                            users = users,
                            instructors = instructors,
                            currentTerm = int(tid),
                            page        = page,
                            rooms       = rooms,
                            cfg = cfg
                            )

@main_bp.route("/editcourse/<tid>/<prefix>/<page>", methods=["POST"])
@can_modify
def editcourse(tid, prefix, page, can_edit):
  #WE NEED TO CHECK TO ENSURE THE USER HAS THE RIGHT TO EDIT PAGES
    cfg = load_config()
    au = AuthorizedUser()
    username = au.username
    user = au.user
    page1 =  "/" + request.url.split("/")[-1]
    data = request.form.to_dict()
    crosslistedCourse = request.form.getlist('crossListedCourses[]')
    data["crossListed"] = 1 if crosslistedCourse else 0
    professors = request.form.getlist('professors[]')
    if ((not au.user.isAdmin) and (Term.get(Term.termCode == tid).term_state.number) != 1): #If the term is not open for scheduling changes:
        print(au.user.isAdmin)
        print(Term.get(Term.termCode == tid).term_state.number)
        return render_template("schedulingLocked.html", tid = tid, prefix = prefix, cfg = cfg)
    databaseInterface.editCourse(data, prefix, professors, crosslistedCourse)
    message = "Course: course {} has been edited".format(data['cid'])
    flash("Course information has successfully been modified!")
    if page == 'courses':
      return redirect(url_for("main.courses", tID=tid, prefix=prefix))
    else:
      url = "/courseManagement/" + page + "/" + tid
      return redirect(url)

@main_bp.route("/editSTCourseModal/<tid>/<prefix>/<stid>/<page>", methods=["GET"])
def editSTCourseModal(tid, prefix, stid, page):
  checkUser = DataUpdate()

  # Select all schedules
  schedules = BannerSchedule.select().order_by(BannerSchedule.order)
  # Select all terms
  terms = Term.select()
  # Select the course informations
  course = SpecialTopicCourse.get(SpecialTopicCourse.stId == stid)
  # Select all users
  users = User.select().order_by(User.lastName)
  # Select instructors for the course
  instructors = {}
  instructors[course.stId] = InstructorSTCourse.select().where(InstructorSTCourse.course == course.stId)
  # SELECT ALL ROOMS
  rooms     = Rooms.select()

  return render_template("snips/courseElements/editSTCourse.html",
                          schedules = schedules,
                          cfg = cfg,
                          terms     = terms,
                          course    = course,
                          users = users,
                          instructors = instructors,
                          currentTerm = int(tid),
                          page        = page,
                          rooms       = rooms
                          )


@main_bp.route("/editstcourse/<tid>/<prefix>/<page>", methods=["POST"])
@can_modify
def editSTcourse(tid, prefix, page, can_edit):
  if can_edit:
      #WE NEED TO CHECK TO ENSURE THE USER HAS THE RIGHT TO EDIT PAGES
      page1 =  "/" + request.url.split("/")[-1]
      data = request.form
      specialCourse = SpecialTopicCourse.get(SpecialTopicCourse.stId == int(data['stid']))
      if data['submitbtn'] == "Submit":
        specialCourse.status = cfg['specialTopicLogic']['submitted']
      professors = request.form.getlist('professors[]')
      if page1 == "/specialCourses":
          if data['statusChange']:
            databaseInterface.editSTCourse(data, prefix, professors, int(data['statusChange']),cfg)
          else:
            databaseInterface.editSTCourse(data, prefix, professors, specialCourse.status,cfg)

      else:
          databaseInterface.editSTCourse(data, prefix, professors, specialCourse.status ,cfg)

      message = "Course: course {} has been edited".format(data['stid'])
      # log.writer("INFO", page1, message)
      flash("Course information has successfully been modified!")
      if page == 'courses':
        return redirect(url_for("main.courses", tID=tid, prefix=prefix))
      else:
        url = "/courseManagement/" + page + "/" + tid
        return redirect(url)
  else:
      abort(403)
