# This script needs to get the data from the existing sqlite database and randomizes it so we don't use real production data while testing 
from peewee import *
import mysql.connector
from app.models import *
import app.models_sqlite as old 
import time
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


building = old.Building.select()


divisions = old.Division.select()


banner_schedule = old.BannerSchedule.select()

term_states = old.TermStates.select()


education_tech = old.EducationTech.select()


deadline = old.Deadline.select()



rooms = old.Rooms.select()
for i in rooms: 
    rID = int(i.rID)
    building_id = int(i.building.bID)
    # print(building_id)
    number = str(i.number)
    maxCapacity = int(i.maxCapacity)
    roomType = str(i.roomType)
    visualAcc = str(i.visualAcc)
    audioAcc = str(i.audioAcc)
    physicalAcc = str(i.physicalAcc)
    educationTech_id = int(i.educationTech.eId)
    specializedEq = str(i.specializedEq)
    specialFeatures = str(i.specialFeatures)
    movableFurniture = bool(i.movableFurniture)

programs = old.Program.select()


subjects = old.Subject.select()


users = old.User.select()
for i in users: 
    problems = ['Brumbaughc', 'Boumaj', 'Webba', 'Colesa']
    if i.username not in problems:
        if i.lastVisited:
            lastVisited_id = str(i.lastVisited.prefix)
        else: 
            lastVisited_id = 'MAT'



banner_courses = old.BannerCourses.select()
for i in banner_courses: 
    reFID = int(i.reFID)
    subject_id = str(i.subject.prefix)
    number = str(i.number)
    section = str(i.section)
    ctitle = str(i.ctitle)
    is_active = bool(i.is_active)


terms = old.Term.select()
# print("terms begotten")
for i in terms: 
    # print(i.termCode)
    termCode = int(i.termCode)
    semester = str(i.semester)
    if i.year:
        year = int(i.year)
    else:
        year = int((str(i.termCode))[:4])
    name = str(i.name)
    state = int(i.state)
    term_state_id=  int(i.term_state.csID)  

    editable = bool(i.editable) 
    
schedule_days = old.ScheduleDays.select()
for i in schedule_days: 
    schedule_id = str(i.schedule.sid)
    day = str(i.day)
    
    
courses = old.Course.select()
for i in courses:
    cId = int(i.cId)
    prefix_id = str(i.prefix.prefix)
    bannerRef_id = int(i.bannerRef.reFID)
    term_id = int(i.term.termCode)
    if i.schedule:
        schedule_id = str(i.schedule.sid)
    else:
        schedule_id = None
    if i.capacity:
        capacity = int(i.capacity)
    else:
        capacity = None
    specialTopicName = str(i.specialTopicName)
    notes = str(i.notes).encode('utf-8').strip()
    lastEditBy = str(i.lastEditBy)
    crossListed = bool(i.crossListed)
    if i.rid:
        rid_id = int(i.rid.rID)
    else:
        rid_id = None
    section = str(i.section)
    prereq = str(i.prereq)


special_topic_courses = old.SpecialTopicCourse.select()
for i in special_topic_courses:
    stId = int(i.stId)
    prefix_id = str(i.prefix.prefix)
    bannerRef_id = int(i.bannerRef.reFID)
    term_id = int(i.term.termCode)
    if i.schedule:
        schedule_id = str(i.schedule.sid)
    else:
        schedule_id = None
    if i.capacity:
        capacity = int(i.capacity)
    else:
        capacity = None
    specialTopicName = str(i.specialTopicName)
    notes = str(i.notes)
    lastEditBy = str(i.lastEditBy)
    submitBy = str(i.submitBy)
    crossListed = bool(i.crossListed)
    if i.rid:
        rid_id = int(i.rid.rID)
    else:
        rid_id = None
    status = int(i.status)
    credits = str(i.credits)
    description = str(i.description)
    prereqs = str(i.prereqs)
    majorReqsMet = str(i.majorReqsMet)
    concentrationReqsMet = str(i.concentrationReqsMet)
    minorReqsMet = str(i.minorReqsMet)
    perspectivesMet = str(i.perspectivesMet)
    section = str(i.section)
    

program_chairs = old.ProgramChair.select()
for i in program_chairs: 
    username_id = str(i.username.username)
    pid_id = int(i.pid.pID)

division_chairs = old.DivisionChair.select()
for i in division_chairs: 
    username_id = str(i.username.username)
    did_id = int(i.did.dID)

# THERE IS NO DATA YET IN BUILDINGMANAGER. 

# add_building_managers = ("INSERT INTO buildingmanager(username_id, bmid_id) VALUES (%s, %s)")

# building_managers = BuildingManager.select()
# for i in building_managers:
#     username_id = str(i.username.username)
#     bmid_id = int(i.bmid.bID)
#     data_building_managers = (username_id, bmid_id)
#     print(data_building_managers)
#     cursor.execute(add_building_managers, data_building_managers)

# The problems array is a collection of all the course ids that were in the InstructorCourse Table for which the course instance was already deleted

problems = [1124,1141,1390,1401,1468,1133,968,1480,1499,1502,1504,1505,1196,1528,1041,1555,1135,1577,1343,999,1600,1105,1644,1346,1576,1690,1692,1165,1696,1698,1700,1164,1168,1179,1706,2297,2528,2543,2522,2666,1729,1734,1730,2334,1726,2678,2681,2508,2013,2013,2032,2469,2206,2200,2705,2710,2462,2503,2711,2715,2055,2722,2722,2732,2733,2734,2065,2321,2771,1902,2773,2044,2781,2784,2812,2815,2816,1158,2819,2820,1190,2827,2535,2146,2482,2852,2853,2873,2878,2879,2116,2339,2888,2891,1887,2480,2900,2901,2911,2916,2921,1879,1867,1894,1897,2623,2620,2766,2565,2599,2611,2767,2768,2621,2995,2640,3012,2344,3013,3014,3015,2356,2637,2635,2636,2352,2632,2366,3018,3019,3020,3021,3022,2631,3023,3024,3024,3025,3026,2350,3027,2633,3028,3029,2355,3025,3026,2342,2345,3033,2639,3038,3039,3043,2365,3044,3045,3046,3063,3069,3070,3079,3080,2675,3104,3105,2606,2606,3180,4280,4273,3567,4292,3958,3959,4303,4313,4316,4019,4323,3561,4013,3520,3521,3522,4335,4339,4348,3289,4373,3789,3933,3354,3355,4390,4392,3353,4418,3384,4448,3669,4466,4468,4469,4470,4209,4073,3854,4189,4542,4219,3930,4545,4471,4594,4595,4472,4598,4602,4641,4651,4653,4656,4659,4662,4664,4665,4668,4670,4671,4672]
for i in problems:
    query = old.InstructorCourse.delete().where(InstructorCourse.course == i).execute()
    
    
    

instructor_courses = old.InstructorCourse.select()
for i in instructor_courses:
    f = open("problemfile.txt", "a")
    username_id = str(i.username.username)
    
    try:
        course_id = int(i.course.cId)
    except Exception as e: 
        f.write(str(e))
        f.write('\n')
        
    f.close()

problems = [5,6,8,46]    
for i in problems:
    query = old.InstructorSTCourse.delete().where(InstructorSTCourse.course == i).execute()
    

instructor_st_courses = old.InstructorSTCourse.select()
for i in instructor_st_courses:
    f = open("problemfile2.txt", "a")
    username_id = str(i.username.username)
    try:
        course_id = int(i.course.stId)
        # print(course_id)
    except Exception as e: 
        f.write(str(e))
        f.write('\n')
        


course_changes = old.CourseChange.select()
for i in course_changes:
    cId = int(i.cId)
    prefix_id = str(i.prefix.prefix)
    bannerRef_id = int(i.bannerRef.reFID)
    term_id = int(i.term.termCode)
    # print (cId, i.schedule)
    if i.schedule:
        schedule_id = str(i.schedule.sid)
    else:
        schedule_id = None
    # print(schedule_id)
    if i.capacity:
        capacity = int(i.capacity)
    else:
        capacity = None
    specialTopicName = str(i.specialTopicName)
    notes = str(i.notes)
    lastEditBy = str(i.lastEditBy)
    changeType = str(i.changeType)
    verified = bool(i.verified)
    crossListed = bool(i.crossListed)
    if i.rid:
        rid_id = int(i.rid.rID)
    else:
        rid_id = None
    tdcolors = str(i.tdcolors)
    section = str(i.section)

problems = ['3218','3219','3220','3221','3222','3224', '3225']
for i in problems:
    query = old.InstructorCourseChange.delete().where(InstructorCourseChange.username == i).execute()
 
add_instructor_course_change = ("INSERT INTO instructorcoursechange (username_id, course_id) VALUES (%s, %s)")

instructor_course_change = old.InstructorCourseChange.select()
for i in instructor_course_change:
    
    username_id = str(i.username.username)
   
    course_id = int(i.course.cId)
    


############# The Table Courses in Banner did not exist in the sqlite database yet #################
# add_courses_in_banner = ("INSERT INTO coursesinbanner (CIBID, bannerRef_id, instructor_id) VALUES (%s, %s, %s)")

# courses_in_banner = CoursesInBanner.select()
# for i in courses_in_banner:
#     CIBID = int(i.CIBID)
#     bannerRef_id = str(i.bannerRef.reFID)
#     instructor_id = str(i.instructor.username)
#     data_courses_in_banner = (CIBID, bannerRef_id, instructor_id)

#     cursor.execute(add_courses_in_banner, data_courses_in_banner)
# 


# Fix courses in room preferences to remove courses in room preferences not in course table
add_room_preferences = ("INSERT INTO roompreferences (`rpID`, `course_id`, `pref_1_id`, `pref_2_id`, `pref_3_id`, `notes`, `any_Choice`, `none_Choice`, `none_Reason`, `initial_Preference`, `priority`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

problems = ['4651', '4665', '4668', '4670'] # This is an array that has cids for which there is no course object because the course had been deleted
for i in problems: 
    query  = old.RoomPreferences.delete().where(RoomPreferences.course == i).execute()

    
    
room_preferences = old.RoomPreferences.select()
for i in room_preferences:
    f = open("problemfile4.txt", "a")
    rpID = int(i.rpID)
    # print(rpID)
    try:
        course_id = i.course.cId
    except Exception as e:
        f.write(str(e))
        f.write('\n')       
        
   
    pref_1_id = int(i.pref_1.rID) if i.pref_1 else None
    
    pref_2_id = int(i.pref_2.rID) if i.pref_2 else None
    
    pref_3_id = int(i.pref_3.rID) if i.pref_3 else None

    notes = str(i.notes)
    any_Choice = str(i.any_Choice)
    none_Choice = str(i.none_Choice)
    none_Reason = str(i.none_Reason)
    initial_Preference = str(i.initial_Preference)
    priority = int(i.priority)

