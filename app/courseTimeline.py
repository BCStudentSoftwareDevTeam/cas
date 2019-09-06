from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.databaseInterface import getCourseTimelineSchedules
from app.logic.timeline import timeline
from datetime import datetime, date, time
from flask import json, jsonify

@app.route('/courseTimeline/', defaults={'tid':0}, methods=["GET"])
@app.route('/courseTimeline/<tid>',methods=["GET","POST"])
@login_required
def courseTimeline(tid):
  #This information has to be passed for the courseManagementSidebar...
  #TODO: Turn this information into a json call so that it doesn't have to be
  #passed in every course management controller.
  terms = Term.select().order_by(-Term.termCode)
  if tid == 0:
    tid = terms[0].termCode
  page = "courseTimeline"
  return render_template('courseTimeline.html',
                            allTerms=terms,
                            page=page,
                            currentTerm=int(tid),
                            cfg = cfg)

@app.route('/courseTimeline/<tid>/json', methods=["GET","POST"])
def timelineJson(tid):
  if int(tid) == 0:
    terms = Term.select().order_by(-Term.termCode)
    tid   = terms[0].termCode
  # print (type(tid))
  google_chart_dict = dict()
  timeline_obj = timeline()
  for key, day in cfg['scheduleDaysShort'].items():
    schedule_info = dict()
    schedule_list  = []
    schedules = getCourseTimelineSchedules(day,tid)
    for schedule in schedules:
      try:
        num_of_courses = Course.select().where(Course.schedule == schedule.schedule).where(Course.term == tid).count()
      except Exception as e:
        num_of_courses = 0
      schedule_info[schedule.schedule.sid] = [num_of_courses, schedule.schedule.startTime, schedule.schedule.endTime]
      schedule_list.append(schedule.schedule.sid)
    timeline_obj.collect_schedule_details(schedule_info,schedule_list)
    google_chart_data = timeline_obj.google_chart_data()
    google_chart_dict[key]=google_chart_data
  try:
    json_str = json.dumps(google_chart_dict)
  except Exception as e:
    print str(e)
  return jsonify(json_str)
