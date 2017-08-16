from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.databaseInterface import *

@app.route("/courses/<pid>/", methods=["GET", "POST"])
def retrieveCourses(pid):
    # Retrieve 5 most recents terms in the database to display courses from.
    allTerms = Term.select().order_by(Term.termCode.desc()).limit(5)
    terms = []
    for term in allTerms:
        terms.append(term)
    terms.reverse()
    
    # Retrieve all the courses that will be offered from each program
    allCourses = BannerCourses.select().join(Subject).where(Subject.pid== pid)
    
    # Check when each specific course will be offered.
    
    
    
    
    return render_template("courseTable.html", terms = terms, allCourses = allCourses,cfg=cfg)
