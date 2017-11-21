from app.models import SpecialTopicCourse
from app.models import InstructorSTCourse
from playhouse.migrate import *
from app.models import mainDB

def create_table():
  # create the table
  InstructorSTCourse.create_table(True)
  SpecialTopicCourse.create_table(True)
  
  
if __name__ == "__main__":
  create_table()
  
  
