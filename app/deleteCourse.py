from allImports import *
from updateCourse import DataUpdate
from app.logic import databaseInterface
from app.logic.redirectBack import redirect_url
from app.logic.authorization import must_be_authorized

@app.route("/deletecourse/<tid>/<prefix>", methods=["POST"])
@must_be_authorized
def deletecourse(prefix, tid):
    
    current_page = "/" + request.url.split("/")[-1]


    # DATA NEEDED FOR MANIPULATION
    # TODO: Change the colors when a course is updated
    dataUpdateObj = DataUpdate()
    data = request.form
    cid = int(data['cid'])
    print("HI", cid)
    # START PROCESSING THE DELETION OF THE COURSE
    course = Course.get(Course.cId == cid)
    # MAKE SURE THE USER HAS THE CORRECT RIGHTS TO DELETE A COURSE
    if not databaseInterface.isTermOpen(tid):

        change = CourseChange.select().where(CourseChange.cId == cid)
        # IF THE RECORD ALREADY EXSISTED THEN WE NEED TO UPDATE THE
        # INFORMATION
        if change.exists():
            updateRecord = CourseChange.get(CourseChange.cId == cid)
            if updateRecord.changeType == 'create' and not updateRecord.verified:
                updateRecord.delete_instance()
            else:
                updateRecord.changeType = cfg["changeType"]["delete"]
                colors = dataUpdateObj.createColorString(cfg["changeType"]["delete"])
                updateRecord.tdcolors = colors
                updateRecord.verified = False
                updateRecord.save()
        else:
            dataUpdateObj.addCourseChange(
                course.cId, cfg["changeType"]['delete'])
    instructors = InstructorCourseChange.select().where(
        InstructorCourseChange.course == cid)
    for instructor in instructors:
        instructor.delete_instance()
        
    #delete course instructor relationship
    course_instructor = InstructorCourse.get(InstructorCourse.course_id == cid)
    course_instructor.delete_instance()
    #delete course itself
    course.delete_instance()
    message = "Course: course {} has been deleted".format(course.cId)
    log.writer("INFO", current_page, message)

    flash("Course has been successfully deleted")
    return redirect(redirect_url())


@app.route("/deletestcourse/<tid>/<prefix>", methods=["POST"])
@must_be_authorized
def deleteSTcourse(prefix, tid):

    current_page = "/" + request.url.split("/")[-1]

    # DATA NEEDED FOR MANIPULATION
    # TODO: Change the colors when a course is updated
    dataUpdateObj = DataUpdate()
    data = request.form
    stid = int(data['stid'])
    # START PROCESSING THE DELETION OF THE COURSE
    course = SpecialTopicCourse.get(SpecialTopicCourse.stId == stid)
    # MAKE SURE THE USER HAS THE CORRECT RIGHTS TO DELETE A COURSE
    
    course.delete_instance()
    message = "Course: course {} has been deleted".format(course.stId)
        
    log.writer("INFO", current_page, message)

    flash("Special Topic Request has been deleted.")
    return redirect(redirect_url())
