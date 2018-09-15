from peewee import *
from playhouse.migrate import *
#from app.models import Rooms, Building
from app.models import Rooms, Building, EducationTech, RoomPreferences, Course

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

#my_db.drop_tables([Building, Rooms])
my_db.drop_tables([Building, Rooms, EducationTech, RoomPreferences])

  
  
class RoomPreferences(dbModel):
  rpID          = PrimaryKeyField()
  course        = ForeignKeyField(Rooms, related_name='course')
  pref_1        = ForeignKeyField(Rooms, related_name='pref_1', null=True)
  pref_2        = ForeignKeyField(Rooms, related_name='pref_2', null=True)
  pref_3        = ForeignKeyField(Rooms, related_name='pref_3', null=True) #We are making sure we have all the preferences jotted down.
  notes         = CharField(null=True)
  any_Choice    = CharField(null=True)
  none_Choice   = CharField(null=True)
  none_Reason   = CharField(null=True)
  initial_Preference = CharField(null=True, default = 1)

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


class Building(dbModel):
  bID           = PrimaryKeyField()
  name          = CharField()
  shortName     = CharField()

  
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



my_db.create_tables([RoomPreferences, EducationTech, Building, Rooms])
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


q = Course.select()
for course in q:
  course.rid = None
  course.save()
  
  
  