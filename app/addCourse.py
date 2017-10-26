from allImports import *
from updateCourse import DataUpdate
from app.logic import databaseInterface
from app.logic.NullCheck import NullCheck
from app.logic.redirectBack import redirect_url
from app.logic.authorization import must_be_authorized
from flask import jsonify
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

@app.route("/courses/get_sections/", methods=["POST"])
def get_sections():
    course = request.json['course']
    term = request.json['term']
    print(term)
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
	existing_section = list()
	sections = list()
        if edit and section is not None:
            sections.append(section)
            existing_section.append(section)
        for course in current_courses:
            existing_section.append(course.section)
	if len(existing_section) ==  0 or len(current_courses) == 0:
	    return jsonify(list("A"))
	else:
	    for i in range(1, 3):
		for letter in range(65,91):
		    letter = chr(letter) * i
		    if letter not in existing_section:
			sections.append(letter)

	    return jsonify(sections)




@app.route("/test_form", methods=["POST"])
def form_sample():
    data = request.form

    return "The parameter was: {0}".format(data['var1'])


