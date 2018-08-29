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
      term_states     = TermState.select().order_by()
      term_to_state  = {}
      
      for term in terms: 
         term_to_state[term.termCode, term.name] = term.new_state.order
         
         
      # print (term_to_state)
      
      
      
      
      # for i in term_states:
      #    print (i.display_name)
      # for i in terms:
      #    print (i.new_state.order)
      # for i in terms:
      #    print i.new_state.name
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
                              term_to_state   = term_to_state,
                              term_states     = term_states)