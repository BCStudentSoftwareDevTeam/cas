"""
  everything that should be migrated happens there
  to migrate use playhouse
  http://docs.peewee-orm.com/en/latest/peewee/database.html#schema-migrations
"""
    
from app.models import *
from playhouse.migrate import *
from .base import Base


class create_foreignkey_course(Base):
    def __init__(self):
      Base.__init__(self)

    def up(self):
        """ migrates file to new schema """
        # preparation code goes here
        migrate(
          self.migrator.add_column("SpecialTopicCourse","course_id", ForeignKeyField(Course, null=True, to_field=Course.cId))
        )
        
    def down(self):
        """ reverts migration """
        # preparation code goes here
        migrate(
             # schema migration happens here
        )
  
  