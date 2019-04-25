from peewee import *
from playhouse.migrate import *
from app.models import *
from app.loadConfig import *

here = os.path.dirname(__file__)
cfg       = load_config(os.path.join(here, 'app/config.yaml'))
db	  = os.path.join(here,cfg['databases']['dev']) 
# print("here", here)
# print('Test', cfg['databases'])
# print("db", db)
# mainDB    = SqliteDatabase(cfg['databases']['dev'])
# my_db    = SqliteDatabase(db,
#                           pragmas = ( ('busy_timeout',  100),
#                                       ('journal_mode', 'WAL')
#                                   ),
#                           threadlocals = True
#                           )

mainDB     = MySQLDatabase ( db_name, host = host, user = username, passwd = password)


# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta: 
    database = mainDB


migrator = MySQLMigrator(mainDB)

# my_db.drop_tables([RoomPreferences])


#TODO: make a function & wrap it up in try/catch statement so it doesn't break when tables are already there/aren't there
# def dropTables():
#   tables = [Rooms, Building, EducationTech, RoomPreferences, CourseChange, ScheduleDays, Course]
#   for table in tables:
#     try:
#         my_db.drop_tables([table])
#     except:
#         pass

# dropTables()


  
# class Building(dbModel):
#   bID           = PrimaryKeyField()
#   name          = CharField()
#   shortName     = CharField()
  

# class EducationTech(dbModel):
#   eId                  = PrimaryKeyField()
#   projector            = IntegerField(default = 0) #each room has a default of 0 projectors
#   smartboards          = IntegerField(default = 0) #default of 0 in room
#   instructor_computers = IntegerField(default = 0) #default of 0 no. of instructor computers to zero
#   podium               = IntegerField(default = 0) #default of 0 no. of podium
#   student_workspace    = IntegerField(default = 0) #default of 0 no. f student workspace
#   chalkboards          = IntegerField(default = 0) #default of 0 no. chalkboards
#   whiteboards          = IntegerField(default = 0) #default of 0 no. of whiteboards
#   dvd                  = BooleanField()  #has or doesnt have dvd player
#   blu_ray              = BooleanField()  #has or doesnt have blu ray player
#   audio                = BooleanField()  #has or doesnt have audio hookup
#   extro                = BooleanField()
#   doc_cam              = BooleanField()
#   vhs                  = BooleanField()
#   mondopad             = BooleanField()
#   tech_chart           = BooleanField()
  
# class Rooms(dbModel):
#   rID            = PrimaryKeyField()
#   building       = ForeignKeyField(Building, related_name='rooms')
#   number         = CharField(null=False)
#   maxCapacity    = IntegerField(null=False)
#   roomType       = CharField(null=False)
#   visualAcc     = CharField(null=True)
#   audioAcc      = CharField(null=True)
#   physicalAcc   = CharField(null=True)
#   educationTech = ForeignKeyField(EducationTech, related_name='rooms')
#   specializedEq = CharField(null=True)
#   specialFeatures = CharField(null=True)
#   movableFurniture = BooleanField()
#   lastModified = CharField(null=True) #This is implemented for the Building Manager interface. Dont think it will be needed anywhere else/break anything 
  

# class ScheduleDays(dbModel):
#   schedule = ForeignKeyField(BannerSchedule, null = True, related_name='schedule_days')
#   day         = CharField(null=True)
  
# class Course(dbModel):
#   cId               = PrimaryKeyField()
#   prefix            = ForeignKeyField(Subject, related_name='course_prefix') #Removed DO NOT USE THIS! Instead use Course.bannerRef.subject
#   bannerRef         = ForeignKeyField(BannerCourses, related_name='courses_bannerRef')
#   term              = ForeignKeyField(Term, null = False, related_name='course_term')
#   schedule          = ForeignKeyField(BannerSchedule, null = True, related_name='course_schedule')
#   # days              = ForeignKeyField(ScheduleDays, null= True, related_name='course_days')
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


# class EducationTech(dbModel):
#   eId                  = PrimaryKeyField()
#   projector            = IntegerField(default = 0) #each room has a default of 0 projectors
#   smartboards          = IntegerField(default = 0) #default of 0 in room
#   instructor_computers = IntegerField(default = 0) #default of 0 no. of instructor computers to zero
#   podium               = IntegerField(default = 0) #default of 0 no. of podium
#   student_workspace    = IntegerField(default = 0) #default of 0 no. f student workspace
#   chalkboards          = IntegerField(default = 0) #default of 0 no. chalkboards
#   whiteboards          = IntegerField(default = 0) #default of 0 no. of whiteboards
#   dvd                  = BooleanField()  #has or doesnt have dvd player
#   blu_ray              = BooleanField()  #has or doesnt have blu ray player
#   audio                = BooleanField()  #has or doesnt have audio hookup
#   extro                = BooleanField()
#   doc_cam              = BooleanField()
#   vhs                  = BooleanField()
#   mondopad             = BooleanField()
#   tech_chart           = BooleanField()


# class Building(dbModel):
#   bID           = PrimaryKeyField()
#   name          = CharField()
#   shortName     = CharField()



class TermStates(dbModel):
   csID          = PrimaryKeyField()
   number        = IntegerField(null = False)
   name          = CharField(null = False)
   order         = IntegerField(null = False)
   display_name  = CharField(null = False)
   editable          = BooleanField(null = False, default = True)
# my_db.drop_tables([TermStates])
# my_db.create_tables([RoomPreferences, EducationTech, Building, Rooms,TermStates])

# my_db.create_tables([TermStates])

# To add states to Temstates table
# state_1 = TermStates(number = 0, order = 0, name = "term_created", display_name = "Term Created").save()
# state_2 = TermStates(number = 1, order = 1, name = "schedule_opened", display_name = "Open Scheduling").save()
# state_3 = TermStates(number = 2, order = 2, name = "schedule_closed", display_name = "Lock Scheduling").save()
# state_3 = TermStates(number = 3, order = 3, name = "roomprefrences_opened", display_name = "Open Room Preferences").save()
# state_4 = TermStates(number = 4, order = 4, name = "roomprefrences_closed", display_name = "Lock Room Preferences").save()
# state_5 = TermStates(number = 5, order = 5, name = "rooms_assigned", display_name = "Assign Rooms").save()
# state_6 = TermStates(number = 6, order = 6, name = "term_finished", display_name = "Finish").save()
# state_7 = TermStates(number = 7, order = 7, name = "term_archived", display_name = "Archive").save()
 

# class CourseChange(dbModel):
#   cId               = IntegerField(primary_key = True)
#   prefix            = ForeignKeyField(Subject, related_name='courseChange_prefix')
#   bannerRef         = ForeignKeyField(BannerCourses, related_name='courseChange_bannerRef')
#   term              = ForeignKeyField(Term, null = False, related_name='courseChange_term')
#   schedule          = ForeignKeyField(BannerSchedule, null = True, related_name='courseChange_schedule')
#   capacity          = IntegerField(null = True)
#   specialTopicName  = CharField(null = True)
#   notes             = TextField(null = True)
#   lastEditBy        = CharField(null = True)
#   changeType        = CharField(null = True)
#   verified          = BooleanField(default = False)
#   crossListed       = BooleanField()
#   rid               = ForeignKeyField(Rooms, null = True, related_name='courseChange_rid')
#   tdcolors          = CharField(null = False)
#   section           = TextField(null = True)


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
  
  

# my_db.create_tables([BuildingManager])

# bmanager = BuildingManager( username = "stamperf",
#                             bmid = 6
#                           ).save()
# migrate(
#     migrator.add_column('Rooms', 'lastModified', CharField(null=True))
    # migrator.add_column('RoomPreferences', 'priority', IntegerField(default=6)),
    # migrator.add_column('Course', 'days_id', ForeignKeyField(ScheduleDays, to_field = ScheduleDays.sdID , null = True, related_name='course_days'))

# my_db.create_tables([ScheduleDays])


# my_db.create_tables([RoomPreferences])
# migrate(
#     migrator.add_column('RoomPreferences', 'priority', IntegerField(default=6))
#     # migrator.add_column('Course', 'days_id', ForeignKeyField(ScheduleDays, to_field = ScheduleDays.sdID , null = True, related_name='course_days'))

     
#     # migrator.drop_not_null('CourseChange','rid')
# )

# my_db.drop_tables([ScheduleDays])

# class ScheduleDays(dbModel):
#   sdID = PrimaryKeyField()
#   schedule = ForeignKeyField(BannerSchedule, null = True, related_name='course_schedule_days')
#   day         = CharField(null=True)
  
  

migrate(
    # migrator.add_column('RoomPreferences', 'priority', IntegerField(default=6)),
    # migrator.drop_column("Term", "state"),
    # migrator.add_column('Term', 'term_state_id', ForeignKeyField(TermStates, to_field = TermStates.csID , default = 1, related_name='term_states')),
    # migrator.add_column('Term', 'algorithm_running', BooleanField(null = False, default = False))
    migrator.add_column('Term', 'editable', BooleanField(null = False, default = True))
    
#     # migrator.drop_not_null('CourseChange','rid')
# )

# t = Term.select()
# for term in t:
#   term.algorithm_running = False
#   term.save()

# q = Course.select()
# for course in q:
#   course.rid = None
#   course.save()
  
  
# q = SpecialTopicCourse.select()
# for course in q:
#   course.rid = None
#   course.save()


# PART OF PR 265  
# migrate(
#     migrator.add_column("rooms", "lastModified", CharField(null = True)))
    