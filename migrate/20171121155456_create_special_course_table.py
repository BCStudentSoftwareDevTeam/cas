"""
  everything that should be migrated happens there
  to migrate use playhouse
  http://docs.peewee-orm.com/en/latest/peewee/database.html#schema-migrations
"""
    
from app.models import *
from playhouse.migrate import *
from .base import Base


class create_special_course_table(Base):
    def __init__(self):
      Base.__init__(self)

    def up(self):
        """ migrates file to new schema """
        # preparation code goes here
        InstructorSTCourse.create_table(True)
        SpecialTopicCourse.create_table(True)
        
    def down(self):
        """ reverts migration """
        # preparation code goes here
        migrate(
             # schema migration happens here
        )
  
  