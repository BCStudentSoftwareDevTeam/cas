from __future__ import print_function
'''
Include all imports in this file; it will be called at the beginning of all files.
'''
# We need a bunch of Flask stuff
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import g
from flask import url_for
from flask import flash
from flask import abort
from flask import session
from flask_admin import Admin

from peewee import prefetch

import time
import sys,os, yaml
import pprint
from flask_login import login_user, logout_user, current_user, LoginManager, login_required

from app.loadConfig import load_config

cfg = load_config()

# from app import course
# from app import editCourse
# from app import deleteCourse
# from app import errorHandler
# from app import editProgram
# from app import editDivision
# from app import editTerm
# from app import newTerm
# from app import changeAdmin
# from app import programManagement
# from app import divisionManagement
# from app import termManagement
# from app import redirectAdminProgram
# from app import deadline
# from app import courseManagement
# from app import addCourse
# from app import excelDownload
# from app import databaseAdmin
# from app import selectTerm
# from app import selectTermForRoomPreferences
# from app import contributors
# from app import editActiveCourses
# from app import selectProgram
# from app import courseTable
# from app import courseTimeline
# from app import login_logout
# from app import roomPreference
# from app import roomResolution
# from app import userManagement
# from app import buildingManagement
# from app import removeUser
