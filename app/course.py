from allImports import *
from app.logic.databaseInterface import getSidebarElements

from app.logic.course import define_term_code_and_prefix
from app.logic.course import save_last_visited
from app.logic.authorization import can_modify


@app.route("/courses/", methods=["GET"] )
@app.route("/courses/<tID>/<prefix>", methods=["GET"])
@define_term_code_and_prefix
@save_last_visited
@can_modify
def courses(tID, prefix, can_edit):
    page = "courses"
    
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

    # We need these for populating add course
    courseInfo = (BannerCourses
                        .select(BannerCourses, Subject)
                        .join(Subject)
                        .where(BannerCourses.subject == prefix)
                        .where(BannerCourses.is_active == True)
                        .order_by(BannerCourses.number))

    schedules = BannerSchedule.select().order_by(BannerSchedule.order)
    
    rooms = Rooms.select().order_by(Rooms.building)
    
    termd = list(tID)
    key = int(termd[-1])
    courses = (Course.select(Course, BannerCourses).join(BannerCourses)
                     .where(Course.prefix == prefix)
                     .where(Course.term == tID))
    
    instructors = InstructorCourse.select(InstructorCourse, User).join(User)
    
    
    courses_prefetch = prefetch(courses, instructors, Rooms, Subject, BannerSchedule, BannerCourses)
    
    return render_template(
            "course.html",
            courses=courses_prefetch,
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
            key = key)