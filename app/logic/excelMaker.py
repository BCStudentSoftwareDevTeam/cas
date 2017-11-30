import xlsxwriter
from app.allImports import *
import sys,os

class ExcelMaker:
    def __init__(self):
        self.program_row = 2
        self.cross_row   = 2
        self.master_row  = 2

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
        sheet.write('I1', 'Room Preference')
        sheet.write('J1','Instructors')
        sheet.write('K1','Section')



    def write_course_info(self,sheet,row,course):
        # Course Information
        sheet.write('A{0}'.format(row),course.prefix.prefix)
        sheet.write('B{0}'.format(row),course.bannerRef.number)
        sheet.write('C{0}'.format(row),course.bannerRef.ctitle)
        #Course Schedule
        if course.schedule is not None:
            self.writeRow(sheet,'D',row,course.schedule.sid)
            self.writeRow(sheet,'E',row,course.schedule.letter)
            days = course.schedule.days.get().day
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
        sheet.write('I{0}'.format(row),room_name)
        #Instructor Information
        instructors = InstructorCourse.select().where(InstructorCourse.course == course.cId)
        colNum = ord('J')
        for  instructor in instructors:
            self.writeRow(sheet,chr(colNum),row,instructor.username.username)
            colNum += 1
            self.writeRow(sheet,chr(colNum),row,instructor.username.bNumber)
            colNum += 1
        sheet.write('K{0}'.format(row),course.section)

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
        for program in programs:
            self.program_row = 2 #reset the program row
            program_sheet = workbook.add_worksheet(program.prefix)
            self.writeHeaders(program_sheet)

            #Loop through Courses in that program
            courses = Course.select().where(Course.prefix == program.prefix).where(Course.term == term).order_by(Course.bannerRef)
            for course in courses:
                sheet_matrix = [[master_sheet,self.master_row],[program_sheet,self.program_row]]
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
        'author':   'Cas System',
        'comments': 'Created with Python and XlsxWriter'})

        #Create Master worksheet and Set Headers
        master_sheet = workbook.add_worksheet('CrossListed')
        self.writeHeaders(master_sheet)

        courses = Course.select().where(Course.term == term).where(Course.crossListed == 1)
        self.master_row = 2
        for course in courses:
            self.write_course_info(master_sheet,self.master_row,course)
            self.master_row += 1
        workbook.close()
        return path
