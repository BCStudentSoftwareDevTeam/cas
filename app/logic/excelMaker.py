import xlsxwriter
from app.allImports import *
import sys,os

class ExcelMaker:
    def __init__(self):
        self.program_row = 2
        self.cross_row   = 2
        self.master_row  = 2
        self.intr_letter = ''

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
       
        
    def write_course_info(self,sheet,row,course):
        # Course Information
        sheet.write('A{0}'.format(row),course.prefix.prefix)
        sheet.write('B{0}'.format(row),course.bannerRef.number)
        sheet.write('C{0}'.format(row),course.bannerRef.ctitle)
        #Course Schedule
        # print('About to enter course.schedule')
        if course.schedule is not None:
            self.writeRow(sheet,'D',row,course.schedule.sid)
            self.writeRow(sheet,'E',row,course.schedule.letter)
            # print('About to get days')
            schedule_days = ScheduleDays.select().where(ScheduleDays.schedule == course.schedule.sid)
            print (schedule_days, "ScheduleDays")
            days = ""
            for i in schedule_days:
                days += schedule_days.day
            
            print("Days", days)
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
        
        room_preferences = RoomPreferences.select().where(RoomPreferences.course == course.cId)
     
        preference_1 = ""
        preference_2 = ""
        preference_3 = ""
        
        if room_preferences: 
            for room_preference in room_preferences:
                preference_1 = room_preference.pref_1.building.shortName + " " + room_preference.pref_1.number
                preference_2 = room_preference.pref_2.building.shortName + " " + room_preference.pref_2.number
                preference_3 = room_preference.pref_3.building.shortName + " " + room_preference.pref_3.number
                print('Course', room_preference.course.cId, room_preference.pref_1.number, room_preference.pref_2.number, room_preference.pref_3.number)
            
                sheet.write('K{0}'.format(row),preference_1)
                sheet.write('L{0}'.format(row),preference_2)
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

    def make_master_file(self,term):
        #Set excel parameter variables
        filename = "cas-{}-courses.xlsx".format(term.termCode)
        path = getAbsolutePath(cfg['filepath']['tmp'],filename,True)
        workbook = xlsxwriter.Workbook(path)
        workbook.set_properties({
        'title':    'Course Schedule for {}'.format(term.name),
        'author':   'Cas System',
        'comments': 'Created with Python and XlsxWriter'})
        self.mater_row = 2
        self.cross_row = 2
        #Create worksheets and Set Headers
        master_sheet = workbook.add_worksheet('All Courses')
        self.writeHeaders(master_sheet)

        cross_sheet = workbook.add_worksheet('CrossListed')
        self.writeHeaders(cross_sheet)

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