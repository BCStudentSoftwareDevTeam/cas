from allImports import *
from updateCourse import DataUpdate
from app.logic import databaseInterface
from app.logic.NullCheck import NullCheck
from app.logic.redirectBack import redirect_url
from flask import jsonify
import json
from playhouse.shortcuts import model_to_dict, dict_to_model
import datetime
from app.logic.authorization import must_be_authorized


'''
adds the course to the course table and to the course change if needed
'''


@app.route("/addCourse/<tid>/<prefix>", methods=["POST"])
@must_be_authorized
def addCourses(tid, prefix):
    # set the current page
    current_page = "/" + request.url.split("/")[-1]

    # get the data
    data = request.form

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
        

@app.route("/addOne/<tid>", methods=["POST"])
def add_one(tid):
    data = request.form
    course=Course.get(Course.cId==data["courses"])
   
    
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
    
    try:  #if there is instructor 
        instructor=InstructorCourse.get(InstructorCourse.course_id==data["courses"])  
        course_instructor=InstructorCourse(
            username_id = instructor.username_id,
            course_id = course.cId
            )
        course_instructor.save()
        return redirect(redirect_url()) 
    except:  #if no instructor, just redirect
        return redirect(redirect_url()) 
    
    
@app.route("/addMany/<tid>", methods=["POST"])
def add_many(tid):
    data = request.form.getlist
    courses = request.form.getlist('courses')
    if courses:
        for i in courses:
            course=Course.get(Course.cId==int(i))
            
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
        
            
            try:  #if there is instructor 
                instructor=InstructorCourse.get(InstructorCourse.course_id==int(i))
                course_instructor=InstructorCourse(
                    username_id = instructor.username_id,
                    course_id = course.cId
                )
                course_instructor.save()
                return redirect(redirect_url()) 
            except:  #if no instructor then it's None
                return redirect(redirect_url()) 
    
        
@app.route('/get_termcourses/<term>/<department>')
def term_courses(term, department):
    try:
        term1=Term.get(Term.name==term)
        courses={}
        for course in Course.select().where(Course.prefix_id==department, Course.term_id==term1.termCode):
            courses[course.cId]=model_to_dict(course)
        print courses
        return json.dumps(courses, default=myconverter)
    except:
        return json.dumps("Error")

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()



@app.route("/test_form", methods=["POST"])
def form_sample():
    data = request.form
    
    return "The parameter was: {0}".format(data['var1'])

