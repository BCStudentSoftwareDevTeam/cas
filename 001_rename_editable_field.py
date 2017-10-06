#import the migrator
from playhouse.migrate import *
# import model for database
from app.models import *

migrator = SqliteMigrator(mainDB)

# Rename the editable column to state, since it now has multiple states
migrate(
    migrator.rename_column("Term","editable","state")
)
