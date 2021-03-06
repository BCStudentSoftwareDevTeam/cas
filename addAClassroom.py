from app.models import *

def addEdTech(room):
    """
    Creates a record in the DB for an EducationTech
    
    param room: a row from the spreadsheet 
    return: an EducationTech object
    """
    pass
    # FIXME: Do no GET. Only Create. Each room needs its own instance of Ed tech, or changes to one ed tech affect multiple rooms. 
    (e, created) = EducationTech.get_or_create(
                        projector = int(room["projector"]),
                        smartboards = int(room["smartboards"]),
                        instructor_computers = int(room["instructor_computers"]),
                        podium = int(room["podium"]),
                        student_workspace = int(room["student_workspace"]),
                        chalkboards = int(room["chalkboards"]),
                        whiteboards = int(room["whiteboards"]),
                        dvd = room["dvd"],
                        blu_ray = room["blu_ray"],
                        audio = room["audio"],
                        extro = room["extro"],
                        doc_cam = room["doc_cam"],
                        vhs = room["vhs"],
                        mondopad = room["mondopad"],
                        tech_chart = room["tech_chart"]
                    )
    e.save()
    return e

def addBuilding(room):
    """
    Creates a record in the DB for a Building
    
    param room: a row from the spreadsheet
    return: a Building object
    """
    (b, created) = Building.get_or_create(
                    name = room["building_name"],
                    shortName = room["shortName"]
        )
    b.save()
    return b


def addRoom(room):
    """
    Creates a room record in the DB
    
    param room: a row from the spreadsheet
    return: None
    """
    r = Rooms(
                    movableFurniture = room["moveableFurniture"],
                    building = addBuilding(room),
                    number = room["roomNumber"].strip(),
                    # TODO: room[roomNumber] needs to be split and used for building & number. Make a relationship to the Building table using the name. 
                    maxCapacity = int(room["seatingCapacity"]),
                    roomType = room["roomType"].strip(),
                    visualAcc = room["visualAccessibility"].strip(),
                    audioAcc = room["hearingAccessibility"].strip(),
                    physicalAcc = room["physicalAccessibility"].strip(),
                    educationTech = addEdTech(room),
                    specializedEq = room["specialEq"].strip(),
                    specialFeatures = room["specialFeatures"].strip()

                )
    # print(r.number)
    r.save()




room = {"moveableFurniture" : True,
        "roomNumber": "301A",
        "seatingCapacity": 16,
        "roomType": "Lecture",
        "visualAccessibility": "C",
        "physicalAccessibility": "C",
        "hearingAccessibility": "C",
        "specialEq": "",
        "specialFeatures": "",
        "projector": 1,
        "smartboards": 0,
        "instructor_computers": 0,
        "podium": 1,
        "student_workspace": 0,
        "chalkboards": 0,
        "whiteboards": 2,
        "dvd": True,
        "blu_ray": False,
        "audio": True,
        "extro": False,
        "doc_cam": False,
        "vhs": False,
        "mondopad": False,
        "tech_chart": False,
        "building_name" : "Stephenson",
        "shortName": "STE"
}

print("FIXME's need fixed before using this file")
if input("Do you want to continue? 1=YES, 0=NO") == 1:
    addRoom(room)
