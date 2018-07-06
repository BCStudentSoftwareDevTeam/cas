from allImports import *
import json
from playhouse.shortcuts import model_to_dict, dict_to_model
#Handles populating the appropriate names depending on the specific program/division/building selection in 
#User Management UI.


@app.route('/get_program_chairs/<program>', methods = ["GET"])
def program_chair(program):
    allchairs = ProgramChair.select().where(ProgramChair.pid==program)
    newchairs={}
    for chair in allchairs:
        newchairs[chair.username.username]={'firstname':chair.username.firstName,
                        'lastname':chair.username.lastName,
                        'username':chair.username.username
        }        
    return json.dumps(newchairs)
    
    
@app.route('/get_division_chairs/<division>', methods = ["GET"])
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
 
@app.route('/get_building_managers/<building>', methods = ["GET"])  
def building_manager(building):
    allmanagers = BuildingManager.select().where(BuildingManager.bmid==building)
    newmanagers={}
    for bmanager in allmanagers:
        newmanagers[bmanager.username.username]={'firstname':bmanager.username.firstName,
                        'lastname':bmanager.username.lastName,
                        'username':bmanager.username.username
        }
    return json.dumps(newmanagers)