from app.models import *
import csv
import re
import sys
import os

#The csv file which we are parsing
csvFileName = 'room-database - Classrooms.csv'

###### Room Model #######
# Indices for the columns.
roomNumber      = 0 
seatingCapacity   = 1
roomType   = 2
moveableFurniture  = 3
educationTech = 4
boardTypeNumber = 5
specialFeatures  = 6
visualAcessibility = 7
physicalAccessibility = 8
hearingAccessibility  = 9
nearestSafeSpace = 10

def addEdTech(edTech):
    #TODO: Add Ed Tech & connect it to the room (Probably return the ID with this function)
    pass

def addBuilding(building):
    #TODO: Add relationship to Building table and connect it to the room (Probably return the ID with this function)
    pass

def addRoom(room):
    # We add a new room instance for each room in the excel using the appropriate indices for each column
    r = Rooms(
                     building = addBuilding(room[roomNumber].strip()), 
                     number = room[roomNumber].strip(), 
                     # TODO: room[roomNumber] needs to be split and used for building & number. Make a relationship to the Building table using the name. 
                     maxCapacity = room[seatingCapacity].strip(),
                     roomType = room[roomType].strip(),
                     visualAcc = room[visualAcessibility].strip(),
                     audioAcc = room[hearingAccessibility].strip(),
                     physicalAcc = room[physicalAccessibility].strip(),
                     maxCapacity = room[seatingCapacity].strip(),
                     maxCapacity = room[seatingCapacity].strip(),
                     educationTech = addEdTech(room[educationTech].strip()),
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