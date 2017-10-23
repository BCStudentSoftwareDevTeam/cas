from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.timeline import timeline
from datetime import datetime, date, time
from flask import json, jsonify

@app.route('/courseTimeline/<tid>',methods=["GET","POST"])
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
  #Monday
  schedule_info = dict()
  schedules = ScheduleDays.select(ScheduleDays.schedule
                          ).join(Course, on=(Course.schedule == ScheduleDays.schedule)
                          ).join(BannerSchedule, on=(BannerSchedule.sid == ScheduleDays.schedule)
                          ).where(ScheduleDays.day == "M"
                          ).where(Course.term == tid
                          ).distinct(
                            ).order_by(BannerSchedule.startTime)
  schedule_list  = []
  for schedule in schedules:
    try:
      num_of_courses = Course.select().where(Course.schedule == schedule.schedule).where(Course.term == tid).count()
    except Exception as e:
      num_of_courses = 0
    schedule_info[schedule.schedule.sid] = [num_of_courses, schedule.schedule.startTime, schedule.schedule.endTime]
    schedule_list.append(schedule.schedule.sid)
  
  obj = timeline(schedule_info,schedule_list)
  google_chart = obj.google_chart_data()
  try: 
    chart_dict = {"google_chart" : google_chart}
    json_str = json.dumps(chart_dict)
  except Exception as e:
    print str(e)
  return jsonify(json_str)
 
  