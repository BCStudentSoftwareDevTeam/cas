from app.allImports import *
from flask import g
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
        


    
    
