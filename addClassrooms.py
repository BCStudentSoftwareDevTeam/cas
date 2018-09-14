from app.models import *
import csv
import re
import sys
import os

#The csv file which we are parsing
# TODO Update filepath
csvFileName = 'room-database.csv'

###### Room Model #######
# Indices for the columns. The first column is 0.

# TODO Fix the column numbers to match Kenny's clean data

roomNumber          = 2 
seatingCapacity     = 7
roomType            = 8
moveableFurniture   = 9
boardTypeNumber     = 12
specialFeatures     = 13
specialEq           = 11
visualAccessibility  = 14
physicalAccessibility = 15
hearingAccessibility  = 16
projector = 18
smartboards = 31
instructor_computers = 32
podium = 28
student_workspace = 27
chalkboards = 29
whiteboards = 30
dvd = 19
blu_ray = 20
audio = 21
extro = 23
doc_cam = 24
vhs = 22
mondopad = 25
tech_chart = 26
building_name = 1            # Building name
shortName = 33       # Building short name


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
    print(r.number)
    r.save()
                     

def main():
    # try:
    with open(csvFileName, 'rb') as csvfile: #Open CSV file
        roomData = csv.reader(csvfile)
        next(roomData) #Disregard the first line because it is the header
        print "Adding classroom data, this may take a moment."
        for room in roomData: #Iterating through each line
            addRoom(room)
    # except Exception as e:
    #     print("You are a failure: ", e)
        
main()