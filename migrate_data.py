# This script needs to get the data from the existing sqlite database and save it into mysql 
from peewee import *
import mysql.connector
from app.models import * 
import time
from datetime import datetime

# db = MySQLConnectorDatabase('c9', host = 'localhost', password = '', username = 'nelsonk')
cnx = mysql.connector.connect(database='c9', host = 'localhost', password = '', user = 'nelsonk')
cursor = cnx.cursor()

# add_building = ("INSERT INTO building (bID, name, shortName) VALUES (%s, %s, %s)")
               
# building = Building.select()
# for i in building:
#     bID = int(i.bID)
#     name = str(i.name)
#     shortName = str(i.shortName)
#     # print('did', did)
#     data_building = (bID, name, shortName)
#     cursor.execute(add_building, data_building)

# add_divisions = ("INSERT INTO division (dID, name) VALUES (%s, %s)")

# divisions = Division.select()
# for i in divisions: 
#     dID = int(i.dID)
#     name = str(i.name)
#     data_division = (dID, name)
#     cursor.execute(add_divisions, data_division)
    

add_banner_schedule = ("INSERT INTO bannerschedule (letter, startTime, endTime, sid, order) VALUES (%s,%s,%s,%s,%s)")

banner_schedule = BannerSchedule.select()
for i in banner_schedule: 
    letter = str(i.letter)
    startTime = str(i.startTime)
    print(type(startTime))
    endTime = str(i.endTime) 
    print(type(endTime))
    
    sid = str(i.sid)
    order = int(i.order)
    data_bannerschedule = (letter, startTime, endTime, sid, order)
    cursor.execute(add_banner_schedule, data_bannerschedule)
    

add_termstates = ("INSERT INTO termstates (csID, number, name, order, display_name) VALUES (%s, %s, %s, %s, %s)")

term_states = TermStates.select()
for i in term_states: 
    csID = int(i.csID)
    number = int(i.number)
    name = str(i.name)
    order = int(i.order)
    display_name = str(i.display_name)
    data_termstates = (csID, number, name, order, display_name)
    print(data_termstates)
    cursor.execute(add_termstates, data_termstates)
    
    

# add_educationtech = ("INSERT INTO educationtech (eId, projector, smartboards, instructor_computers, podium, student_workspace, chalkboards, whiteboards, dvd, blu_ray, audio, extro, doc_cam, vhs, mondopad, tech_chart) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

# education_tech = EducationTech.select()
# for i in education_tech:
#     eId = int(i.eId)
#     projector = int(i.projector)
#     smartboards = int(i.smartboards)
#     instructor_computers = int(i.instructor_computers)
#     podium = int(i.podium)
#     student_workspace = int(i.student_workspace)
#     chalkboards = int(i.chalkboards)
#     whiteboards = int(i.whiteboards)
#     dvd = i.dvd
#     blu_ray = i.blu_ray
#     audio = i.audio
#     extro = i.extro
#     doc_cam = i.doc_cam
#     vhs = i.vhs
#     mondopad = i.mondopad
#     tech_chart = i.tech_chart
#     data_educationTech = (eId, projector, smartboards, instructor_computers, podium, student_workspace, chalkboards, whiteboards, dvd, blu_ray, audio, extro, doc_cam, vhs, mondopad, tech_chart)
#     cursor.execute(add_educationtech, data_educationTech)

# add_deadline  = ("INSERT INTO deadline (description, date) VALUES (%s, %s)")

# deadline = Deadline.select()
# for i in deadline: 
#     description = i.description
#     date = i.date 
#     data_deadline = (description, date)
#     cursor.execute(add_deadline, data_deadline)
    

cnx.commit()
cursor.close()
cnx.close()
               
