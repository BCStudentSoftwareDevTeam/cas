from functools import wraps
from flask import g
from app.models import Term, BannerCourses, Course, CrossListed
from collections import defaultdict

def find_crosslist_via_id(cid):
    print("hello world")
    course_to_crosslisted = defaultdict(list)
    course = Course.get(Course.cId == cid)
    if course.crossListed:
        qs = CrossListed.select().where(CrossListed.courseId == cid)
        if qs.exists:
            for cross_course in qs:
                #skip the parent itself
                print("ya", cross_course.crosslistedCourse.cId, cid)
                if cross_course.crosslistedCourse.cId != int(cid):
                    course_to_crosslisted[cid].append(cross_course.crosslistedCourse.bannerRef)
                
            return course_to_crosslisted
    return False
    
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
        course_to_crosslisted = defaultdict(list)
        for curr_course in courses_prefetch.select().where(Course.crossListed):  
        
            #if the course is crosslisted_child
            if curr_course.parentCourse:
                
                #find its parent
                parent_course = Course.get(Course.cId == curr_course.parentCourse)
            
                #add parent course to child's list of crosslised courses
                #course_to_crosslisted[curr_course].append(parent_course)
                
                #add siblings to child's list of crosslisted courses
                for cross_course in CrossListed.select().where(CrossListed.courseId == parent_course.cId):
                    
                    #skip the child itself
                    if cross_course.crosslistedCourse.cId != curr_course.cId:
                        course_to_crosslisted[curr_course].append(cross_course)
                    else:
                        course_to_crosslisted[curr_course].insert(0, cross_course.verified)
                        
            
            #if the course is crosslisted_parent
            else:
                
                #add children to parent's list of crosslisted courses
                for cross_course in CrossListed.select().where(CrossListed.courseId == curr_course.cId):
                    
                    #skip the parent itself
                    if cross_course.crosslistedCourse.cId != curr_course.cId:
                        course_to_crosslisted[curr_course].append(cross_course)
                    else:
                        course_to_crosslisted[curr_course].insert(0, cross_course.verified)
        print(course_to_crosslisted)
        return course_to_crosslisted
    
    
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
    