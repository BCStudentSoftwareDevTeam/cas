from peewee import *
from playhouse.migrate import *
from app.models import *
# from app.models import Rooms, Building, EducationTech, RoomPreferences, Course, SpecialTopicCourse

from app.loadConfig import *
here = os.path.dirname(__file__)
cfg       = load_config(os.path.join(here, 'app/config.yaml'))
db	  = os.path.join(here,cfg['databases']['dev']) 
print("db", db)
# mainDB    = SqliteDatabase(cfg['databases']['dev'])
my_db    = SqliteDatabase(db,
                          pragmas = ( ('busy_timeout',  100),
                                      ('journal_mode', 'WAL')
                                  ),
                          threadlocals = True
                          )

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta: 
    database = my_db


migrator = SqliteMigrator(my_db)

from app.models import  Rooms

#Create these two tables first 
"""


"""
#TODO: make a function & wrap it up in try/catch statement so it doesn't break when tables are already there/aren't there
# my_db.drop_tables([Rooms, Building, ])

def dropTables():
  tables = [Rooms, Building, EducationTech, RoomPreferences, CourseChange, ScheduleDays, Course]
  for table in tables:
    try:
        my_db.drop_tables([table])
    except:
        pass

# dropTables()

  
class Building(dbModel):
  bID           = PrimaryKeyField()
  name          = CharField()
  shortName     = CharField()
  
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
  
class Rooms(dbModel):
  rID            = PrimaryKeyField()
  building       = ForeignKeyField(Building, related_name='rooms')
  number         = CharField(null=False)
  maxCapacity    = IntegerField(null=False)
  roomType       = CharField(null=False)
  visualAcc     = CharField(null=True)
  audioAcc      = CharField(null=True)
  physicalAcc   = CharField(null=True)
  educationTech = ForeignKeyField(EducationTech, related_name='rooms')
  specializedEq = CharField(null=True)
  specialFeatures = CharField(null=True)
  movableFurniture = BooleanField()
  lastModified = CharField(null=True) #This is implemented for the Building Manager interface. Dont think it will be needed anywhere else/break anything 
  
# class ScheduleDays(dbModel):
#   schedule = ForeignKeyField(BannerSchedule, null = True, related_name='schedule_days')
#   day         = CharField(null=True)
  
# class Course(dbModel):
#   cId               = PrimaryKeyField()
#   prefix            = ForeignKeyField(Subject, related_name='course_prefix') #Removed DO NOT USE THIS! Instead use Course.bannerRef.subject
#   bannerRef         = ForeignKeyField(BannerCourses, related_name='courses_bannerRef')
#   term              = ForeignKeyField(Term, null = False, related_name='course_term')
#   schedule          = ForeignKeyField(BannerSchedule, null = True, related_name='course_schedule')
#   days              = ForeignKeyField(ScheduleDays, null= True, related_name='course_days')
#   capacity          = IntegerField(null = True)
#   specialTopicName  = CharField(null = True)
#   notes             = TextField(null = True)
#   lastEditBy        = CharField(null = True)
#   crossListed       = BooleanField()
#   rid               = ForeignKeyField(Rooms, null = True, related_name='courses_rid')
#   section           = TextField(null = True)
#   prereq            = CharField(null = True) 
  
# class RoomPreferences(dbModel):
#   rpID           = PrimaryKeyField()
#   course        = ForeignKeyField(Course, related_name='courses')
#   pref_1        = ForeignKeyField(Rooms, related_name='preference_1', null=True)
#   pref_2        = ForeignKeyField(Rooms, related_name='preference_2', null=True)
#   pref_3        = ForeignKeyField(Rooms, related_name='preference_3', null=True) #We are making sure we have all the preferences jotted down.
#   notes         = CharField(null=True)
#   any_Choice    = CharField(null=True)
#   none_Choice   = CharField(null=True)
#   none_Reason   = CharField(null=True)
#   initial_Preference = CharField(null=True, default = 1)
#   priority = IntegerField(default = 6)  

class CourseChange(dbModel):
  cId               = IntegerField(primary_key = True)
  prefix            = ForeignKeyField(Subject, related_name='courseChange_prefix')
  bannerRef         = ForeignKeyField(BannerCourses, related_name='courseChange_bannerRef')
  term              = ForeignKeyField(Term, null = False, related_name='courseChange_term')
  schedule          = ForeignKeyField(BannerSchedule, null = True, related_name='courseChange_schedule')
  capacity          = IntegerField(null = True)
  specialTopicName  = CharField(null = True)
  notes             = TextField(null = True)
  lastEditBy        = CharField(null = True)
  changeType        = CharField(null = True)
  verified          = BooleanField(default = False)
  crossListed       = BooleanField()
  rid               = ForeignKeyField(Rooms, null = True, related_name='courseChange_rid')
  tdcolors          = CharField(null = False)
  section           = TextField(null = True)


#my_db.create_tables([RoomPreferences, EducationTech, Building, Rooms, Course, CourseChange, ScheduleDays])

#Add these columns to existing tables in the production
#Building column add

# migrate(
#     migrator.add_column('Building', 'shortName', TextField(default='')),
# )

# #Rooms Column Add
# migrate(
#     #migrator.add_column('Rooms', 'maxCapacity', IntegerField(null=False)),  #update already exists
#     migrator.add_column('Rooms', 'visualAcc', CharField(null=True)),
#     migrator.add_column('Rooms', 'audioAcc', CharField(null=True)),
#     migrator.add_column('Rooms', 'physicalAcc',CharField(null=True)),
#     migrator.add_column('Rooms', 'educationTech_id', ForeignKeyField(EducationTech, to_field = EducationTech.eId, related_name='rooms', null=True)),
#     migrator.add_column('Rooms', 'specializedEq', CharField(null=True)),
#     migrator.add_column('Rooms', 'specialFeatures', CharField(null=True)),
#     migrator.add_column('Rooms', 'movableFurniture', BooleanField(default=False)),
#     )
  
  
# migrate(
#   migrator.drop_column("Course", "rid"),
#   migrator.add_column("Course", "rid_id", ForeignKeyField(Rooms, to_field = Rooms.rID, null = True, related_name='courses_rid'))
#   )
# my_db.drop_tables([ScheduleDays])

# class ScheduleDays(dbModel):
#   sdID = PrimaryKeyField()
#   schedule = ForeignKeyField(BannerSchedule, null = True, related_name='course_schedule_days')
#   day         = CharField(null=True)
  
  
# my_db.create_tables([ScheduleDays])
migrate(
    migrator.add_column('Rooms', 'lastModified', CharField(null=True)),
    # migrator.add_column('RoomPreferences', 'priority', IntegerField(default=6)),
    # migrator.add_column('Course', 'days_id', ForeignKeyField(ScheduleDays, to_field = ScheduleDays.sdID , null = True, related_name='course_days'))
     
    # migrator.drop_not_null('CourseChange','rid')
)


# q = Course.select()
# for course in q:
#   course.rid = None
#   course.save()
  
  
# q = SpecialTopicCourse.select()
# for course in q:
#   course.rid = None
#   course.save()
  
