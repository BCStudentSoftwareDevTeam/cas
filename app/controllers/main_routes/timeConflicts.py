from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *

from app.allImports import *
from app.loadConfig import load_config
from app.logic.timeConflicts import get_time_conflict_groups


@main_bp.route("/timeConflicts/", defaults={"tid": 0}, methods=["GET"])
@main_bp.route("/timeConflicts/<tid>", methods=["GET"])
def time_conflicts(tid):
    """Read-only page listing every time conflict on campus for a term, grouped by time slot."""
    terms = Term.select().order_by(-Term.termCode)
    if int(tid) == 0:
        tid = terms[0].termCode  # default to the newest term

    currentTerm = Term.get_or_none(Term.termCode == tid)
    if currentTerm is None:
        abort(404)

    groups = get_time_conflict_groups(currentTerm.termCode)
    return render_template("timeConflicts.html",
                           groups=groups,
                           allTerms=terms,
                           currentTerm=currentTerm,
                           cfg=load_config())