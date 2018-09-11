from functools import wraps
from flask import g
from app.models import Term, BannerCourses, Course, CrossListed


def find_crosslist_courses(courses_prefetch):
        """Return crosslisted courses for given courses
        
        Args:
            courses_prefetch : class 'app.models.Course'
               Course Model instance returned after doing Select query from the database
            
        Returns:
            course_to_crosslist : dict
                Dictionary that maps course_id to its crosslisted courses (list of tuples). 
                
                Example: 
                       {21: [("Data Structures", False), ("BUS112", True)]}
                Note:
                    List of tuples: Each crosslisted course is stored in a tuple.
                    Tuple: contains Crosslisted Course Name, Verification State
        """
        course_to_crosslist={}
        #get crosslisted courses for each course
        for each_course in courses_prefetch:
            qs=CrossListed.select(CrossListed, CrossListed.verified, BannerCourses.ctitle).join(BannerCourses).switch(CrossListed).join(Course).where(CrossListed.courseId_id==each_course.cId).naive()
            if qs.exists():
                #map cross-courses to actual courses to be used in frontend
                for crosslist_course in qs:
                    if each_course.cId in course_to_crosslist:
                        course_to_crosslist[each_course.cId].append((crosslist_course.ctitle, crosslist_course.verified))
                    else:
                        course_to_crosslist[each_course.cId]=[(crosslist_course.ctitle,crosslist_course.verified)]
        return course_to_crosslist
    
    
def define_term_code_and_prefix(f):
    @wraps(f)
    def set_tId_and_prefix(*args, **kwargs):
        #Set default values if no values were found
        if not 'prefix' in kwargs:
            last_visited = g.user.lastVisited
            if g.user.lastVisited is not None:
                kwargs['prefix'] = last_visited.prefix
            else:
                kwargs['prefix'] = Subject.get().prefix
        if not 'tID' in kwargs:
            termCode = (Term.select(Term.termCode).where(Term.state == 0))[0].termCode
            kwargs['tID'] = termCode
        print kwargs
            
        return f(*args, **kwargs)
    return set_tId_and_prefix


''' Author-> CDM 20160728
Purpose: we store the prefix as lastVisted and 
call function with after saving last visited
@param -tid      {{integer}} -> term identification number
@param -prefix   {{string}}  -> course prefix
@param -username {{string}}  -> unique id for users

@return -list [tid,prefix]   -> contains the value sets
'''
def save_last_visited(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.user.lastVisited = kwargs['prefix']
        g.user.save()
        return f(*args, **kwargs)
        
    return decorated_function
    