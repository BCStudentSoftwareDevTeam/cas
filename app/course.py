from allImports import *
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic.course import define_term_code_and_prefix
from app.logic.course import save_last_visited
from app.logic.course import find_crosslist_courses
from app.logic.authorization import can_modify
import json

@app.route("/courses/", methods=["GET"] )
@app.route("/courses/<tID>/<prefix>", methods=["GET"])
@define_term_code_and_prefix
@save_last_visited
@can_modify
def courses(tID, prefix, can_edit):
    page = "courses"
    username = g.user.username
    current_user = User.get(User.username == username)

    # These are the necessary components of the sidebar. Should we move them
    # somewhere else?

    divisions_prefetch = getSidebarElements()
    subject = Subject.get(Subject.prefix == prefix)
    users = User.select(User.username, User.firstName, User.lastName)

    # THIS IS SO THAT WE CAN HAVE THE NAME OF THE PROGRAM AS A HEADER ON THE
    # TOP OF EVERY PAGE
    currentProgram = subject.pid

    # THIS IS SO THAT WE CAN HAVE THE TERM BEING VIEWED AT TEH TOP OF EVERY
    # PAGE
    curTermName = Term.get(Term.termCode == tID)

    terms = Term.select().order_by(-Term.termCode)

    allCourses = BannerCourses.select().order_by(BannerCourses.reFID)
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
    key = 1
    try:
        key = int(tID[-1])
    except ValueError as error:
        log.writer("Unable to parse Term ID, course.py", e)

    courses = (Course.select(Course, BannerCourses).join(BannerCourses).where(
        (Course.prefix == prefix) & (Course.term == tID)))

    approved = cfg['specialTopicLogic']['approved'][0]
    specialCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.prefix == prefix).where(SpecialTopicCourse.term == tID).where(SpecialTopicCourse.status != approved)
                     #We exclude the approved courses, because they'll be stored in the 'Course' table already
    instructors = InstructorCourse.select(InstructorCourse, User).join(User)
    instructors2 = InstructorSTCourse.select(InstructorSTCourse, User).join(User)

    courses_prefetch = prefetch(courses, instructors,Subject, BannerSchedule, BannerCourses)
    # banner_prefetch = prefetch(courseInfo,BannerCourses, Subject)

    special_courses_prefetch = prefetch(specialCourses, instructors2, Rooms, Subject, BannerSchedule, BannerCourses)
    # get crosslisted for given courses

    course_to_crosslist=find_crosslist_courses(courses_prefetch)
    stCourseInfo = SpecialTopicCourse.get()
    return render_template(
            "course.html",
            crosslisted=course_to_crosslist,
            allCourses= allCourses, #Courses,
            courses=courses_prefetch,
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
            prefix=prefix,
            page=page,
            rooms=rooms,
            key = key,
            stCourseInfo=stCourseInfo)


@app.route("/verifycrosslisted/<intValue>", methods=["POST"])
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
