from functools import wraps
from flask import g
from app.models.models import Term, BannerCourses, Course, CrossListed, SpecialTopicCourse
from collections import defaultdict
from app.logic.authorizedUser import AuthorizedUser

def find_crosslist_via_id(cid):
    course_to_crosslisted = defaultdict(list)
    course = Course.get(Course.cId == cid)
    if course.crossListed:
        qs = CrossListed.select().where(CrossListed.courseId == cid)
        if qs.exists:
            for cross_course in qs:
                #skip the parent itself
                # print("ya", cross_course.crosslistedCourse.cId, cid)
                if cross_course.crosslistedCourse.cId != int(cid):
                    course_to_crosslisted[cid].append(cross_course.crosslistedCourse.bannerRef)

            return course_to_crosslisted
    return False

def find_crosslist_courses(prefix, tID):
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
        courses = (Course.select(Course, BannerCourses)
                         .join(BannerCourses)
                         .where(
                            (Course.prefix == prefix) & (Course.term == tID) & (Course.crossListed == 1)))
        # courses = courses_prefetch.select().where(Course.crossListed == 1)

        # line 46-49 Access courses in SpecialTopicCourse table that are crossListed and append it to course_to_crosslisted dict. -Sreynit 6/11/2021
        special_courses = SpecialTopicCourse.select().where(SpecialTopicCourse.crossListed == 1)
        for sp_crssl_course in special_courses:
            course_to_crosslisted[crssl_course].append(sp_crssl_course)

        for curr_course in courses:

            #if the course is crosslisted_child
            # print("cid", curr_course.cId, curr_course.capacity)
            if curr_course.parentCourse_id:
                # print("error", curr_course.parentCourse_id)
                #find its parent

                parent_course = Course.get(Course.cId == curr_course.parentCourse_id)

                #add parent course to child's list of crosslised courses
                #course_to_crosslisted[curr_course].append(parent_course)

                #add siblings to child's list of crosslisted courses
                for cross_course in CrossListed.select().where(CrossListed.courseId == parent_course.cId):

                    # print(cross_course.verified)
                    #skip the child itself
                    if cross_course.crosslistedCourse.cId != curr_course.cId:
                        course_to_crosslisted[curr_course].append(cross_course)
                    else:
                        course_to_crosslisted[curr_course].insert(0, cross_course.verified)


            #if the course is crosslisted_parent
            else:

                #add children to parent's list of crosslisted courses
                for cross_course in CrossListed.select().where(CrossListed.courseId == curr_course.cId):
                    # print(cross_course.verified)
                    #skip the parent itself
                    if cross_course.crosslistedCourse.cId != curr_course.cId:
                        course_to_crosslisted[curr_course].append(cross_course)
                    else:
                        course_to_crosslisted[curr_course].insert(0, cross_course.verified)
        # print(course_to_crosslisted)
        print(course_to_crosslisted)
        return course_to_crosslisted



# FIXME I don't know what this function does or why it exists. -SH
# def define_term_code_and_prefix(f):
#     @wraps(f)
#     def set_tId_and_prefix(*args, **kwargs):
#         #Set default values if no values were found
#         au = AuthorizedUser()
#         if not 'prefix' in kwargs:
#             last_visited = au.user.lastVisited
#             if au.user.lastVisited is not None:
#                 kwargs['prefix'] = last_visited.prefix
#             else:
#                 kwargs['prefix'] = Subject.get().prefix
#         if not 'tID' in kwargs:
#             termCode = (Term.select(Term.termCode).where(Term.state == 0))[0].termCode
#             kwargs['tID'] = termCode
#         # print kwargs
#
#         return f(*args, **kwargs)
#     return set_tId_and_prefix



def save_last_visited(f):
    ''' Author-> CDM 20160728
    Saves the last visited Program so the user always goes back to that one
    when they load the courses page.

    @param -tid      {{integer}} -> term identification number
    @param -prefix   {{string}}  -> course prefix (e.g., CSC)
    @param -username {{string}}  -> unique id for users

    @return -list [tid,prefix]   -> contains the value sets
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        au = AuthorizedUser()
        au.user.lastVisited = kwargs['prefix']
        au.user.save()
        return f(*args, **kwargs)

    return decorated_function
