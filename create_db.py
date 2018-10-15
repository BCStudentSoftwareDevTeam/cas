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
                isAdmin   = 1,
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
            
users = User(  firstName = "Emily",
                lastName  = "Lovell",
                username  = "lovelle",
                email     = "lovelle@berea.edu",
                isAdmin   = 0,
                bNumber   = "1239475"
            ).save(force_insert=True)

##########
#DIVISION#
##########
division = Division(  name = "Division I"
              ).save()

division = Division(  name = "Division II"
              ).save()
division = Division(  name = "Division III"
              ).save()

division = Division(  name = "Division IV"
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
program  = Program( name = "Foreign Languages",
                    division = 4,
                    prefix   = "FL"
              ).save()
program  = Program( name = "Health and Human Performance",
                    division = 3,
                    prefix   = "HHP"
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
                  
                  
subject = Subject(  prefix  = "TAD",
                    pid     = 3,
                    webname = "math.berea.edu"
                  ).save(force_insert=True)
                  
subject = Subject(  prefix  = "CHI",
                    pid     = 4,
                    webname = "chinese.berea.edu"
                  ).save(force_insert=True)
                  
subject = Subject(  prefix  = "FRN",
                    pid     = 4,
                    webname = "french.berea.edu"
                  ).save(force_insert=True)
                  
subject = Subject(  prefix  = "GER",
                    pid     = 4,
                    webname = "german.berea.edu"
                  ).save(force_insert=True)
subject = Subject(  prefix  = "HHP",
                    pid     = 5,
                    webname = "health.berea.edu"
                  ).save(force_insert=True)
subject = Subject(  prefix  = "HLT",
                    pid     = 5,
                    webname = "health.berea.edu"
                  ).save(force_insert=True)
                  

                  
########                  
#BANNER#
########
banner = BannerSchedule(  letter        = "Standard A",
                          startTime     = datetime.time(8, 0, 0),
                          endTime       = datetime.time(9, 10, 0),
                          sid           = "A",
                          order         = 1
                        ).save(force_insert=True)

banner = BannerSchedule(  letter        = "Standard B",
                          startTime     = datetime.time(9, 20, 0),
                          endTime       = datetime.time(10, 30, 0),
                          sid           = "B",
                          order         = 2
                        ).save(force_insert=True)
banner = BannerSchedule(  letter        = "Standard C",
                          startTime     = datetime.time(8, 0, 0),
                          endTime       = datetime.time(9, 10, 0),
                          sid           = "C",
                          order         = 3
                        ).save(force_insert=True)
                        
banner = BannerSchedule(  letter        = "Standard D",
                          startTime     = datetime.time(9, 20, 0),
                          endTime       = datetime.time(10, 30, 0),
                          sid           = "D",
                          order         = 4
                        ).save(force_insert=True) 
banner = BannerSchedule(  letter        = "Standard E",
                          startTime     = datetime.time(8, 0, 0),
                          endTime       = datetime.time(9, 10, 0),
                          sid           = "E",
                          order         = 5
                        ).save(force_insert=True)                         

###############
#Schedule Days#
###############
scheduledays = ScheduleDays( schedule = "A",
                             day =  "MWF"
                             ).save(force_insert=True)
    
scheduledays = ScheduleDays( schedule = "B",
                             day =  "MWF"
                             ).save(force_insert=True)
                             
scheduledays = ScheduleDays( schedule = "C",
                             day =  "TR"
                             ).save(force_insert=True)

scheduledays = ScheduleDays( schedule = "D",
                             day =  "TR"
                             ).save(force_insert=True)
scheduledays = ScheduleDays( schedule = "E",
                             day =  "MR"
                             ).save(force_insert=True)                             
##############
#BANNERCOURSE#
##############
bannercourse =  BannerCourses(  subject       = "CSC",
                                number        = 236,
                                ctitle        = "Data Structures",
                                program       = 1,
                                is_active     = True,
                                ).save()

bannercourse =  BannerCourses(  subject       = "MAT",
                                number        = 135,
                                ctitle        = "Calculus I",
                                program       = 2,
                                is_active     = True
                                ).save()
                        
bannercourse =  BannerCourses(  subject       = "MAT",
                                number        = 225,
                                ctitle        = "Calculus II",
                                program       = 2,
                                is_active     = True
                                
                              ).save()
bannercourse =  BannerCourses(  subject       = "TAD",
                                number        = 486,
                                ctitle        = "Wood Shop",
                                program       = 3,
                                is_active     = True
                              ).save()

bannercourse =  BannerCourses(  subject       = "TAD",
                                number        = 265,
                                ctitle        = "Electricity",
                                program       = 3,
                                is_active     = True
                              ).save()
                    
bannercourse =  BannerCourses(  subject       = "TAD",
                                number        = 486,
                                ctitle        = "Something Shop",
                                is_active     = True
                              ).save()
                              
bannercourse =  BannerCourses(  subject       = "CSC",
                                number        = 124,
                                ctitle        = "Building Better Apps",
                                program       = 1,
                                is_active     = True
                              ).save()
                              
bannercourse =  BannerCourses(  subject       = "CSC",
                                number        = 226,
                                ctitle        = "Software Design and Implement",
                                program       = 1,
                                is_active     = True
                              ).save()  
bannercourse =  BannerCourses(  subject       = "CHI",
                                number        = 101,
                                ctitle        = "Intro to Chinese I",
                                program       = 4,
                                is_active     = True
                              ).save()       
                              
bannercourse =  BannerCourses(  subject       = "CHI",
                                number        = 102,
                                ctitle        = "Intro to Chinese II",
                                program       = 4,
                                is_active     = True
                              ).save()    
bannercourse =  BannerCourses(  subject       = "CHI",
                                number        = 103,
                                ctitle        = "Intro to Chinese III",
                                program       = 4,
                                is_active     = True
                              ).save()    
bannercourse =  BannerCourses(  subject       = "CHI",
                                number        = 104,
                                ctitle        = "Intro to Chinese IV",
                                program       = 4,
                                is_active     = True
                              ).save()    
bannercourse =  BannerCourses(  subject       = "FRN",
                                number        = 101,
                                ctitle        = "Intro to Frn Lang & Culture I",
                                program       = 4,
                                is_active     = True
                              ).save()       
                              
bannercourse =  BannerCourses(  subject       = "FRN",
                                number        = 102,
                                ctitle        = "Intro to Frn Lang & Culture II",
                                program       = 4,
                                is_active     = True
                              ).save()    
bannercourse =  BannerCourses(  subject       = "FRN",
                                number        = 103,
                                ctitle        = "Intermediate French III",
                                program       = 4,
                                is_active     = True
                              ).save()    
bannercourse =  BannerCourses(  subject       = "FRN",
                                number        = 140,
                                ctitle        = "Frn Civilization Past/Present",
                                program       = 4,
                                is_active     = True
                              ).save()   
bannercourse =  BannerCourses(  subject       = "GER",
                                number        = 101,
                                ctitle        = "Intro to German I",
                                program       = 4,
                                is_active     = True
                              ).save()       
                              
bannercourse =  BannerCourses(  subject       = "GER",
                                number        = 102,
                                ctitle        = "Intro to German II",
                                program       = 4,
                                is_active     = True
                              ).save()    
bannercourse =  BannerCourses(  subject       = "GER",
                                number        = 103,
                                ctitle        = "Intermediate German III",
                                program       = 4,
                                is_active     = True
                                
                              ).save()    
bannercourse =  BannerCourses(  subject       = "GER",
                                number        = 140,
                                ctitle        = "German Civilization",
                                program       = 4,
                                is_active     = True
                              ).save()   
bannercourse =  BannerCourses(  subject       = "HHP",
                                number        = 200,
                                ctitle        = "Survival Swimming",
                                program       = 3,
                                is_active     = True
                              ).save()    
bannercourse =  BannerCourses(  subject       = "HLT",
                                number        = 100,
                                ctitle        = "Intro to Lifetime Health and Wellness",
                                program       = 3,
                                is_active     = True
                              ).save()   

######
######
#TERM#
######
term = Term(  name             = "Fall 2016",
              semester          = "Fall",
              year              = 2016,
            #   editable          = 0,
              termCode          = 201611,
              state             = 0
            ).save(force_insert = True)
            
term = Term(  name              = "Spring 2017",
              semester          = "Spring",
              year              = 2017,
              termCode          = 201612,
            #   editable          = 0,
              state             = 0
            ).save(force_insert = True)  
term = Term(  name              = "Fall 2017",
              semester          = "Fall",
              year              = 2017,
              termCode          = 201711,
            #   editable          = 0,
              state             = 0
            ).save(force_insert = True)
            
term = Term(  name              = "Spring 2018",
              semester          = "Spring",
              year              = 2018,
              termCode          = 201712,
            #   editable          = 0,
              state             = 0
            ).save(force_insert = True)      
term = Term(  name              = "Fall 2018",
              semester          = "Fall",
              year              = 2018,
              termCode          = 201811,
            #   editable          = 0,
              state             = 0
            ).save(force_insert = True)
            


            
########
#COURSE#
########
course = Course(  bannerRef         = 1, #Course 1
                  prefix            = "CSC",
                  term              = 201611,
                  schedule          = "A",
                  capacity          = 20,
                  notes             = "This is 236, yo",
                  section           = "A",
                  crossListed       = 1,
                  rid               = 1,
                  time              = "8:00 - 9:20 am"
                ).save()
                
course = Course(  bannerRef         = 2, #Course 2
                  prefix            = "MAT",
                  schedule          = "B",
                  term              = 201611,
                  capacity          = 20,
                  notes             = "Math yo",
                  section           = "A",
                  crossListed       = 1,
                  rid               = 2
                ).save()                

course = Course(  bannerRef         = 3, #Course 3
                  prefix            = "MAT",
                  term              = 201611,
                  schedule          = "A",
                  section           = "C",
                  capacity          = 20,
                  notes             = "mattth",
                  crossListed       = 0
                  ).save()
                  
course = Course(  bannerRef         = 4, #Course 4
                  prefix            = "TAD",
                  term              = 201611,
                  schedule          = "E",
                  capacity          = 20,
                  notes             = "TAD",
                  crossListed       = 0,
                  section           = "A",
                  rid               =  4
                  ).save()                  
                  
course = Course(  bannerRef         = 8, #Course 5
                  prefix            = "CSC",
                  term              = 201611,
                  schedule          = "A",
                  capacity          = 20,
                  notes             = "CHINESE",
                  crossListed       = 1,
                  section           = "D"
                  ).save()       
                              
course = Course(  bannerRef         = 9, #Course 6
                  prefix            = "CHI",
                  term              = 201611,
                  schedule          = "E",
                  capacity          = 20,
                  notes             = "Course 6",
                  crossListed       = 1,
                  section           = "E",
                  rid               = 7
                 
                  ).save() 
course = Course(  bannerRef         = 10, #Course 7
                  prefix            = "CHI",
                  term              = 201611,
                  schedule          = "C",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1,
                  section           = "E",
                  
                  ).save() 
course = Course(  bannerRef         = 11, #Course 8
                  prefix            = "CHI",
                  term              = 201611,
                  schedule          = "E",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1,
                  section           = "A",
                  rid               = 13
                  ).save() 
#I set all courses to be in the same term. Change the term code on twice listed courses (bannerRef == bannerRef)
# course = Course(  bannerRef         = 11, #Course 9
#                   prefix            = "CHI",
#                   term              = 201611,
#                   schedule          = "B",
#                   capacity          = 20,
#                   notes             = "Preference2",
#                   crossListed       = 1,
#                   section           = "A"
#                   ).save() 
course = Course(  bannerRef         = 13, #Course 10
                  prefix            = "FRN",
                  term              = 201611,
                  schedule          = "A",
                  capacity          = 20,
                  notes             = "Preference1",
                  crossListed       = 1,
                  section           = "A",
                  rid               = 13
                ).save()
                
course = Course(  bannerRef         = 14, #Course 11
                  prefix            = "FRN",
                  term              = 201611,
                  schedule          = "A",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1,
                  section           = "A",
                   rid               = 6
                  
                ).save()                

course = Course(  bannerRef         = 15, #Course 12
                  prefix            = "FRN",
                  term              = 201611,
                  schedule          = "A",
                  capacity          = 20,
                  notes             = "Preference1",
                  crossListed       = 0,
                  section           = "A",
                   rid               = 5
                  ).save()
#I set all courses to be in the same term. Change the term code on twice listed courses (bannerRef == bannerRef)
# course = Course(  bannerRef         = 15, #Course 13
#                   prefix            = "FRN",
#                   term              = 201611,
#                   schedule          = "B",
#                   capacity          = 20,
#                   notes             = "Preference2",
#                   crossListed       = 1,
#                   section           = "A"
#                   ).save()       
                              
course = Course(  bannerRef         = 17, #Course 14
                  prefix            = "GER",
                  term              = 201611,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1,
                  section           = "A",
                  ).save() 
course = Course(  bannerRef         = 18, #Course 15
                  prefix            = "GER",
                  term              = 201611,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1,
                  section           = "A"
                  ).save() 
course = Course(  bannerRef         = 19, #Course 16
                  prefix            = "GER",
                  term              = 201611,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1,
                  section           = "A"
                  ).save() 
#I set all courses to be in the same term. Change the term code on twice listed courses (bannerRef == bannerRef)                  
# course = Course(  bannerRef         = 19, #Course 17
#                   prefix            = "GER",
#                   term              = 201611,
#                   schedule          = "B",
#                   capacity          = 20,
#                   notes             = "Preference2",
#                   crossListed       = 1,
#                   section           = "A"
#                   ).save() 
# course = Course(  bannerRef         = 19,#Course 18
#                   prefix            = "GER",
#                   term              = 201611,
#                   schedule          = "B",
#                   capacity          = 20,
#                   notes             = "Preference2",
#                   crossListed       = 1,
#                   section           = "A"
#                   ).save() 
course = Course(  bannerRef         = 20, #Course 19
                  prefix            = "GER",
                  term              = 201611,
                  schedule          = "B",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1,
                  section           = "A",
                  ).save() 
course = Course(  bannerRef         = 21, #Course 20
                  prefix            = "HLT",
                  term              = 201611,
                  section           = "A",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1,
                  schedule          = "B",
                  ).save() 


########
#PCHAIR#
########
chair = ProgramChair(  username  = "jadudm",
                        pid       = 1
                    ).save()
chair = ProgramChair(  username = "pearcej",
                        pid = 1
                    ).save()
chair = ProgramChair(  username = "myersco",
                        pid = 2
                    ).save()

                    
########
#DCHAIR#
########
dchair = DivisionChair(  username  = "pearcej",
                        did       = 3
                      ).save()
dchair = DivisionChair(  username  = "myersco",
                        did       = 2
                      ).save()  
dchair = DivisionChair(  username  = "heggens",
                        did       = 1
                      ).save()                      
############
#INSTRUCTOR#
############
instructor = InstructorCourse(  username = "heggens",
                                course   = 1
                              ).save()

instructor = InstructorCourse(  username = "heggens",
                                course   = 2
                              ).save()
                
instructor = InstructorCourse(  username = "heggens",
                                course   = 3
                              ).save()

instructor = InstructorCourse(  username = "heggens",
                                course   = 4
                              ).save()
                              
instructor = InstructorCourse(  username = "heggens",
                                course   = 1
                              ).save()

instructor = InstructorCourse(  username = "heggens",
                                course   = 3
                              ).save()
                              
instructor = InstructorCourse(  username = "jadudm",
                                course   = 2
                              ).save()
                              
instructor = InstructorCourse(  username = "myersco",
                                course   = 3
                              ).save()  

instructor = InstructorSTCourse(  username = "myersco",
                                course   = 1
                              ).save()  
###########
#Buildings#
###########                          

                              
building     = Building(name = 'Ag Building', shortName = 'Ag').save()
building     = Building(name = 'Tech Building', shortName="Tech").save()
building     = Building(name = 'Draper', shortName="Dra").save()
building     = Building(name = 'Sci Building', shortName="Sci").save()
building     = Building(name = 'Frost', shortName="Fro").save()
building     = Building(name = 'Knapp', shortName="Kna").save()
building     = Building(name = 'Emery', shortName="Em").save()
building     = Building(name = 'Presser Hall', shortName="Pre").save()
building     = Building(name = 'Nursing', shortName="Nur").save()
building     = Building(name = 'Art', shortName="Art").save()

###################
#Building Managers#
###################

bmanager = BuildingManager( username = "heggens",
                            bmid = 1
                          ).save()
bmanager = BuildingManager( username = "myersco",
                            bmid = 2
                          ).save()
bmanager = BuildingManager( username = "pearcej",
                            bmid = 3
                          ).save()




###############
#Building Manager#
##################

# bmanager = BuildingManager( username = "heggens",
#                             bmid = 1
#                           ).save()

              
###EDUCATION TECH###


educationTech= EducationTech( 
  projectors           = 1,
  smartboards          = 2,
  instructor_computers = 3,
  podium               = 3,
  student_workspace    = 4,
  chalkboards          = 1,
  whiteboards          = 2,
  dvd                  = False,
  blu_ray              = False,
  audio                = True,
  extro                = True,
  doc_cam              = True,
  vhs                  = True,
  mondopad           = True,
  tech_chart           = False
  ).save()
  
  
###################
#Education Tech#
###################

educationTech= EducationTech( 
  projectors           = 1,
  smartboards          = 2,
  instructor_computers = 3,
  podium               = 3,
  student_workspace    = 4,
  chalkboards          = 2,
  whiteboards          = 2,
  dvd                  = False,
  blu_ray              = False,
  audio                = True,
  extro                = True,
  doc_cam              = True,
  vhs                  = True,
  mondopad           = True,
  tech_chart           = False
  ).save()

educationTech= EducationTech( 
<<<<<<< HEAD
  projector            = 8,
  smartboards          = 3,
  instructor_computers = 1,
  podium               = 4,
=======
  projectors           = 1,
  smartboards          = 2,
  instructor_computers = 3,
  podium               = 3,
>>>>>>> c82e90f7a3638775f0843cd02f1dddf75b5128d3
  student_workspace    = 4,
  chalkboards          = 3,
  whiteboards          = 2,
  dvd                  = False,
  blu_ray              = False,
  audio                = True,
  extro                = True,
  doc_cam              = True,
  vhs                  = True,
  mondopad           = True,
  tech_chart           = False
  ).save()

#####
#ROOMS#
######
<<<<<<< HEAD
room = Rooms(building = 1, number ='102', maxCapacity=12, roomType="Lecture",   educationTech = 1, visualAcc = "A", audioAcc = "B", physicalAcc= "A", specializedEq= "Electronics", specialFeatures= "ethernet on desks", movableFurniture= True).save()
room = Rooms(building = 2, number ='105', maxCapacity=15, roomType="Lecture",   educationTech = 2, visualAcc = "A",  audioAcc = "C", physicalAcc= "B", specializedEq= "Chem Equipment", specialFeatures= "globes", movableFurniture= True).save()
room = Rooms(building = 3, number ='108', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "B", audioAcc = "B", physicalAcc= "A", specializedEq= "Electronics", specialFeatures= "woodworking tools", movableFurniture= True).save()
room = Rooms(building = 1, number ='202', maxCapacity=12, roomType="Lab",       educationTech = 1, visualAcc = "C", audioAcc = "B", physicalAcc= "C", specializedEq= "Kiln", specialFeatures= "ceramics tools", movableFurniture= True).save()
room = Rooms(building = 2, number ='205', maxCapacity=15, roomType="Lecture",   educationTech = 1, visualAcc = "B",  audioAcc = "A", physicalAcc= "A", specializedEq= "Electronics", specialFeatures= "couches", movableFurniture= True).save()
room = Rooms(building = 3, number ='208', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "A", audioAcc = "B", physicalAcc= "A", specializedEq= "Soldering Kits", specialFeatures= "eternet at tables", movableFurniture= True).save()
# room = Rooms(building = 2, number ='305', maxCapacity=15, roomType="Lab",       educationTech = 3, visualAcc = "Bad",  audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 3, number ='308', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "Fine", audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 1, number ='402', maxCapacity=12, roomType="Studio",    educationTech = 2, visualAcc = "Good", audioAcc = "L", physicalAcc= "A").save()
# room = Rooms(building = 2, number ='405', maxCapacity=15, roomType="Lecture",   educationTech = 1, visualAcc = "Bad",  audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 3, number ='408', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "Fine", audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 1, number ='102', maxCapacity=12, roomType="Lab",       educationTech = 1, visualAcc = "Good", audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 2, number ='105', maxCapacity=15, roomType="Lecture",   educationTech = 2, visualAcc = "Bad",  audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 3, number ='108', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "Fine", audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 1, number ='202', maxCapacity=12, roomType="Lab",       educationTech = 1, visualAcc = "checkingifworks", audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 2, number ='205', maxCapacity=15, roomType="Lecture",   educationTech = 1, visualAcc = "Bad",  audioAcc = "D", physicalAcc= "A").save()
# room = Rooms(building = 3, number ='208', maxCapacity=18, roomType="Studio",    educationTech = 3, visualAcc = "Fine", audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 2, number ='305', maxCapacity=15, roomType="Lab",       educationTech = 3, visualAcc = "Bad",  audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 3, number ='308', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "Fine", audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 1, number ='402', maxCapacity=12, roomType="Lab",       educationTech = 2, visualAcc = "Good", audioAcc = "L", physicalAcc= "A").save()
# room = Rooms(building = 2, number ='405', maxCapacity=15, roomType="Lecture",   educationTech = 1, visualAcc = "Bad",  audioAcc = "B", physicalAcc= "A").save()
# room = Rooms(building = 3, number ='408', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "Fine", audioAcc = "B", physicalAcc= "A").save()
=======
room = Rooms(building = 1, number ='101', maxCapacity=24, roomType="Lecture",   educationTech = 1, visualAcc  = "A", audioAcc = "C", physicalAccessibility= "B", movableFurniture = True).save()
room = Rooms(building = 2, number ='102', maxCapacity=24, roomType="Lecture",   educationTech = 2, visualAcc  = "B",  audioAcc = "B", physicalAccessibility= "A", movableFurniture = False).save()
room = Rooms(building = 3, number ='103', maxCapacity=24, roomType="Lecture",   educationTech = 3, visualAcc  = "C", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 4, number ='104', maxCapacity=24, roomType="Lecture",   educationTech = 3, visualAcc  = "A", audioAcc = "A", physicalAccessibility= "A", movableFurniture = False).save()
room = Rooms(building = 5, number ='105', maxCapacity=24, roomType="Lecture",   educationTech = 3, visualAcc  = "B", audioAcc = "B", physicalAccessibility= "A", movableFurniture = False).save()
room = Rooms(building = 6, number ='106', maxCapacity=24, roomType="Lecture",   educationTech = 3, visualAcc  = "C", audioAcc = "B", physicalAccessibility= "B", movableFurniture = True).save()
room = Rooms(building = 7, number ='107', maxCapacity=24, roomType="Lecture",   educationTech = 3, visualAcc  = "A", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 8, number ='108', maxCapacity=24, roomType="Lecture",   educationTech = 3, visualAcc  = "B", audioAcc = "A", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 9, number ='109', maxCapacity=24, roomType="Lecture",   educationTech = 3, visualAcc = "C", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 1, number ='201', maxCapacity=24, roomType="Classroom", educationTech = 1, visualAcc = "A", audioAcc = "B", physicalAccessibility= "C", movableFurniture = False).save()
room = Rooms(building = 2, number ='202', maxCapacity=24, roomType="Lecture",   educationTech = 1, visualAcc = "B",  audioAcc = "A", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 3, number ='203', maxCapacity=24, roomType="Lecture",   educationTech = 3, visualAcc = "C", audioAcc = "B", physicalAccessibility= "A", movableFurniture = False).save()
room = Rooms(building = 4, number ='204', maxCapacity=24, roomType="Lecture",   educationTech = 3, visualAcc = "A",  audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 5, number ='205', maxCapacity=24, roomType="Lecture",   educationTech = 3, visualAcc = "B", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 6, number ='206', maxCapacity=24, roomType="Classroom", educationTech = 2, visualAcc = "C", audioAcc = "A", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 7, number ='207', maxCapacity=30, roomType="Lecture",   educationTech = 1, visualAcc = "A", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 8, number ='208', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "B", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 9, number ='209', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "C", audioAcc = "B", physicalAccessibility= "A", movableFurniture = False).save()
room = Rooms(building = 1, number ='301', maxCapacity=18, roomType="Classroom", educationTech = 1, visualAcc = "A", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 2, number ='302', maxCapacity=15, roomType="Lecture",   educationTech = 1, visualAcc = "B", audioAcc = "A", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 3, number ='303', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "C", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 4, number ='304', maxCapacity=15, roomType="Lecture",   educationTech = 3, visualAcc = "A", audioAcc = "C", physicalAccessibility= "B", movableFurniture = False).save()
room = Rooms(building = 5, number ='305', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "B", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 6, number ='306', maxCapacity=12, roomType="Lab", educationTech = 2, visualAcc = "C", audioAcc = "A", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 7, number ='307', maxCapacity=15, roomType="Lecture",   educationTech = 1, visualAcc = "A",  audioAcc = "B", physicalAccessibility= "C", movableFurniture = True).save()
room = Rooms(building = 8, number ='308', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "B", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()
room = Rooms(building = 9, number ='309', maxCapacity=18, roomType="Lecture",   educationTech = 3, visualAcc = "C", audioAcc = "B", physicalAccessibility= "A", movableFurniture = True).save()

#######
#ROOMS#
#######
roompreference= RoomPreferences(course=1, pref_1=1, pref_2=2, pref_3=3, notes="I want these rooms just bc pls", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=2, pref_1=2, pref_2=5, pref_3=6, notes="I need a room with tech", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=3, pref_1=4, pref_2=5, pref_3=6, notes="I need a room with an A for all 3 accessibilities", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=4, pref_1=4, notes="I want these rooms just because pls", any_Choice = "any").save()
roompreference= RoomPreferences(course=5, pref_1=7, pref_2=8, notes="My course needs good hearing access", any_Choice = "any").save()
roompreference= RoomPreferences(course=6, pref_1=13, pref_2=14, pref_3=15, notes="I need 36 seats", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=7, pref_1=13, pref_2=14, pref_3=15, notes="I need a room with good physical access", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=8, pref_1=19, pref_2=20, pref_3=21, notes="Gimme dis room i neeeeed it", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=9, pref_1=4, pref_2=8, pref_3=7, notes="I need a room with good visual access", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=10, pref_1=2, pref_2=23, pref_3=24, notes="I prefer a room with good physical access", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=11, pref_1=2, pref_2=23, pref_3=24, notes="I would like a room in frost", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=13, pref_1=3, pref_2=5, notes="I prefer a room with good physical access", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=14, notes="I prefer a room with good physical access", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences(course=15,  pref_1=3, notes="I prefer a room in Draper", any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()






# try:
#   os.system('mysql-ctl start')


#   os.system('python migrateDatabase.py')
# except:
#   print "Migration failed"
#   raise

