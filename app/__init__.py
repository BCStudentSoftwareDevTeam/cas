'''
This file is called by "from app import app" inside the app.py file.

It includes all the imports to be used in the app (from allImports import *).
It also includes all the application files that are used as "pages" in the app
(e.g., "from app import start" imports all the code in start.py that is behind the start.html webpage)
'''

from app import allImports
from allImports import *

# Include an import for every python file that is serving a webpage
# import your new python files here. It is not a part of the module until
# it is imported


from app import course
from app import editCourse
from app import deleteCourse
from app import errorHandler
from app import editProgram
from app import editDivision
from app import editTerm
from app import newTerm
from app import changeAdmin
from app import programManagement
from app import divisionManagement
from app import systemManagement
from app import redirectAdminProgram
from app import deadline
from app import courseManagement
from app import addCourse
from app import excelDownload
from app import databaseAdmin
from app import selectTerm
from app import contributors
from app import editActiveCourses
from app import selectProgram
from app import courseTable
from app import courseTimeline
from app import login_logout
from app import roomResolution
from app import roomResolution
from app import userManagement
