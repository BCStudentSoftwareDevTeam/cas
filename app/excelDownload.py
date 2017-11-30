from allImports import *
from app.logic.authorization import must_be_admin
from app.logic.redirectBack import redirect_url
from app.logic.excelMaker import ExcelMaker
from flask import send_file
from os.path import basename
import os

@app.route("/excel/<tid>", methods=["GET"])
@must_be_admin
def makeExcel(tid):

    page        = "/" + request.url.split("/")[-1]
    term = Term.get(Term.termCode == tid)
    excel = ExcelMaker()
    completePath = excel.make_master_file(term)


    return send_file(completePath,as_attachment=True)



@app.route('/excel/crossListed/<tid>', methods=["GET"])
@must_be_admin
def makeCrossListedExcel(tid):
  page = "/" + request.url.split("/")[-1]
  term = Term.get(Term.termCode == tid)
  excel = ExcelMaker()
  completePath = excel.make_cross_listed_file(term)
  return send_file(completePath,as_attachment=True)
