from app.models import *
import csv
import re
import sys
import os

#The csv file which we are parsing
# TODO Update filepath
csvFileName = 'roomdbver4_1.csv'

###### Room Model #######
# Indices for the columns. The first column is 0.

# TODO Fix the column numbers to match Kenny's clean data

roomNumber          = 1 -1
seatingCapacity     = 3-1
roomType            = 4-1
moveableFurniture   = 5-1
boardTypeNumber     = 7-1
specialFeatures     = 8-1
specialEq           = 13-1
visualAccessibility  = 9-1
physicalAccessibility = 10-1
hearingAccessibility  = 11-1
projector = 15-1
smartboards = 28-1
instructor_computers = 29-1
podium = 25-1
student_workspace = 24-1
chalkboards = 26-1
whiteboards = 27-1
dvd = 16-1
blu_ray = 17-1
audio = 18-1
extro = 20-1
doc_cam = 21-1
vhs = 19-1
mondopad = 22-1
tech_chart = 23-1
building_name = 14-1            # Building name
shortName = 30-1       # Building short name


def addEdTech(room):
    """
    Creates a record in the DB for an EducationTech
    
    param room: a row from the spreadsheet 
    return: an EducationTech object
    """
    pass
    (e, created) = EducationTech.get_or_create(
                        projector = int(room[projector]),
                        smartboards = int(room[smartboards]),
                        instructor_computers = int(room[instructor_computers]),
                        podium = int(room[podium]),
                        student_workspace = int(room[student_workspace]),
                        chalkboards = int(room[chalkboards]),
                        whiteboards = int(room[whiteboards]),
                        dvd = room[dvd],
                        blu_ray = room[blu_ray],
                        audio = room[audio],
                        extro = room[extro],
                        doc_cam = room[doc_cam],
                        vhs = room[vhs],
                        mondopad = room[mondopad],
                        tech_chart = room[tech_chart]
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
                    name = room[building_name],
                    shortName = room[shortName]
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
                    movableFurniture = room[moveableFurniture], 
                    building = addBuilding(room), 
                    number = room[roomNumber].strip(), 
                    # TODO: room[roomNumber] needs to be split and used for building & number. Make a relationship to the Building table using the name. 
                    maxCapacity = room[seatingCapacity].strip(),
                    roomType = room[roomType].strip(),
                    visualAcc = room[visualAccessibility].strip(),
                    audioAcc = room[hearingAccessibility].strip(),
                    physicalAcc = room[physicalAccessibility].strip(),
                    educationTech = addEdTech(room),
                    specializedEq = room[specialEq].strip(),
                    specialFeatures = room[specialFeatures].strip()
                    
                )
    # print(r.number)
    r.save()
                     

def main():
    # try:
    with open(csvFileName, 'rb') as csvfile: #Open CSV file
        roomData = csv.reader(csvfile)
	next(roomData) #Disregard the first line because it is the header
        print "Adding classroom data, this may take a moment."
        for room in roomData: #Iterating through each line
	    print room
            addRoom(room)
    # except Exception as e:
    #     print("You are a failure: ", e)
        
main()
