from flask import render_template
from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.controllers.main_routes import main_routes
from app.controllers.main_routes import addCourse
from app.controllers.main_routes import buildingManagement
from app.controllers.main_routes import contributors
from app.controllers.main_routes import course
from app.controllers.main_routes import courseTable
from app.controllers.main_routes import courseTimeline
from app.controllers.main_routes import deleteCourse
from app.controllers.main_routes import editCourse
from app.controllers.main_routes import roomPreference
from app.controllers.main_routes import selectProgram
from app.controllers.main_routes import selectTerm
from app.controllers.main_routes import selectTermForRoomPreferences
