from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url

@app.route('/courseTimeline/<tid>',methods=["GET","POST"])
def courseTimeline(tid):
    
    return render_template('courseTimeline.html',
                            cfg = cfg)
                            