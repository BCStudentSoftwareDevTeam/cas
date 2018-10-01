from allImports import *
import random
import pdb
import json
from collections import defaultdict

# Globals
WILDCARD = '*'
NONE     = 'None'
PRIORITY = [1,2,3,4,5,6]

'''
Essential Data Structure Layouts


defining priority_list structure
1: [108, None]            # One Pick then None
2: ['B16','104','None']   # Two Picks then None
3: ['B16','111','112B']   # Three Picks 
4: ['104','*']            # One Pick then Any
5: ['108A', '111', '*']   # Two Picks then Any
6: [*]                    # Any

<data_set> from the create_data_set() method
CID: priority_list #eg 1353: [108,None]


<priority_map> from create_priority_map() metho
dict:
    key:   PRIORITY[X] #The global variable above currently int 1-6
    value: [(CID, startTime, endTime, [days])] 
'''

class RoomAssigner:
    def __init__(self, semester):
        self.default_semester = semester 
        self.priority_map     = None
        self.preference_map   = dict()
        self.rooms_scheduled  = dict()
        self.anywhere         = []
        self.unhappy          = []
        self.cid_num          = 0
        self.debug            = True
        
    def lazy_print(self, info=None, variable=None, results=False):
        if results == False:
            message = '{0}: {1}'.format(info, variable)
            print message
            print '--------------------- \n'
        else:
            total = 0
            scheduled_values = []
            unhappy_values   = []
            anywhere_values  = []
            for key, value in self.rooms_scheduled.items():
                print key
                for v in value:
                    scheduled_values.append(v[0])
                    print v
                total += len(value)
                print '{0} courses scheduled for Room ({1})'.format(len(value),key)
                print 'Total: {0} \n'.format(total)
            print '{0} Courses have been scheduled a classroom.'.format(total)
            print '--------------------- \n'
            print '{0} Unable to be Scheduled'.format(len(self.unhappy))
            print self.unhappy
            for h in self.unhappy:
                unhappy_values.append(h[0])
            total += len(self.unhappy)
            print '--------------------- \n'
            print '{0} will be scheduled anywhere'.format(len(self.anywhere))
            print self.anywhere
            for a in self.anywhere:
                anywhere_values.append(a[0])
            total += len(self.anywhere)
            print '--------------------- \n'
            print '{0} out of {1} have been scheduled'.format(total, self.cid_num)
            print '{0} are missing'.format(self.cid_num - total)
            print 'Scheduled CIDs: {}'.format(scheduled_values)
            print 'Unhappy CIDs: {}'.format(unhappy_values)
            print 'Anywhre CIDs: {}'.format(anywhere_values)
            duplicate_check = scheduled_values + unhappy_values + anywhere_values            
            duplicates = set([x for x in duplicate_check if duplicate_check.count(x) > 1])
            print 'Duplicate CIDs: {}\n'.format(duplicates)
            print '#DATA_SET_C = {0}'.format(DATA_SET)
            print '#Results: Total: {0}, Scheduled: {1}, Unhappy: {2}, Anywhere: {3}'.format(self.cid_num,len(scheduled_values),len(unhappy_values),len(anywhere_values))
            
    def courses_query(self):
        '''This method will grab all of the courses that need to be scheduled.'''
        #TODO: This query will need to be modified to grab all of the unscheduled courses.
        #The current query is still setup for my testing suite. 
        
        # This should query the RoomPreferences table, not the course table
        preferences = RoomPreferences.select(
                                    ).join(Course, on = (RoomPreferences.course == Course.cId)
                                    ).join(BannerSchedule, on = (RoomPreferences.course.schedule == BannerSchedule.sid)
                                    ).where(
                                        Term.termCode == self.default_semester,
                                        RoomPreferences.course.rid == null
                                    ).order_by(BannerSchedule.order)
                                    
        # courses = Course.select(
        #               ).join(Rooms, JOIN.LEFT_OUTER, on = (Course.rid == Rooms.rID)
        #               ).join(BannerSchedule, on = (Course.schedule == BannerSchedule.sid)
        #               ).join(Term, on = (Course.term == Term.termCode)
        #               ).where(
        #                   Term.termCode == self.default_semester,
        #                   Course.schedule != 'ZZZ'
        #               ).order_by(BannerSchedule.order)        
        
        return preferences
    
    def pick_random_room(self,building_id,room_list):
        '''FIXME: This method will need to be removed from the class. This was
        only meant to be used during the algorithm testing phase. '''
        query = Rooms.select(Rooms.rID).where(Rooms.building == building_id)
        rooms = list(t.rID for t in query)
        pick = random.choice(rooms)
        if len(rooms) > 3:
            pick = random.choice(rooms)
            while (pick in room_list):
                pick = random.choice(rooms)
        room_list.append(pick)
        return room_list
    
    def create_data_set(self):
        '''This method was built with the intention to convert the data within
        the model to the data structure used by the algorithm. Therefore, the
        method should convert the models data to the data structure needed for
        the algorithm. This method is essentially the middleware.'''
        data_set         = dict()
        preferences      = self.courses_query()
        if self.debug:
            self.lazy_print('Courses query:',courses)
        for course_preferences in preferences:
            # pdb.set_trace()
            # priority = random.choice(PRIORITY) 
            #TODO: The priority should live inside of the database now.
            #We can add it to the RoomPreferences table
            try:
                #TODO: The room list will now need to be built based off of 
                #pref_1, pref_2 & pref_3.
                #building_id = course.rid.building
                room_list = []
                
                if course_preferences.priority == 1:
                    room_list = [course_preferences.pref_1.rID, None]
                elif course_preferences.priority == 2:
                    room_list = [course_preferences.pref_1.rID, course_preferences.pref_2.rID, None]
                elif course_preferences.priority == 3:
                    room_list = [course_preferences.pref_1.rID, course_preferences.pref_2.rID, course_preferences.pref_3.rID]
                elif course_preferences.priority == 4:
                    room_list = [course_preferences.pref_1.rID, "*"]
                elif course_preferences.priority == 5:
                    room_list = [course_preferences.pref_1.rID, course_preferences.pref_2.rID, "*"]
                elif course_preferences.priority == 6:
                    room_list = [course_preferences.pref_1.rID, course_preferences.pref_2.rID, course_preferences.pref_3.rID, "*"]
                
                data_set[course.cId] = room_list
            
            except Exception as e:
                print(e)
                
                #building_id = random.choice([3,5]) #3 is the id for drapper, 5 is the id for frost
                #room_list = self.pick_random_room(building_id,[])
                #TODO: Remove the building_id this was used to help with the testing
            #FUTURE: We could keep the building_idit could be used later to help try to assign
            # courses to a similar room
            # if priority == 1:
            #     room_list.append(NONE)
            #     data_set[course.cId] = room_list
            # elif priority == 2:
            #     room_list = self.pick_random_room(building_id,room_list)
            #     room_list.append(NONE)
            #     data_set[course.cId] = room_list
            # elif priority == 3:
            #     room_list = self.pick_random_room(building_id,room_list)
            #     room_list = self.pick_random_room(building_id,room_list)
            #     data_set[course.cId] = room_list
            # elif priority == 4:
            #     room_list.append(WILDCARD)
            #     data_set[course.cId] = room_list
            # elif priority == 5: 
            #     room_list = self.pick_random_room(building_id,room_list)
            #     room_list.append(WILDCARD)
            #     data_set[course.cId] = room_list
            # else:
            #     data_set[course.cId] = [WILDCARD]
        if self.debug:
            self.lazy_print('The Complete data_set: ',data_set)
        
        return data_set
            
    #FUTURE: Will the layout of the new database there may be a way to combine
    # the create_priority_map & the create_data_set method.
    def create_priority_map(self):
        '''This method will create the priority_map data structure, listed in 
        the notes above.
        '''
        #the following query will order based off of time. 
        courses = self.courses_query()
        priority_list = []
        for course in courses:
            days = list(str(t.day) for t in course.schedule.days)
            self.cid_num += 1
            CID         = course.cId
            prefs       = DATA_SET[CID]
            course_info = (CID, course.schedule.startTime, course.schedule.endTime, days) 
            if len(prefs) == 1:
                priority_list.append((6, course_info))
            else:
                if NONE in prefs:
                    priority_list.append((len(prefs) - 1, course_info))
                elif WILDCARD in prefs:
                    priority_list.append((len(prefs) + 2, course_info))
                else:
                    priority_list.append((len(prefs), course_info))
        priority_map = defaultdict(list)
        for priority, course in priority_list:
            priority_map[priority].append(course)
        self.priority_map = priority_map
        if self.debug:
            self.lazy_print('priority_map:',self.priority_map)
    
    def check_room_availability(self,choice,course):
        ''' course & taken_time = (cid, start_time, endtime, [days]) '''
        #print self.rooms_scheduled
        if choice in self.rooms_scheduled:
            can_schedule = True
            unavailable_times = self.rooms_scheduled[choice] #All of the courses currently scheduled into to the room
            start_timeA = course[1]
            end_timeA   = course[2]
            A_days      = course[3]
            for taken_time in unavailable_times:
                B_days      = taken_time[3]
                all_days = A_days + B_days
                duplicates = set([x for x in all_days if all_days.count(x) > 1]) 
                #duplicates: Check to see if the two courses have days in common
                if len(duplicates) != 0: 
                    #Check the specific times only if they have days in common
                    start_timeB = taken_time[1]
                    end_timeB   = taken_time[2]
                    if end_timeA <= start_timeB or start_timeA >= end_timeB:
                        pass
                    else:
                        can_schedule = False
            if can_schedule == True:
                unavailable_times.append(course)
                self.rooms_scheduled[choice] = unavailable_times
                return True
            else: 
                return False
        else:
            self.rooms_scheduled[choice] = [course]
            return True
    
    def assign_room(self):
        for priority in PRIORITY:
            courses = self.priority_map[priority]
            for course in courses:
                prefs = DATA_SET[course[0]]
                for choice in prefs:
                    if choice == WILDCARD:
                        self.anywhere.append(course)
                    elif choice == NONE:
                        self.unhappy.append(course)
                    else: 
                        available = self.check_room_availability(choice,course)
                        if available == True:
                            break
                        else:
                            if choice == prefs[-1]: #if this is the last element in a list
                                self.unhappy.append(course)
                                break
        if self.debug:
            self.lazy_print(None,None,True)
            
    def assign_happy(self):
        '''This method should assign the rooms for the courses that were in the
        scheduled category. The way that you will assign the room is by modifing
        the course.rid field with the rid number.'''
        #This was not done yet, because there are still some process questions
        #hanging around out there. 
        pass
    
    def assign_anywhere(self):
        '''This method should assign the courses that stated that they were okay
        with being placed "anywhere".'''
        pass
    
    '''
    FUTURE: Process Question 
    There still needs to be a discussion to whether the unhappy people should be
    assigned by Jolena Prior to running the assign_anywhere method.
    
    Pros:
    1) I think that if we run the assign_anywhere method after Jolena has
    cleared all of the unhappy people.
    
    2) If we were to assign the scheduled & anywhere group there would be no way
    within the interface to distinguish between the two groups. Therefore, Jolena
    may think that she is causes conflicts by reassigning anywhere courses when
    in actually it is no issue at all. 
    
    Cons: 
    1) Unfortunately, I believe that our current UI design for the "resolving 
    conflicts" page is to grab all courses where rid is null. Which means that if
    we don't run the assign_anywhere group, the anywhere group would then be 
    merged with the unhappy group making Jolena thing there is a 100+ conflicts.
    Therefore, for now it may be better to assign the anywhere group before 
    the unhappy group. '''

if __name__ == "__main__":
    test_semester = '201612'
    room_assigner = RoomAssigner(test_semester)
    global DATA_SET 
    DATA_SET = room_assigner.create_data_set()
    print(DATA_SET)
    room_assigner.create_priority_map()
    room_assigner.assign_room()      
    
    
'''Testing Data'''

''' HOW TO:
Currently the algorithm is not set up for the new database changes. There are
functions that are meant to act as middleware, but have not been implemented 
with new changes. Therefore, there are some steps you will need to take in order
to test the data.

1) Rename data/algorith.data to data/db.sqlite
2) Move the room_assignment.py to the top level so that it can access app.models
3) It will be helpful to turn on the debuging mode in the __init__ so that you
can see what is happening. 

Additionally, I have listed out TODO, FIXME, FUTURE tags throughout the algorithm. 

'''

#The current testing setup is to put all of 201612 into 
#two building in order to setup a worse case scenerio 

#past results
#test0: Total: 383, Scheduled: 246, Unhappy: 21, Anywhere: 116
#test1: Total: 383, Scheduled: 250, Unhappy: 21, Anywhere: 112
#test2: Total: 383, Scheduled: 250 , Unhappy: 18, Anywhere: 115
#test3: Total: 383, Scheduled: 257, Unhappy: 14, Anywhere: 112
#test4: Total: 383, Scheduled: 262, Unhappy: 11, Anywhere: 110
#test5: Total: 383, Scheduled: 249, Unhappy: 12, Anywhere: 122
#test6: Total: 383, Scheduled: 256, Unhappy: 20, Anywhere: 107
#test7: Total: 383, Scheduled: 259, Unhappy: 16, Anywhere: 108
#test8: Total: 383, Scheduled: 252, Unhappy: 18, Anywhere: 113
#test9: Total: 383, Scheduled: 254, Unhappy: 16, Anywhere: 113