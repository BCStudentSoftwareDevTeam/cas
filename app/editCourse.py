from allImports import *
from updateCourse import DataUpdate
from app.logic.TrackerEdit import TrackerEdit
from app.logic import databaseInterface
from app.logic.authorization import must_be_authorized
from app.logic.course import find_crosslist_via_id
from collections import defaultdict


@app.route("/editCourseModal/<tid>/<prefix>/<cid>/<page>", methods=["GET"])
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
    # SELECT ALL ROOMS
    rooms     = Rooms.select()

    getCrosslistedCourses = find_crosslist_via_id(cid)
    allCourses = BannerCourses.select().order_by(BannerCourses.reFID)
    currentCrosslistedCourse = None
    if(getCrosslistedCourses):
      for c in getCrosslistedCourses:
        currentCrosslistedCourse = list(getCrosslistedCourses[c])

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
                            rooms       = rooms
                            )

@app.route("/editcourse/<tid>/<prefix>/<page>", methods=["POST"])
@must_be_authorized
def editcourse(tid, prefix, page):
  #WE NEED TO CHECK TO ENSURE THE USER HAS THE RIGHT TO EDIT PAGES

    username = g.user.username
    user = User.get(User.username == username)
    page1 =  "/" + request.url.split("/")[-1]
    data = request.form.to_dict()
    crosslistedCourse = request.form.getlist('crossListedCourses[]')
    # faculty_credit= request.form.getlist('faculty_credit')
    #if no crosslisted children, update hidden crosslisted to true or false
    data["crossListed"] = 1 if crosslistedCourse else 0
    trackerEdit = TrackerEdit(data)
    professors = request.form.getlist('professors[]')
    # if (not databaseInterface.isTermOpen(tid)):
    #   if user.isAdmin:
    #     # created = trackerEdit.make_edit(professors, username) #WE AINT USING THE CHANGE TRACKER ANYMORE
    #     pass
    #   else:
    # print("did the damn thing worked?") #this whole bit broke other things...
    #                                       in /logic/databaseinterface.py, it was checking for term states in a yucky way -Kat 9/9/19
    # print (Term.get(Term.termCode == tid).term_state.number)
    if ((Term.get(Term.termCode == tid).term_state.number) != 1): #If the term is not open for scheduling changes:
        return render_template("schedulingLocked.html", tid = tid, prefix = prefix)
    print("data", data)
    print("prefix", prefix)
    print("professors", professors)
    # print("crosslist", crossListedCourses)
    databaseInterface.editCourse(data, prefix, professors, crosslistedCourse)
    message = "Course: course {} has been edited".format(data['cid'])
    log.writer("INFO", page1, message)
    flash("Course information has successfully been modified!")
    if page == 'courses':
      return redirect(url_for("courses", tID=tid, prefix=prefix))
    else:
      url = "/courseManagement/" + page + "/" + tid
      return redirect(url)

@app.route("/editSTCourseModal/<tid>/<prefix>/<stid>/<page>", methods=["GET"])
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


@app.route("/editstcourse/<tid>/<prefix>/<page>", methods=["POST"])
@must_be_authorized
def editSTcourse(tid, prefix, page):
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
  log.writer("INFO", page1, message)
  flash("Course information has successfully been modified!")
  if page == 'courses':
    return redirect(url_for("courses", tID=tid, prefix=prefix))
  else:
    url = "/courseManagement/" + page + "/" + tid
    return redirect(url)
