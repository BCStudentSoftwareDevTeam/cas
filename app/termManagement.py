from allImports import *
from updateCourse import DataUpdate
import datetime 
from app.logic.authorization import must_be_admin
from app.logic.roomAssignment import RoomAssigner
# import threading
from threading import Thread, Event


@app.route("/admin/termManagement", methods=["GET"])
@must_be_admin
def termManagement():
   
      terms          = Term.select().where(Term.term_state < 8) # Select all the terms for the terms table with the state buttons
      
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
                              


def run_algorithm(termCode):
   room_assigner = RoomAssigner(termCode)
   room_assigner.courses_query()
   DATA_SET = room_assigner.create_data_set()
   # print(DATA_SET)
   # print("here")
   room_assigner.assign_room(DATA_SET)
   return 1



@app.route("/admin/termManagement/updateTermState", methods=["POST"])
@must_be_admin
def updateTermState():
   
   ''' Updates a term's state to the correct state ID based on state order '''
   
   data   = request.form # collect data from the view

   term   = Term.get(Term.termCode == data['termCode']) # Retrieve from the database the term whose state was changed by the user and that needs to be updated
   
   state  = TermStates.get(TermStates.order == data['stateOrder'] ) # Retrieve the state that will be associated with the term

   Term.update({Term.state: state.csID}).where(Term.termCode == data['termCode']).execute() # update the state of the specific term retrieved
   
   print('State Order', data['stateOrder'])
   
   if data['stateOrder'] == str(5): # Call the Room Assignment Algorithm
      # term.algorithm_ready = False
      # term.save()
      # print("Term Ready", term.algorithm_ready)
      ready = Event()
      ready.set()
      algorithm_thread = Thread(target = run_algorithm, args = (data['termCode'],))
      # print(algorithm_thread)
      algorithm_thread.start()
      ready.wait()
      # algorithm_thread.join()
      # result = RoomAssigner(data['termCode'])
      # result.run_algorithm() 
 
   return redirect(url_for("termManagement")) 
   
