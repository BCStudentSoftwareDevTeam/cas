#import the migrator
from playhouse.migrate import *
# import model for database
from app.models import *

migrator = SqliteMigrator(mainDB)

# Rename the editable column to state, since it now has multiple states
migrate(
    migrator.drop_column("User","bNumber"),
    migrator.add_column("User","bNumber", CharField(default='',null=True))
)
