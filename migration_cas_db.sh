# pip install peewee==3.9.6
# pip install peewee-migrations==0.3.18

rm -f migrations_cas.json 2> /dev/null

pem init

# See: https://stackoverflow.com/questions/394230/how-to-detect-the-os-from-a-bash-script/18434831
if [[ "$OSTYPE" == "linux-gnu" ]]; then
        # Linux
    sed -i 's/migrate/cas_migrations/g/' migrations_cas.json
elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX
    sed -i '' 's/migrate/cas_migrations/g/' migrations_cas.json
elif [[ "$OSTYPE" == "win64" ]]; then
  #windows operating system
    sed -i  '' 's/migrate/cas_migrations/g/' migrations_cas.json
fi

#pem add app.models.[filename].[classname]
pem add app.models.Division
pem add app.models.BannerSchedule
pem add app.models.TermStates
pem add app.models.Building
pem add app.models.EducationTech
pem add app.models.Deadline
pem add app.models.ScheduleDays
pem add app.models.Term
pem add app.models.Rooms
pem add app.models.Program
pem add app.models.Subject
pem add app.models.User
pem add app.models.BannerCourses
pem add app.models.Course
pem add app.models.CrossListed
pem add app.models.SpecialTopicCourse
pem add app.models.ProgramChair
pem add app.models.DivisionChair
pem add app.models.BuildingManager
pem add app.models.InstructorCourse
pem add app.models.InstructorSTCourse
pem add app.models.CourseChange
pem add app.models.InstructorCourseChange
pem add app.models.CoursesInBanner
pem add app.models.RoomPreferences

pem watch
pem migrate
