from peewee import *
from playhouse.migrate import *
from app.models import *
from app.loadConfig import *

here = os.path.dirname(__file__)
cfg       = load_config(os.path.join(here, 'app/config.yaml'))
db	     = os.path.join(here,cfg['databases']['dev']) 
print("here", here)
print('Test', cfg['databases'])

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
# my_db.drop_tables([RoomPreferences])


#TODO: make a function & wrap it up in try/catch statement so it doesn't break when tables are already there/aren't there
def dropTables():
  tables = [Rooms, Building, EducationTech, RoomPreferences, CourseChange, ScheduleDays, Course]
  for table in tables:
    try:
        my_db.drop_tables([table])
    except:
        pass

# dropTables()

class BuildingManager(baseModel):
  username     = ForeignKeyField(User, related_name='building_manager')
  bmid         = ForeignKeyField(Building,related_name='building_manager_id', on_delete= 'CASCADE')
  
my_db.create_tables([BuildingManager])

