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

class Term(dbModel):
  termCode          = IntegerField(primary_key = True)     #This line will result in an autoincremented number, which will not allow us to enter in our own code
  semester          = CharField(null = True)
  year              = IntegerField(null = True)
  name              = CharField()
  state             = IntegerField(default=0)
  
  def __str__(self):
    return self.name
  
class Building(dbModel):
  bID           = PrimaryKeyField()
  name          = CharField()
  

class Rooms(dbModel):
  rID            = PrimaryKeyField()
  building       = ForeignKeyField(Building, related_name='rooms')
  number         = CharField(null=False)
  maxCapacity    = IntegerField(null=True)
  roomType       = CharField(null=False)
  
#MODELS WITH A FOREIGN KEY
class Program(dbModel):
  pID           = PrimaryKeyField()
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
    return '{0} {1}'.format(self.firstname, self.lastname)
  
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
  rid               = ForeignKeyField(Rooms, null = True)
  
  def __str__(self):
    return '{0} {1} {2}'.format(self.bannerRef.subject, self.bannerRef.number, self.bannerRef.ctitle)

class ProgramChair(dbModel):
  username     = ForeignKeyField(User)
  pid          = ForeignKeyField(Program)

class DivisionChair(dbModel):
  username     = ForeignKeyField(User)
  did          = ForeignKeyField(Division)

class InstructorCourse(dbModel):
  username     = ForeignKeyField(User, related_name='instructor_courses')
  course       = ForeignKeyField(Course, related_name='instructors_course')
  
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
  rid               = ForeignKeyField(Rooms, null = True)
  tdcolors          = CharField(null = False)
  
class InstructorCourseChange(dbModel):
  username     = ForeignKeyField(User)
  course       = ForeignKeyField(CourseChange)
  
class CoursesInBanner(dbModel):
  CIBID        = PrimaryKeyField()
  bannerRef    = ForeignKeyField(BannerCourses)
  instructor   = ForeignKeyField(User, null=True)

