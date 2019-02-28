from app.allImports import *
from app.updateCourse import DataUpdate

# TODO: standarize docstring see https://www.python.org/dev/peps/pep-0257/


'''
adds the professors from a list to a database
@param {list} professors - list of professors to be added
@param {int} cid = the course id the where the instructors need to be added to
'''


def addCourseInstructors(instructors, cid):
    for instructor in instructors:
        InstructorCourse(username=instructor, course=cid).save()

def addSTCourseInstructors(instructors, stid):
    for instructor in instructors:
        InstructorSTCourse(username=instructor, course=stid).save()

'''
adds division chair to database
@param {list} users - list of users that need to be added as division chair
@param {int} did - the division id where the division chairs are added to
'''


def addDivisionChairs(users, did):
    for user in users:
        DivisionChair(username=user, did=did).save()

'''
adds division chair to database
@param {list} users - list of users that need to be added as program chair
@param {int} pid - the program id where the program chairs are added to
'''


def addProgramChairs(users, pid):
    for user in users:
        ProgramChair(username=user, pid=pid).save()

'''
creates division
@param {string} name
'''


def createDivision(name):
    division = Division(name=name)
    division.save()
    return(division.name, division.dID)

'''creates program
@param {string} name
@param {int} divisionID

@returns string, int
'''


def createProgram(name, divisionID):
    program = Program(name=name, division=divisionID)
    program.save()
    return(program.name, program.pID)


'''
gets elements for the course sidebar
@returns selectQuery
'''


def getSidebarElements():

    return prefetch(Division.select(), Program, Subject)



''' gets the instructors belonging to a course
@param {list} courses - list of courses

@returns{dict} dictionary of courses keys and instructor values
'''


def createInstructorDict(courses):
    instructors = {}
    try:
        for course in courses:
            if "app.models.SpecialTopicCourse" in str(type(course)) :
                instructors[course.stId] = InstructorSTCourse.select().where(
                    InstructorSTCourse.course == course.stId)
            else:
                instructors[course.cId] = InstructorCourse.select().where(
                    InstructorCourse.course == course.cId)
    except:
        for course in courses:
                instructors[course.cId] = InstructorCourse.select().where(
                    InstructorCourse.course == course.cId)
    return instructors

'''
gets all of the buildings
@returns query object of the buildings
'''


def getAllBuildings():
    return Building.select().order_by(Building.name)

'''
gets all the rooms that belong to a building
'''


def getRoomsByBuilding(building):
    return Rooms.select().where(Rooms.building == building.building)

'''
gets all terms
return terms
'''


def getAllTerms():
    return Term.select().order_by(-Term.termCode)
    
def isTermOpen(termID):
    ''' returns booleans stating whether the term is open'''
    if (Term.get(Term.termCode == int(termID)).state == 0):
        return True
    else:
        return False
        
def isTermLocked(termID):
    ''' returns booleans stating whether the term is locked'''
    if (Term.get(Term.termCode == int(termID)).state == 2):
        return True
    else:
        return False
        
def isTermTracking(termID):
    ''' returns booleans stating whether the term is locked'''
    if (Term.get(Term.termCode == int(termID)).state == 1):
        return True
    else:
        return False
        
   

def editInstructors(newInstructors, courseID):
    ''' edits the instructs give a list of the new instructors
        @param {list} newInstructors - list of new instructors
        @param {int} courseID
    '''
 
    oldInstructors = InstructorCourse.select().where(InstructorCourse.course == courseID)
    for oldInstructor in oldInstructors:
        if oldInstructor.username.username not in newInstructors:
            oldInstructor.delete_instance()
        else:
            newInstructors.remove(oldInstructor.username.username)
    for instructor in newInstructors:
        newInstructor = InstructorCourse(username=instructor, course=courseID)
        newInstructor.save()

def editSTInstructors(newInstructors, courseID):
    ''' edits the instructs give a list of the new instructors
        @param {list} newInstructors - list of new instructors
        @param {int} courseID
    '''
    oldInstructors = InstructorSTCourse.select().where(
            InstructorSTCourse.course == courseID)
    for oldInstructor in oldInstructors:
            if oldInstructor.username.username not in newInstructors:
                oldInstructor.delete_instance()
            else:
                newInstructors.remove(oldInstructor.username.username)
    for instructor in newInstructors:
            newInstructor = InstructorSTCourse(
                username=instructor, course=courseID)
            newInstructor.save()
            

def editCourse(data, prefix, professors, crosslistedCourses):
        '''THIS FUNCTION EDITS THE COURSE DATA TABLE'''
        # check to see if the user has privileges to edit
        # get the course object
        #TODO: We are not doing null checks on the portion of
        #the code which is causing crashes on the system 
        
        course = Course.get(Course.cId == int(data['cid']))
        #CHECK VALUES FOR NULL
        room     = data["room"] if data["room"] else None
        capacity = data['capacity'] if data['capacity'] else None
        schedule = data['schedule'] if data['schedule'] else None
        section  = data['section']  if data['section'] else None
        if data['notes'].replace(" ", "") == "":
            notes = None
        else:
            notes = data['notes']
        
        course.crossListed = int(data["crossListed"])
        course.term = data['term']
        course.capacity = capacity
        course.section = section
        course.rid  = room
        course.schedule = schedule
        course.notes = notes
        course.lastEditBy = authUser(request.environ)
        course.save()
        new_instruc =  professors[:]
        editInstructors(professors, data['cid'])
        editCrosslistedCourse(course, crosslistedCourses, new_instruc)
        
def editCrosslistedCourse(parent, newCourses, newInstructors):
        
        '''
        
        
        '''
        newCourses = map(int, newCourses)
        #find courses where parent is equal to course.cId
        oldChildCourses = Course.select().where(Course.parentCourse == parent.cId)
        
        #if course has crosslisted children or newCrosslist course has been selested
        if oldChildCourses.exists() or newCourses:
            for oldCourse in oldChildCourses:
                
                #update it with parent data it if newCourse still contains oldcourse
                if oldCourse.bannerRef.reFID in newCourses:
                    updateChildCourse(oldCourse, parent, newInstructors)
                    #remove this course from current newCourses list after updating
                    newCourses = filter(lambda a: a != oldCourse.bannerRef.reFID, newCourses)    
                else:
                    #childCrosslistcourse has been removed, so delete it from database
                    rm =  RoomPreferences()
                    deleteChildCourse(oldCourse, rm)
                    
            #add remaing courses as new crosslisted child course to parent course
            if newCourses:
                for newCourse in newCourses:
                    #create a new childCrosslisted course for parent
                    createChildCourse(newCourse, parent, newInstructors)
        
      
def getCourseTimelineSchedules(day,tid):
    schedules = ScheduleDays.select(ScheduleDays.schedule
                          ).join(Course, on=(Course.schedule == ScheduleDays.schedule)
                          ).join(BannerSchedule, on=(BannerSchedule.sid == ScheduleDays.schedule)
                          ).where(ScheduleDays.day == day
                          ).where(Course.term == tid
                          ).distinct(
                          ).order_by(BannerSchedule.startTime)
    return schedules


def editSTCourse(data, prefix, professors, status, cfg):
        '''THIS FUNCTION EDITS THE COURSE DATA TABLE'''
        # check to see if the user has privileges to edit
        # get the specialTopicCourse object
        #TODO: We are not doing null checks on the portion of
        #the code which is causing crashes on the system
        specialTopicCourse = SpecialTopicCourse.get(SpecialTopicCourse.stId == int(data['stid']))
        #import pdb; pdb.set_trace()
        
        #CHECK VALUES FOR NULL
        room     = data["room"] if data["room"] else None
        capacity = data['capacity'] if data['capacity'] else None
        schedule = data['schedule'] if data['schedule'] else None
        section  = data['section']  if data['section'] else None            
        if data['notes'].replace(" ", "") == "":
            notes = None
        else:
            notes = data['notes']
        
        
        specialTopicCourse.status = status
        if status in cfg['specialTopicLogic']['approved']:
            bannercourses = BannerCourses(subject = specialTopicCourse.prefix,
                                          number  = specialTopicCourse.bannerRef.number,
                                          ctitle  = specialTopicCourse.specialTopicName,
                                          is_active = 1)
            bannercourses.save()
            course = Course(bannerRef = bannercourses,
                            prefix = specialTopicCourse.prefix,
                            term = specialTopicCourse.term,
                            schedule = specialTopicCourse.schedule,
                            capacity = specialTopicCourse.capacity,
                            section = specialTopicCourse.section,
                            specialTopicName = specialTopicCourse.specialTopicName,
                            notes = specialTopicCourse.notes,
                            crossListed = specialTopicCourse.crossListed,
                            rid = specialTopicCourse.rid)
            course.save()
            update_course = DataUpdate()
            structors(professors, course.cId)
            if isTermTracking(specialTopicCourse.term.termCode):
                update_course.addCourseChange(int(course.cId), "create")
        specialTopicCourse.status = status
        specialTopicCourse.crossListed = int(data["crossListed"])
        specialTopicCourse.capacity = capacity
        specialTopicCourse.rid  = room
        specialTopicCourse.schedule = schedule
        specialTopicCourse.notes = notes
        specialTopicCourse.section = section
        specialTopicCourse.lastEditBy = authUser(request.environ)
        specialTopicCourse.credits = data['credits']
        specialTopicCourse.description = data['description']
        specialTopicCourse.prereqs = data['prereqs']
        specialTopicCourse.majorReqsMet = data['majorReqsMet']
        specialTopicCourse.minorReqsMet = data['minorReqsMet']
        specialTopicCourse.concentrationReqsMet = data['concentrationReqsMet']
        specialTopicCourse.perspectivesMet = data['perspectivesMet']
        editSTInstructors(professors, data['stid'])    
        specialTopicCourse.save()

def addInstructorsChild(instructors, parentId, cid):
    '''
    add parent course instructors to childCourses when editing parent course
    
    '''
    parentInstructors = InstructorCourse.select().where(InstructorCourse.course == parentId)
    childInstructors = InstructorCourse.select().where(InstructorCourse.course == cid) 
    present = False
    for parentInstructor in parentInstructors:
        for childInstructor in childInstructors:
            if(childInstructor.username.username) == parentInstructor.username.username:
                present = True
        if present == False:
            #clone parent instructor to child
            InstructorCourse(username = parentInstructor.username.username, course = cid).save()
        present =  False
    #delete entries that is present in child but not parent
    
    exists = False
    for childInstructor in childInstructors:
        for parentInstructor in parentInstructors:
            if(childInstructor.username.username) == parentInstructor.username.username:
                exists = True
        if exists == False:
            #remove the child instructor
            childInstructor.delete_instance()
        exists = False
    
        
def createChildCourse(course_id, parent, newInstructors):
    '''
    create a crosslisted child course for a parent course
    Functionalities:
    a. Creates a child course in Course table
    b. Creates an entry in Crosslisted table to maintain its verified relationship with parent
    c. Create entries in InstructorCourse table so child course instructors same as parent
    d. if parent has roomPreference entry, clone it for child
    '''
    qs = CrossListed.select().where((CrossListed.courseId == parent.cId) & (CrossListed.crosslistedCourse == parent.cId))
    #if uncrosslisted course has selected a crosslist course
    if not qs.exists():
        crosslisted = CrossListed(
                courseId = parent.cId,
                crosslistedCourse= parent.cId,
                prefix= parent.prefix,
                verified = True,
                term= parent.term
            ).save()
    
    course_prefix=BannerCourses.get(BannerCourses.reFID == int(course_id)).subject_id
    
    #create a child course
    cc_course = Course.create(bannerRef=course_id,
            prefix = course_prefix,
            term = parent.term,
            schedule = parent.schedule,
            capacity = parent.capacity,
            specialTopicName = parent.specialTopicName,
            notes = parent.notes,
            crossListed = parent.crossListed,
            parentCourse = parent.cId,
            section = parent.section,
            prereq = parent.prereq
            )
    #TODO:create its instructors 
    addInstructorsChild(newInstructors, parent.cId, cc_course.cId)
    
    #create its crosslisted relationship entry with parent
    crosslisted = CrossListed(
                courseId = parent.cId,
                crosslistedCourse= cc_course.cId,
                prefix= course_prefix,
                verified = False,
                term= parent.term
            ).save()
    
    #create its roomPreference if parent has any

def deleteChildCourse(childCourse, roompreference):
    '''
    deletes crosslisted course from parent
    deletes course itself, Crosslisted relationship, instructors, roompreference entry if any
    '''
    #delete its crosslisted relationship with parent
    q = CrossListed.select().where(
        (CrossListed.crosslistedCourse == childCourse.cId) &
        (CrossListed.courseId == childCourse.parentCourse)
        )
    
    q.first().delete_instance()
        
    #delete the course itself
    childCourse.delete_instance()
        
    #delete course instructors
    instructors = InstructorCourse.select().where(InstructorCourse.course == childCourse.cId)
    for instructor in instructors:
        instructor.delete_instance()
        
    #delete course roompreference if any; check if it has a term so we where with AND
    roompreference.delete_room_preference(childCourse.cId)
    
def updateChildCourse(course, parent, newInstructors):
    '''
    updates crosslisted child course when edit has been made to its parent
    
    '''
    #update general course data with parent data
    course.term = parent.term
    course.schedule = parent.schedule
    course.capacity = parent.capacity
    course.specialTopicName = parent.specialTopicName
    course.notes = parent.notes
    course.crossListed = parent.crossListed
    course.parentCourse = parent.cId
    course.section = parent.section
    course.prereq = parent.prereq
    course.save()
    
    #update its instructors
    addInstructorsChild(newInstructors, parent.cId, course.cId)
    