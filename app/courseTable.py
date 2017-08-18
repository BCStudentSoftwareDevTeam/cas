from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.databaseInterface import *

@app.route("/courses/<pid_or_prefix>/", methods=["GET", "POST"])
def retrieveCourses(pid_or_prefix):
    # Retrieve 5 most recents years in the database to display courses from.
    terms = Term.select().distinct().order_by(Term.termCode.asc()).limit(10)

    term_list = []
    for term in terms:
        term_list.append(term.termCode)
    term_list.reverse()
    lowest_term = int(term_list.pop())
    
    try:
        if pid_or_prefix.isnumeric():
            # print("In the if")
            # Retrieve all the courses that will be offered from each program
            allCourses = BannerCourses.select().join(Subject).where(Subject.pid== pid_or_prefix)
            # print("Out of the if")
        else:
            # print ("In the else")
            allCourses = BannerCourses.select().join(Subject).where(Subject.prefix== pid_or_prefix)
        
        courses_offered = [];
        test_list =[]
        reFID_to_term = dict()
        for bannerRef in allCourses:
            print 'This is bannerRef{}'.format(bannerRef.reFID)
            ref_course = Course.select().where(Course.bannerRef == bannerRef.reFID, Course.term >= lowest_term ).distinct()
            terms_offered = []
            for course in ref_course:
                terms_offered.append(course.term.termCode)
            reFID_to_term[bannerRef.reFID] = terms_offered
        print reFID_to_term            
        return render_template("courseTable.html", terms = terms, allCourses = allCourses, cfg=cfg)
    
    except Exception as e:
        print ("Here is the error:")
        print(e)
        return redirect('/')
    # Check when each specific course will be offered.
    
    
    
    
    