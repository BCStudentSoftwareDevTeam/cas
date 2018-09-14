from app.models import *
import csv
import re
import sys
import os

#The csv file which we are parsing
# TODO Update filepath
csvFileName = 'room-database.csv'

###### Room Model #######
# Indices for the columns.

# TODO Fix the column numbers to match Kenny's clean data

roomNumber      = 0 
seatingCapacity   = 1
roomType   = 2
moveableFurniture  = 3
# educationTech = 4
boardTypeNumber = 5
specialFeatures  = 6
visualAcessibility = 7
physicalAccessibility = 8
hearingAccessibility  = 9
# nearestSafeSpace = 10
projector = "???"
smartboards = "???"
instructor_computers = "???"
podium = "???"
student_workspace = "???"
chalkboards = "???"
whiteboards = "???"
dvd = "???"
blu_ray = "???"
audio = "???"
extro = "???"
doc_cam = "???"
vhs = "???"
mondopad = "???"
tech_chart = "???"
name = "???"            # Building name
shortName = "???"       # Building short name


def addEdTech(room):
    """
    Creates a record in the DB for an EducationTech
    
    param room: a row from the spreadsheet 
    return: an EducationTech object
    """
    pass
    e = EducationTech(
                        projector = room[projector],
                        smartboards = room[smartboards],
                        instructor_computers = room[instructor_computers],
                        podium = room[podium],
                        student_workspace = room[student_workspace],
                        chalkboards = room[chalkboards],
                        whiteboards = room[whiteboards],
                        dvd = room[dvd],
                        blu_ray = room[blu_ray],
                        audio = room[audio],
                        extro = room[extro],
                        doc_cam = room[doc_cam],
                        vhs = room[vhs],
                        mondopad = room[mondopad],
                        tech_chart = room[tech_chart]
                    ).save()
    return e

def addBuilding(room):
    """
    Creates a record in the DB for a Building
    
    param room: a row from the spreadsheet
    return: a Building object
    """
    b = Building(
                    name = room[building_name],
                    shortName = room[shortName]
        ).save()
    return b

def addRoom(room):
    """
    Creates a room record in the DB
    
    param room: a row from the spreadsheet
    return: None
    """
    r = Rooms(
                    building = addBuilding(room), 
                    number = room[roomNumber].strip(), 
                    # TODO: room[roomNumber] needs to be split and used for building & number. Make a relationship to the Building table using the name. 
                    maxCapacity = room[seatingCapacity].strip(),
                    roomType = room[roomType].strip(),
                    visualAcc = room[visualAcessibility].strip(),
                    audioAcc = room[hearingAccessibility].strip(),
                    physicalAcc = room[physicalAccessibility].strip(),
                    educationTech = addEdTech(room),
                    specializedEq = None, # TODO: Check what needs to be done for this. I couldn't find specializedEq column in the csv 
                    specialFeatures = room[specialFeatures].strip(),
                    movableFurniture = room[moveableFurniture].strip()
                ).save()
                     

def main():
    try:
        with open(csvFileName, 'rb') as csvfile: #Open CSV file
            roomData = csv.reader(csvfile)
            next(courses) #Disregard the first line because it is the header
            print "Adding classroom data, this may take a moment."
            for room in roomData: #Iterating through each line
                addRoom(room)
    except e:
        print("You are a failure: ", e)
        
main()