from app.models import BannerSchedule
from app.models import ScheduleDays
from playhouse.migrate import *
from app.models import mainDB

def create_table():
  # create the table
  ScheduleDays.create_table(True)
  
def create_days():
  
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
  

def migrate_table():
  create_table()
  migrator = SqliteMigrator(mainDB)
  
  create_days()
  
  migrate(
    migrator.drop_column('bannerschedule', 'days')
  )
  
  
if __name__ == "__main__":
  migrate_table()
  
  
  
  
  