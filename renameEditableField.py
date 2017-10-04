from playhouse.migrate import *
from app.models import *

migrator = SqliteMigrator(mainDB)
migrate(
    migrator.rename_column('Term', 'editable', 'state'),
)

