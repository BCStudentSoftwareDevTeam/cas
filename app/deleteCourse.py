from allImports import *
from updateCourse import DataUpdate
from app.logic import databaseInterface
from app.logic.redirectBack import redirect_url
from app.logic.authorization import must_be_authorized

@app.route("/deletecourse/<tid>/<prefix>", methods=["POST"])
@must_be_authorized
def deletecourse(prefix, tid):
    current_username = AuthorizedUser().getUsername()
    user = User.get(User.username == current_username)
    current_page = "/" + request.url.split("/")[-1]


    # DATA NEEDED FOR MANIPULATION
    # TODO: Change the colors when a course is updated
    dataUpdateObj = DataUpdate()
    rm = RoomPreferences()
    data = request.form
    cid = int(data['cid'])
    # START PROCESSING THE DELETION OF THE COURSE
    course = Course.get(Course.cId == cid)
    # MAKE SURE THE USER HAS THE CORRECT RIGHTS TO DELETE A COURSE
    
    #delete course crosslisted children
    if course.crossListed:
        delete_if_crosslisted(course, rm)
    
    #delete course instructors  
    instructors = InstructorCourse.select().where(InstructorCourse.course == course.cId)
    for instructor in instructors:
        instructor.delete_instance()    

# Removing change tracker code - 9/10/19 - Scott
    
#    #update changetracker if term is closed
#    if not databaseInterface.isTermOpen(tid):
#        if user.isAdmin:
#            change = CourseChange.select().where(CourseChange.cId == cid)
#            # IF THE RECORD ALREADY EXSISTED THEN WE NEED TO UPDATE THE
#            # INFORMATION
#            if change.exists():
#                updateRecord = CourseChange.get(CourseChange.cId == cid)
#                if updateRecord.changeType == 'create' and not updateRecord.verified:
#                    updateRecord.delete_instance()
#                else:
#                    updateRecord.changeType = cfg["changeType"]["delete"]
#                    colors = dataUpdateObj.createColorString(cfg["changeType"]["delete"])
#                    updateRecord.tdcolors = colors
#                    updateRecord.verified = False
#                    updateRecord.save()
#            else:
#		updateRecord = CourseChange(cId = cid)
#                updateRecord.changeType = cfg["changeType"]["delete"]
#                colors = dataUpdateObj.createColorString(cfg["changeType"]["delete"])
#                updateRecord.tdcolors = colors
#                updateRecord.verified = False
#                updateRecord.save()
#        else:
#            dataUpdateObj.addCourseChange(
#                course.cId, cfg["changeType"]['delete'])
#    instructorsChange = InstructorCourseChange.select().where(InstructorCourseChange.course == cid)
#    for instructor in instructorsChange:
#        instructor.delete_instance()
#        
    #delete course room preference if exists
    rm.delete_room_preference(course.cId)
    
    message = "Course: course {} has been deleted".format(course.cId)
    course.delete_instance()
    
    log.writer("INFO", current_page, message)

    flash("The course has been successfully deleted")
    return redirect(redirect_url())

def delete_if_crosslisted(course, roompreference):
    '''
    Functionalities:
        delete child/parent CC relationship from Crosslisted
        delete actual parent/child course from Course
        delete Instructors from InstructorCourse
        delete course RoomPreference if exists 
    '''
      #if course is a crosslisted parent course, delete it with all its child courses
    if not course.parentCourse:
        crosslistedCourses = CrossListed.select().where(CrossListed.courseId == course.cId)
        crosslistedChildCourses = Course.select().where(Course.parentCourse ==course.cId)
        #delete all related crosslisted courses in crosslisted table
        for crosslisted_course in crosslistedCourses:
            crosslisted_course.delete_instance()
        #delete all related courses child courses in course table
        for childcourse in crosslistedChildCourses:
            #remove its roompreference if exist
            roompreference.delete_room_preference(childcourse.cId)
            #delete instructors for course
            instructors = InstructorCourse.select().where(InstructorCourse.course == childcourse.cId)
            for instructor in instructors:
                instructor.delete_instance()
            childcourse.delete_instance()
        #child course instructors
    else:
        #if course being deleted is a child crossListed, delete this relationship
        CrossListed.select().where(
            (CrossListed.crosslistedCourse == course.cId) &
            (CrossListed.courseId == course.parentCourse)
            ).delete_instance()
        
        


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
