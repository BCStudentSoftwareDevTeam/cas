from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.databaseInterface import *

@app.route("/courses/<prefix>/", methods=["GET", "POST"])
def retrieveCourses(prefix):
    # Retrieve 5 most recents years in the database to display courses from.
    terms = Term.select().distinct().order_by(Term.termCode.asc()).limit(10)

    term_list = []
    for term in terms:
        term_list.append(term.termCode)
    term_list.reverse()
    lowest_term = int(term_list.pop())
    
    try:
        allCourses = BannerCourses.select().join(Subject).where(Subject.prefix== prefix)
        
        courses_offered = [];
        reFID_to_term = dict()
        for bannerRef in allCourses:
            print 'This is bannerRef{}'.format(bannerRef.reFID)
            ref_course = Course.select().where(Course.bannerRef == bannerRef.reFID, Course.term >= lowest_term ).distinct()
            terms_offered = []
            for course in ref_course:
                terms_offered.append(course.term.termCode)
            reFID_to_term[bannerRef.reFID] = terms_offered
        print reFID_to_term            
        return render_template("courseTable.html", terms = terms, allCourses = allCourses, reFID_to_term = reFID_to_term, cfg=cfg)
    
    except Exception as e:
        print ("Here is the error:")
        print(e)
        return redirect('/')

    
    
    
    