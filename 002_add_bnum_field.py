#import the migrator
from playhouse.migrate import *
# import model for database
from app.models import *

migrator = SqliteMigrator(mainDB)

# Adds the bNumber column to the database.
migrate(
    migrator.drop_column("User","bNumber"),
    migrator.add_column("User","bNumber", CharField(default='',null=True))
)
