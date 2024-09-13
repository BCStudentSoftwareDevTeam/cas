from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.allImports import *
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
# from app.logic.course import define_term_code_and_prefix
from app.logic.courseLogic import find_crosslist_courses, save_last_visited
from app.logic.authorizedUser import AuthorizedUser, can_modify
import json
import ast

from app.models.models import *

@main_bp.route("/courses/", methods=["GET"] )
@main_bp.route("/courses/<tID>/<prefix>", methods=["GET"])
#FIXME: @define_term_code_and_prefix
@save_last_visited
@can_modify
def courses(tID, prefix, can_edit):     #can_edit comes from @can_modify
    page = "courses"

    au = AuthorizedUser()

    # For the sidebar
    divisions_prefetch = getSidebarElements()
    subject = Subject.get(Subject.prefix == prefix)
    users = User.select(User.username, User.firstName, User.lastName)

    # Header of each page
    currentProgram = subject.pid

    # Header of each page
    curTermName = Term.get(Term.termCode == tID)
    terms = Term.select().order_by(-Term.termCode)

    allCourses = BannerCourses.select().order_by(BannerCourses.subject.asc())
    # We need these for populating add course
    courseInfo = (BannerCourses
                        .select(BannerCourses, Subject)
                        .join(Subject)
                        .where(BannerCourses.subject == prefix)
                        .where(BannerCourses.is_active == True)
                        .order_by(BannerCourses.number))

    schedules = BannerSchedule.select().order_by(BannerSchedule.order)

    rooms = Rooms.select().order_by(Rooms.building)

    # Key  - 1 indicates Fall
    # Key  - 2 indicates Spring
    # Key  - 3 indicates Summer
    key = 0
    try:
        key = int(tID[-1])
    except ValueError as error:
        pass
        # log.writer("Unable to parse Term ID, course.py", e)
    instructors = InstructorCourse.select(InstructorCourse, User).join(User)

    courses = (Course.select(Course, BannerCourses)
                     .join(BannerCourses)
                     .where((Course.prefix == prefix) & (Course.term == tID))
                     .order_by(Course.prefix, Course.bannerRef.number))


    approved = cfg['specialTopicLogic']['approved'][0]
    specialCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.prefix == prefix).where(SpecialTopicCourse.term == tID).where(SpecialTopicCourse.status != approved)
    test_stCourse = SpecialTopicCourse.select()
    test_instructors = createInstructorDict(test_stCourse)
    # print("specialcourse ", specialCourses)
                     #We exclude the approved courses, because they'll be stored in the 'Course' table already
    instructors2 = InstructorSTCourse.select(InstructorSTCourse, User).join(User)

    # Inject instructors for every course into the courses object; clean up course materials
    for idx in range(len(courses)):
        instructors = InstructorCourse.select().where(InstructorCourse.course == courses[idx].cId)
        courses[idx].instructors = instructors
        if courses[idx].courseResources:
            resources = ast.literal_eval(courses[idx].courseResources)
            resources_cleaned = ""
            resources_cleaned += "No course materials required" if resources["NoneRequired"] else ""
            resources_cleaned += ("Open educational resources" if len(resources_cleaned) == 0 else ", Open educational resources") if resources["OER"] else ""
            resources_cleaned += ("Library resources" if len(resources_cleaned) == 0 else ", Library resources") if resources["Library"] else ""
            resources_cleaned += ("Paid resources" if len(resources_cleaned) == 0 else ", Paid resources") if resources["Paid"] else ""
            if resources_cleaned == "":
                resources_cleaned = "Unspecified"
        courses[idx].courseResources = resources_cleaned


    special_courses_prefetch = prefetch(specialCourses, instructors2, Rooms, Subject, BannerSchedule, BannerCourses)
    # get crosslisted for given courses

    course_to_crosslist=find_crosslist_courses(prefix, tID)
    return render_template(
            "course.html",
            crosslisted=course_to_crosslist,
            allCourses= allCourses, #Courses,
            courses=courses, #courses,
            specialCourses=special_courses_prefetch,
            divisions = divisions_prefetch,
            currentTerm=int(tID),
            courseInfo=courseInfo,
            users=users,
            schedules=schedules,
            allTerms=terms,
            can_edit = can_edit,
            currentProgram=currentProgram,
            curTermName=curTermName,
            current_user = au.user,
            isAdmin = au.user.isAdmin,
            prefix=prefix,
            page=page,
            rooms=rooms,
            key = key,
            cfg = cfg,
            test_instructors= test_instructors
            )


@main_bp.route("/verifycrosslisted/<intValue>", methods=["POST"])
def verifycrosslisted(intValue):
    try:
        course = Course.get(Course.cId==int(intValue))
        parentCourse = course.parentCourse
        data = request.form
        clicked = data['check']
        cond = True if clicked == u'true' else False
        parent_or_child = parentCourse if parentCourse else course.cId
        crosslisted = CrossListed.select().where(
                (CrossListed.courseId == parent_or_child) &
                (CrossListed.crosslistedCourse == course.cId)
                ).get()
        crosslisted.verified=cond
        crosslisted.save()
        return json.dumps({"success": 1})
    except:
        flash("An error has occurred. Please try again.","error")
        return json.dumps({"error":0})
