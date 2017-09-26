from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.databaseInterface import *

@app.route("/courses/<prefix>/", methods=["GET", "POST"])
def retrieveCourses(prefix):
    # Select 5 most recents years in the database to display courses from.
    terms = Term.select().distinct().order_by(Term.termCode.asc()).limit(10)

    term_list = []
    for term in terms:
        term_list.append(term.termCode)
    term_list.reverse()
    lowest_term = int(term_list.pop())
    
    try:
        # allCourses is the list of all the classes for each program 
        allCourses = BannerCourses.select().join(Subject).where(Subject.prefix== prefix)
        
        subject = Subject.get(Subject.prefix==prefix)
        
        courses_offered = []
        
        # courseName_to_term is a dictionary that maps the course name to the semesters when it was offered
        courseName_to_term = dict()
        
        for bannerRef in allCourses:
            # ref_course is the list of all the classes that were offered for all the terms that were selected
            ref_course = Course.select().where(Course.bannerRef == bannerRef.reFID, Course.term >= lowest_term ).distinct()
            terms_offered = []
            
            for course in ref_course:
                terms_offered.append(course.term.termCode)
            courseName_to_term[str(bannerRef.subject)+" "+ str(bannerRef.number)] = terms_offered
            
        return render_template("courseTable.html", terms = terms, allCourses = allCourses, courseName_to_term = courseName_to_term, subject = subject, cfg=cfg)
    
    except Exception as e:
        print ("Here is the error:")
        print(e)
        return redirect('/')

    
    
    
    