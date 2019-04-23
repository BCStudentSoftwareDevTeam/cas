from app.allImports import *
from flask import g
here = os.path.dirname(__file__)
conflicts = load_config(os.path.join(here, 'conflicts.yaml'))
# TODO: standarize docstring see https://www.python.org/dev/peps/pep-0257/


'''
returns all course that do not have schedule of none
separates the schedules that have ZZZ as schedule ID
@param roomID - id of the room we are looking at
@param termID - id of term the course are being held in

@returns {list} - list of all the courses except ZZ
@returns {list} - list of all courses that have Schedule ID ZZZ
'''


def getCoursesByRoom(room_id, term_id):
    specialScheduleCourseList = []
    courseList = []

    courses = Course.select().where(~(Course.schedule >> None),
                                    Course.rid == roomID,
                                    Course.term == termID).order_by(Course.rid)
    for course in courses:
        if course.schedule.sid in cfg['specialSchedule']['conflicts']:
            specialScheduleCourseList.append(course)
        else:
            courseList.append(course)

    return(specialScheduleCourseList, courseList)
    
def conflicts_sql(column):
    """Return the query to get all the conflicts in the database"""
    return '''(SELECT cb1.{0}
            FROM
                (SELECT * 
                FROM course c1 
                 INNER JOIN bannerschedule b1 
                    ON b1.sid = c1.schedule_id 
                 INNER JOIN scheduledays s1
                    ON s1.schedule_id = b1.sid
                 WHERE c1.term_id = ?) cb1
            JOIN 
                (SELECT * 
                 FROM course c1 
                 INNER JOIN bannerschedule b1 
                    ON b1.sid = c1.schedule_id 
                 INNER JOIN scheduledays s1
                    ON s1.schedule_id = b1.sid
                WHERE c1.term_id = ?) cb2
            ON (    cb1.rid_id = cb2.rid_id
                    AND
                    cb1.day = cb2.day 
                    AND 
                    cb2.startTime >= cb1.startTime 
                    AND 
                    cb2.startTime <= cb1.endTime
                    AND 
                    cb1.cId != cb2.cId))'''.format(column)


def getRoomConflicts(room_id, term_id):
    '''
    Return the conflicts for a room
    @param {int} room_id - the id of the room to search in
    @param {int} term_id - the code of the term to look in

    return {QueryResults} conflicts - A QueryResults object containing courses that conflict
    '''
    conflicts = (Course
                    .select()
                    .where(
                            Course.cId << SQL(conflicts_sql('cId'), term_id, term_id))
                    .where(Course.rid_id == room_id))
    return conflicts

def get_all_conflicts(term_id):
    '''
    Returns all the courses with conflicts
    @param {int} term_id - the code of the term to look in

    return {QueryResults} conflicts - A QueryResults object containing courses that conflict
    '''
    all_conflicts = (Course.select()
                            .where(Course.cId << SQL(conflicts_sql('cId'), term_id, term_id)))
    return all_conflicts
    
def get_rooms_with_conflicts(term_id):
    '''
    Returns all the rooms with conflicts
    @param {int} term_id - the code of the term to look in

    return {QueryResults} conflicts - A QueryResults object containing rooms that have conflicts
    '''
    rooms_with_conflicts = (Rooms.select(Rooms)
                            .where(Rooms.rID << SQL(conflicts_sql('rid_id'), term_id, term_id))
                            .group_by(Rooms.rID))
    return rooms_with_conflicts
    
def get_buildings_with_conflicts(term_id):
    '''
    Returns all the buildings with conflicts
    @param {int} term_id - the code of the term to look in

    return {QueryResults} conflicts - A QueryResults object containing buildings that have conflicts
    '''
    rooms_with_conflicts = get_rooms_with_conflicts(term_id).alias('room_conflicts')
    buildings_with_conflicts = (Building
                                    .select()
                                    .join(rooms_with_conflicts, 
                                    on=(Building.bID == rooms_with_conflicts.c.building_id))
                                    .group_by(Building.bID))
                                    
    return buildings_with_conflicts
    
def get_special_times(term_id):
    special_times = (Course.select(Course, BannerSchedule).join(BannerSchedule).where(Course.term == term_id, (BannerSchedule.sid=='ZZZ') | (BannerSchedule.sid=='A1')))
    return special_times

'''
removes duplicates from a list
@param {list} list to be parsed through

@returns {list} list without duplicates
'''


def removeDuplicates(array):
    seen = set()
    seenAdd = seen.add
    return [x for x in array if not (x in seen or seenAdd(x))]

'''
returns a dicitionary with the courseID as key
and the colorClass list as value
It also replaces the colors for verified entries
@param courses - course list to get colors from
@return {Dict} dicitionary of colorClassList
'''


def getColorClassDict(courses):
    
    colorClassDict = {}
    for course in courses:
        tdClass = course.tdcolors
        tdClassList = tdClass.split(",")
        if course.verified == True:
            for index, color in enumerate(tdClassList):
                tdClassList[index] =  cfg['columnColor']['verified']
        colorClassDict[course.cId] = tdClassList
    return colorClassDict

       
    
def createColorString(changeType):
        ''' Purpose: This method will create a comma seperated list depending on the changeType entered
        @param -changeType {string} = This should only ever be a type located in the config.yaml
        -->Author: CDM 20160713 '''
        # SET THE COLOR SCHEME FOR THE TD'S
        color = cfg["columnColor"][changeTpe]
        colorList = []

        for x in cfg["tableLayout"]["order"]:
            colorList.append(color)
        tdcolors = ",".join(colorList)

        return tdcolors

        
def map_unavailable_rooms(curr, unavailableRId):
    '''
    map unavailable rooms to their courses
    '''
    #select unavailable rooms
    unavailable_rooms = Rooms.select().where(Rooms.rID << unavailableRId)
    #select all the courses that use this room
    courses_obj=Course.select(Course).where(Course.rid << unavailableRId)
    #map unavailable rooms to their respective courses: Note: final mapper is passed to template
    unavailable_to_course={}
    for course in courses_obj:
        #these check is important: only consider courses whose startime is less than current course startTime and 
        #endTime greater than currentCourse startTime and courses term are equal to current course term
        
        #if course.schedule and course.schedule.startTime < curr.schedule.endTime and course.schedule.endTime > curr.schedule.startTime and course.term_id == curr.term_id:
            #map room object to list of courses that is taking place in this room
        if course.schedule and course.term_id == curr.term_id:
            if course.rid in unavailable_to_course:
                unavailable_to_course[course.rid].append(course)
            else:
                unavailable_to_course[course.rid]=[course]
    return unavailable_to_course

def rooms_to_course_schedule(assignedRooms):
    '''
    maps rooms to their assigned course schedule
    '''
    rooms_cache = {}  
    for room in assignedRooms.naive():
        if int(room.rID) in rooms_cache:
            rooms_cache[int(room.rID)].append(room.schedule)
        else:
            rooms_cache[int(room.rID)] = [room.schedule]
    print(rooms_cache)
    return rooms_cache
    
    
def find_avail_unavailable_rooms(curr_course):
    '''
    find all the room ids for the course if the room is free during a course schedule
    '''
    
    availablerooms = [] 
    unavailablerooms = []
    #query 1: get all the rooms that are not assigned to courses in current term
    join_cond = (
        (Rooms.rID == Course.rid) &
        (Course.term_id == curr_course.term.termCode) 
    )
    
    #select COUNT(*) from rooms LEFT OUTER JOIN course ON rooms.rID = course.rid_id and course.term_id = '201611' WHERE course.rid_id is NULL;          
    unassignedRooms = (Rooms
         .select()
         .join(Course, JOIN_LEFT_OUTER, on=join_cond)).where(Course.rid.is_null(True))
    
    print(unassignedRooms)
    #for i in unassignedRooms:
    #    print(i.rID)
    availablerooms = [room.rID for room in unassignedRooms]
    print("Unassigned:", len(availablerooms))
    #query 2: all the rooms that are assigned to courses in current term
    
    join_cond1 = (
        (Rooms.rID == Course.rid) &
        (Course.term_id == curr_course.term.termCode) 
    )
    
    
    assignedRooms = (Rooms.select(Rooms, Course.schedule).join(Course, on=join_cond1).where(Course.rid.is_null(False))
                    ).distinct() 
    
    print(assignedRooms)
    counter=0
    for i in assignedRooms.naive():
        counter+=1
        print(i.rID, i.schedule)
    print("Assigned: ", counter)
    print("before")
    #map assigned rooms to their courses' schedule 
    rooms_to_courses = rooms_to_course_schedule(assignedRooms)
    print(len(rooms_to_courses))
    #find non-conflicting assignedRooms rooms for course using conflict logic defined in config.yaml: room is free during a course schedule
    courseConflictsWith = set(cfg['conflicts'][curr_course.schedule_id])
    for key in rooms_to_courses:
        curr_room_schedules = set(rooms_to_courses[key]) 
        #if current course schedule does not conflict with schedules of assigned room courses, then room is available
        if (not courseConflictsWith & curr_room_schedules):
            availablerooms.append(key)
        else:
            unavailablerooms.append(key)
    return availablerooms, unavailablerooms

    
