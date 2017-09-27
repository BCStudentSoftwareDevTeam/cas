import xlsxwriter
from app.allImports import *
import sys,os

class ExcelMaker:
    def __init__(self):
        self.program_row = 2
        self.cross_row   = 2
        self.master_row  = 2
        
    def writeHeaders(self,sheet):
        sheet.write('A1','Prefix')
        sheet.write('B1','Number')
        sheet.write('C1','Title')
        sheet.write('D1','Block ID')
        sheet.write('E1','Block')
        sheet.write('F1', 'Capacity')
        sheet.write('G1', 'Notes')
        
    def writeRow(self,sheet,column,row,value):
        sheet.write('{0}{1}'.format(column,row), value)
        
    def make_master_file(self,term):
        #Set excel parameter variables
        filename = "cas-{}-courses.xlsx".format(term.termCode)
        path = getAbsolutePath(cfg['filepath']['tmp'],filename,True)
        workbook = xlsxwriter.Workbook(path)
        workbook.set_properties({
        'title':    'Course Schedule for {}'.format(term.name),
        'author':   'Cas System',
        'comments': 'Created with Python and XlsxWriter'})
        
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
                    sheet = sheet_list[0]
                    row   = sheet_list[1]
                    self.writeRow(sheet,'A',row,course.prefix.prefix)
                    self.writeRow(sheet,'B',row,course.bannerRef.number)
                    self.writeRow(sheet,'C',row,course.bannerRef.ctitle)
                    if course.schedule is not None:
                        self.writeRow(sheet,'D',row,course.schedule.sid)
                        self.writeRow(sheet,'E',row,course.schedule.letter)
                    self.writeRow(sheet,'F',row,course.capacity)
                    self.writeRow(sheet,'G',row,course.notes)
                    
                    #Handle Instructors
                    instructors = InstructorCourse.select().where(InstructorCourse.course == course.cId)
                    colNum = ord('H')
                    for instructor in instructors:
                        self.writeRow(sheet,chr(colNum),row,instructor.username.username)
                        colNum += 1
                #Increment Rows
                self.program_row  += 1
                self.master_row += 1
                if course.crossListed:
                    self.cross_row += 1
                    
        workbook.close()
        return path