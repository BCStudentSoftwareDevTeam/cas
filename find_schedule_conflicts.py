import datetime
from peewee import *
from app.models.models import *
from app.loadConfig import *

here = os.path.dirname(__file__)
cfg       = load_config()


mainDB     = MySQLDatabase ( cfg["db"]["db_name"], host = cfg["db"]["host"], user = cfg["db"]["username"], passwd = cfg["db"]["password"])

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta:
    database = mainDB


def isConflict(a, b):
  ''' Finds schedule conflicts '''
  a_start = a.startTime
  a_end = a.endTime
  b_start = b.startTime 
  b_end = b.endTime

  schedADays = ScheduleDays().select(ScheduleDays.day).where(ScheduleDays.schedule == a.sid)
  schedBDays = ScheduleDays().select(ScheduleDays.day).where(ScheduleDays.schedule == b.sid)
  daysA = []
  for val in list(schedADays.dicts()):
    daysA.append(val['day'])

  daysOverlap = False
  for day in schedBDays:
    if day.day in daysA:
      daysOverlap = True
      break

  if not daysOverlap:
    return False

  if a_start <= b_end and a_end >= b_start:
    return True
  elif b_start <= a_end and b_end >= a_start:
    return True
  return False 

# Get all schedules
schedules = BannerSchedule().select()

conflicts_dict = {}

for schedA in schedules:
  if schedA.sid != "ZZZ":    
    conflicts_dict[schedA.sid] = []
    for schedB in schedules:
      if schedB.sid != "ZZZ":
        if isConflict(schedA, schedB):
#          print(conflicts_dict)
          conflicts_dict[schedA.sid].append(schedB.sid)



print(conflicts_dict)
