from app.controllers.admin_routes import *
from app.logic.authorizedUser import AuthorizedUser, must_be_admin

from app.allImports import *
from app.updateCourse import DataUpdate
import datetime
from app.logic.roomAssignment import RoomAssigner
from threading import Thread, Event
from app.models import *
import sqlite3
import time
from app.models.models import Term, TermStates
from app.loadConfig import load_config

@admin_bp.route("/admin/termManagement", methods=["GET"])
@must_be_admin
def termManagement():
      au = AuthorizedUser()
      terms = Term.select().where(Term.term_state <= 8) # Select all the terms for the terms table with the state buttons

#      for term in terms:
         #  Update the term_state column in the term table from the state column
         #  FIX-ME: The state column was not deleted in a measure not to destroy existing data in that column when updating the schema of the database
#          term.term_state = term.state
#          print(term.termCode)
#          term.save()

      today          = datetime.date.today()
      term_state     = TermStates.select().order_by(TermStates.order)
      years          = [] #WE WANT THE USER TO HAVE THE ABILITY TO SELECT A YEAR AGO AND THREE YEARS PAST THE CURRENT YEAR
      year           = int(time.strftime("%Y")) - 1   #START WITH ONE YEAR AGO
      for x in range (5):
         if x == 0:
            years.append(str(year))  #APPEND THE ONE YEAR AGO
         year += 1
         years.append(str(year))    #APPEND CURRENT NUMBER PLUS ONE
      cfg = load_config()
      return render_template("termManagement.html",
                              terms          = terms,
                              years          = years,
                              today          = today,
                              term_state     = term_state,
                              cfg = cfg,
                              isAdmin = au.user.isAdmin)

def run_algorithm(termCode, term):
   room_assigner = RoomAssigner(termCode)
   room_assigner.courses_query()
   DATA_SET = room_assigner.create_data_set()
   room_assigner.assign_room(DATA_SET, term)





@admin_bp.route("/admin/termManagement/updateTermState", methods=["POST"])
@must_be_admin
def updateTermState():

   ''' Updates a term's state to the correct state ID based on state order '''

   data   = request.form # collect data from the view

   term   = Term.get(Term.termCode == data['termCode']) # Retrieve from the database the term whose state was changed by the user and that needs to be updated

   state  = TermStates.get(TermStates.order == data['stateOrder'] ) # Retrieve the state that will be associated with the term

   if data['stateOrder'] == str(5): # Call the Room Assignment Algorithm
      run_algorithm(data['termCode'], term)

   term.state = state
   term.term_state = state
   term.save()


   return redirect(url_for("admin.termManagement"))
