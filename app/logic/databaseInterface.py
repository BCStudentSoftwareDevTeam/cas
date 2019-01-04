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
    oldInstructors = InstructorCourse.select().where(
            InstructorCourse.course == courseID)
    for oldInstructor in oldInstructors:
            if oldInstructor.username.username not in newInstructors:
                oldInstructor.delete_instance()
            else:
                newInstructors.remove(oldInstructor.username.username)
    for instructor in newInstructors:
            newInstructor = InstructorCourse(
                username=instructor, course=courseID)
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
            

def editCourse(data, prefix, professors):
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
        crossliscourses = data.getlist('crossListedCourses')
        # print(crossliscourses)
        if course.crossListed == 1 and len(crossliscourses) != 0:
            currentCrosslistCourses = Course.select().where(Course.parentCourse == data['cid'])
            crosslistedrelationship = CrossListed.select().where(CrossListed.courseId == data['cid'])
            for course in currentCrosslistCourses:
                course.delete_instance()
            for relationship in crosslistedrelationship:
                relationship.delete_instance()
            for futurecourse in crossliscourses:
                temp = BannerCourses.select().where(BannerCourses.reFID == futurecourse)  
                for course in temp:
                    newcrosslist = Course.create(prefix = course.subject,bannerRef = futurecourse,term = data['term'],capacity = capacity,section = section,schedule = schedule,
            notes = notes,crossListed =int(data["crossListed"]), parentCourse = int(data['cid']))
                newcrosslist.save()
            
        course.term = data['term']
        course.capacity = capacity
        course.section = section
        course.rid  = room
        course.schedule = schedule
        course.notes = notes
        course.lastEditBy = authUser(request.environ)
        course.save()
        editInstructors(professors, data['cid'])
        
        
        # for value in crossliscourses:
        #     newcrosscourse = Course.select().where(Course.bannerRef == value)
        #     for cours in newcrosscourse:
        #         cc = CrossListed.create(courseId = int(data['cid']),crosslistedCourse = cours.cId, verified = 0,prefix=cours.prefix,term = int(data['term']))
        #         cc.save()
  
        # n1 = Course.select()
        
        # for i in n1:
        #     temp = CrossListed.create(courseId = int(data['cid']), crosslistedCourse = i.cId,verified = 0, prefix = "2018992", term =data['term'] )
        #     temp.save()
            
            
            
       # for course in crossliscourses:
        #     n1 = Course.select().where(Course.bannerRef == course)
        #     for i in n1:
                # temp = CrossListed.create(courseId = int(data['cid']), crosslistedCourse = i.cId,verified = 0, prefix = "2018992", term =data['term'] )
                # temp.save()

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
            addCourseInstructors(professors, course.cId)
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
