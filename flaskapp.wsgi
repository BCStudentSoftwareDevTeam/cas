activate_this = '/var/www/html/cas-flask/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


import sys
import logging

logging.basicConfig(stream=sys.stderr)
#This should be be the base location for the app on the server
sys.path.insert(0,"/var/www/html/cas-flask")
from app import app as application
