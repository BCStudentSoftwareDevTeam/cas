from app.allImports import *
from app.logic.redirectBack import redirect_url
import os
from app.models import BuildingManager

class AuthorizedUser:

    '''
    initializes the authorized user class
    @param username - name of the user accessing the information
    @param prefix   - prefix of the subject being accessed
    '''

    def __init__(self, prefix = None):
        # @private
        self.username = authUser(request.environ)
        self.prefix = prefix


    '''
    returns the username of the user
    '''
    def getUsername(self):
        return self.username
        
        
    '''
    checks to see if the user is an admin
    @public
    '''

    def checkIfUser(self):
        user = User.select().where(User.username == self.username)
        if user.exists():
            return user
        else: 
            result = self.isUser()
            return result
    
    
    def isAdmin(self):
        user = User.select().where(User.username == self.username)
        if user.exists():
            user = user.get()
            return user.isAdmin
        else:
            return None
    
    
    def isBuildingManager(self):
        return (BuildingManager.select()
                               .where(BuildingManager.username == self.username)
                               .exists())

    '''
    check to see if the user is a division chair
    @private
    '''

    def isDivisionChair(self):
        subject = self.getSubject()

        return DivisionChair.select().where(
            DivisionChair.username == self.username).where(
            DivisionChair.did == subject.pid.division.dID).exists()

    '''
    check to see if the user is program chair
    @private
    '''

    def isProgramChair(self):
        subject = self.getSubject()

        return ProgramChair.select().where(
            ProgramChair.username == self.username).where(
            ProgramChair.pid == subject.pid.pID).exists()
    '''
    gets the subject we are trying to get
    @private
    '''

    def getSubject(self):
        return Subject.get(Subject.prefix == self.prefix)

    '''
    checks to see if user is program chair, admin, or division chair
    @public
    '''

    def isAuthorized(self):
        isAdminBool = self.isAdmin()
        isProgramChairBool = self.isProgramChair()
        isDivisionChairBool = self.isDivisionChair()
        return(isAdminBool or isProgramChairBool or isDivisionChairBool)
        
    
    '''
    checks to see if the user is currently in our database, if they are not in the database
    the method will also add them using environ variables. Only if their decscription lvl is 
    not a student. If it is a student it will provide a 403 error
    @public
    '''
    def isUser(self):
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
