from peewee import *
from playhouse.migrate import *
from app.models.models import *
from app.loadConfig import *

here = os.path.dirname(__file__)
cfg       = load_config()


mainDB     = MySQLDatabase ( cfg["db"]["db_name"], host = cfg["db"]["host"], user = cfg["db"]["username"], passwd = cfg["db"]["password"])

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta:
    database = mainDB


migrator = MySQLMigrator(mainDB)



migrate(
    migrator.add_column('Course','offCampusFlag', BooleanField(default=False)),
)

