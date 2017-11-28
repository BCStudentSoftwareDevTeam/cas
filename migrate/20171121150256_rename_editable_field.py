"""
  everything that should be migrated happens there
  to migrate use playhouse
  http://docs.peewee-orm.com/en/latest/peewee/database.html#schema-migrations
"""
    
from app.models import *
from playhouse.migrate import *
from .base import Base


class rename_editable_field(Base):
    def __init__(self):
      Base.__init__(self)

    def up(self):
        """ migrates file to new schema """
        # preparation code goes here
        migrate(
          self.migrator.rename_column("Term","editable","state")
        )
        
    def down(self):
        """ reverts migration """
        # preparation code goes here
        migrate(
          self.migrator.rename_column("Term","state","editable")
        )
  
  