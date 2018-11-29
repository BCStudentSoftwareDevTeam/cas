from allImports import *
import sys
from models import *
from app.logic.authorization import must_be_admin
from app.logic.redirectBack import redirect_url

@app.route("/newTerm", methods=["POST"])
@must_be_admin
def newterm():
  page        = request.path  
  
  try: 
    data            = request.form
    info_key        = int(data['keyValue'])
    term_year       = data['year']
    same_year       = [11]
    #USE THE VALUE OF THE POST TO GET THE NAME
    semester_name   = cfg['termInfo'][info_key]   
    term_name       = semester_name + " " + term_year
    #LOOK AT CONFIG.YAML ANY KEY THAT REQUIRES THE SAME YEAR FOR THE TERM CODE PLACE INSIDE THE same_year LIST
    for x in same_year:
      if info_key == x:
        term_code = term_year + str(info_key)
      else:
        term_code = str(int(term_year)-1) + str(info_key)
    #STOP DUPLICATES#
    #I NEED TO ENSURE THAT THE TERM CODE DOES NOT ALREADY EXSIST IN THE DATABASE
    newTerm = Term.select().where(Term.termCode == term_code)
    if newTerm:
      message = "Term: {} already exists in the database.".format(term_name)
      log.writer("ERROR",page,message)
      flash(message,'error')
    else:
      #ADD THE INFORMATION TO THE DATABASE
      newTerm = Term(termCode=int(term_code), name=term_name, semester=semester_name, year=int(term_year), state=1, term_state = 1)
      newTerm.save(force_insert=True)
      message = "Term: Term {} has been created".format(data['year'])
      log.writer("INFO", page, message)
      flash("Term successfully created")
  except Exception as e:
    log.writer("ERROR","newTerm",e)
  return redirect(redirect_url())