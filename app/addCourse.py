from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
from app.logic import databaseInterface
from app.logic.NullCheck import NullCheck
from app.logic.redirectBack import redirect_url
from flask import jsonify
import json
from playhouse.shortcuts import model_to_dict, dict_to_model
import datetime

'''
adds the course to the course table and to the course change if needed
'''
@app.route("/addOne/<tid>", methods=["POST"])
def add_one(tid):
    data = request.form
    print data
    print data["courses"]
    print tid
    course=Course.get(Course.cId==data["courses"])
    instructor=InstructorCourse.get(InstructorCourse.course_id==data["courses"])
    print course.prefix_id   
    course = Course(bannerRef=course.bannerRef_id,
                    prefix=course.prefix_id,
                    term=int(tid),
                    schedule=course.schedule_id,
                    capacity=course.capacity,
                    specialTopicName=course.specialTopicName,
                    notes=None,
                    crossListed=int(course.crossListed), rid=None
                    )
    course.save()

    course_instructor=InstructorCourse(
        username_id = instructor.username_id,
        course_id = course.cId
        
        )
    course_instructor.save()
        
    #for course in data["courses[]"]:
     #   print course
    return redirect(redirect_url()) 
    


@app.route("/addMany/<tid>", methods=["POST"])
def add_many(tid):
    data = request.form.getlist
    courses = request.form.getlist('courses')
    if courses:
        for i in courses:
            course=Course.get(Course.cId==int(i))
            instructor=InstructorCourse.get(InstructorCourse.course_id==int(i))
            course = Course(bannerRef=course.bannerRef_id,
                    prefix=course.prefix_id,
                    term=int(tid),
                    schedule=course.schedule_id,
                    capacity=course.capacity,
                    specialTopicName=course.specialTopicName,
                    notes=None,
                    crossListed=int(course.crossListed), rid=None
                    )
            course.save()
        
            course_instructor=InstructorCourse(
                username_id = instructor.username_id,
                course_id = course.cId
                
                )
            course_instructor.save()
            
    
    
    #for course in data["courses[]"]:
     #   print course
    return redirect(redirect_url()) 
    


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
        print data
        

        # instructors need to be a list
        instructors = request.form.getlist('professors[]')

        # start a null checker
        nullCheck = NullCheck()

        values = nullCheck.add_course_form(data)

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

        # we will need to keep the cid to enter the intructors
        cid = course.cId
        databaseInterface.addCourseInstructors(instructors, course.cId)

        newCourse = DataUpdate()
        if not databaseInterface.isTermOpen(tid):  # IF THE TERM IS NOT EDITABLE
            # ADD THE COURSE TO THE COURSECHANGE TABLE
            newCourse.addCourseChange(cid, cfg["changeType"]["create"])

        # log the change
        message = "Course: #{0} has been added".format(cid)
        log.writer("INFO", current_page, message)
        flash("Course has successfully been added!")
        return redirect(redirect_url())
    else:
        abort(404) 

        
@app.route('/get_termcourses/<term>/<department>')
def term_courses(term, department):
    #user_obj = User.select().where(User.username == 'charlie').get()
    #json_data = json.dumps(model_to_dict(user_obj))
    
    term1=Term.get(Term.name==term)
    courses={}
    for course in Course.select().where(Course.prefix_id==department, Course.term_id==term1.termCode):
        courses[course.cId]=model_to_dict(course)
    print courses
    return json.dumps(courses, default=myconverter)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

    
    
        

@app.route("/test_form", methods=["POST"])
def form_sample():
    data = request.form
    
    return "The parameter was: {0}".format(data['var1'])

