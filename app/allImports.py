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
from flask_admin import Admin
import time
import sys,os
import subprocess

import pprint
from app import models
# all the database models
from models import *   
from flask_login import login_user, logout_user, current_user, LoginManager, login_required

''' Creates an Flask object; @app will be used for all decorators.
from: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
"A decorator is just a callable that takes a function as an argument and
returns a replacement function. See start.py for an example"
'''

def authUser(env):
    envK = "eppn"
    if (envK in env):
        return env[envK].split("@")[0]
    elif ("DEBUG" in app.config) and app.config["DEBUG"]:
        return cfg["DEBUG"]["user"]
    else:
        return None

'''Creates the AbsolutePath based off of the relative path.
Also creates the directories in path if they are not found.
@param {string} relaitivePath - a string of directories found in config.yaml
@param {string} filename - the name of the file that should be in that directory
@return {string} filepath -returns the absolute path of the directory'''
'''TODO: ADD @PARAm for make dirs'''
def getAbsolutePath(relaitivePath,filename=None,makeDirs=False):
    filepath = os.path.join(sys.path[0],relaitivePath)
    if makeDirs == True:
        try:
            os.makedirs(filepath)
        except:
            pass
    if filename != None:
        filepath = os.path.join(filepath,filename)
    return filepath

from app import logtool
log = logtool.Log()

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object('settings')
# Builds all the database connections on app run
# Don't panic, if you need clarification ask.
admin = Admin(app)

import logging
# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())



@app.before_request
def before_request():
    mainDB.get_conn() #.connect() caused a crash 20180108 CDM
    g.user = current_user       # Careful using g elsewhere. See: https://stackoverflow.com/questions/15083967/when-should-flask-g-be-used

# @app.after_request
# def add_header(response):
#     response.cache_control.private = True
#     response.cache_control.public = False
#     return response


@app.teardown_request
def teardown_request(exception):
    mainDB.close()
    
@login_manager.user_loader
def load_user(username):
  return User.get(User.username == username)

from app.logic.getAuthUser import AuthorizedUser
@app.context_processor
def inject_dict_for_all_templates():
    gitHash = subprocess.check_output(["git", "rev-parse","HEAD"]).strip()[:8]

    #HACK
    au = AuthorizedUser()
    try: 
        return dict({'isAdmin': au.isAdmin(), 'cfg': cfg, "isBuildingManager": au.isBuildingManager(), 'gitHash': gitHash})
    except Exception as e:
        return dict({'isAdmin': au.isAdmin(), 'cfg': cfg, "isBuildingManager": au.isBuildingManager(), 'gitHash': gitHash})
