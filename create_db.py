from create_tables import *
from app.models.models import *

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

users = User( firstName = "Farrah",
                lastName  = "Stamper",
                username  = "stamperf",
                email     = "farrah_stamper@berea.edu",
                isAdmin   = 0,
                bNumber   = "123456789"
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


schedule = ScheduleDays(schedule = "A", day = "R").save(force_insert=True)

schedule = ScheduleDays(schedule = "B", day = "M").save(force_insert=True)


schedule = ScheduleDays(schedule = "B", day = "T").save(force_insert=True)


schedule = ScheduleDays(schedule = "A", day = "R").save(force_insert=True)


schedule = ScheduleDays(schedule = "B", day = "W").save(force_insert=True)


schedule = ScheduleDays(schedule = "A", day = "R").save(force_insert=True)


schedule = ScheduleDays(schedule = "A", day = "M").save(force_insert=True)
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
              state             = 4
            ).save(force_insert = True)

term = Term(  name              = "Spring 2017",
              semester          = "Spring",
              year              = 2017,
              termCode          = 201612,
              editable          = 0,
              state             = 3
            ).save(force_insert = True)
term = Term(  name              = "Fall 2017",
              semester          = "Fall",
              year              = 2017,
              termCode          = 201711,
              editable          = 0,
              state             = 2
            ).save(force_insert = True)

term = Term(  name              = "Spring 2018",
              semester          = "Spring",
              year              = 2018,
              termCode          = 201712,
              editable          = 0,
              state             = 1
            ).save(force_insert = True)
term = Term(  name              = "Fall 2018",
              semester          = "Fall",
              year              = 2018,
              termCode          = 201811,
              editable          = 0,
              state             = 1
            ).save(force_insert = True)

term = Term(  name              = "Fall 2019",
              semester          = "Fall",
              year              = 2019,
              termCode          = 201911,
              editable          = 0,
              state             = 1
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
                  section           = "A",
                  crossListed       = 1,
                  time              = "8:00 - 9:20 am"
                ).save()

course = Course(  bannerRef         = 2,
                  prefix            = "MAT",
                  term              = 201612,
                  section           = "A",
                  schedule          = "B",
                  capacity          = 25,
                  notes             = "Preference2",
                  crossListed       = 1,
                  time             = "10:00 - 11:20 am"
                ).save()

course = Course(  bannerRef         = 3,
                  prefix            = "TAD",
                  term             = 201612,
                  schedule          = "A",
                  section           = "C",
                  capacity          = 20,
                  notes          = "Preference1",
                  crossListed       = 0
                  ).save()
course = Course(  bannerRef         = 8,
                  prefix            = "CHI",
                  term              = 201612,
                  section           = "D",
                  schedule          = "A",

                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()

course = Course(  bannerRef         = 9,
                  prefix            = "CHI",
                  term              = 201711,
                  schedule          = "A",

                  days              =  1,
                  capacity          = 20,
                  notes             = "Preference1",
                  crossListed       = 1
                  ).save()

course = Course(  bannerRef         = 21,
                  prefix            = "CSC",
                  term              = 201611,
                  schedule          = "A",
                  days              = 1,

                  capacity          = 20,
                  notes             = "Preference1",
                  section           = "A",
                  crossListed       = 1
                ).save()

course = Course(  bannerRef         = 22,
                  prefix            = "MAT",
                  term              = 201612,
                  section           = "A",
                  schedule          = "B",

                  days              = 1,



                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                ).save()

course = Course(  bannerRef         = 21,
                  prefix            = "TAD",
                  term             = 201612,
                  schedule          = "A",

                  section           = "A",
                  capacity          = 20,
                  notes          = "Preference1",
                  crossListed       = 0
                  ).save()
course = Course(  bannerRef         = 22,
                  prefix            = "CHI",
                  term              = 201612,
                  section           = "D",
                  schedule          = "A",

                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()

course = Course(  bannerRef         = 22,
                  prefix            = "CHI",
                  term              = 201711,
                  schedule          = "A",

                  capacity          = 20,
                  section           = "E",
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()

course = Course(  bannerRef         = 21,
                  prefix            = "CHI",
                  term              = 201711,
                  section           = "A",
                  schedule          = "B",

                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()

course = Course(  bannerRef         = 11,
                  prefix            = "CHI",
                  term              = 201712,
                  schedule          = "B",

                  section           = "A",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()
course = Course(  bannerRef         = 11,
                  prefix            = "CHI",
                  term              = 201811,
                  schedule          = "B",


                  section           = "A",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()
course = Course(  bannerRef         = 13,
                  prefix            = "FRN",
                  term              = 201611,
                  schedule          = "A",

                  section           = "A",
                  capacity          = 20,
                  notes             = "Preference1",
                  crossListed       = 1
                ).save()

course = Course(  bannerRef         = 14,
                  prefix            = "FRN",
                  term              = 201612,
                  schedule          = "B",

                  section           = "A",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                ).save()

course = Course(  bannerRef         = 15,
                  prefix            = "FRN",
                  term              = 201712,
                  schedule          = "A",

                  capacity          = 20,
                  section           = "A",
                  notes          = "Preference1",
                  crossListed       = 0
                  ).save()
course = Course(  bannerRef         = 15,
                  prefix            = "FRN",
                  term              = 201612,
                  schedule          = "B",

                  capacity          = 20,
                  notes             = "Preference2",
                  section           = "A",
                  crossListed       = 1
                  ).save()

course = Course(  bannerRef         = 17,
                  prefix            = "GER",
                  term              = 201711,
                  schedule          = "B",

                  section           = "A",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()
course = Course(  bannerRef         = 18,
                  prefix            = "GER",
                  term              = 201711,
                  schedule          = "B",
                 days      = 3,
                  section           = "A",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()
course = Course(  bannerRef         = 19,
                  prefix            = "GER",
                  term              = 201712,
                  schedule          = "B",

                  capacity          = 20,
                  section           = "A",
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()
course = Course(  bannerRef         = 19,
                  prefix            = "GER",
                  term              = 201811,
                  schedule          = "B",

                  capacity          = 20,
                  section           = "A",
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()
course = Course(  bannerRef         = 19,
                  prefix            = "GER",
                  term              = 201612,
                  schedule          = "B",

                  section           = "A",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()
course = Course(  bannerRef         = 20,
                  prefix            = "HHP",
                  term              = 201712,
                  schedule          = "B",

                  section           = "A",
                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()
course = Course(  bannerRef         = 21,
                  prefix            = "HLT",
                  term              = 201811,
                  section           = "A",
                  schedule          = "B",

                  capacity          = 20,
                  notes             = "Preference2",
                  crossListed       = 1
                  ).save()


# crossListed = CrossListed(
#                   courseId          = 1,
#                   crosslistedCourse = 1,
#                   verified          = 0,
#                   prefix            = "CSC",
#                   term              = 201611
#                   )

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

# instructor = InstructorSTCourse(  username = "myersco",
#                                 course   = 1
#                               ).save()

######
#Buildings
######
building     = Building(name = 'Ag Building', shortName = "DR").save()
building     = Building(name = 'Tech Building', shortName = "DFT").save()
building     = Building(name = 'Emory Building', shortName="EMR").save()
building     = Building(name = 'Frost Building', shortName="FR").save()
building     = Building(name = 'Ag Building', shortName = "DR").save()
building     = Building(name = 'Tech Building', shortName = "DFT").save()
building     = Building(name = 'Draper', shortName = "DRA").save()
building     = Building(name = 'Knapp Hall', shortName = "KH").save()
building     = Building(name = 'Emery', shortName = "EMY").save()
building     = Building(name = 'Nursing', shortName = "NUR").save()
building     = Building(name = 'Science', shortName = "SC").save()
building     = Building(name = 'Frost', shortName = "FR").save()
building     = Building(name = 'Seabury', shortName = "SEA").save()
building     = Building(name = 'Theater', shortName = "THR").save()
building     = Building(name = 'Bingham', shortName = "BING").save()
building     = Building(name = 'Library', shortName = "LIB").save()
building     = Building(name = 'Emory Building', shortName="EMR").save()
building     = Building(name = 'Frost Building', shortName="FR").save()


###################
#Building Managers#
###################

# bmanager = BuildingManager( username = "heggens",
#                             bmid = 1
#                           ).save()
# bmanager = BuildingManager( username = "myersco",
#                             bmid = 2
#                           ).save()
# bmanager = BuildingManager( username = "pearcej",
#                             bmid = 3
#                           ).save()
bmanager = BuildingManager( username = "stamperf",
                            bmid = 6
                          ).save()


####
#Education Tech for Rooms
#####


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


#### THERE WERE TWO FOR SOME REASON. DELETE ONE
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





#######
#ROOMS#
#######
# TODO: ADD THIS TO ROOMS BELOW, MISSING ATTRIBUTES visualAcc= , audioAcc= ,physicalAcc= , educationTech= , specializedEq= , specialFeatures= ,

room = Rooms(building = 1, educationTech=1, number ='102', maxCapacity=12, roomType="Lab", visualAcc= "A", audioAcc= "A", physicalAcc= "A", specializedEq= "Ethernet @ desks", specialFeatures= "Big ole' windows", movableFurniture=True, lastModified="DATE").save()
room = Rooms(building = 2, educationTech=1, number ='103', maxCapacity=15, roomType="Lecture",  visualAcc= "A", audioAcc= "B" ,physicalAcc= "A",  specializedEq= "Kiln", specialFeatures= "Throwing wheels", movableFurniture= False).save()
room = Rooms(building = 3, educationTech=1,number ='104', maxCapacity=12, roomType="Lab",  visualAcc= "C", audioAcc= "B" ,physicalAcc= "B", specializedEq= "Lab equipment", specialFeatures= "Movable podium", movableFurniture=True).save()
room = Rooms(building = 4, educationTech=1,number ='105', maxCapacity=15, roomType="Lecture",  visualAcc= "A", audioAcc= "C" ,physicalAcc= "B", specializedEq= "Rolly chairs", specialFeatures= "Footstools", movableFurniture= False).save()
room = Rooms(building = 5, educationTech=1,number ='106', maxCapacity=12, roomType="Lab",  visualAcc="A", audioAcc= "B" ,physicalAcc= "C", specializedEq= "Lab equipment", specialFeatures= "Science stuff",movableFurniture=True).save()
room = Rooms(building = 6, educationTech=1,number ='107', maxCapacity=15, roomType="Lecture", visualAcc= "A", audioAcc= "A", physicalAcc= "A", specializedEq= "Ethernet @ desks", specialFeatures= "Big ole' windows", movableFurniture= True).save()
room = Rooms(building = 7, educationTech=1, number ='108', maxCapacity=12, roomType="Workshop", visualAcc= "A", audioAcc= "A", physicalAcc= "B", specializedEq= "Ethernet @ desks", specialFeatures= "Big ole' windows", movableFurniture=False).save()
room = Rooms(building = 8, educationTech=1,number ='109', maxCapacity=15, roomType="Lecture", visualAcc= "A", audioAcc= "A", physicalAcc= "A", specializedEq= "Ethernet @ desks", specialFeatures= "Big ole' windows", movableFurniture= True).save()
room = Rooms(building = 9, educationTech=1, number ='110', maxCapacity=12, roomType="Workshop", visualAcc= "A", audioAcc= "A", physicalAcc= "B", specializedEq= "Ethernet @ desks", specialFeatures= "Big ole' windows", movableFurniture=False).save()
room = Rooms(building = 10, educationTech=1,number ='111', maxCapacity=15, roomType="Lecture",visualAcc= "A", audioAcc= "A", physicalAcc= "B", specializedEq= "Ethernet @ desks", specialFeatures= "Big ole' windows", movableFurniture= True).save()
# room = Rooms(building = 11, educationTech=1,number ='1025', maxCapacity=12, roomType="Something", movableFurniture=1).save()
# room = Rooms(building = 12, educationTech=1,number ='1055', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()
# room = Rooms(building = 1,educationTech=1, number ='1029', maxCapacity=12, roomType="Something", movableFurniture=1).save()
# room = Rooms(building = 4, educationTech=1,number ='1045', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()
# room = Rooms(building = 5, educationTech=1,number ='1023', maxCapacity=12, roomType="Something", movableFurniture=1).save()
# room = Rooms(building = 6,educationTech=1, number ='1050', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()

#################
#Room Preference#
#################

roompreference= RoomPreferences(course= 1, priority=1, pref_1=1,pref_2=2,pref_3=3,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course=3, priority=2, pref_1=2,pref_2=3,pref_3=4,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course=8, priority=3,pref_1=3,pref_2=4,pref_3=5,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 4,priority=3, pref_1=4,pref_2=5,pref_3=6,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 2, priority=3,pref_1=5,pref_2=6,pref_3=7,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 6, priority=2,pref_1=6,pref_2=7,pref_3=8,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 7,priority=1, pref_1=7,pref_2=8,pref_3=9,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 5, priority=2,pref_1=8,pref_2=9,pref_3=10,notes="None",any_Choice = "any").save()
# roompreference= RoomPreferences(course= 9, priority=3,pref_1=9,pref_2=10,pref_3=11,notes="None",any_Choice = "any").save()
# roompreference= RoomPreferences(course= 10, priority=1,pref_1=10,pref_2=11,pref_3=12,notes="None",any_Choice = "any").save()

#####


#ROOMS#


# educationTech= EducationTech(
#   projectors           = 1,
#   smartboards          = 2,
#   instructor_computers = 3,
#   podium               = 3,
#   student_workspace    = 4,
#   chalkboards          = 2,
#   whiteboards          = 2,
#   dvd                  = False,
#   blu_ray              = False,
#   audio                = True,
#   extro                = True,
#   doc_cam              = True,
#   vhs                  = True,
#   mondopad           = True,
#   tech_chart           = False
#   ).save()






room = Rooms(building = 1, educationTech=1, number ='102', maxCapacity=12, roomType="Something", movableFurniture=1).save()
room = Rooms(building = 2,educationTech=1, number ='103', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()
room = Rooms(building = 3, educationTech=1,number ='104', maxCapacity=12, roomType="Something", movableFurniture=1).save()
room = Rooms(building = 4, educationTech=1,number ='105', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()
room = Rooms(building = 5, educationTech=1,number ='106', maxCapacity=12, roomType="Something", movableFurniture=1).save()
room = Rooms(building = 6, educationTech=1,number ='107', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()
room = Rooms(building = 7,educationTech=1, number ='108', maxCapacity=12, roomType="Something", movableFurniture=1).save()
room = Rooms(building = 8, educationTech=1,number ='109', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()
room = Rooms(building = 9,educationTech=1, number ='110', maxCapacity=12, roomType="Something", movableFurniture=1).save()
room = Rooms(building = 10, educationTech=1,number ='111', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()
room = Rooms(building = 11, educationTech=1,number ='1025', maxCapacity=12, roomType="Something", movableFurniture=1).save()
room = Rooms(building = 12, educationTech=1,number ='1055', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()
room = Rooms(building = 1,educationTech=1, number ='1029', maxCapacity=12, roomType="Something", movableFurniture=1).save()
room = Rooms(building = 4, educationTech=1,number ='1045', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()
room = Rooms(building = 5, educationTech=1,number ='1023', maxCapacity=12, roomType="Something", movableFurniture=1).save()
room = Rooms(building = 6,educationTech=1, number ='1050', maxCapacity=15, roomType="Lecture", movableFurniture= 1).save()

roompreference= RoomPreferences(course= 1, priority=1, pref_1=1,pref_2=2,pref_3=3,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course=3, priority=2, pref_1=2,pref_2=3,pref_3=4,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course=8, priority=3,pref_1=3,pref_2=4,pref_3=5,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 4,priority=3, pref_1=4,pref_2=5,pref_3=6,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 2, priority=3,pref_1=5,pref_2=6,pref_3=7,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 6, priority=2,pref_1=6,pref_2=7,pref_3=8,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 7,priority=1, pref_1=7,pref_2=8,pref_3=9,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 5, priority=2,pref_1=8,pref_2=9,pref_3=10,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 9, priority=3,pref_1=9,pref_2=10,pref_3=11,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences(course= 10, priority=1,pref_1=10,pref_2=11,pref_3=12,notes="None",any_Choice = "any").save()

room = Rooms(building = 2,educationTech=1, number ="102", maxCapacity=12, roomType="Lab", visualAcc= True, audioAcc=False, physicalAcc=True, specializedEq="Important stuff", specialFeatures="Special tools that matter a lot", movableFurniture="there 24 chairs and tables").save()

room = Rooms(building = 1, educationTech =1, number ="105", maxCapacity=15,roomType="Lecture",visualAcc= True, audioAcc=True, physicalAcc=True, movableFurniture= " The materials herea are movable").save()

room = Rooms(building = 2,educationTech=1, number ="302", maxCapacity=22, roomType="System", audioAcc=False, physicalAcc=False, specializedEq="Very important things", specialFeatures="Nothing", movableFurniture="there are chairs and tables").save()

room = Rooms(building = 2,educationTech=1, number ="202", maxCapacity=12, roomType="Lab", visualAcc= True, audioAcc=False, physicalAcc=True, specializedEq="Important stuff", specialFeatures="Special tools that matter a lot", movableFurniture="there 24 chairs and tables").save()

room = Rooms(building = 1, educationTech =1, number ="205", maxCapacity=15,roomType="Lecture",visualAcc= True, audioAcc=True, physicalAcc=True, movableFurniture= " The materials herea are movable").save()

room = Rooms(building = 2,educationTech=1, number ="402", maxCapacity=22, roomType="System", audioAcc=False, physicalAcc=False, specializedEq="Very important things", specialFeatures="Nothing", movableFurniture="there are chairs and tables").save()

room = Rooms(building = 1,educationTech=1, number ="106", maxCapacity=22, roomType="System", audioAcc=False, physicalAcc=False, specializedEq="Very important things", specialFeatures="Nothing", movableFurniture="there are chairs and tables").save()

room = Rooms(building = 2,educationTech=1, number ="305", maxCapacity=22, roomType="System", audioAcc=False, physicalAcc=False, specializedEq="Very important things", specialFeatures="Nothing", movableFurniture="there are chairs and tables").save()


roompreference= RoomPreferences(course= 4, pref_1=1,pref_2=2,pref_3=3,notes="None",any_Choice = "any").save()
roompreference= RoomPreferences( course= 1, pref_1=2, pref_2=1, pref_3=3,notes="notes",any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences( course= 2, pref_1=3, pref_2=2, pref_3=1,notes="notes",any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
roompreference= RoomPreferences( course= 3, pref_1=3, pref_2=1, pref_3=2,notes="notes",any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()


# roompreference= RoomPreferences( course= 1, pref_1=1, pref_2=2, pref_3=3,notes="notes",any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
# roompreference= RoomPreferences( course= 2, pref_1=1, pref_2=2, pref_3=3,notes="notes",any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()
#roompreference= RoomPreferences( course= 3, pref_1=1, pref_2=2, pref_3=3,notes="notes",any_Choice = "any", none_choice = "no other rooms work", none_Reason = "None").save()




# try:
#   os.system('mysql-ctl start')


#   os.system('python migrateDatabase.py')
# except:
#   print "Migration failed"
#   raise
state_1 = TermStates(number = 0, order = 0, name = "term_created", display_name = "Term Created").save()
state_2 = TermStates(number = 1, order = 1, name = "schedule_opened", display_name = "Open Scheduling").save()
state_3 = TermStates(number = 2, order = 2, name = "schedule_closed", display_name = "Lock Scheduling").save()
state_3 = TermStates(number = 3, order = 3, name = "roomprefrences_opened", display_name = "Open Room Preferences").save()
state_4 = TermStates(number = 4, order = 4, name = "roomprefrences_closed", display_name = "Lock Room Preferences").save()
state_3 = TermStates(number = 3, order = 3, name = "roomprefrences_opened", display_name = "Open Room Preferences").save()
state_5 = TermStates(number = 5, order = 5, name = "rooms_assigned", display_name = "Assign Rooms").save()
state_6 = TermStates(number = 6, order = 6, name = "term_finished", display_name = "Finish").save()
state_7 = TermStates(number = 7, order = 7, name = "term_archived", display_name = "Archive").save()




# class Current_State(dbModel):
#   csID          = PrimaryKeyField()
#   number        = IntegerField(null = False)
#   name          = CharField(null = False)
#   order         = IntegerField(null = False)
