# from app.allImports import *
# from flask_admin.contrib.peewee import ModelView
# from app.models import *
# class AuthenticatedUser(ModelView):
#     def is_accessible(self):
#         access = False
#         for x in cfg['databaseAdmin']['user']:
#             if authUser(request.environ) == x:
#                 access = True
#         return access
#
# admin.add_view(AuthenticatedUser(Building))
# admin.add_view(AuthenticatedUser(RoomPreferences))
# admin.add_view(AuthenticatedUser(EducationTech))
# admin.add_view(AuthenticatedUser(Division))
# admin.add_view(AuthenticatedUser(BannerSchedule))
# admin.add_view(AuthenticatedUser(TermStates))
# admin.add_view(AuthenticatedUser(Term))
# admin.add_view(AuthenticatedUser(Rooms))
# admin.add_view(AuthenticatedUser(Program))
# admin.add_view(AuthenticatedUser(Subject))
# admin.add_view(AuthenticatedUser(User))
# admin.add_view(AuthenticatedUser(BannerCourses))
# admin.add_view(AuthenticatedUser(Course))
# admin.add_view(AuthenticatedUser(ProgramChair))
# admin.add_view(AuthenticatedUser(DivisionChair))
# admin.add_view(AuthenticatedUser(InstructorCourse))
# admin.add_view(AuthenticatedUser(Deadline))
# admin.add_view(AuthenticatedUser(CourseChange))
# admin.add_view(AuthenticatedUser(InstructorCourseChange))
