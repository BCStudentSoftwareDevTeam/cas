from flask import jsonify
from flask import jsonify
import json
from playhouse.shortcuts import model_to_dict, dict_to_model
import datetime

from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.allImports import *
from app.updateCourse import DataUpdate
from app.logic import databaseInterface
from app.logic.NullCheck import NullCheck
from app.logic.redirectBack import redirect_url

from app.models.models import *
from app.logic.authorizedUser import can_modify

'''
adds the course to the course table and to the course change if needed
'''


def convertPrereqs(prereqs):
    "prevents from storing empty prereq string into the database"
    if prereqs[0]:
        return prereqs[0]
    return None


@main_bp.route("/addCourse/<tid>/<prefix>", methods=["POST"])
@can_modify
def addCourses(tid, prefix, can_edit):      # can_edit comes from @can_modify
    current_page = "/" + request.url.split("/")[-1]
    data = request.form

    # # instructors need to be a list

    instructors = request.form.getlist('professors[]')
    prereqs = request.form.getlist('prereqs')
    faculty_credit= request.form.getlist("faculty_credit")

    nullCheck = NullCheck()

    values = nullCheck.add_course_form(data)
    values.update({'offCampusFlag': bool(data.get('offCampusFlag', False))})
    banner = BannerCourses.get(BannerCourses.reFID == values['bannerRef'])
    bannerNumber = str(banner.number)[-2:]

    cId = ""

    if (bannerNumber == "86" and banner.ctitle == "Special Topics"):

        specialTopicCourse = SpecialTopicCourse(
            bannerRef=values['bannerRef'],
            prefix=values['prefix'],
            term=int(tid),
            schedule=values['schedule'],
            capacity=values['capacity'],
            specialTopicName=values['specialTopicName'],
            notes=values['requests'],
            crossListed=int(
                data['crossListed']),
            # rid=values['rid'],
            status=0,
            credits=data['credits'],
            description=data['description'],
            prereqs=data['prereqs'],
            majorReqsMet=data['majorReqsMet'],
            concentrationReqsMet=data['concentrationReqsMet'],
            minorReqsMet=data['minorReqsMet'],
            perspectivesMet=data['perspectivesMet'],
            section=data['section'],
            faculty_credit=data["faculty_credit"],
            offCampusFlag=bool(data.get('offCampusFlag', False))
	)
        if data['formBtn'] == "submit":
            specialTopicCourse.status = 1
        specialTopicCourse.save()
        databaseInterface.addSTCourseInstructors(
            instructors, specialTopicCourse.stId)

        if bannerNumber == "86" and data['formBtn'] == "save":
            message = "Course: #{0} has been saved. It needs to be submitted before it can be approved.".format(
                specialTopicCourse.stId)
            flash(
                "Course has been saved. It needs to be submitted before it can be approved.")
            # log.writer("INFO", current_page, message)
            # return redirect(redirect_url())
        else:
            flash("Course has successfully been added!")
            # return redirect(redirect_url())

    else:
        section_exists = Course.select().where(
            Course.bannerRef == values['bannerRef']).where(
            Course.term == int(tid)).where(
            Course.section == values['section']).exists()
        if section_exists:
            message = "Course: TID#{0} prefix#{1} with section {2} exists".format(
                tid, prefix, values["section"])
            # log.writer("INFO", current_page, message)
            flash(
                "Course with section %s already exists" %
                (values['section']), "error")
            # return redirect(redirect_url())

        # cross_courses=values["crossListed"]# [1,2,3]
        course = Course(bannerRef=values['bannerRef'],
                        prefix=values['prefix'],
                        term=int(tid),
                        schedule=values['schedule'],
                        capacity=values['capacity'],
                        specialTopicName=values['specialTopicName'],
                        notes=values['requests'],
                        crossListed=int(data['crossListed']),
                        section=values['section'],
                        faculty_credit=values['faculty_credit'],
                        prereq=convertPrereqs(prereqs),
                        offCampusFlag = bool(data.get('offCampusFlag', False))
                        )

        course.save()

        # update coursechange table if term is not editable:
        # the changetracker feature will be removed soon
        newCourse = DataUpdate()
        databaseInterface.addCourseInstructors(instructors, course.cId)
        if not databaseInterface.isTermOpen(
                tid):  # IF THE TERM IS NOT EDITABLE
            # ADD THE COURSE TO THE COURSECHANGE TABLE
            # Removed next line, don't think it's needed anymore. Is it? -Scott
	    # newCourse.addCourseChange(course.cId, cfg["changeType"]["create"])

            message = "Course: #{0} has been added".format(course.cId)
            # log.writer("INFO", current_page, message)

        # save crosslisted courses of the newly-created course in a database
        if(course.crossListed):
            create_crosslisted_courses(
                values, course, tid, prereqs, instructors, faculty_credit)

        flash("Course has successfully been added!")
    return redirect(redirect_url())


def create_crosslisted_courses(values, course, tid, prereqs, instructors, faculty_credit):
    '''
    Creates a crosslisted child relationship for a course

    '''
    crosslistedCourses = values["crossListedCourses"]
    if crosslistedCourses:

        # save parent crosslisted to itself
        crosslisted = CrossListed(
            courseId=course.cId,
            crosslistedCourse=course.cId,
            prefix=course.prefix,
            verified=True,
            term=int(tid))
        crosslisted.save()
        for course_id in crosslistedCourses:
            course_prefix = BannerCourses.get(
                BannerCourses.reFID == int(course_id)).subject_id
            cc_course = Course(bannerRef=course_id,
                               prefix=course_prefix,
                               term=int(tid),
                               schedule=values['schedule'],
                               capacity=values['capacity'],
                               specialTopicName=values['specialTopicName'],
                               notes=values['requests'],
                               crossListed=True,
                               parentCourse=course.cId,
                               section=values['section'],
                               prereq=convertPrereqs(prereqs),
                               faculty_credit= 0,
                               offCampusFlag = bool(values.get('offCampusFlag', False))
                               )
            cc_course.save()
            databaseInterface.addCourseInstructors(instructors, cc_course.cId)
            crosslisted = CrossListed(
                courseId=course.cId,
                crosslistedCourse=cc_course.cId,
                prefix=course_prefix,
                verified=False,
                term=int(tid)
            )

            crosslisted.save()


@main_bp.route("/addOne/<tid>", methods=["POST"])
@can_modify
def add_one(tid, can_edit):
    data = request.form
    # get an existing course
    course = Course.get(Course.cId == data["courses"])

    # create a new course using fields from an existing course because we are
    # importing it as new
    course = Course(bannerRef=course.bannerRef_id,
                    prefix=course.prefix_id,
                    term=int(tid),
                    schedule=course.schedule_id,
                    capacity=course.capacity,
                    specialTopicName=course.specialTopicName,
                    notes=None,
                    crossListed=int(course.crossListed),
                    rid=None,
                    prereq=course.prereq,
                    faculty_credit=course.faculty_credit
                    )
    course.save()

    # if there are instructors for an existing course, update instructors of
    # new course as well
    for instructor in InstructorCourse.select().where(
            InstructorCourse.course_id == data["courses"]):
        if instructor:
            course_instructor = InstructorCourse(
                username_id=instructor.username_id,
                course_id=course.cId
            )
            course_instructor.save()

    return redirect(redirect_url())


@main_bp.route("/addMany/<tid>", methods=["POST"])
@can_modify
def add_many(tid, can_edit):
    data = request.form.getlist
    courses = request.form.getlist('courses')
    if courses:
        for i in courses:
            course = Course.get(Course.cId == int(i))  # get an existing course
            # create a new course using fields from an existing course because
            # we are importing it as new
            newCourse = Course(bannerRef=course.bannerRef_id,
                               prefix=course.prefix_id,
                               term=int(tid),
                               schedule=course.schedule_id,
                               capacity=course.capacity,
                               specialTopicName=course.specialTopicName,
                               notes=None,
                               crossListed=int(course.crossListed),
                               rid=None,
                               section=course.section,
                               prereq=course.prereq,
                               faculty_credit=course.faculty_credit
                               )
            newCourse.save()

     # if there are many instructors for an existing course, update instructors
     # of new course as well
            for instructor in InstructorCourse.select().where(
                    InstructorCourse.course_id == int(i)):
                if instructor:
                    course_instructor = InstructorCourse(
                        username_id=instructor.username_id,
                        course_id=course.cId
                    )
                    course_instructor.save()

    return redirect(redirect_url())


@main_bp.route('/get_termcourses/<term>/<dept_prefix>')
def term_courses(term, dept_prefix):
    '''returns all courses for a specific term to ajax call when importing one/many course from terms'''

    try:
        selected_term = Term.get(Term.name == term)
        courses_list = []

        courses = Course.select().where(Course.prefix == dept_prefix,
                                        Course.term == selected_term.termCode)
        if courses:
            for course in courses:
                course_info = []
                bannerNumber = str(course.bannerRef.number)[-2:]

                if bannerNumber != '86': # Don't add special topics courses (they all end with x86)
                    course_prefix = course.prefix.prefix
                    course_info.append(course_prefix)

                    course_number = course.bannerRef.number
                    course_info.append(course_number + ' - ')

                    course_section = course.bannerRef.section
                    if course_section:
                        course_info.append(course_section)

                    course_ctitle = course.bannerRef.ctitle
                    course_info.append(course_ctitle)

                    if course.schedule and course.schedule != 'ZZZ':
                        course_start_time = course.schedule.startTime.strftime("%I:%M %p")
                        course_end_time = course.schedule.endTime.strftime("%I:%M %p")
                        course_info.append('(' + course_start_time + ' ' + course_end_time + ')')

                    instructors = InstructorCourse.select().where(InstructorCourse.course == course)
                    instructors_name = []
                    if instructors:
                        for instructor in instructors:
                            instructors_name.append(instructor.username.firstName [0]+ ". " + instructor.username.lastName)
                        course_info.append(str(instructors_name))

                courses_list.append({"course_id": course.cId, "course_info": ' '.join(course_info)})

        #sorting w.r.t course_info
        courses_list = sorted(courses_list,key= lambda i:i['course_info'])

        return json.dumps(courses_list)
    except Exception as e:
        print("Error on importing courses: ", e)
        return jsonify({'Success': False})


@main_bp.route("/courses/get_sections/", methods=["POST"])
def get_sections():
    course = request.json['course']
    term = request.json['term']
    course = course.replace("(New)", "").strip()
    try:
        term = int(term)
    except ValueError:
        return jsonify(list())
    edit = False
    if "edit" in request.json:
        edit = True
    prefix, number, section = course.split(" ", 2)
    bannerCourse = BannerCourses.select().where(
        BannerCourses.subject == prefix).where(
        BannerCourses.number == number)
    if bannerCourse.exists():
        bRef = bannerCourse.get().reFID
        current_courses = Course.select().where(
            Course.bannerRef == bRef).where(
            Course.term == term)
        if "86" in number:
            current_courses = SpecialTopicCourse.select().where(
                SpecialTopicCourse.bannerRef == bRef).where(
                SpecialTopicCourse.term == term)
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
    return jsonify(list("A"))


def generate_sections(existing_section):
    sections = list()
    for i in range(1, 3):
        for letter in range(65, 91):
            letter = chr(letter) * i
            if letter not in existing_section:
                sections.append(letter)
    return sections
