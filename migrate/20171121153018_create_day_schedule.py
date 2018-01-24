"""
  everything that should be migrated happens there
  to migrate use playhouse
  http://docs.peewee-orm.com/en/latest/peewee/database.html#schema-migrations
"""
    
from app.models import *
from playhouse.migrate import *
from .base import Base


class create_day_schedule(Base):
    def __init__(self):
      Base.__init__(self)
      
    def create_table(self):
      # create the table
      ScheduleDays.create_table(True)
      
    def create_days(self):
  
      # Get all schedules
      schedules = mainDB.execute_sql("SELECT sid, days, startTime, endTime FROM bannerschedule")
      
      # Create new buildings
      for schedule in schedules.fetchall():
        if 'N/A' not in schedule[1]:
          for letter in schedule[1]:
            schedule_day = ScheduleDays(schedule = schedule[0], day=letter)
            schedule_day.save()
        else:
          schedule_day = ScheduleDays(schedule = schedule[0], day=None)
          schedule_day.save()
  

    def up(self):
        """ migrates file to new schema """
        # preparation code goes here
        self.create_table()
  
        self.create_days()
  
        migrate(
          self.migrator.drop_column('bannerschedule', 'days')
        )
        
    def down(self):
        """ reverts migration """
        # preparation code goes here
        migrate(
             # schema migration happens here
        )
  
  