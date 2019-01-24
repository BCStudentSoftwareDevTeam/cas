#activate_this= '/var/www/html/cas-flask/venv/bin/activate_this.py'
activate_this= '/var/www/html/cas-flask-v6/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
#This should be be the base location for the app on the server
sys.path.insert(0,"/var/www/html/cas-flask-v6/")
from app import app as application

