from allImports import *
from updateCourse import DataUpdate
import datetime 
from app.logic.authorization import must_be_admin


@app.route("/admin/systemManagement", methods=["GET"])
@must_be_admin
def systemManagement():
   
      terms          = Term.select() # Select all the terms for the terms table with the state buttons
      
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
      return render_template("systemManagement.html",
                              
                              terms          = terms,
                              
                              years          = years,
                              
                              today          = today,
                              
                              term_state     = term_state)
                              




@app.route("/admin/systemManagement/updateTermState", methods=["POST"])
@must_be_admin
def updateTermState():
   ''' Updates a term's state to the correct state ID based on state order '''
   
   data   = request.form # collect data from the view

   term   = Term.get(Term.termCode == data['termCode']) # Retrieve from the database the term whose state was changed by the user and that needs to be updated
   
   state  = TermStates.get(TermStates.order == data['stateOrder'] ) # Retrive the state that will be associated with the term

   Term.update({Term.state: state.csID}).where(Term.termCode == data['termCode']).execute() # update the state of the specific term retrieved
   
   return redirect(url_for("systemManagement")) 