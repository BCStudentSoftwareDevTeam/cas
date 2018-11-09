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


@app.route("/admin/termManagement", methods=["GET"])
@must_be_admin
def termManagement():
   
      terms = Term.select().where(Term.term_state < 8) # Select all the terms for the terms table with the state buttons
      
      for term in terms:
          # Update the term_state column in the term table from the state column 
          # FIX-ME: The state column was not deleted in a measure not to destroy existing data in that column when updating the schema of the database
          term.term_state = term.state
          term.save()
          
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
                              

term_to_dataset = {}

def create_dataset():
   room_assigner = RoomAssigner(termCode)
   room_assigner.courses_query()
   DATA_SET = room_assigner.create_data_set()
   term_to_dataset[termcode] = DATA_SET

   
def run_algorithm(termCode, term):
   # t = Term.get(Term.termCode == termCode)
   # t.algorithm_running = True
   # t.save()
   # print(t.algorithm_running)
   room_assigner = RoomAssigner(termCode)
   room_assigner.courses_query()
   DATA_SET = room_assigner.create_data_set()
   # print(DATA_SET)
   # print("before assigning")
   room_assigner.assign_room(DATA_SET, term)
   # print("after assigning")
   # t.algorithm_running = False
   # t.save()
   # print(t.algorithm_running)






@app.route("/admin/termManagement/updateTermState", methods=["POST"])
@must_be_admin
def updateTermState():
   
   ''' Updates a term's state to the correct state ID based on state order '''
   
   data   = request.form # collect data from the view

   term   = Term.get(Term.termCode == data['termCode']) # Retrieve from the database the term whose state was changed by the user and that needs to be updated
   
   if term.editable is False:
      time.sleep(500)
   state  = TermStates.get(TermStates.order == data['stateOrder'] ) # Retrieve the state that will be associated with the term

   # if data['stateOrder'] == str(4): 
   #    if data['termCode'] not in term_to_dataset:
   #       create_dataset()
     
   if data['stateOrder'] == str(5): # Call the Room Assignment Algorithm
      term.editable = False
      run_algorithm(data['termCode'], term)
     
   
   # while term.algorithm_running:
   #    time.sleep(500)
      # print("Running...")
   
   term.state = state
   term.save()
      
  
   # print("Done Updating: {0}".format(term.state.csID))
   return redirect(url_for("termManagement")) 
   
