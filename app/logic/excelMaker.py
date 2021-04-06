import xlsxwriter
from app.allImports import *
import sys,os
from app.loadConfig import load_config
from app.models.models import *

def getAbsolutePath(relativePath,filename=None,makeDirs=False):
    '''
    Creates the AbsolutePath based off of the relative path. Also creates the directories in path if they are not found.

    @param {string} relativePath - a string of directories found in config.yaml
    @param {string} filename - the name of the file that should be in that directory
    @return {string} filepath -returns the absolute path of the directory'''

    filepath = os.path.join(sys.path[0],relativePath)
    if makeDirs == True:
        try:
            os.makedirs(filepath)
        except:
            pass
    if filename != None:
        filepath = os.path.join(filepath,filename)
    return filepath

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
        sheet.write('N1','Instructor1')
        sheet.write('O1','Bnumber1')
        sheet.write('P1','Instructor2')
        sheet.write('Q1','Bnumber2')
        sheet.write('R1','Instructor3')
        sheet.write('S1','Bnumber3')
        sheet.write('T1', "Crosslisted with")
        sheet.write('U1', "Off-Campus")
        sheet.write('V1', 'Faculty Load Credit')

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


    def write_course_info(self,sheet,row,course, master_sheet=None):
        # Course Information
        sheet.write('A{0}'.format(row),course.prefix.prefix)
        sheet.write('B{0}'.format(row),course.bannerRef.number)
        sheet.write('C{0}'.format(row),course.bannerRef.ctitle)


        #Course Schedule
        if course.schedule is not None:
            self.writeRow(sheet,'D',row,course.schedule.sid)
            self.writeRow(sheet,'E',row,course.schedule.letter)
            # print('About to get days')

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
            room_number_clean = course.rid.number.split(" - ")[0].strip()
            # print(room_number_clean)
            room_name = course.rid.building.shortName + ' ' + room_number_clean
            sheet.write('J{0}'.format(row),room_name)
            sheet.write('I{0}'.format(row),course.section)


        # Off-campus and Room Information
        if course.offCampusFlag:
            sheet.write('U{0}'.format(row), 'Yes')

        if course.crossListed and course.parentCourse and (sheet is master_sheet): # child crosslisted course
            sheet.write('V{0}'.format(row), "0")
        else:
            sheet.write('V{0}'.format(row), course.faculty_credit)

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

        #write crosslisted with courses for a course if any
        self.writeCrosslistedWith(sheet, row, course)

    def writeCrosslistedWith(self, sheet, row, course):
        try:
            res=[]
            courseTitle = None
            if course.crossListed:
                qs = CrossListed.select().where(CrossListed.courseId == course.cId)
                if qs.exists:
                    for cc in qs:
                        #skip the parent itself
                        if cc.crosslistedCourse.cId != int(course.cId):
                            section = cc.crosslistedCourse.section if cc.crosslistedCourse.section else "None"
                            courseTitle = cc.crosslistedCourse.prefix.prefix + cc.crosslistedCourse.bannerRef.number + "-" + section
                        res.append(courseTitle) if courseTitle else 0
            if res:
                sheet.write('T{0}'.format(row), " , ".join(res))
        except Exception as e:
            print( "Unexpected error:", e)

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
        print(cfg['filepath']['tmp'])
        path = getAbsolutePath(cfg['filepath']['tmp'], filename, True)
        # Delete the file if it already exists
        if os.path.isfile(path):
            os.remove(path)
            print("Deleted ", path)
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
                    self.write_course_info(sheet_list[0],sheet_list[1],course, master_sheet)
                self.increment_rows(course)

        workbook.close()
        return path

    def make_cross_listed_file(self, term):
        #set excel parameters variables
        filename = "cas-{}-crossListed.xlsx".format(term.termCode)
        cfg = load_config()
        path = getAbsolutePath(cfg['filepath']['tmp'],filename,True)
        if os.path.isfile(path):
            os.remove(path)
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
        if os.path.isfile(path):
            os.remove(path)
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
