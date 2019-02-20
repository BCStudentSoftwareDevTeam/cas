from allImports import *
from updateCourse import DataUpdate
import datetime 
from app.logic.authorization import must_be_admin
from app.logic.roomAssignment import RoomAssigner
# import threading
from threading import Thread, Event
from models import *
import sqlite3
import time

# pylint disable=wildcard-import

@app.route("/admin/termManagement", methods=["GET"])
@must_be_admin
def termManagement():
      
      terms = Term.select().where(Term.term_state < 8) # Select all the terms for the terms table with the state buttons
      
      today          = datetime.date.today()       
      term_state     = TermStates.select().order_by(TermStates.order)
      years          = [] #WE WANT THE USER TO HAVE THE ABILITY TO SELECT A YEAR AGO AND THREE YEARS PAST THE CURRENT YEAR
      year           = int(time.strftime("%Y")) - 1   #START WITH ONE YEAR AGO
      for x in range (5):
         if x == 0:
            years.append(str(year))  #APPEND THE ONE YEAR AGO        
         year += 1
         years.append(str(year))    #APPEND CURRENT NUMBER PLUS ONE       
      return render_template("termManagement.html",            
                              terms          = terms,
                              years          = years,                             
                              today          = today,                              
                              term_state     = term_state)
                              
def run_algorithm(termCode, term):
   room_assigner = RoomAssigner(termCode)
   room_assigner.courses_query()
   DATA_SET = room_assigner.create_data_set()
   room_assigner.assign_room(DATA_SET, term)





@app.route("/admin/termManagement/updateTermState", methods=["POST"])
@must_be_admin
def updateTermState():
   
   ''' Updates a term's state to the correct state ID based on state order '''
   # print("Did it get here!")
   data   = request.form # collect data from the view

   term   = Term.get(Term.termCode == data['termCode']) # Retrieve from the database the term whose state was changed by the user and that needs to be updated

   state  = TermStates.get(TermStates.order == data['stateOrder'] ) # Retrieve the state that will be associated with the term

   if data['stateOrder'] == str(5): # Call the Room Assignment Algorithm
      run_algorithm(data['termCode'], term)
     
   term.state = state
   term.term_state = state
   term.save()
      
  
   return redirect(url_for("termManagement")) 
   