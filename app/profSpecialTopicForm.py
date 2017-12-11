from allImports import *

@app.route("/professor/specialTopicForm", methods=["GET"])
def profSpecialTopicForm():
    users = User.select(User.username, User.firstName, User.lastName)
    current_term = Term.get()
    TID = current_term.termCode
    terms = Term.select().order_by(-Term.termCode)
    courseInfo = (BannerCourses
                        .select(BannerCourses)
                        .where(BannerCourses.number.contains('86'))
                        .where(BannerCourses.is_active == True)
                        .order_by(BannerCourses.number))

    schedules = BannerSchedule.select().order_by(BannerSchedule.order)

    rooms = Rooms.select().order_by(Rooms.building)

    # Key  - 1 indicates Fall
    # Key  - 2 indicates Spring
    # Key  - 3 indicates Summer
    # key = 1
    # try:
    #     key = int(tID[-1])
    # except ValueError as error:
    #     log.writer("Unable to parse Term ID, course.py", e)


    courses = (Course.select(Course, BannerCourses).join(BannerCourses).where(Course.term == TID))

    specialCourses = SpecialTopicCourse.select().where(SpecialTopicCourse.term == TID)
                     #We exclude the approved courses, because they'll be stored in the 'Course' table already

    instructors = InstructorCourse.select(InstructorCourse, User).join(User)
    instructors2 = InstructorSTCourse.select(InstructorSTCourse, User).join(User)

    courses_prefetch = prefetch(courses, instructors, Rooms, BannerSchedule, BannerCourses)

    special_courses_prefetch = prefetch(specialCourses, instructors2, Rooms, BannerSchedule, BannerCourses)
    return render_template("profSpecialTopicForm.html",
                            courses=courses_prefetch,
                            specialCourses=special_courses_prefetch,
                            currentTerm=int(TID),
                            courseInfo=courseInfo,
                            users=users,
                            schedules=schedules,
                            allTerms=terms,
                            curTermName=current_term.name,
                            rooms=rooms
                            )