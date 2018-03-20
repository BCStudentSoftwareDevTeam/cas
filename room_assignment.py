from app.models import * 
import random
import pdb
from collections import defaultdict

DATA_SET = {
            3542: ['108A','None'],      #1
            4360: ['104','None'],       #1
            4314: ['104','None'],       #1
            4513: ['104','B16','None'], #2
            4361: ['104','B16','None'], #2
            4391: ['B16','104','None'], #2
            4318: ['111','B16','None'], #2
            3479: ['112B','104','108A'],#3
            4364: ['112B','B16','104'], #3
            3587: ['108A','104','111'], #3
            3293: ['B16','111','112B'], #3
            3573: ['104','108A','B16'], #3
            3711: ['104','111','108A'], #3
            4369: ['B16','111','104'],  #3
            3575: ['B16','*'],          #4
            4363: ['104','*'],          #4
            3480: ['112B','*'],         #4
            4317: ['111','*'],          #4
            4315: ['112B','B16','*'],   #5
            3584: ['111','104','*'],    #5
            4362: ['104','112B','*'],   #5
            3294: ['108A', '111', '*'], #5
            4384: ['104','111','*'],    #5
            3590: ['*'],                #6
            3503: ['*']                 #6             
           }

WILDCARD = '*'
NONE = 'None'

'''
First we should order each list by priority:
1: [108, None]            # One Pick then None
2: ['B16','104','None']   # Two Picks then None
3: ['B16','111','112B']   # Three Picks 
4: ['104','*']            # One Pick then Any
5: ['108A', '111', '*']   # Two Picks then Any
6: [*]                    # Any

Then within each priority dictionary we should organize by time.
'''

class RoomAssigner:
    def __init__(self):
        self.default_semester = '201811' #Spring 2018
        self.priority_map     = None
        self.course_info      = dict()
        self.rooms_scheduled  = dict()
        self.anywhere         = []
        self.unhappy          = []
        self.all_CID          = []
        
    def random_pick(self, room_list):
        '''room_ids: list of integers'''
        #pdb.set_trace()
        random_rid = random.randint(1,137) #There are currently 137 courses
        if random_rid in room_list:
            return self.random_pick(room_list)
        else:
            room_list.append(random_rid)
            if len(room_list) > 2:
                return room_list
            else:
                return self.random_pick(room_list)
                
    def add_dummy_data(self):
        #pdb.set_trace()
        preferences = RoomPreference.select()
        new_pref = dict()
        for preference in preferences:
            '''Could not create the entries as I was looping through preferences
            because it was actively appending to the loop variable. Which 
            created an infinite loop'''
            course = preference.cId.cId
            room_list = self.random_pick([preference.rID.rID])
            room_list.pop(0)
            self.lazy_print("room", room_list)
            new_pref[course] = room_list
            self.lazy_print('# of elements', new_pref)    
        
        for key in new_pref:
            CID = key
            RID_list = new_pref[key]
            for RID in RID_list:
                RoomPreference.create(cId = CID, rID = RID)
        return True
    
    def lazy_print(self, info, variable):
        message = '{0}: {1}'.format(info, variable)
        print message
        print '--------------------- \n'
        
    def create_priority_map(self):
        #the following query will order based off of time. 
        courses = Course.select(
                       ).join(BannerSchedule, on = (Course.schedule == BannerSchedule.sid)
                       ).join(Term, on = (Course.term == Term.termCode)
                       ).join(Subject, on = (Course.prefix == Subject.prefix)
                       ).where(
                            Term.termCode == self.default_semester,
                            (Subject.prefix == 'CSC') | (Subject.prefix == 'TAD')
                       ).order_by(BannerSchedule.order)    
        print courses
        priority_list = []
        for course in courses:
            CID         = course.cId
            self.all_CID.append(CID)
            prefs       = DATA_SET[CID]
            course_info = (CID, course.schedule.startTime, course.schedule.endTime) 
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
        #self.lazy_print('Mapping: ',self.priority_map)
    
    def check_room_availability(self,choice,course):
        ''' course = (cid, start_time, endtime) '''
        if choice in self.rooms_scheduled:
            start_timeA = course[1]
            end_timeA   = course[2]
            unavailable_times = self.rooms_scheduled[choice]
            #print unavailable_times
            can_schedule = True
            for taken_time in unavailable_times:
                start_timeB = taken_time[1]
                end_timeB   = taken_time[2]
                #print "A: {0}-{1}".format(start_timeA,end_timeA)
                #print "B: {0}-{1}".format(start_timeB,end_timeB)
                #print '{} <= {} or {} >= {}'.format(end_timeA, start_timeB, start_timeA, end_timeB)
                if end_timeA <= start_timeB or start_timeA >= end_timeB:
                    pass
                else:
                    can_schedule = False
            if can_schedule == True:
                unavailable_times.append(course)
                return True
            else: 
                return False
        else:
            self.rooms_scheduled[choice] = [course]
            return True
    
    def assign_room(self):
        #TODO: GET COURSE starttime & endtime ::DONE
        #TODO: Check if room available...
        #TODO: Assign Room if available
        #TODO: Discover what to do if room is unavailble 
        order = [1,2,3,4,5,6]
        for priority in order: 
            courses = self.priority_map[priority]
            #self.lazy_print('SET',(priority,courses))
            for course in courses:
                prefs = DATA_SET[course[0]]
                count = 0
                for choice in prefs:
                    count += 1
                    if choice == WILDCARD:
                        self.anywhere.append(course)
                    elif choice == NONE:
                        self.unhappy.append(course)
                    else: 
                        available = self.check_room_availability(choice,course)
                        if available == True:
                            #print course
                            #print 'Found a Room'
                            break
                        else:
                            if count == priority:
                                self.unhappy.append(course)
        print "Room Schedules"
        total = 0
        for key, value in self.rooms_scheduled.items():
            print key
            total += len(value)
            for v in value:
                print v
            print 'Courses: {}'.format(len(value))
            print 'Total:   {}'.format(total)
            print '----------------------\n'
        print "Unhappy Rooms"
        print len(self.unhappy)
        print self.unhappy
        print '----------------------\n'
        print "Anywhere"
        print len(self.anywhere)
        print self.anywhere
        print '----------------------\n'
        total += len(self.anywhere)
        total += len(self.unhappy)
        print '{0}/{0}'.format(total,len(self.all_CID))
        print 'I have lost: {}'.format(len(self.all_CID)-total)
        #self.lazy_print('Rooms Scheduled',self.rooms_scheduled)
if __name__ == "__main__":
    room_assigner = RoomAssigner()
    room_assigner.create_priority_map()
    room_assigner.assign_room()
            
            