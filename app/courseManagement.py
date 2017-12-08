# ADD ANY IMPORTS HERE
from allImports import *
from updateCourse import DataUpdate
from app.logic import databaseInterface
from app.logic import functions
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic.redirectBack import redirect_url
from app.logic.authorization import must_be_admin
import pprint
from flask import jsonify

#CROSS LISTED COURSES#


@app.route(
    "/courseManagement/crossListed/",
    defaults={
        'tid': 0},
    methods=[
        "GET",
        "POST"])
@app.route("/courseManagement/crossListed/<tid>", methods=["GET", "POST"])
@must_be_admin
def crossListed(tid):
    # DATA FOR THE NAVBAR AND SIDE BAR
    terms = Term.select().order_by(-Term.termCode)
    if tid == 0:
        tid = terms[0].termCode

    page = "crossListed"
    ##DATA FOR THE CROSS LISTED COURSE TABLE##
    crossListedCourses = Course.select(
        ).join(BannerCourses, on=(BannerCourses.reFID == Course.bannerRef)
        ).where(Course.crossListed == 1
        ).where(Course.term == tid
        ).order_by(BannerCourses.ctitle)

    instructors = databaseInterface.createInstructorDict(crossListedCourses)

    ##DATA FOR THE ADD COURSE FORM##
    courseInfo = BannerCourses.select().order_by(
        BannerCourses.number).order_by(
        BannerCourses.subject)
    users = User.select(User.username, User.firstName, User.lastName)
    schedules = BannerSchedule.select()
    rooms = Rooms.select()

    # Key  - 1 indicates Fall
    # Key  - 2 indicates Spring
    # Key  - 3 indicates Summer
    key = 1
    try:
        key = int(str(tid)[-1])
    except ValueError as error:
        log.writer("Unable to parse Term ID, courseManagment.py", e)

    return render_template("crossListed.html",
                           allTerms=terms,
                           page=page,
                           currentTerm=int(tid),
                           courses=crossListedCourses,
                           instructors=instructors,
                           courseInfo=courseInfo,
                           users=users,
                           schedules=schedules,
                           rooms=rooms,
                           key = key
                           )
#############################
#SCHEDULE AND ROOM CONFLICTS#
#############################


@app.route("/courseManagement/conflicts/", defaults={'term_id':0}, methods=["GET"])
@app.route("/courseManagement/conflicts/<term_id>", methods=["GET"])
@must_be_admin
def conflictsListed(term_id):
    #DATA FOR THE NAVEBAR AND SIDEBAR#
    page = "conflicts"
    terms = Term.select().order_by(-Term.termCode)



    if term_id == 0:
      for term in terms:
        if term.termCode > term_id:
          term_id = term.termCode

    buildings = functions.get_buildings_with_conflicts(term_id)
    rooms = functions.get_rooms_with_conflicts(term_id)
    conflicts = functions.get_all_conflicts(term_id)

    current_term = Term.get(Term.termCode == term_id)
    buildings_prefetch = prefetch(buildings, rooms, conflicts, BannerSchedule, ScheduleDays, InstructorCourse, User)



    return render_template("conflicts.html",
                           allTerms=terms,
                           page=page,
                           currentTerm = term_id,
                           current_term=current_term,
                           buildings_prefetch = buildings_prefetch
                           )
################
#CHANGE TRACKER#
################

@app.route("/courseManagement/tracker/", defaults={'tID':0}, methods=["GET"])
@app.route("/courseManagement/tracker/<tID>/", methods=["GET"])
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
    return render_template("tracker.html",
                           allTerms=terms,
                           page=page,
                           currentTerm=int(tID),
                           courses=courses,
                           instructorsDict=instructorsDict,
                           classDict=colorClassDict
                           )



@app.route("/courseManagement/tracker/verified", methods=["POST"])
@must_be_admin
def verifyChange():
        page = "/" + request.url.split("/")[-1]
        data = request.form
        verify = DataUpdate()
        verify.verifyCourseChange(data)
        message = "Course Change: {0} has been verified".format(data['id'])
        log.writer("INFO", page, message)
        flash("Your course has been marked verified")
        return redirect(redirect_url())



@app.route("/courseManagement/specialTopics/get/<tid>", methods=["GET"])
@must_be_admin
def get_speical_topic_courses(tid):
    submittedCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.status == 1).where(SpecialTopicCourse.term == int(tid))
    sentToDeanCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.status == 2).where(SpecialTopicCourse.term == int(tid))
    approvedCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.status == 3).where(SpecialTopicCourse.term == int(tid))
    deniedCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.status == 4).where(SpecialTopicCourse.term == int(tid))
    savedCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.status == 0).where(SpecialTopicCourse.term == int(tid))

    course_data = dict()
    course_data["0"] = map(format_course_data, savedCourses)
    course_data["1"] = map(format_course_data, submittedCourses)
    course_data["2"] = map(format_course_data, sentToDeanCourses)
    course_data["3"] = map(format_course_data, approvedCourses)
    course_data["4"] = map(format_course_data, deniedCourses)
    return jsonify(course_data)

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
            schedule = " ".join(days) + " " + str(course.schedule.startTime.strftime("%X %p")) +" - "+ str(course.schedule.endTime.strftime("%X %p"))


    name = course.bannerRef.ctitle
    if course.bannerRef.ctitle is not None:
        name = "%s %s %s" % (course.prefix, course.bannerRef.number, course.specialTopicName)

    taught = " ".join(instructors)

    capacity = "No capacity specified"
    if course.capacity is not None:
        capacity= course.capacity

    room = "No room listed"
    if course.rid is not None:
        room= "%s %s" % (course.rid.building.name, course.rid.number)

    cross = "No"
    if course.crossListed:
        coss = "Yes"

    notes = "Notes"
    if course.notes is not None:
        notes = course.notes
    edit = course.lastEditBy
    edit_button =  "%s,%s,%s"% (term, prefix,stId)

    delete_button = """
                    """ % (stId, term, prefix)

    if course.status != 3 and course.status != 4:
        buttons = """
                    <div class="child">
                    %s 
                    %s
                    </div>
                """ % (edit_button, delete_button)
    elif course.status == 4:
        buttons = """
                    <div class="child">
                    %s 
                    </div>
                """ % (edit_button)
    else:
        buttons = ""
    entry = [name, taught, schedule, capacity, room, cross, notes, edit,edit_button, buttons]
    return entry

def format_instructor(instructor):
    """ Formats the instructors name for rendering in the ajax dataTable
    
    Args:
        instructor(InstructorSTCourse): An instructor object to be turned into a name
    """
    return instructor.username.firstName[0] +  ". " + instructor.username.lastName+","




@app.route("/courseManagement/specialCourses/", defaults={'tid':0}, methods=["GET"])
@app.route("/courseManagement/specialCourses/<tid>", methods=["GET", "POST"])
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
                          currentTerm=int(tid),
                          page = page,
                          instructors = instructors)
