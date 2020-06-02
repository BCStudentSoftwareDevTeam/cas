from app.controllers.admin_routes import *
from app.logic.authorizedUser import AuthorizedUser, must_be_admin


from app.allImports import *
import json
from playhouse.shortcuts import model_to_dict, dict_to_model
#Handles populating the appropriate names depending on the specific program/division/building selection in
#User Management UI.

from app.models.models import *

@admin_bp.route('/get_program_chairs/<program>', methods = ["GET"])
@must_be_admin
def program_chair(program):
    allchairs = ProgramChair.select().where(ProgramChair.pid==program)
    newchairs={}
    for chair in allchairs:
        newchairs[chair.username.username]={'firstname':chair.username.firstName,
                        'lastname':chair.username.lastName,
                        'username':chair.username.username
        }
    return json.dumps(newchairs)


@admin_bp.route('/get_division_chairs/<division>', methods = ["GET"])
@must_be_admin
def division_chair(division):
#returns all users for a specific division to ajax call when removing users from a specific division in User Management UI
    allchairs = DivisionChair.select().where(DivisionChair.did==division)
    print(allchairs)
    newchairs={}
    for dchair in allchairs:
        newchairs[dchair.username.username]={'firstname':dchair.username.firstName,
                        'lastname':dchair.username.lastName,
                        'username':dchair.username.username
        }
    return json.dumps(newchairs)

@admin_bp.route('/get_building_managers/<building>', methods = ["GET"])
@must_be_admin
def building_manager(building):
    allmanagers = BuildingManager.select().where(BuildingManager.bmid==building)
    newmanagers={}
    for bmanager in allmanagers:
        newmanagers[bmanager.username.username]={'firstname':bmanager.username.firstName,
                        'lastname':bmanager.username.lastName,
                        'username':bmanager.username.username
        }
    return json.dumps(newmanagers)


@admin_bp.route('/get_admin/', methods = ["GET"])
@must_be_admin
def administrators():
    alladmin = User.select().where(User.isAdmin == 1)
    newadmin={}
    for admin in alladmin:
        newadmin[admin.username]={'firstname':admin.firstName,
                        'lastname':admin.lastName,
                        'username':admin.username
        }
    return json.dumps(newadmin)
