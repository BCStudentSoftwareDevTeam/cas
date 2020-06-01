from app.controllers.admin_routes import *
# from app.controllers.admin_routes.admin_routes import *

from app.allImports import *
from app.logic.authorizedUser import must_be_admin
from app.logic.redirectBack import redirect_url
from app.logic.excelMaker import ExcelMaker
from flask import send_file
from os.path import basename
import os
from app.models.models import Term

@admin_bp.route("/excel/<tid>", methods=["GET"])
@must_be_admin
def makeMainExcel(tid):
    page        = "/" + request.url.split("/")[-1]
    term = Term.get(Term.termCode == tid)

    excel = ExcelMaker() # Creates a class object

    completePath = excel.make_master_file(term)

    filename = completePath.split('/').pop()


    return send_file(completePath,as_attachment=True, attachment_filename=filename)



# @admin_bp.route('/excel/crossListed/<tid>', methods=["GET"])
# @must_be_admin
# def makeSecondaryExcel(tid):
#   page = "/" + request.url.split("/")[-1]
#   term = Term.get(Term.termCode == tid)
#   excel = ExcelMaker()
#   completePath = excel.make_cross_listed_file(term)3
#   return send_file(completePath,as_attachment=True)

@admin_bp.route('/excel/<excel_type>/<tid>', methods=["GET"])
@must_be_admin
def makeSecondaryExcel(excel_type,tid):
  page = "/" + request.url.split("/")[-1]
  term = Term.get(Term.termCode == tid)
  excel = ExcelMaker()
  if excel_type == "crossListed":
    completePath = excel.make_cross_listed_file(term)
  elif excel_type == "specialTopics":
    completePath = excel.make_special_topics_file(term)
  return send_file(completePath,as_attachment=True)
