from flask import render_template
from flask import Blueprint

error_bp = Blueprint('error', __name__)

from app.controllers.error_routes import errorHandler
