from flask import render_template
from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

from app.controllers.admin_routes import changeAdmin
from app.controllers.admin_routes import courseManagement
from app.controllers.admin_routes import deadline
from app.controllers.admin_routes import divisionManagement
from app.controllers.admin_routes import editActiveCourses
from app.controllers.admin_routes import editDivision
from app.controllers.admin_routes import editProgram
from app.controllers.admin_routes import editTerm
from app.controllers.admin_routes import excelDownload
from app.controllers.admin_routes import newTerm
from app.controllers.admin_routes import programManagement
from app.controllers.admin_routes import redirectAdminProgram
from app.controllers.admin_routes import removeUser
from app.controllers.admin_routes import roomResolution
from app.controllers.admin_routes import termManagement
from app.controllers.admin_routes import userManagement
