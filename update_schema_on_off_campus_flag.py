from peewee import *
from playhouse.migrate import *
from app.models.models import *
from app.loadConfig import *

here = os.path.dirname(__file__)
cfg       = load_config()


mainDB     = MySQLDatabase ( cfg["db"]["db_name"], host = cfg["db"]["host"], user = cfg["db"]["username"], passwd = cfg["db"]["password"])

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta:
    database = mainDB


migrator = MySQLMigrator(mainDB)



migrate(
 migrator.add_column('Course','offCampusFlag', BooleanField(default=False)),
 migrator.add_column('SpecialTopicCourse','offCampusFlag', BooleanField(default=False)),
)

# Shift existing schedule's order up by 300 to give space for the new ones
 for prior_schedule in BannerSchedule().select():
    print(prior_schedule.order)
    prior_schedule.order = int(prior_schedule.order) + 300 
    prior_schedule.save()


# Adds Scheduling data to BannerSchedule 

f = open('covid_schedule.csv', 'r')

for (idx, row) in enumerate(f):
    row_list = row.split(",")
    days = "".join(row_list[1:6])
    schedule = BannerSchedule.create(sid = row_list[0],
                                     letter = days + " (PANDEMIC " + row_list[0] + ")", 
                                     startTime = row_list[8][0:-2] + ":" + row_list[8][-2:],                                      
                                     endTime = row_list[9][0:-3] + ":" + row_list[9][-3:],      # there must be rough spaces at beginning/end, so it's 3 instead of 2
                                     order = idx
                                    )
    schedule.save()

    # Insert ScheduleDays to associate schedule to specific days of the week
    for day in days:
        insert_day = ScheduleDays.create(schedule = schedule.sid, day = day)


