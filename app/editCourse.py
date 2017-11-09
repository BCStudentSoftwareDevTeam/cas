from allImports import *
from updateCourse import DataUpdate
from app.logic.TrackerEdit import TrackerEdit
from app.logic import databaseInterface
from app.logic.authorization import must_be_authorized

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
    return render_template("snips/courseElements/editCourse.html",
                            schedules = schedules,
                            terms     = terms,
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
    page1 =  "/" + request.url.split("/")[-1]
    data = request.form
    trackerEdit = TrackerEdit(data)
    professors = request.form.getlist('professors[]')
    
    if (not databaseInterface.isTermOpen(tid)):
      created = trackerEdit.make_edit(professors, username)
    databaseInterface.editCourse(data, prefix, professors)
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
  professors = request.form.getlist('professors[]')
  if page1 == "/specialCourses": 
      if data['statusChange']:
        databaseInterface.editSTCourse(data, prefix, professors, int(data['statusChange']))
      else:
        databaseInterface.editSTCourse(data, prefix, professors, specialCourse.status)
  else:
      databaseInterface.editSTCourse(data, prefix, professors, 1)
      
  message = "Course: course {} has been edited".format(data['stid'])
  log.writer("INFO", page1, message)
  flash("Course information has successfully been modified!")
  
  if page == 'courses':
    return redirect(url_for("courses", tID=tid, prefix=prefix))
  else:
    url = "/courseManagement/" + page + "/" + tid
    return redirect(url)
