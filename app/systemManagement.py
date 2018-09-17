from allImports import *
from updateCourse import DataUpdate
import datetime 
from app.logic.authorization import must_be_admin


@app.route("/admin/systemManagement", methods=["GET"])
@must_be_admin
def systemManagement():
      terms          = Term.select()
      users          = User.select()
      program        = Program.get()
      today          = datetime.date.today()
      term_state     = TermStates.select().order_by(TermStates.order)
      #WE WANT THE USER TO HAVE THE ABILITY TO SELECT A YEAR AGO AND THREE YEARS PAST THE CURRENT YEAR
      years       = []
      #START WITH ONE YEAR AGO
     
      year  = int(time.strftime("%Y")) - 1   
      for x in range(5):
         if x == 0:
            #APPEND THE ONE YEAR AGO
            years.append(str(year))          
         year += 1
         #APPEND CURRENT NUMBER PLUS ONE
         years.append(str(year))          
      return render_template("systemManagement.html",
                              terms          = terms,
                              years          = years,
                              program        = program,
                              users          = users,
                              isAdmin        = g.user.isAdmin,
                              today          = today,
                              term_state     = term_state)
                              
#Tomorrow: 

#Then I will start working on the reverse actions which occurs under open room preferences, assign rooms and finish panels

#Thursday and Friday
# In addition to updating the state for the terms I should also implement functionality that opens/locks scheduling, open/lock room preferences, assign rooms

@app.route("/admin/systemManagement/updateTermState", methods=["POST"])
@must_be_admin
def updateTermState():
   data = request.form

   # Updates the term's state to the correct state ID based on state order
   term = Term.get(Term.termCode == data['termCode'])
   state = TermStates.get(TermStates.order == data['stateOrder'] )
   print("This is the state", state.order)
   # term.state = state.csID
   print ('state csID', state.csID)
   term = Term.update({Term.state: state.csID}).where(Term.termCode == data['termCode']).execute()
   # print("Updated state again", term.state.order)
   # print("State again id", term.state.csID)
   # term.save()

   
   
   # message = "Course: #{0} has been added".format(course.cId)
   # flash("Course has successfully been added!")
   # log.writer("INFO", current_page, message)
   
   return redirect(url_for("systemManagement")) 