# WARNING: NOT FOR USE IN PRODUCTION AFTER REAL DATA EXISTS!!!!!!!!!!!!!!!!!!!!!!
'''
This script creates the database tables in the SQLite file. 
Update this file as you update your database.
'''
import os, sys
import importlib
import datetime

# Don't forget to import your own models!
from app.models import *
conf = load_config(os.path.join(here,'config.yaml'))
#onf = load_config('app/config.yaml')

sqlite_dbs  = [ conf['databases']['dev']
                # add more here if multiple DBs
              ]

# Remove DBs
for fname in sqlite_dbs:
  try:
    print ("Removing {0}.".format(fname))
    os.remove(fname)
  except OSError:
    pass

# Creates DBs
for fname in sqlite_dbs:
  if os.path.isfile(fname):
    print ("Database {0} should not exist at this point!".format(fname))
  print ("Creating empty SQLite file: {0}.".format(fname))
  open(fname, 'a').close()
  

def class_from_name (module_name, class_name):
  # load the module, will raise ImportError if module cannot be loaded
  # m = __import__(module_name, globals(), locals(), class_name)
  # get the class, will raise AttributeError if class cannot be found
  c = getattr(module_name, class_name)
  return c
    
"""This file creates the database and fills it with some dummy run it after you have made changes to the models pages."""
def get_classes (db):
  classes = []
  for str in conf['models'][db]:
    print ("\tCreating model for '{0}'".format(str))
    c = class_from_name(sys.modules[__name__], str)
    classes.append(c)
  return classes

  
mainDB.create_tables(get_classes('mainDB'))

######
#USERS#
######
users = User(  firstName = "Scott",
                lastName  = "Heggen",
                username  = "heggens",
                email     = "heggens@berea.edu",
                isAdmin   = 1,
                program   = 1
            ).save(force_insert=True)
            
users = User(  firstName = "Jan",
                lastName  = "Pearce",
                username  = "pearcej",
                email     = "jadudm@berea.edu",
                isAdmin   = 0,
                program   = 2
            ).save(force_insert=True)     

users = User(  firstName = "Matt",
                lastName  = "Jadud",
                username  = "jadudm",
                email     = "jadudm@berea.edu",
                isAdmin   = 0,
                program   = 2
            ).save(force_insert=True)
            
users = User(  firstName = "Cody",
                lastName  = "Myers",
                username  = "myersco",
                email     = "jadudm@berea.edu",
                isAdmin   = 0,
                program   = 2
            ).save(force_insert=True) 
##########
#DIVISION#
##########
division = Division(  name = "Division I"
              ).save()

division = Division(  name = "Division II"
              ).save()
#########
#PROGRAM#
#########
program  = Program( name = "Computer Science",
                    division = 2,
                    prefix   = "CSC",
                    has_subjects = False
              ).save()
              
program  = Program( name = "Mathematics",
                    division = 1,
                    prefix   = "MAT",
                    has_subjects = False
              ).save()
              
program  = Program( name = "Technology and Design",
                    division = 2,
                    prefix   = "TAD",
                    has_subjects = False
              ).save()
program  = Program( name = "Foreign Languages",
                    division = 4,
                    prefix   = "FL", 
                    has_subjects = True
              ).save()
program  = Program( name = "Health and Human Performance",
                    division = 3,
                    prefix   = "HHP", 
                    has_subjects = True
              ).save()
#########         
#SUBJECT#
#########
subject = Subject(  prefix  = "CSC",
                    pid     = 1,
                    name    = "Computer Science",
                    webname = "cs.berea.edu"
                    ).save(force_insert=True)
                    
subject = Subject(  prefix  = "MAT",
                    pid     = 2,
                    name    = "Mathematics",
                    webname = "math.berea.edu"
                  ).save(force_insert=True)
                  
                  
subject = Subject(  prefix  = "TAD",
                    pid     = 3,
                    name    = "Technology and Applied Design",
                    webname = "math.berea.edu"
                  ).save(force_insert=True)
                  
subject = Subject(  prefix  = "CHI",
                    pid     = 4,
                    name    = "Chinese",
                    webname = "chinese.berea.edu"
                  ).save(force_insert=True)
                  
subject = Subject(  prefix  = "FRN",
                    pid     = 4,
                    name    = "French",
                    webname = "french.berea.edu"
                  ).save(force_insert=True)
                  
subject = Subject(  prefix  = "GER",
                    pid     = 4,
                    name    = "German",
                    webname = "german.berea.edu"
                  ).save(force_insert=True)
subject = Subject(  prefix  = "HHP",
                    pid     = 5,
                    name    = "Health and Human Performance",
                    webname = "health.berea.edu"
                  ).save(force_insert=True)
subject = Subject(  prefix  = "HLT",
                    pid     = 5,
                    name    = "Health",
                    webname = "health.berea.edu"
                  ).save(force_insert=True)
########                  
#BANNER#
########
banner = BannerSchedule(  letter        = "Standard A",
                          days          = "MWF",
                          startTime     = datetime.time(8, 0, 0),
                          endTime       = datetime.time(9, 10, 0),
                          sid           = "A",
                          order         = 1
                        ).save(force_insert=True)

banner = BannerSchedule(  letter        = "Standard B",
                          days          = "MWF",
                          startTime     = datetime.time(9, 20, 0),
                          endTime       = datetime.time(10, 30, 0),
                          sid           = "B",
                          order         = 2
                        ).save(force_insert=True)
##############
#BANNERCOURSE#
##############
bannercourse =  BannerCourses(  subject       = "CSC",
                                number        = 236,
                                ctitle        = "Data Structures",
                                program       = 1
                              ).save()

bannercourse =  BannerCourses(  subject       = "MAT",
                                number        = 135,
                                ctitle        = "Calculus I",
                                program       = 2
                                
                              ).save()
                        

bannercourse =  BannerCourses(  subject       = "MAT",
                                number        = 225,
                                ctitle        = "Calculus II",
                                program       = 2
                                
                              ).save()
bannercourse =  BannerCourses(  subject       = "TAD",
                                number        = 435,
                                ctitle        = "Wood Shop",
                                program       = 3
                              ).save()

bannercourse =  BannerCourses(  subject       = "TAD",
                                number        = 265,
                                ctitle        = "Electricity",
                                program       = 3
                              ).save()
                    
bannercourse =  BannerCourses(  subject       = "CSC",
                                number        = 124,
                                ctitle        = "Better Apps",
                                program       = 1
                              ).save()
                              
bannercourse =  BannerCourses(  subject       = "CSC",
                                number        = 226,
                                ctitle        = "Software Design",
                                program       = 1
                              ).save()  
bannercourse =  BannerCourses(  subject       = "CHI",
                                number        = 101,
                                ctitle        = "Intro to Chinese I",
                                program       = 4
                              ).save()       
                              
bannercourse =  BannerCourses(  subject       = "CHI",
                                number        = 102,
                                ctitle        = "Intro to Chinese II",
                                program       = 4
                              ).save()    
bannercourse =  BannerCourses(  subject       = "CHI",
                                number        = 103,
                                ctitle        = "Intro to Chinese III",
                                program       = 4
                              ).save()    
bannercourse =  BannerCourses(  subject       = "CHI",
                                number        = 104,
                                ctitle        = "Intro to Chinese IV",
                                program       = 4
                              ).save()    
bannercourse =  BannerCourses(  subject       = "FRN",
                                number        = 101,
                                ctitle        = "Intro to Frn Lang & Culture I",
                                program       = 4
                              ).save()       
                              
bannercourse =  BannerCourses(  subject       = "FRN",
                                number        = 102,
                                ctitle        = "Intro to Frn Lang & Culture II",
                                program       = 4
                              ).save()    
bannercourse =  BannerCourses(  subject       = "FRN",
                                number        = 103,
                                ctitle        = "Intermediate French III",
                                program       = 4
                              ).save()    
bannercourse =  BannerCourses(  subject       = "FRN",
                                number        = 140,
                                ctitle        = "Frn Civilization Past/Present",
                                program       = 4
                              ).save()   
bannercourse =  BannerCourses(  subject       = "GER",
                                number        = 101,
                                ctitle        = "Intro to German I",
                                program       = 4
                              ).save()       
                              
bannercourse =  BannerCourses(  subject       = "GER",
                                number        = 102,
                                ctitle        = "Intro to German II",
                                program       = 4
                              ).save()    
bannercourse =  BannerCourses(  subject       = "GER",
                                number        = 103,
                                ctitle        = "Intermediate German III",
                                program       = 4
                              ).save()    
bannercourse =  BannerCourses(  subject       = "GER",
                                number        = 140,
                                ctitle        = "German Civilization",
                                program       = 4
                              ).save()   
bannercourse =  BannerCourses(  subject       = "HHP",
                                number        = 200,
                                ctitle        = "Survival Swimming",
                                program       = 3
                              ).save()    
bannercourse =  BannerCourses(  subject       = "HLT",
                                number        = 100,
                                ctitle        = "Intro to Lifetime Health and Wellness",
                                program       = 3
                              ).save()   

######
######
#TERM#
######
term = Term(  name              = "Fall 2016",
              semester          = "Fall",
              year              = 2016,
              termCode          = 201612,
              editable          = 0
            ).save(force_insert = True)
            
term = Term(  name              = "Spring 2017",
              semester          = "Spring",
              year              = 2017,
              termCode          = 201711,
              editable          = 0
            ).save(force_insert = True)  
term = Term(  name              = "Fall 2017",
              semester          = "Fall",
              year              = 2017,
              termCode          = 201712,
              editable          = 0
            ).save(force_insert = True)
            
term = Term(  name              = "Spring 2018",
              semester          = "Spring",
              year              = 2018,
              termCode          = 201811,
              editable          = 0
            ).save(force_insert = True)      
term = Term(  name              = "Fall 2018",
              semester          = "Fall",
              year              = 2018,
              termCode          = 201812,
              editable          = 0
            ).save(force_insert = True)
            
term = Term(  name              = "Spring 2019",
              semester          = "Spring",
              year              = 2019,
              termCode          = 201911,
              editable          = 0
            ).save(force_insert = True)      
term = Term(  name              = "Fall 2019",
              semester          = "Fall",
              year              = 2019,
              termCode          = 201912,
              editable          = 0
            ).save(force_insert = True)
            

            
########
#COURSE#
########
course = Course(  bannerRef         = 1,
                  prefix            = "CSC",
                  term              = 201611,
                  schedule          = "A",
                  capacity          = 20,
                  notes             = "Preference1",
                  crossListed       = 1
                ).save()
                
course = Course(  bannerRef         = 2,
                  prefix            = "MAT",
                  term              = 201612,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                ).save()                

course = Course(  bannerRef         = 3,
                  prefix            = "TAD",
                  term              = 201612,
                  schedule          = "A",
                  capacity          = 20,
                  notes          = "Preference1",
                  crossListed       = 0
                  ).save()
course = Course(  bannerRef         = 8,
                  prefix            = "CHI",
                  term              = 201612,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()       
                              
course = Course(  bannerRef         = 9,
                  prefix            = "CHI",
                  term              = 201711,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save() 
course = Course(  bannerRef         = 10,
                  prefix            = "CHI",
                  term              = 201711,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save() 
course = Course(  bannerRef         = 11,
                  prefix            = "CHI",
                  term              = 201712,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save() 
course = Course(  bannerRef         = 11,
                  prefix            = "CHI",
                  term              = 201811,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save() 
course = Course(  bannerRef         = 13,
                  prefix            = "FRN",
                  term              = 201611,
                  schedule          = "A",
                  capacity          = 20,
                  notes             = "Preference1",
                  crossListed       = 1
                ).save()
                
course = Course(  bannerRef         = 14,
                  prefix            = "FRN",
                  term              = 201612,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                ).save()                

course = Course(  bannerRef         = 15,
                  prefix            = "FRN",
                  term              = 201712,
                  schedule          = "A",
                  capacity          = 20,
                  notes          = "Preference1",
                  crossListed       = 0
                  ).save()
course = Course(  bannerRef         = 15,
                  prefix            = "FRN",
                  term              = 201612,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()       
                              
course = Course(  bannerRef         = 17,
                  prefix            = "GER",
                  term              = 201711,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save() 
course = Course(  bannerRef         = 18,
                  prefix            = "GER",
                  term              = 201711,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save() 
course = Course(  bannerRef         = 19,
                  prefix            = "GER",
                  term              = 201712,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save() 
course = Course(  bannerRef         = 19,
                  prefix            = "GER",
                  term              = 201811,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save() 
course = Course(  bannerRef         = 20,
                  prefix            = "HHP",
                  term              = 201712,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save() 
course = Course(  bannerRef         = 21,
                  prefix            = "HLT",
                  term              = 201811,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save() 


########
#PCHAIR#
########
chair = ProgramChair(  username  = "jadud",
                        pid       = 1
                    ).save()
                    
########
#DCHAIR#
########
dchair = DivisionChair(  username  = "pearcej",
                        did       = 2
                      ).save()
############
#INSTRUCTOR#
############
instructor = InstructorCourse(  username = "heggens",
                                course   = 1
                              ).save()
                              
instructor = InstructorCourse(  username = "jadudm",
                                course   = 2
                              ).save()
                              
instructor = InstructorCourse(  username = "myersco",
                                course   = 3
                              ).save()  
                              
######
#ROOMS#
######
room = Rooms(building = 'Ag Building', number ='102', maxCapacity=12, roomType="Something").save()
room = Rooms(building = 'Tech Building', number ='105', maxCapacity=15, roomType="Lecture").save()

room = Rooms(building = 'Ag Building', number ='103A', maxCapacity=12, roomType="Something").save()

# try:
#   os.system('mysql-ctl start')
#   os.system('python migrateDatabase.py')
# except:
#   print "Migration failed"
#   raise
