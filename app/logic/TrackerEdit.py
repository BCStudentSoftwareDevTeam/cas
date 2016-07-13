from app.allImports import *

class TrackerEdit():
  '''@param -data {dict} -Should always come directly from a request.form'''
  def __init__(data):
    '''@param -colorList will contain the order of color names for the tdColors field'''
    self.colorList         = [cfg['columnColor']['default']]
    self.formData          = self.format_data(data)
    self.courseChangeExist = self.check_course_change()
    
  def format_data(self,data):
    '''Purpose: To format the form post data to ensure that all empty 
    strings are replaced by None values. Also, ensures that all the data
    in dataKeys exist
    @param -data {dict} -Should always come directly from a request.form
    -> Author: CDM 20160713'''
    try:
      formData = {}
      dataKeys = cfg['editForm']['dataKeys']
      for key in dataKeys:
          formData[key] = data[key] if data[key] != '' else None
      return formData
    except Exception as e:
        #TODO: Log Error
        return 'Error'
        
  def check_course_change():
    '''Purpose to check if the cid exist in courseChange.
    @param  -cid {number} : Course Identification Number
    @return -changeExist: if course exist return peewee object of course else return None
    Author -> CDM 20160713'''
    try:
      changeExist = CourseChange.get(CourseChange.cId == self.formData['cid'])
      #Set the class variable colorList to the current tdcolors
      self.colorList    = changeExist.tdcolors.split(",")
      return changeExist
    except CourseChange.DoesNotExist:
      return None
    
  
    def create_instructor_list():
      '''Purpose: To create a list of instructor usernames from InstructorsCourse matching self.formData['cid']
        @param -instructors {{PeeWee Object}}
        @return -instrList {{list user's usernames}}
        Author --> CDM 20160713'''
      findCourseInstructors = InstructorCourse.select().where(InstructorCourse.course == self.formData['cid'])
      if instructors:
        instrList = []
        for instructor in instructors:
          instrList.append(instructor.username)
      return innstrList
    
    def add_instructors(usernameList):
      ''' Purpose: To remove the old entries found in InstructorCourseChange if
      there are any then add the new instructors
      Author --> CDM 201607'''
      instructorChange = InstructorCourseChange.select().where(InstructorCourseChange.course == self.formData['cid'])
      if instructorChange:
        InstructorCourseChange.delete().where(InstructorCourseChange.course == self.formData['cid']).execute()
      if usernameList != []:
        for instructor in usernameList:
          addUser = InstructorCourseChange(course=self.formData['cid'], username=instructor)
          addUser.save(force_insert=True)
      return True
    
    def check_instructor_change(newInstructors,courseInstructors): 
      '''Purpose: To record the newInstructors to InstructorCourseChange 
      based off if changes exist. Author --> CDM 20160713
      @param  -newInstructors {{list of strings}}
      @param  -courseInstructors {{list of strings}}
      @return -color{{string}} indicates if a change was made or not
      '''
      if len(newInstructors) == len(courseInstructors):
        duplicates = set(newInstructors) & set(courseInstructors)
        if len(duplicates) == len(newInstructors) and len(duplicates) == len(courseInstructors):
          #No changes where made to the Instructors of this course
          color = cfg['columnColor']['default']
        else:
          color = cfg['columnColor']['update']
          self.add_instructors(newInstructors)
      else:
        color = cfg['columnColor']['update']
        self.add_instructors(newInstructors)
        
    def add_color(self, color, index):
      '''PURPOSE: To either append or change the index of a list to the color
      depending if a course exist in courseChange
      @param -color {string}
      @param -index {integer}'''
      if color == cfg['columnColor']['update']:
        if self.courseChangeExist is None:
            self.colorList.append(color)
        else:
            self.colorList[index] = color
      else:
        if self.courseChangeExist is None:
            self.colorList.append(color)   
          
      def check_course_change():
        '''PURPOSE: To create and use three list (formKeys,courseData,tableLayout) to loop
        through all of the form data related to Course details, then check to see if the
        values are different, and record the color of the result
        @param -formData {dict} -Should always come directly from a request.form 
        Author -> CDM 20160713'''
        #Reduce formKeys to only keys related to courseChange
        formKeys = ['schedule','room','capacity','crossListed','notes']
        course = Course.get(Course.cId == self.formData['cid'])
        #Check null before using forgein key
        courseSchedule = course.schedule.sid if course.schedule is not None else None
        courseRoom  = course.rid.rID if course.rid is not None else None
        #Order the course data to match the order as the formCourseKeys
        courseData  = [courseSchedule,courseRoom,course.capacity,course.crossListed,course.notes]
        #Order the tableLayout keys to match the order as the formCourseKeys
        tableLayout = ['Schedule','Room','Capacity','Cross Listed','Notes']
        
        for index in len(range(formCourseKeys)):
          color = cfg['columnColor']['edit'] if self.formData[formKeys[index]] != courseData[index] else cfg['columnColor']['default']
          self.addColor(color,cfg['tableLayout'][tableLayout[index]])        
      
    def find_change_type():
      '''PURPOSE: To return the correct changeType depending on the current changeType.Author-> CDM 20160713'''
      if self.courseChangeExist is None:
        return cfg['changeType']['update']
      elif self.courseChangeExist.changeType == cfg['changeType']['create'] or self.courseChangeExist.changeType == cfg['changeType']['create/update']:
        return cfg['changeType']['create/update']
      else:
        #TODO: Log the error
        return 'Error'
        
    def record_edit(changeType,username):
      course = Course.get(Course.cId == self.formData['cid'])
      if self.courseChangeExist is not None:
        courseChangeExist.delete_instance()
      edit          = CourseChange(
        cId         = self.formData['cid'],
        prefix      = course.prefix.prefix,
        bannerRef   = course.bannerRef,
        term        = self.formData['term'],
        schedule    = self.formData['schedule'],
        capacity    = self.formData['capacity'],
        notes       = formData['notes'],
        # USERNAME IS PASSED INTO THE METHOD
        lastEditBy  = username,
        changeType  = changeType,
        rid         = self.formData['room'],
        crossListed = self.formData['crossListed'],
        # Turn self.colorList into a comma seperated list
        tdcolors    = ",".join(self.colorList))
      result = edit.save(force_insert=True)
        
    def make_edit(self, newInstructors, username):
      '''Purpose: Acts as a main controller for editing a course 
         @param -data {{form.request}}
         @param -newInstructors {{list of usernames}}
         @param -username {{string}} : is the user making the edit
         Author -> CDM 20160713'''
      #Check if the instructors have changed for the course
      courseInstructors  = self.create_instructor_list()
      color              = self.check_instructor_change(newInstructors,courseInstructors)
      index       = cfg['tableLayout']['Taught By']  
      self.addColor(color,index)     
      #Indicate if a change was made using colorList
      #index is for editing a the current tdColors
      courseEdits = self.check_course_change()
      changeType  = self.find_change_type()
      self.record_edit(changeType,username)
      return True
        
    