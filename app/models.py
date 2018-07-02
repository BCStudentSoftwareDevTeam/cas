from peewee import *
import os

# Create a database
from app.loadConfig import *
here = os.path.dirname(__file__)
cfg       = load_config(os.path.join(here, 'config.yaml'))
db	  = os.path.join(here,'../',cfg['databases']['dev']) 
# mainDB    = SqliteDatabase(cfg['databases']['dev'])
mainDB    = SqliteDatabase(db,
                          pragmas = ( ('busy_timeout',  100),
                                      ('journal_mode', 'WAL')
                                  ),
                          threadlocals = True
                          )

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta: 
    database = mainDB
    
"""
When adding new tables to the DB, add a new class here 
Also, you must add the table to the config.yaml file

Example of creating a Table

class tableName (dbModel):
  column1       = PrimaryKeyField()
  column2       = TextField()
  column3       = IntegerField()

For more information look at peewee documentation
"""


#MODELS WITHOUT A FOREIGN KEY
class Division(dbModel):
  dID           = PrimaryKeyField()
  name          = CharField()
  
  def __str__(self):
    return str(self.name)
  
class BannerSchedule(dbModel):
  letter        = CharField()
  startTime     = TimeField(null = True)
  endTime       = TimeField(null = True)
  sid           = CharField(primary_key = True)
  order         = IntegerField(unique = True)
  
  def __str__(self):
    return self.letter
    
class ScheduleDays(dbModel):
  schedule = ForeignKeyField(BannerSchedule, null = True, related_name='days')
  day         = CharField(null=True)

"""
Possible States:
    0 - Open - open for all but not tracked
    1 - tracked - tracking but not open
    2 - locked - not open and not tracked
"""
class State(dbModel):#added
  stateID         =PrimaryKeyField()
  state_name      =CharField(null=False)
  state_order     = IntegerField(null=False)
  
  
  def __str__(self):
    return self.state_name


class Term(dbModel):
  termCode          = IntegerField(primary_key = True)     #This line will result in an autoincremented number, which will not allow us to enter in our own code
  semester          = CharField(null = True)
  year              = IntegerField(null = True)
  name              = CharField()
  state             = ForeignKeyField(State, null=False, related_name="terms")# should we make change on this one bc we used foreignKey for the state instead of IntegerField 
 
  
  def __str__(self):
    return self.name
    
    


  
  
class Building(dbModel):
  bID           = PrimaryKeyField()
  name          = CharField()
  shortName     = CharField()
  
  
  def __str__(self):
    return self.name 
  



class Rooms(dbModel):
  rID            = PrimaryKeyField()
  building       = ForeignKeyField(Building, related_name='rooms')
  number         = CharField(null=False)
  maxCapacity    = IntegerField(null=False)
  roomType       = CharField(null=False)
  visualAcc     = CharField(null=True)
  audioAcc      = CharField(null=True)
  physicalAcc   = CharField(null=True)
 #educationTech        = ForeignKeyField(educationTech, related_name='rooms')
  specializedEq = CharField(null=True)
  specialFeatures = CharField(null=True)
  movableFurniture = BooleanField(default=False)
  
  
class RoomPreferences(dbModel):
  rpID           = PrimaryKeyField()
  course        = ForeignKeyField(Rooms, related_name='courses')
  pref_1        = ForeignKeyField(Rooms, related_name='preference_1')
  pref_2        = ForeignKeyField(Rooms, related_name='preference_2')
  pref_3        = ForeignKeyField(Rooms, related_name='preference_3') #We are making sure we have all the preferences jotted down.
  notes         = CharField(null=True)
  any_Choice    = CharField(null=True)
  none_Choice   = CharField(null=True)
  none_Reason   = CharField(null=True)
  
  
  
#added
class Building_User(dbModel):
  buID = ForeignKeyField(Rooms, null=False)
  building = CharField(null=False)
  username = TextField()
#added
  
#MODELS WITH A FOREIGN KEY
class Program(dbModel):
  pID           = PrimaryKeyField()# Should get rid of this bc it is not included in the database design 
  name          = CharField()
  division      = ForeignKeyField(Division, related_name='programs')

  
  def __str__(self):
    return str(self.name)
    

    
class Subject(dbModel):
  prefix        = CharField(primary_key=True)
  pid           = ForeignKeyField(Program, related_name='subjects')
  webname       = TextField()
  
  def __str__(self):
    return self.prefix

class User(dbModel):
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
  
class BannerCourses(dbModel):
  reFID         = PrimaryKeyField()
  subject       = ForeignKeyField(Subject)
  number        = CharField(null = False)
  section       = CharField(null = True)
  ctitle        = CharField(null = False)
  is_active     = BooleanField()
  
  def __str__(self):
    return '{0} {1}'.format(self.subject, self.number)

class Course(dbModel):
  cId               = PrimaryKeyField()
  prefix            = ForeignKeyField(Subject)
  bannerRef         = ForeignKeyField(BannerCourses, related_name='courses')
  term              = ForeignKeyField(Term, null = False)
  schedule          = ForeignKeyField(BannerSchedule, null = True)
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

class SpecialTopicCourse(dbModel):
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

class ProgramChair(dbModel):
  username     = ForeignKeyField(User)
  pid          = ForeignKeyField(Program)

class DivisionChair(dbModel):
  username     = ForeignKeyField(User)
  did          = ForeignKeyField(Division)
  
# class BuildingManager(dbModel):
#   username     = ForeignKeyField(User)
#   bmid         = ForeignKeyField(Building)

class InstructorCourse(dbModel):
  username     = ForeignKeyField(User, related_name='instructor_courses')
  course       = ForeignKeyField(Course, related_name='instructors_course')
  
class InstructorSTCourse(dbModel):
  username     = ForeignKeyField(User, related_name='instructor_stcourses')
  course       = ForeignKeyField(SpecialTopicCourse, related_name='instructors_stcourse')
  
# class InstructorSTCourse(dbModel):  ###There is a special topics table above. Dont know why this was included
#   username     = ForeignKeyField(User)
#   course       = ForeignKeyField(SpecialTopicCourse)
  
class Deadline(dbModel):
  description  = TextField()
  date         = DateField()
  
class CourseChange(dbModel):
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
  rid               = ForeignKeyField(Rooms, null = False)
  tdcolors          = CharField(null = False)
  section           = TextField(null = True)
  
class InstructorCourseChange(dbModel):
  username     = ForeignKeyField(User)
  course       = ForeignKeyField(CourseChange)
  
class CoursesInBanner(dbModel):
  CIBID        = PrimaryKeyField()
  bannerRef    = ForeignKeyField(BannerCourses)
  instructor   = ForeignKeyField(User, null=True)

  
#Begin education tech class
class EducationTech(dbModel):
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

# #Begin crosslisted table  #Jolena asked for an extra step in the new crosslisting courses process.
# class newcrosslisted (dbModel): 
#   clId                 = PrimaryKeyField()
#   created_course_1     = ForeignKeyField(Course) #Created by one of the program chairs
#   verified_course_2    = ForeignKeyField(Course) #Verified with the other program chair(s)
#   verified             = BooleanField() #Verified? = yes or no
# We are not sure why it is not running when we have these uncommented
# it says newcrosslisted is already in use by another foreign key
  

