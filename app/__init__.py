from flask import Flask

# from app import logtool
# import logging

app = Flask(__name__)
from app.allImports import *

# def load_config(file):
#     with open(file, 'r') as ymlfile:
#         cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
#     return cfg





# secret config first
cfg = load_config("app/secret_config.yaml")
app.secret_key = cfg["secret_key"]
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.loadConfig import load_config
from app import login_logout
from app.login_manager import *
# regular config
# cfg = load_config()


from app.controllers.main_routes import main_bp as main_bp
app.register_blueprint(main_bp)

from app.controllers.error_routes import error_bp as error_bp
app.register_blueprint(error_bp)

from app.controllers.admin_routes import admin_bp as admin_bp
app.register_blueprint(admin_bp)



# log = logtool.Log()


#FIXME: Refactor as secret.yaml file
# app.config.from_object('settings')


# admin = Admin(app)

# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())


#FIXME: What is this for?
# @app.context_processor
# def inject_dict_for_all_templates():
    #HACK
    # au = AuthorizedUser()
    # try:
        # return dict({'isAdmin': au.isAdmin(), 'cfg': cfg, "isBuildingManager": au.isBuildingManager()})
    # except Exception as e:
        # return dict({'isAdmin': au.isAdmin(), 'cfg': cfg, "isBuildingManager": au.isBuildingManager()})
