from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
from app.logic import databaseInterface
from app.logic.NullCheck import NullCheck
from app.logic.redirectBack import redirect_url


'''
adds the course to the course table and to the course change if needed
'''


@app.route(
    "/addCourse/<tid>/",
    defaults={
        'prefix': 0},
    methods=["POST"])
@app.route("/addCourse/<tid>/<prefix>", methods=["POST"])
def addCourses(tid, prefix):
    # check to see if they are authorized to change anything
    authorizedUser = AuthorizedUser(prefix)
    # only do the bottom if authorized
    if authorizedUser.isAuthorized():
        # set the current page
        current_page = "/" + request.url.split("/")[-1]

        # get the data
        data = request.form
        # instructors need to be a list
        instructors = request.form.getlist('professors[]')

        # start a null checker
        nullCheck = NullCheck()

        values = nullCheck.add_course_form(data)
        banner = BannerCourses.get(BannerCourses.reFID == values['bannerRef'])
        bannerNumber = str(banner.number)[-2:]
        cId = ""
        
        if bannerNumber != "86":

            # update the course
            course = Course(bannerRef=values['bannerRef'],
                            prefix=values['prefix'],
                            term=int(tid),
                            schedule=values['schedule'],
                            capacity=values['capacity'],
                            specialTopicName=values['specialTopicName'],
                            notes=values['requests'],
                            crossListed=int(data['crossListed']),
                            rid=values['rid']
                            )
    
            course.save()
            databaseInterface.addCourseInstructors(instructors, course.cId)

            
            
            message = "Course: #{0} has been added".format(course.cId)
            flash("Course has successfully been added!")
            log.writer("INFO", current_page, message)
                
            newCourse = DataUpdate()
            if not databaseInterface.isTermOpen(tid):  # IF THE TERM IS NOT EDITABLE
                # ADD THE COURSE TO THE COURSECHANGE TABLE
                newCourse.addCourseChange(course.cId, cfg["changeType"]["create"])
                
            
        else:
            specialTopicCourse = SpecialTopicCourse(bannerRef=values['bannerRef'],
                            prefix=values['prefix'],
                            term=int(tid),
                            schedule=values['schedule'],
                            capacity=values['capacity'],
                            specialTopicName=values['specialTopicName'],
                            notes=values['requests'],
                            crossListed=int(data['crossListed']),
                            rid=values['rid'],
                            status = 0,
                            submitBy = authorizedUser.username,
                            credits = data['credits'],
                            description = data['description'],
                            prereqs = data['prereqs'],
                            majorReqsMet = data['majorReqsMet'],
                            concentrationReqsMet = data['concentrationReqsMet'],
                            minorReqsMet = data['minorReqsMet'],
                            perspectivesMet = data['perspectivesMet']
            )
            
            if data['formBtn'] == "submit":
                specialTopicCourse.status = 1 
                
            specialTopicCourse.save()
            databaseInterface.addSTCourseInstructors(instructors, specialTopicCourse.stId)

            if bannerNumber == "86" and data['formBtn'] == "save":
                message = "Course: #{0} has been saved. It needs to be submitted before it can be approved.".format(specialTopicCourse.stId)
                flash("Course has been saved. It needs to be submitted before it can be approved.")
                log.writer("INFO", current_page, message)
            else:
                flash("Course has successfully been added!")
                
        return redirect(redirect_url())
        
    else:
        abort(404) 
        
@app.route("/test_form", methods=["POST"])
def form_sample():
    data = request.form
    
    return "The parameter was: {0}".format(data['var1'])