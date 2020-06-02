from app.allImports import *
from app.logic.redirectBack import redirect_url
import os
from app.models.models import *
from app.loadConfig import load_config
from functools import wraps

cfg = load_config()

def authUser(env):
    envK = "eppn"
    if (envK in env):
        return env[envK].split("@")[0]
    elif ("DEBUG" in cfg) and cfg["DEBUG"]:
        return cfg["DEBUG"]["user"]
    else:
        return None

def must_be_admin(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    au = AuthorizedUser()
    if not au.user.is_authenticated: # check if user is logged in
      return redirect(url_for('login', next=request.url))

    if not au.user.isAdmin:
      abort(403)

    return f(*args, **kwargs)
  return decorated_function


def can_modify(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    au = AuthorizedUser()
    # if not g.user.is_authenticated: # check if user is logged in
    #   return redirect(url_for('login', next=request.url))
    prefix = kwargs.get('prefix', None)
    
    if au.isAuthorized(prefix):
      kwargs['can_edit'] = True
    else:
      kwargs['can_edit'] = False
    return f(*args, **kwargs)
  return decorated_function

class AuthorizedUser():

    '''
    initializes the authorized user class
    @param username - name of the user accessing the information
    @param prefix   - prefix of the subject being accessed
    '''

    def __init__(self):
        # @private
        self.username = authUser(request.environ)
        if self.username is not None:
            self.user = User.get(User.username == self.username)
        else:
            abort(403)

    def getUsername(self):
        '''
        returns the username of the user
        '''
        return self.username




    def getBuildingManaged(self):
        '''
        returns Select object of all Buildings managed by this user
        '''
        return (BuildingManager.select()
                               .where(BuildingManager.username == self.username)
                               .exists())


    def isProgramChair(self, prefix):
      return (ProgramChair.select()
                          .join(Subject, on=(ProgramChair.pid == Subject.pid))
                          .where(ProgramChair.username == self.username)
                    .where(Subject.prefix == prefix).exists())

    def isDivisionChair(self, prefix):
      return (DivisionChair.select()
                           .join(Division)
                           .join(Program)
                           .join(Subject)
                           .where(Subject.prefix == prefix)
                           .where(DivisionChair.username == self.username))


    def getSubject(self):
        '''
        returns the Subject object associated with this user
        '''
        return Subject.get(Subject.prefix == self.user.lastVisited)



    def isAuthorized(self, prefix):
        '''
        checks to see if user is program chair, admin, or division chair
        '''
        return(self.user.isAdmin or self.isProgramChair(prefix) or self.isDivisionChair(prefix))



    def isUser(self):
        '''
        checks to see if the user is currently in our database, if they are not in the database
        the method will also add them using environ variables. Only if their decscription lvl is
        not a student. If it is a student it will provide a 403 error
        @public
        '''
        #Grab their user level
        page = "getAuthUser.py"
        description = request.environ['description'].lower()
        message =  "This is decription {}".format(description)
        log.writer("DEBUG",page,message)
        if description != 'student':
            try:
		#DEBUG STATEMENTS
		#log.writer("DEBUG",page,str(request.environ['givenName']))
		#log.writer("DEBUG",page,str(request.environ['sn']))
		#log.writer("DEBUG",page,str(request.environ['mail']))
                addUser = User(username   = self.username,
                               firstName  = request.environ['givenName'],
                               lastName   = request.environ['sn'],
                               email      = request.environ['mail'],
                               isAdmin    = 0,
                               lastVisted = None)
                addUser.save(force_insert = True)
                message = "Added user to db with username:({})".format(self.username)
                log.writer("INFO",page,message)
                return True
            except Exception as e:
                message = "Could not make account for username:({0}). {1}".format(self.username,e)
                log.writer("ERROR", page, e)
                abort(404)
                return False
        else:
            message = "Student with username:({}) tried to access the system".format(self.username)
            log.writer("WARNING",page,message)
            abort(403)
            return False


# au = AuthorizedUser()
