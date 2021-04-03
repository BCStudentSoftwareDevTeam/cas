from app.controllers.admin_routes import *

import pprint
from flask import jsonify, redirect
from app.logic.redirectBack import redirect_url

from app.allImports import *
from app.updateCourse import DataUpdate
from app.logic import databaseInterface
from app.logic import functions
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic.redirectBack import redirect_url
from app.logic.authorizedUser import AuthorizedUser, must_be_admin
from app.models.models import *
from app.loadConfig import load_config
#CROSS LISTED COURSES#


@admin_bp.route("/courseManagement/crossListed/", defaults={'tid': 0}, methods=["GET", "POST"])
@admin_bp.route("/courseManagement/crossListed/<tid>", methods=["GET", "POST"])
@must_be_admin
def crossListed(tid):
    au = AuthorizedUser()
    curTermName = None
    if tid:
        curTermName = Term.get(Term.termCode == tid)


    # DATA FOR THE NAVBAR AND SIDE BAR
    terms = Term.select().order_by(-Term.termCode)
    if tid == 0:
        tid = terms[0].termCode

    page = "crossListed"
    crossListedCourses = Course.select(
        ).join(BannerCourses, on=(BannerCourses.reFID == Course.bannerRef)
        ).where(Course.crossListed == 1
        ).where(Course.term == tid
        ).order_by(BannerCourses.ctitle)

    instructors = InstructorCourse.select(InstructorCourse, User).join(User)
    courses_prefetch = prefetch(crossListedCourses, instructors, Rooms, Subject, BannerSchedule, BannerCourses)
    schedules = BannerSchedule.select()
    rooms = Rooms.select()

    # Key  - 1 indicates Fall
    # Key  - 2 indicates Spring
    # Key  - 3 indicates Summer
    key = 1
    try:
        key = int(str(tid)[-1])
    except ValueError as error:
        # log.writer("Unable to parse Term ID, courseManagment.py", e)
        pass
    cfg = load_config()
    return render_template("crossListed.html",
                           allTerms=terms,
                           page=page,
                           currentTerm=int(tid),
                           courses=courses_prefetch,
                           #courseInfo=courseInfo,
                           schedules=schedules,
                           rooms=rooms,
                           key = key,
                           cfg = cfg,
                           curTermName = curTermName,
                           isAdmin = au.user.isAdmin

                           )
#############################
#SCHEDULE AND ROOM CONFLICTS#
#############################


@admin_bp.route("/courseManagement/conflicts/", defaults={'term_id':0}, methods=["GET"])
@admin_bp.route("/courseManagement/conflicts/<term_id>", methods=["GET"])
@must_be_admin
def conflictsListed(term_id):
    au = AuthorizedUser()
    #DATA FOR THE NAVEBAR AND SIDEBAR#
    page = "conflicts"
    terms = Term.select().order_by(-Term.termCode)



    if term_id == 0:
      for term in terms:
        if term.termCode > term_id:
          term_id = term.termCode

    buildings = functions.get_buildings_with_conflicts(term_id)
    rooms = functions.get_rooms_with_conflicts(term_id)
    conflicts = functions.get_courses_with_conflicts(term_id)

    courses_special_time = functions.get_special_times(term_id)
    special_time_courses_prefetch = prefetch(courses_special_time, InstructorCourse, User)

    current_term = Term.get(Term.termCode == term_id)

    # buildings_prefetch = prefetch(buildings, rooms, conflicts, BannerSchedule, ScheduleDays, InstructorCourse, User)
    cfg = load_config()
    return render_template("time_conflicts.html",
                           allTerms=terms,
                           page=page,
                           currentTerm = term_id,
                           current_term=current_term,
                           buildings_prefetch = buildings,#_prefetch,
                           courses_special_time = special_time_courses_prefetch,
                           cfg = cfg,
                           isAdmin = au.user.isAdmin

                           )
################
#CHANGE TRACKER#
################

@admin_bp.route("/courseManagement/tracker/", defaults={'tID':0}, methods=["GET"])
@admin_bp.route("/courseManagement/tracker/<tID>/", methods=["GET"])
@must_be_admin
def trackerListed(tID):
    # DATA FOR THE NAVBAR AND SIDE BAR
    page = "tracker"
    terms = Term.select().order_by(-Term.termCode)
    if tID == 0:
      for term in terms:
        if term.termCode > tID:
          tID = term.termCode
    # DATA FOR THE CHANGE TRACKER PAGE
    # ALL OF THIS CAME FROMT HE COURSECHANGE.PY



    courses = CourseChange.select().order_by(CourseChange.verified, CourseChange.term.desc())
    instructorsDict = databaseInterface.createInstructorDict(courses)
    colorClassDict = functions.getColorClassDict(courses)
    '''
    DATA STRUCTURES
    NOTE: The keys for both dictionaries the course identification number
    classDict[cId] = [className,className,className,className,className]
    *Then it will return a list of classnames that can be accessed through an index

    instructorsDict[cid] = intructorCourseChange peewee object
    '''
    cfg = load_config()
    return render_template("tracker.html",
                           allTerms=terms,
                           page=page,
                           currentTerm=int(tID),
                           courses=courses,
                           instructorsDict=instructorsDict,
                           classDict=colorClassDict,
                           cfg = cfg
                           )



@admin_bp.route("/courseManagement/tracker/verified", methods=["POST"])
@must_be_admin
def verifyChange():
        page = "/" + request.url.split("/")[-1]
        data = request.form
        verify = DataUpdate()
        verify.verifyCourseChange(data)
        message = "Course Change: {0} has been verified".format(data['id'])
        # log.writer("INFO", page, message)
        flash("Your course has been marked verified")
        return redirect(redirect_url())



@admin_bp.route("/courseManagement/specialTopics/get/<tid>/<table>", methods=["GET"])
@must_be_admin
def get_speical_topic_courses(tid, table):
    status = None
    for state in cfg['specialTopicStates']:
        if state['name'] == table:
            status = state['value']

    if status is not None:
        courses= SpecialTopicCourse.select().where(SpecialTopicCourse.status == status).where(SpecialTopicCourse.term == int(tid))
        course_data = map(format_course_data, courses)
        return jsonify(list(course_data))

def format_course_data(course):
    """Generates the list of data used by """
    instructors = map(format_instructor, InstructorSTCourse.select().where(InstructorSTCourse.course == course))
    term = course.term.termCode
    prefix = course.prefix.prefix
    stId = course.stId
    status = course.status
    days = ""
    schedule = ""
    if course.schedule is not None:
        days = map(lambda schedule: schedule.day, ScheduleDays.select(ScheduleDays.day).where(ScheduleDays.schedule == course.schedule.sid))
        schedule = "See Notes"
        if course.schedule.sid not in cfg['specialSchedule']['unknownTime']:
            schedule = " ".join(days) + " " + str(course.schedule.startTime.strftime("%I:%M %p")) +" - "+ str(course.schedule.endTime.strftime("%I:%M %p"))


    name = course.bannerRef.ctitle
    if course.bannerRef.ctitle is not None:
        name = "%s %s %s" % (course.prefix, course.bannerRef.number, course.specialTopicName)

    taught = " ".join(instructors)

    capacity = "No capacity specified"
    if course.capacity is not None:
        capacity= course.capacity

    room = "No room listed"
    if course.rid is not None:
        room= "%s:%s" % (course.rid.building.name, course.rid.number)

    cross = "No"
    if course.crossListed:
        cross = "Yes"

    notes = "Notes"
    if course.notes is not None:
        notes = course.notes
    edit = course.lastEditBy
    edit_button =  "%s,%s,%s"% (term, prefix,stId)

    delete_button = "%s,%s,%s" % (stId, term, prefix)

    entry = None
    if course.status in cfg["specialTopicLogic"]["admin_disabled"]:
        entry = [name, taught, schedule, capacity, room, cross, notes, edit]
    else:
        entry = [name, taught, schedule, capacity, room, cross, notes, edit, edit_button]
    return entry

def format_instructor(instructor):
    """ Formats the instructors name for rendering in the ajax dataTable

    Args:
        instructor(InstructorSTCourse): An instructor object to be turned into a name
    """
    return instructor.username.firstName[0] +  ". " + instructor.username.lastName+","

################
#Special Topics#
################
@admin_bp.route("/courseManagement/specialCourses/", defaults={'tid':0}, methods=["GET"])
@admin_bp.route("/courseManagement/specialCourses/<tid>", methods=["GET", "POST"])
@must_be_admin
def specialCourses(tid):
    #DATA FOR THE NAVEBAR AND SIDEBAR#
    page = "specialCourses"
    terms = Term.select().order_by(-Term.termCode)

    if (request.method == "POST"):
        data = request.form
    if tid == 0:
      for term in terms:
        if term.termCode > tid:
          tid = term.termCode

    curTermName = Term.get(Term.termCode == tid)

    terms = Term.select().order_by(-Term.termCode)

    specialCourses = SpecialTopicCourse.select()
    instructors = createInstructorDict(specialCourses)

    special_dict = dict()
    for state in cfg['specialTopicStates']:
        special_dict[state['id']] = SpecialTopicCourse.select().where(SpecialTopicCourse.status == state['value']).where(SpecialTopicCourse.term == int(tid))

    return render_template("specialTopicRequests.html",
                          cfg=cfg,
                          special_dict = special_dict,
                          isAdmin = True,
                          allTerms = terms,
                          curTermName = curTermName,
                          currentTerm=int(tid),
                          page = page,
                          instructors = instructors)

@admin_bp.route("/courseManagement/addNewCourse", methods=["POST", "GET"])
@must_be_admin
def addNewCourse():
    try:
        if request.method == "POST":
            data = request.form
            subject = Subject.select().where(Subject.prefix == data['subjectPrefix'])

            new_course = BannerCourses.create(subject = subject,
                                             number = data['courseNumber'],
                                             section = None,
                                             ctitle = data['courseTitle'],
                                             is_active = True)

            flash("New Course created successfully!")
            return redirect(redirect_url())
        else:
            subject_prefix = Subject.select()
            return render_template("addNewCourse.html",
                                   cfg=cfg,
                                   isAdmin = True,
                                   page="addNewCourse",
                                   subjectPrefix = subject_prefix)
    except Exception as e:
        print("Error on creating a new course: ", e)
        return jsonify({"Success": False}), 500
