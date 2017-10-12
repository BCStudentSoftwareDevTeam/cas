# ADD ANY IMPORTS HERE
from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
from app.logic import databaseInterface
from app.logic import functions
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic.redirectBack import redirect_url
import pprint

#CROSS LISTED COURSES#


@app.route(
    "/courseManagement/crossListed/",
    defaults={
        'tid': 0},
    methods=[
        "GET",
        "POST"])
@app.route("/courseManagement/crossListed/<tid>", methods=["GET", "POST"])
def crossListed(tid):
    # DATA FOR THE NAVBAR AND SIDE BAR
    terms = Term.select().order_by(-Term.termCode)
    if tid == 0:
        tid = terms[0].termCode

    page = "crossListed"
    authorizedUser = AuthorizedUser()
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
    return render_template("crossListed.html",

                           cfg=cfg,
                           isAdmin=authorizedUser.isAdmin(),
                           allTerms=terms,
                           page=page,
                           currentTerm=int(tid),
                           courses=crossListedCourses,
                           instructors=instructors,
                           courseInfo=courseInfo,
                           users=users,
                           schedules=schedules,
                           rooms=rooms
                           )
#############################
#SCHEDULE AND ROOM CONFLICTS#
#############################


@app.route("/courseManagement/conflicts/<term_id>", methods=["GET"])
def conflictsListed(term_id):
    #DATA FOR THE NAVEBAR AND SIDEBAR#
    page = "conflicts"
    terms = Term.select().order_by(-Term.termCode)
    authorizedUser = AuthorizedUser()
    
    current_term = Term.get(Term.termCode == term_id)



    buildings = functions.get_buildings_with_conflicts(term_id)
    rooms = functions.get_rooms_with_conflicts(term_id)
    conflicts = functions.get_all_conflicts(term_id)
    
    buildings_prefetch = prefetch(buildings, rooms, conflicts, BannerSchedule, ScheduleDays, InstructorCourse, User)


                
    return render_template("conflicts.html",
                           cfg=cfg,
                           isAdmin=authorizedUser.isAdmin(),
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
def trackerListed(tID):
    # DATA FOR THE NAVBAR AND SIDE BAR
    page = "tracker"
    terms = Term.select().order_by(-Term.termCode)
    authorizedUser = AuthorizedUser()
    if tID == 0:
      for term in terms:
        if term.termCode > tID:
          tID = term.termCode
    # DATA FOR THE CHANGE TRACKER PAGE
    # ALL OF THIS CAME FROMT HE COURSECHANGE.PY
    if (request.method == "GET"):
        if authorizedUser.isAdmin():

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
                                   cfg=cfg,
                                   isAdmin=authorizedUser.isAdmin(),
                                   allTerms=terms,
                                   page=page,
                                   currentTerm=int(tID),
                                   courses=courses,
                                   instructorsDict=instructorsDict,
                                   classDict=colorClassDict
                                   )
        else:
            abort(404)
    else:
        abort(404)

@app.route("/courseManagement/tracker/verified", methods=["POST"])
def verifyChange():
    if (request.method == "POST"):
        page = "/" + request.url.split("/")[-1]
        authorizedUser = AuthorizedUser()
        if authorizedUser.isAdmin():
            data = request.form
            verify = DataUpdate()
            verify.verifyCourseChange(data)
            message = "Course Change: {0} has been verified".format(data['id'])
            log.writer("INFO", page, message)
            flash("Your course has been marked verified")
            return redirect(redirect_url())
        return render_template("404.html", cfg=cfg)
    return render_template("404.html", cfg=cfg)
    

@app.route("/courseManagement/specialCourses/<tid>", methods=["GET", "POST"])
def specialCourses(tid):
    #DATA FOR THE NAVEBAR AND SIDEBAR#
    page = "specialCourses"
    terms = Term.select().order_by(-Term.termCode)
    authorizedUser = AuthorizedUser()
    
    if (request.method == "POST"):
        data = request.form
    
    curTermName = Term.get(Term.termCode == tid)

    terms = Term.select().order_by(-Term.termCode)
    
    specialCourses = SpecialTopicCourse.select()
    submittedCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.status == 1)
    sentToDeanCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.status == 2)
    approvedCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.status == 3)
    deniedCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.status == 4)
        
    # rooms = Rooms.select().order_by(Rooms.building)
    instructors = createInstructorDict(specialCourses)
    
    ############################
    
    
                
    return render_template("specialTopicRequests.html",
                          cfg=cfg,
                          submittedCourses = submittedCourses,
                          sentToDeanCourses = sentToDeanCourses,
                          approvedCourses = approvedCourses,
                          deniedCourses = deniedCourses,
                          isAdmin = authorizedUser.isAdmin(),
                          currentTerm=int(tid),
                          page = page,
                          instructors = instructors)