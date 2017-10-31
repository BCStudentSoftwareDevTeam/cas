from create_tables import *
from app.models import *

######
#USERS#
######
users = User(  firstName = "Scott",
                lastName  = "Heggen",
                username  = "heggens",
                email     = "heggens@berea.edu",
                isAdmin   = 1,
                bNumber   = "1239485"
            ).save(force_insert=True)
            
users = User(  firstName = "Jan",
                lastName  = "Pearce",
                username  = "pearcej",
                email     = "jadudm@berea.edu",
                isAdmin   = 0,
                bNumber   = "1239495"
            ).save(force_insert=True)     

users = User(  firstName = "Matt",
                lastName  = "Jadud",
                username  = "jadudm",
                email     = "jadudm@berea.edu",
                isAdmin   = 0,
                bNumber   = "1234409485"
            ).save(force_insert=True)
            
users = User(  firstName = "Cody",
                lastName  = "Myers",
                username  = "myersco",
                email     = "jadudm@berea.edu",
                isAdmin   = 0,
                bNumber   = "1774409485"
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
                    prefix   = "CSC"
              ).save()
              
program  = Program( name = "Mathematics",
                    division = 1,
                    prefix   = "MAT"
              ).save()
              
program  = Program( name = "Technology and Design",
                    division = 2,
                    prefix   = "TAD"
              ).save()
#########         
#SUBJECT#
#########
subject = Subject(  prefix  = "CSC",
                    pid     = 1,
                    webname = "cs.berea.edu"
                    ).save(force_insert=True)
                    
subject = Subject(  prefix  = "MAT",
                    pid     = 2,
                    webname = "math.berea.edu"
                  ).save(force_insert=True)
                  
subject = Subject(  prefix  = "CODY",
                    pid     = 1,
                    webname = "math.berea.edu"
                  ).save(force_insert=True)                 
                  
subject = Subject(  prefix  = "TAD",
                    pid     = 3,
                    webname = "math.berea.edu"
                  ).save(force_insert=True)
########                  
#BANNER#
########
banner = BannerSchedule(  letter        = "Standard A",
                          days          = "MWF",
                          startTime     = datetime.time(8, 0, 0),
                          endTime       = datetime.time(9, 10, 0),
                          sid           = "A",
                          order         = 1,
            
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
                                is_active     = 1
                              ).save()

bannercourse =  BannerCourses(  subject       = "MAT",
                                number        = 135,
                                ctitle        = "Calculus I",
                                is_active     = 1
                              ).save()
                        
bannercourse =  BannerCourses(  subject       = "TAD",
                                number        = 435,
                                ctitle        = "Wood Shop",
                                is_active     = 1
                              ).save()
                    
bannercourse =  BannerCourses(  subject       = "CSC",
                                number        = 124,
                                ctitle        = "Better Apps",
                                is_active     = 1
                              ).save()
                              
bannercourse =  BannerCourses(  subject       = "CSC",
                                number        = 226,
                                ctitle        = "Software Design",
                                is_active     = 1
                              ).save()                                
######
#TERM#
######
term = Term(  name             = "Fall 2016",
              semester          = "Fall",
              year              = 2016,
              termCode          = 201611,
              state             = 0
            ).save(force_insert = True)
            
term = Term(  name              = "Spring 2017",
              semester          = "Spring",
              year              = 2017,
              termCode          = 201612,
              state             = 0
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
########
#PCHAIR#
########
pchair = ProgramChair(  username  = "jadudm",
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
                              
building     = Building(name = 'Ag Building').save()
building     = Building(name = 'Tech Building').save()
building    = Building(name = 'Ag Building').save()

                              
######
#ROOMS#
######
room = Rooms(building = 1, number ='102', maxCapacity=12, roomType="Something").save()
room = Rooms(building = 2, number ='105', maxCapacity=15, roomType="Lecture").save()

room = Rooms(building = 3, number ='103A', maxCapacity=12, roomType="Something").save()

# try:
#   os.system('mysql-ctl start')
#   os.system('python migrateDatabase.py')
# except:
#   print "Migration failed"
#   raise
