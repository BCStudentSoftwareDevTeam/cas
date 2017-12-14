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
from flask import jsonify
'''
adds the course to the course table and to the course change if needed
'''


@app.route("/addCourse/<tid>/<prefix>", methods=["POST"])
@must_be_authorized
def addCourses(tid, prefix):
    current_page = "/" + request.url.split("/")[-1]

    # set the current page

    # get the data
    data = request.form
    # instructors need to be a list
    instructors = request.form.getlist('professors[]')

    nullCheck = NullCheck()

    values = nullCheck.add_course_form(data)
    banner = BannerCourses.get(BannerCourses.reFID == values['bannerRef'])
    bannerNumber = str(banner.number)[-2:]
    cId = ""

    if bannerNumber != "86":
        # update the course
        section_exists = Course.select().where(Course.bannerRef == values['bannerRef']).where(Course.term == int(tid)).where(Course.section ==values['section']).exists()
        if section_exists:
            message = "Course: TID#{0} prefix#{1} with section {2} exists".format(tid,prefix, values["section"])
            log.writer("INFO", current_page, message)
            flash("Course with section %s already exists" % (values['section']),"error")
            return redirect(redirect_url())

        course = Course(bannerRef=values['bannerRef'],
                        prefix=values['prefix'],
                        term=int(tid),
                        schedule=values['schedule'],
                        capacity=values['capacity'],
                        specialTopicName=values['specialTopicName'],
                        notes=values['requests'],
                        crossListed=int(data['crossListed']),
                        rid=values['rid'],
                        section = values['section']
                        )

        course.save()
        databaseInterface.addCourseInstructors(instructors, course.cId)

        newCourse = DataUpdate()
        if not databaseInterface.isTermOpen(tid):  # IF THE TERM IS NOT EDITABLE
            # ADD THE COURSE TO THE COURSECHANGE TABLE
            newCourse.addCourseChange(course.cId, cfg["changeType"]["create"])

            message = "Course: #{0} has been added".format(course.cId)
            flash("Course has successfully been added!")
            log.writer("INFO", current_page, message)
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
                        credits = data['credits'],
                        description = data['description'],
                        prereqs = data['prereqs'],
                        majorReqsMet = data['majorReqsMet'],
                        concentrationReqsMet = data['concentrationReqsMet'],
                        minorReqsMet = data['minorReqsMet'],
                        perspectivesMet = data['perspectivesMet'],
                        section = data['section']
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

@app.route("/addOne/<tid>", methods=["POST"])
def add_one(tid):
    data = request.form
    course= Course.get(Course.cId==data["courses"]) #get an existing course

    #create a new course using fields from an existing course because we are importing it as new
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

     #if there are instructors for an existing course, update instructors of new course as well
    for instructor in InstructorCourse.select().where(InstructorCourse.course_id==data["courses"]):
        if instructor:
            course_instructor=InstructorCourse(
                username_id = instructor.username_id,
                course_id = course.cId
                )
            course_instructor.save()


    return redirect(redirect_url())


@app.route("/addMany/<tid>", methods=["POST"])
def add_many(tid):
    data = request.form.getlist
    courses = request.form.getlist('courses')
    if courses:
        for i in courses:
            course=Course.get(Course.cId==int(i)) #get an existing course
            #create a new course using fields from an existing course because we are importing it as new
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


     #if there are many instructors for an existing course, update instructors of new course as well
            for instructor in InstructorCourse.select().where(InstructorCourse.course_id==int(i)):
                if instructor:
                    course_instructor=InstructorCourse(
                        username_id = instructor.username_id,
                        course_id = course.cId
                        )
                    course_instructor.save()

    return redirect(redirect_url())


@app.route('/get_termcourses/<term>/<department>')
def term_courses(term, department):
    '''returns all courses for a specific term to ajax call when importing one/many course from terms'''
    try:
        term1=Term.get(Term.name==term)
        courses={}
        for course in Course.select().where(Course.prefix_id==department, Course.term_id==term1.termCode):
            courses[course.cId]=model_to_dict(course)
            courses[course.cId]["schedule"]["startTime"]= str(courses[course.cId]["schedule"]["startTime"].strftime("%p %H:%M:%S"))
            courses[course.cId]["schedule"]["endTime"]= str(courses[course.cId]["schedule"]["endTime"].strftime("%p %H:%M:%S"))
        print courses
    
        return json.dumps(courses)
    except:
        return json.dumps("Error")



@app.route("/courses/get_sections/", methods=["POST"])
def get_sections():
    course = request.json['course']
    term = request.json['term']
    try:
        term = int(term)
    except ValueError:
	return jsonify(list())
    edit = False
    if "edit" in request.json:
        edit = True
    prefix, number, section = course.split(" ", 2)
    bannerCourse = BannerCourses.select().where(BannerCourses.subject == prefix).where(BannerCourses.number == number)
    if bannerCourse.exists():
        bRef = bannerCourse.get().reFID
        current_courses = Course.select().where(Course.bannerRef == bRef).where(Course.term == term)
        if "86" in number:
            current_courses = SpecialTopicCourse.select().where(SpecialTopicCourse.bannerRef == bRef).where(SpecialTopicCourse.term == term)
        existing_section = list()
        sections = list()
        if edit and section is not None:
            sections.append(section)
            existing_section.append(section)

        for course in current_courses:
            existing_section.append(course.section)
        if "A" not in existing_section or len(current_courses) == 0:
            return jsonify(list("A"))
        else:
            sections = generate_sections(existing_section)
            return jsonify(sections)



def generate_sections(existing_section):
    sections = list()
    for i in range(1, 3):
        for letter in range(65,91):
            letter = chr(letter) * i
            if letter not in existing_section:
                sections.append(letter)
    return sections

@app.route("/test_form", methods=["POST"])
def form_sample():
    data = request.form
    return "The parameter was: {0}".format(data['var1'])
