from app.loadConfig import *
from peewee import *
import os
import datetime


def getDB():
    dir_name  = os.path.dirname(__file__) # Return the directory name of pathname _file_
    cfg       = load_config(os.path.join(dir_name, 'app/dbConfig.yaml'))
    db_name   = cfg['db']['db_name']
    host      = cfg['db']['host']
    username  = cfg['db']['username']
    password  = cfg['db']['password']
    theDB     = MySQLDatabase ( db_name, host = host, user = username, passwd = password)

    return theDB


mainDB = getDB()


class baseModel(Model):
  class Meta:
    database = mainDB

# Tables without foreign keys 
class Division(baseModel):
  dID           = PrimaryKeyField()
  name          = CharField()
  
  def __str__(self):
    return str(self.name)
  
class BannerSchedule(baseModel):
  letter        = CharField()
  startTime     = TimeField(null = True)
  endTime       = DateTimeField(null = True)
  sid           = CharField(primary_key = True)
  order         = IntegerField(unique = True)
  
  def __str__(self):
    return self.letter

class TermStates(baseModel):
  csID          = PrimaryKeyField()
  number        = IntegerField()
  name          = CharField()
  order         = IntegerField()
  display_name  = CharField()
  
class Building(baseModel):
  bID               = PrimaryKeyField()
  name              = CharField()
  shortName         = CharField()

  def __repr__(self):
    return self.name 

class EducationTech(baseModel):
  eId                  = PrimaryKeyField()
  projector            = IntegerField(default = 0) #each room has a default of 0 projectors
  smartboards          = IntegerField(default = 0) #default of 0 in room
  instructor_computers = IntegerField(default = 0) #default of 0 no. of instructor computers to zero
  podium               = IntegerField(default = 0) #default of 0 no. of podium
  student_workspace    = IntegerField(default = 0) #default of 0 no. f student workspace
  chalkboards          = IntegerField(default = 0) #default of 0 no. chalkboards
  whiteboards          = IntegerField(default = 0) #default of 0 no. of whiteboards
  dvd                  = BooleanField()  #has or doesnt have dvd player
  blu_ray              = BooleanField()  #has or doesnt have blu ray player
  audio                = BooleanField()  #has or doesnt have audio hookup
  extro                = BooleanField()
  doc_cam              = BooleanField()
  vhs                  = BooleanField()
  mondopad             = BooleanField()
  tech_chart           = BooleanField()

  def __repr__(self):
    return str(self.eId)

class Deadline(baseModel):
  description  = TextField()
  date         = DateField()
      
# Tables with foreign keys

class ScheduleDays(baseModel):
  schedule      = ForeignKeyField(BannerSchedule, null = True, related_name='days')
  day           = CharField(null=True)

class Term(baseModel):
  termCode          = IntegerField(primary_key = True)     #This line will result in an autoincremented number, which will not allow us to enter in our own code
  semester          = CharField(null = True)
  year              = IntegerField(null = True)
  name              = CharField()
  state             = IntegerField(null = False)
  term_state        = ForeignKeyField(TermStates, null = True, related_name = "states")
  editable          = BooleanField(null = False, default = True)
  

    
class Rooms(baseModel):
  rID              = PrimaryKeyField()
  building         = ForeignKeyField(Building, related_name='rooms')
  number           = CharField(null=False)
  maxCapacity      = IntegerField(null=False)
  roomType         = CharField(null=False)
  visualAcc        = CharField(null=True)
  audioAcc         = CharField(null=True)
  physicalAcc      = CharField(null=True)
  educationTech    = ForeignKeyField(EducationTech, related_name='rooms')
  specializedEq    = CharField(null=True)
  specialFeatures  = CharField(null=True)
  movableFurniture = BooleanField()
  
 
class Program(baseModel):
  pID               = PrimaryKeyField()
  name              = CharField()
  division          = ForeignKeyField(Division, related_name='programs')

  
  def __str__(self):
    return str(self.name)
    
class Subject(baseModel):
  prefix        = CharField(primary_key=True)
  pid           = ForeignKeyField(Program, related_name='subjects')
  webname       = TextField()
  
  def __str__(self):
    return self.prefix

class User(baseModel):
  username     = CharField(primary_key=True)
  firstName    = CharField()
  lastName     = CharField()
  email        = CharField()
  isAdmin      = BooleanField()
  lastVisited  = ForeignKeyField(Subject, null=True)
  bNumber      = CharField(null = True)
  
  def is_active(self):
      """All user will be active"""
      return True
  
  
  def get_id(self):
      return str(self.username)
      
  def is_authenticated(self):
      """Return True if the user is authenticated"""
      return True
      
  def is_anonymous(self):
      return False
      
  def __repr__(self):
    return '{0} {1}'.format(self.firstName, self.lastName)
  
  def __str__(self):
    return self.username
  
class BannerCourses(baseModel):
  reFID         = PrimaryKeyField()
  subject       = ForeignKeyField(Subject)
  number        = CharField(null = False)
  section       = CharField(null = True)
  ctitle        = CharField(null = False)
  is_active     = BooleanField()
  
  def __str__(self):
    return '{0} {1}'.format(self.subject, self.number)

class Course(baseModel):
  cId               = PrimaryKeyField()
  prefix            = ForeignKeyField(Subject) #Removed DO NOT USE THIS! Instead use Course.bannerRef.subject
  bannerRef         = ForeignKeyField(BannerCourses, related_name='courses')
  term              = ForeignKeyField(Term, null = False)
  schedule          = ForeignKeyField(BannerSchedule, null = True)
  # days            = ForeignKeyField(ScheduleDays, null= True)
  capacity          = IntegerField(null = True)
  specialTopicName  = CharField(null = True)
  notes             = TextField(null = True)
  lastEditBy        = CharField(null = True)
  crossListed       = BooleanField()
  rid               = ForeignKeyField(Rooms, null = True, related_name='courses_rid')
  section           = TextField(null = True)
  prereq            = CharField(null = True) 
  def __str__(self):
    return '{0} {1} {2}'.format(self.bannerRef.subject, self.bannerRef.number, self.bannerRef.ctitle)

class SpecialTopicCourse(baseModel):
  stId                 = PrimaryKeyField()
  prefix               = ForeignKeyField(Subject)
  bannerRef            = ForeignKeyField(BannerCourses)
  term                 = ForeignKeyField(Term, null = False)
  schedule             = ForeignKeyField(BannerSchedule, null = True)
  capacity             = IntegerField(null = True)
  specialTopicName     = CharField(null = True)
  notes                = TextField(null = True)
  lastEditBy           = CharField(null = True)
  submitBy             = CharField(null = True)
  crossListed          = BooleanField() 
  rid                  = ForeignKeyField(Rooms, null = True)
  status               = IntegerField(default = 0) # 0: Saved, 1: Submitted, 2: Sent to Dean, 3: Approved, 4: Denied
  credits              = CharField(default = "1.000")
  description          = TextField(null = True)
  prereqs              = TextField(null = True)
  majorReqsMet         = TextField(null = True)
  concentrationReqsMet = TextField(null = True)
  minorReqsMet         = TextField(null = True)
  perspectivesMet      = TextField(null = True)
  section              = TextField(null = True)
  def __str__(self):
      return '{0} {1} {2}'.format(self.bannerRef.subject, self.bannerRef.number, self.bannerRef.ctitle)

class ProgramChair(baseModel):
  username     = ForeignKeyField(User)
  pid          = ForeignKeyField(Program)

class DivisionChair(baseModel):
  username     = ForeignKeyField(User)
  did          = ForeignKeyField(Division)
  
class BuildingManager(baseModel):
  username     = ForeignKeyField(User)
  bmid         = ForeignKeyField(Building)

class InstructorCourse(baseModel):
  username     = ForeignKeyField(User, related_name='instructor_courses')
  course       = ForeignKeyField(Course, related_name='instructors_course')
  
class InstructorSTCourse(baseModel):
  username     = ForeignKeyField(User, related_name='instructor_stcourses')
  course       = ForeignKeyField(SpecialTopicCourse, related_name='instructors_stcourse')
  

class CourseChange(baseModel):
  cId               = IntegerField(primary_key = True)
  prefix            = ForeignKeyField(Subject)
  bannerRef         = ForeignKeyField(BannerCourses)
  term              = ForeignKeyField(Term, null = False)
  schedule          = ForeignKeyField(BannerSchedule, null = True)
  capacity          = IntegerField(null = True)
  specialTopicName  = CharField(null = True)
  notes             = TextField(null = True)
  lastEditBy        = CharField(null = True)
  changeType        = CharField(null = True)
  verified          = BooleanField(default = False)
  crossListed       = BooleanField()
  rid               = ForeignKeyField(Rooms, null = True)
  tdcolors          = CharField(null = False)
  section           = TextField(null = True)
  
class InstructorCourseChange(baseModel):
  username     = ForeignKeyField(User)
  course       = ForeignKeyField(CourseChange)
  
class CoursesInBanner(baseModel):
  CIBID        = PrimaryKeyField()
  bannerRef    = ForeignKeyField(BannerCourses)
  instructor   = ForeignKeyField(User, null=True)
  
class RoomPreferences(baseModel):
  rpID               = PrimaryKeyField()
  course             = ForeignKeyField(Course, related_name='courses')
  pref_1             = ForeignKeyField(Rooms, related_name='preference_1', null=True)
  pref_2             = ForeignKeyField(Rooms, related_name='preference_2', null=True)
  pref_3             = ForeignKeyField(Rooms, related_name='preference_3', null=True) #We are making sure we have all the preferences jotted down.
  notes              = CharField(null=True)
  any_Choice         = CharField(null=True)
  none_Choice        = CharField(null=True)
  none_Reason        = CharField(null=True)
  initial_Preference = CharField(null=True, default = 1)
  priority           = IntegerField(default = 6)  

mainDB.create_tables([Division, BannerSchedule, ScheduleDays, TermStates, Term, 
                      Building, EducationTech, Rooms, Program, Subject, User, 
                      BannerCourses, Course, SpecialTopicCourse, ProgramChair, 
                      DivisionChair, BuildingManager, InstructorCourse, InstructorSTCourse, 
                      Deadline, CourseChange, InstructorCourseChange, CoursesInBanner, RoomPreferences])







