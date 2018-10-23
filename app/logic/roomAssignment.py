from app.allImports import *
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
        self.priority_map     = defaultdict(list)
        self.rooms_scheduled  = defaultdict(list) 
        self.preference_map   = dict()
        self.anywhere         = []
        self.unhappy          = []
        self.cid_num          = 0
        self.debug            = True
        
    def lazy_print(self, info=None, variable=None, results=False):
        '''This method prints the values of all the class variables'''
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
    
    def calculate_priority(self, roomPref):
        ''' This method defines a priority value to a roomPref object based on the preferences chosen by the user'''
        
        priorityScore = 0
        
        if(roomPref.pref_1 and roomPref.pref_2 and roomPref.pref_3): # If a room was selected for all three preference options
            return 3
        if(roomPref.pref_1 and roomPref.pref_2): # If a room was selected only for pref 1 and pref 2
            if(roomPref.none_Choice == 3): # If 'no other room works' was selected for pref 3
                return 2
            else:
                return 5
        if(roomPref.pref_1): # If a room was selected only for pref 1
            if(roomPref.none_Choice): # If 'no other room works was selected for pref 2 , 3'
                return 1
            else:
                return 4
        else:
            return 6
    
    def set_priority(self):
        ''' This method will grab all of the room preferences and set the correct priority since the 
            room preferences on prod have already been set. '''
            
        preferences = RoomPreferences.select() 
        
        for preference in preferences:
            pref_priority = self.calculate_priority(preference) # This the priority value for a specific roomPref object
            preference.priority = pref_priority
            preference.save()
            
    def courses_query(self):
        '''This method will grab all of the courses that need to be scheduled.
        We are excluding the ZZZ scheduling because it is a special case time that is scheduled from 12 A - 12 A'''
  
        self.set_priority()
        
        preferences = RoomPreferences.select().join(Course).where(Course.rid == None
                                    ).where(RoomPreferences.course == Course.cId
                                    ).where(Course.term == self.default_semester
                                    ).join(BannerSchedule, on = (BannerSchedule.sid == Course.schedule
                                    )).where(Course.schedule != 'ZZZ'
                                    ).order_by(BannerSchedule.order).distinct()
     
        return preferences
    
  
    
    def create_data_set(self):
        '''This method was built with the intention to convert the data within
        the model to the data structure used by the algorithm. This method is essentially the middleware.'''
        data_set         = dict()
        preferences      = self.courses_query()
        
        # if self.debug:
        #     self.lazy_print('Courses query:',preferences)
        
        for course_preferences in preferences:
      
            try:
              
                room_list = [] # This list has the  preference values for a roomPref object Ex: [102, 108, *]
                 
                # * stands for 'any room works' | None stands for 'This course does not require a room' or 'No other room works'
                
                
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
                    room_list = ["*"]
                
                data_set[course_preferences.rpID] = room_list
                self.priority_map[course_preferences.priority].append(course_preferences)
                
                
         
            except Exception as e:
                print(e)
                
            
        # if self.debug:
        #     self.lazy_print('The Complete data_set: ',data_set)
      
        return data_set
            
  
    
    def check_room_availability(self, choice, roomPref):
        ''' This method checks if a room is available for scheduling for a particular time slot. 
            If the room is available, a course is scheduled there for the time. 
            Else it leaves the room alone #deuces. 
            A - course we're trying to schedule based on the room preference (roomPref)
            B - Potentially conflicting course we're currently comparing against
            param choice: a room object
            param roomPref: a RoomPreference object
            
            return: ???
            '''
            
            
        ''' course & taken_time = (cid, start_time, endtime, [days]) '''
         
        if choice in self.rooms_scheduled:         # if the room I'm trying to schedule is in the dictionary of rooms which already have scheduled times
            can_schedule = True
            unavailable_times = self.rooms_scheduled[choice]   # All of the schedules currently used in this room ("choice")
            start_timeA = roomPref.course.schedule.startTime   # Start time of the roomPreference we're trying to schedule
            end_timeA   = roomPref.course.schedule.endTime     # End time of the roomPreference we're trying to schedule
            A_days = []                                        # A days are the days for the course we are trying to put in a room  
            
            schedule_days_A = ScheduleDays.select().where(ScheduleDays.schedule == roomPref.course.schedule.sid)
            for i in schedule_days_A:
                A_days.append(i.day)
       
            for taken_time in unavailable_times:
                 
                B_days = []                                    # These are the days for the courses already scheduled in a particular room 
                
                schedule_days_B =  ScheduleDays.select().where(ScheduleDays.schedule == taken_time.course.schedule.sid)
                for i in schedule_days_B:
                    B_days.append(i.day)
                all_days = A_days + B_days                     # We're gonna check all the days for both A and B
                
                duplicates = set([x for x in all_days if all_days.count(x) > 1])       # Removes any day that only has 0 or 1 entry in all_days
                #duplicates: Check to see if the two courses have days in common
                if len(duplicates) != 0: 
                    #Check the specific times only if they have days in common
                    start_timeB = taken_time.course.schedule.startTime
                    end_timeB   = taken_time.course.schedule.endTime
                    if end_timeA <= start_timeB or start_timeA >= end_timeB:
                        pass
                    else:
                        can_schedule = False
            if can_schedule == True:
                unavailable_times.append(roomPref)         # Add the room to unavailable_times
                roomPref.course.rid = choice               # Saves room to course for this pref               
                roomPref.course.save()                     
                self.rooms_scheduled[choice] = unavailable_times       # Updates schedules taken for this room
                return True
            else:               
                return False
        else:                      # No courses have been scheduled in this room ("choice") yet; create it
            roomPref.course.rid= choice
            roomPref.course.save()
            self.rooms_scheduled[choice] = [roomPref]
            return True
    
    def assign_room(self, DATA_SET):
        ''' This method simply assigns rooms to courses based on their priority granted that the rooms are already found available. '''
        
        for priority in PRIORITY:
            preferences = self.priority_map[priority]
            for roomPref in preferences:
                prefs = DATA_SET[roomPref.rpID]
                for choice in prefs:
                    if choice == "*":
                        self.anywhere.append(roomPref)
                    elif choice == None:
                        self.unhappy.append(roomPref)
                    else: 
                        available = self.check_room_availability(choice, roomPref)
                        if available == True:
                            break
                        else:
                            if choice == prefs[-1]: #if this is the last element in a list
                                self.unhappy.append(roomPref)
                                break
        
            
    # def run_algorithm(self):
    #     # room_assigner = RoomAssigner(termCode)
    #     self.courses_query()
    #     DATA_SET = self.create_data_set()
    #     # print(DATA_SET)
    #     # print("here")
    #     self.assign_room(DATA_SET)
    #     return 1
  
        

# if __name__ == "__main__":
#     ''' This is just for testing purposes'''
    
#     test_semester = '201812'
#     room_assigner = RoomAssigner(test_semester)
#     room_assigner.courses_query()
#     global DATA_SET 
#     DATA_SET = room_assigner.create_data_set()
#     room_assigner.assign_room()      
    
