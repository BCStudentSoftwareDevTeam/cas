#import the migrator
from playhouse.migrate import *
# import model for database
from app.models import *

migrator = SqliteMigrator(mainDB)

# Adds the bNumber column to the database.
migrate(
    migrator.drop_column("SpecialTopicCourse", "course"),
    migrator.add_column("SpecialTopicCourse","course_id", ForeignKeyField(Course, null=True, to_field=Course.cId))
)
