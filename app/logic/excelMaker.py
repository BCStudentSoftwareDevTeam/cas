import xlsxwriter
from app.allImports import *
import sys,os
import time 
from datetime import datetime
import datetime as dt



class ExcelMaker:
    def __init__(self):
        self.program_row = 2
        self.cross_row   = 2
        self.master_row  = 2
        self.intr_letter = ''
        self.all_schedules = ['A', 'A1', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q','R','S','T','U','V','W','X','Y', 'Z','I1']
        self.schedule_to_room = {}
    def writeRow(self,sheet,column,row,value):
        sheet.write('{0}{1}'.format(column,row),value)

    def writeHeaders(self,sheet):
        sheet.write('A1','Prefix')
        sheet.write('B1','Number')
        sheet.write('C1','Title')
        sheet.write('D1','Block ID')
        sheet.write('E1','Block')
        sheet.write('F1', 'Time')
        sheet.write('G1', 'Capacity')
        sheet.write('H1', 'Notes')
        sheet.write('I1','Section')
        sheet.write('J1', 'Assigned Room')
        sheet.write('K1', 'Preference 1')
        sheet.write('L1','Preference 2')
        sheet.write('M1','Preference 3')
        sheet.write('N1','Instructors')
        self.intr_letter = 'N'
        
    def writeSpecialHeaders(self,sheet):
        sheet.write('K1','credits')
        sheet.write('L1','description')
        sheet.write('M1','prerequisites')
        sheet.write('N1','major Req')
        sheet.write('O1','Concentration Req')
        sheet.write('P1', 'Minor Req')
        sheet.write('Q1', 'Perspectives Request')
        sheet.write('R1', 'Instructors')
        self.intr_letter = 'R'
    
    def writeAllRoomHeaders(self, sheet):
        sheet.write('A1', 'Room')
        sheet.write('B1', 'Capacity')
        sheet.write('C1', 'Seating Layout')
        sheet.write('D1', 'Times Scheduled')
        sheet.write('E1', 'Times Available')
        sheet.write('F1', 'Visual Accessibility')
        sheet.write('G1', 'Audio Accessibility')
        sheet.write('H1', 'Physical Accessibility')
        sheet.write('I1', 'Specialized Equipment')
        sheet.write('J1', 'Special Features')
        sheet.write('K1', 'Movable Furniture')
        sheet.write('L1', 'Projector(s)')
        sheet.write('M1', 'SmartBoard(s)')
        sheet.write('N1', 'Instructor Computers')
        sheet.write('O1', 'Podium')
        sheet.write('P1', 'Student Workspaces')
        sheet.write('Q1', 'Chalkboards')
        sheet.write('R1', 'WhiteBoards')
        sheet.write('S1', 'DVD')
        sheet.write('T1', 'Blu-Ray')
        sheet.write('U1', 'Audio')
        sheet.write('V1', 'Extro')
        sheet.write('W1', 'Doc Cam')
        sheet.write('X1', 'VHS')
        sheet.write('Y1', 'Mondopad')
        sheet.write('Z1', 'Tech Cart')
        self.intr_letter = 'Z'
    
        
    def write_all_rooms_info(self, sheet, room, row, available_times):
        sheet.write('A{0}'.format(row), room.building.name +' '+ room.number)
        sheet.write('B{0}'.format(row), room.maxCapacity)
        sheet.write('C{0}'.format(row), room.roomType)
        if room.building.name +' '+ room.number in self.schedule_to_room:
            taken_times = []
            for i in self.schedule_to_room[room.building.name +' '+ room.number]:
                banner_schedule = BannerSchedule.select().where(BannerSchedule.sid == i).first()
                taken_times.append( '(' +self.get_schedule_days(banner_schedule) + ': '+ str(banner_schedule.startTime)+ ' - ' + str(banner_schedule.endTime) + ')')
            sheet.write('D{0}'.format(row), ' , '.join(taken_times))
            
        else:
            sheet.write('D{0}'.format(row),' ')
        sheet.write('E{0}'.format(row), ' , '.join(available_times))
        sheet.write('F{0}'.format(row), room.visualAcc)
        sheet.write('G{0}'.format(row), room.audioAcc)
        sheet.write('H{0}'.format(row), room.physicalAcc)
        sheet.write('I{0}'.format(row), room.specializedEq)
        sheet.write('J{0}'.format(row), room.specialFeatures)
        sheet.write('K{0}'.format(row), room.movableFurniture)
        sheet.write('L{0}'.format(row), room.educationTech.projector)
        sheet.write('M{0}'.format(row), room.educationTech.smartboards)
        sheet.write('N{0}'.format(row), room.educationTech.instructor_computers)
        sheet.write('O{0}'.format(row), room.educationTech.podium)
        sheet.write('P{0}'.format(row), room.educationTech.student_workspace)
        sheet.write('Q{0}'.format(row), room.educationTech.chalkboards)
        sheet.write('R{0}'.format(row), room.educationTech.whiteboards)
        sheet.write('S{0}'.format(row), room.educationTech.dvd)
        sheet.write('T{0}'.format(row), room.educationTech.blu_ray)
        sheet.write('U{0}'.format(row), room.educationTech.audio)
        sheet.write('V{0}'.format(row), room.educationTech.extro)
        sheet.write('W{0}'.format(row), room.educationTech.doc_cam)
        sheet.write('X{0}'.format(row), room.educationTech.vhs)
        sheet.write('Y{0}'.format(row), room.educationTech.mondopad)
        sheet.write('Z{0}'.format(row), room.educationTech.tech_chart)
        
 
    def write_course_info(self,sheet,row,course):
        # Course Information
        sheet.write('A{0}'.format(row),course.prefix.prefix)
        sheet.write('B{0}'.format(row),course.bannerRef.number)
        sheet.write('C{0}'.format(row),course.bannerRef.ctitle)
        
        #Course Schedule
        if course.schedule is not None:
            self.writeRow(sheet,'D',row,course.schedule.sid)
            self.writeRow(sheet,'E',row,course.schedule.letter)
                 
            schedule_days = ScheduleDays.select().where(ScheduleDays.schedule == course.schedule.sid)
      
            days = ""
            for i in schedule_days:
                days += str(i.day)
          
            if days is None:
                days = "TBD"
            time = days + ': '+ str(course.schedule.startTime) + ' - ' + str(course.schedule.endTime)
            self.writeRow(sheet,'F',row, time)
        #Notes & Capacity
        sheet.write('G{0}'.format(row),course.capacity)
        sheet.write('H{0}'.format(row),course.notes)
        # Room Information
        room_name = ""
        if course.rid:
            room_name = course.rid.building.name + ' ' + course.rid.number
        sheet.write('J{0}'.format(row),room_name)
        sheet.write('I{0}'.format(row),course.section)
        
        
        # Room Information
        room_preferences = RoomPreferences.select().where(RoomPreferences.course == course.cId)
     
        preference_1 = ""
        preference_2 = ""
        preference_3 = ""
        
        if room_preferences: 
            for room_preference in room_preferences:
                if room_preference.pref_1:
                    preference_1 = room_preference.pref_1.building.shortName + " " + room_preference.pref_1.number
                    sheet.write('K{0}'.format(row),preference_1)
                if room_preference.pref_2:
                    preference_2 = room_preference.pref_2.building.shortName + " " + room_preference.pref_2.number
                    sheet.write('L{0}'.format(row),preference_2)
                if room_preference.pref_3:
                    preference_3 = room_preference.pref_3.building.shortName + " " + room_preference.pref_3.number
                    sheet.write('M{0}'.format(row),preference_3)
                  
       
       
        #Instructor Information
        if self.intr_letter == 'N':
            instructors = InstructorCourse.select().where(InstructorCourse.course == course.cId)
        else:
            instructors = InstructorCourse.select().where(InstructorCourse.course == course.course)
       
        colNum = ord(self.intr_letter)
        for  instructor in instructors:
            self.writeRow(sheet,chr(colNum),row,instructor.username.username)
            colNum += 1
            self.writeRow(sheet,chr(colNum),row,instructor.username.bNumber)
            colNum += 1
            
    def write_special_course_info(self,sheet,row,course):
        sheet.write('C{0}'.format(row),course.specialTopicName)
        sheet.write('K{0}'.format(row),course.credits)
        sheet.write('L{0}'.format(row),course.description)
        sheet.write('M{0}'.format(row),course.prereqs)
        sheet.write('N{0}'.format(row),course.majorReqsMet)
        sheet.write('O{0}'.format(row),course.concentrationReqsMet)
        sheet.write('P{0}'.format(row),course.minorReqsMet)
        sheet.write('Q{0}'.format(row),course.perspectivesMet)
        
        
    def increment_rows(self,course):
        self.program_row  += 1
        self.master_row += 1
        if course.crossListed:
            self.cross_row += 1
    
    
    def remove_unavailable_time(self, room):
        ''' This method is to filter through all the schedules possible and remove the times already scheduled and conflicts for each room.
        It takes as input a room object and returns an array with all the times that the room is free '''
        available_times = [] 
        if room.building.name+' '+room.number in self.schedule_to_room:
            # Remove taken times
            for i in self.all_schedules:
                if i not in self.schedule_to_room[room.building.name+' '+room.number]:
                    available_times.append(i)
            # Remove conflicts
            for i in self.schedule_to_room[room.building.name+' '+room.number]:
                for j in cfg['conflicts'][i]:
                    if j in available_times:
                        available_times.remove(j)
        return available_times
            
            
    def get_schedule_days(self, banner_schedule):
        ''' This method gets all the days for each letter in banner_schedule'''
        
        schedule_days = ScheduleDays.select().where(ScheduleDays.schedule == banner_schedule.sid)
        days = []
        for i in schedule_days:
            days.append(i.day)
        days = ''.join(days) 
        return days
        
        
    def make_master_file(self,term):
        #Set excel parameter variables
        filename = "cas-{}-courses.xlsx".format(term.termCode)
        path = getAbsolutePath(cfg['filepath']['tmp'],filename,True)
        workbook = xlsxwriter.Workbook(path)
        workbook.set_properties({
        'title':    'Course Schedule for {}'.format(term.name),
        'author':   'Cas System',
        'comments': 'Created with Python and XlsxWriter'})
        self.master_row = 2
        self.cross_row = 2
        self.room_row = 2
        #Create worksheets and Set Headers
        master_sheet = workbook.add_worksheet('All Courses')
        self.writeHeaders(master_sheet)

        cross_sheet = workbook.add_worksheet('CrossListed')
        self.writeHeaders(cross_sheet)
        
        # Create worksheet for Rooms
        allrooms_sheet = workbook.add_worksheet('All Rooms')
        self.writeAllRoomHeaders(allrooms_sheet)
      
        #Select all the courses 
        courses = Course.select().where(Course.rid != None)
        for course in courses:
            banner_schedule = BannerSchedule.select().where(BannerSchedule.sid == course.schedule).first()
            schedule_days = self.get_schedule_days(banner_schedule)
            
            # Map all the times a room is taken to that particular room 
            if course.rid.building.name+' '+course.rid.number in self.schedule_to_room:
                self.schedule_to_room[course.rid.building.name+' '+course.rid.number].append(course.schedule.sid) 
            else:
                self.schedule_to_room[course.rid.building.name+' '+course.rid.number] = [course.schedule.sid]
        
        all_rooms = Rooms.select().order_by(Rooms.building_id)
        for room in all_rooms:
            available_times = self.remove_unavailable_time(room)
            for i in range(len(available_times)):
                banner_schedule = BannerSchedule.select().where(BannerSchedule.sid == available_times[i]).first()
                available_times[i] = '(' +self.get_schedule_days(banner_schedule) + ': '+ str(banner_schedule.startTime)+ ' - ' + str(banner_schedule.endTime) + ')'
            self.write_all_rooms_info(allrooms_sheet, room, self.room_row, available_times)
            self.room_row += 1
            
        #Loop through programs
        programs = Subject.select().order_by(Subject.prefix)
      
        # Create worksheets and set headers for each program
        for program in programs:
            self.program_row = 2 #reset the program row
            program_sheet = workbook.add_worksheet(program.prefix)
            self.writeHeaders(program_sheet)
                
            #Loop through Courses in that program
            courses = Course.select().where(Course.prefix == program.prefix).where(Course.term == term).order_by(Course.bannerRef)
            
            for course in courses:
             
                sheet_matrix = [[master_sheet,self.master_row],[program_sheet,self.program_row]]
                # print(course.cId, course.schedule.letter, course.prefix.prefix, sheet_matrix)
                if course.crossListed:
                    sheet_matrix.append([cross_sheet,self.cross_row])
                for sheet_list in sheet_matrix:
                    self.write_course_info(sheet_list[0],sheet_list[1],course)
                self.increment_rows(course)
        
        workbook.close()
        return path
        
    def make_cross_listed_file(self, term):
        #set excel parameters variables
        filename = "cas-{}-crossListed.xlsx".format(term.termCode)
        path = getAbsolutePath(cfg['filepath']['tmp'],filename,True)
        workbook = xlsxwriter.Workbook(path)
        workbook.set_properties({
        'title':    'Cross Listed Courses  for {}'.format(term.name),
        'author':   'CAS System',
        'comments': 'Created with Python and XlsxWriter'})

        #Create Master worksheet and Set Headers
        master_sheet = workbook.add_worksheet('CrossListed')
        self.writeHeaders(master_sheet)

        courses = Course.select(
        ).join(BannerCourses, on=(BannerCourses.reFID == Course.bannerRef)
        ).where(Course.crossListed == 1
        ).where(Course.term == term
        ).order_by(BannerCourses.ctitle)

        self.master_row = 2
        for course in courses:
            self.write_course_info(master_sheet,self.master_row,course)
            self.master_row += 1
        workbook.close()
        return path
        
    def make_special_topics_file(self, term):
        #set excel parameters variables
        filename = "cas-{}-specialTopics.xlsx".format(term.termCode)
        path = getAbsolutePath(cfg['filepath']['tmp'],filename,True)
        workbook = xlsxwriter.Workbook(path)
        workbook.set_properties({
        'title': 'Special Topic Courses for {}'.format(term.name),
        'author': 'CAS System',
        'comments': 'Created with Python and XlsxWriter'})
        
        #Create Master worksheet and Set Headers
        master_sheet = workbook.add_worksheet('SpecialTopics')
        self.writeHeaders(master_sheet)
        self.writeSpecialHeaders(master_sheet)            
        courses = SpecialTopicCourse.select().where(SpecialTopicCourse.term == term).where(SpecialTopicCourse.status == 3)
        self.master_row = 2
        for course in courses:
            self.write_course_info(master_sheet,self.master_row,course)
            self.write_special_course_info(master_sheet,self.master_row,course)
            self.master_row += 1
        workbook.close()
        return path