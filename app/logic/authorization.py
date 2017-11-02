from functools import wraps
from flask import g, redirect, request, abort, url_for
from app.models import Program, ProgramChair
from app.models import Subject 
from app.models import Division, DivisionChair


def isProgramChair(username, prefix):
  return (ProgramChair.select()
                      .join(Subject, on=(ProgramChair.pid == Subject.pid))
                      .where(ProgramChair.username == username)
                .where(Subject.prefix == prefix).exists())
                
def isDivisionChair(username, prefix):
  return (DivisionChair.select()
                       .join(Division)
                       .join(Program)
                       .join(Subject)
                       .where(Subject.prefix == prefix)
                       .where(DivisionChair.username == username))
                       
def isAuthorized(user, prefix):
  isAdminBool = user.isAdmin
  isProgramChairBool = isProgramChair(user.username, prefix)
  isDivisionChairBool = isProgramChair(user.username, prefix)
  
  return(isAdminBool or  isProgramChairBool or isDivisionChairBool)



def can_modify(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):

    if not g.user.is_authenticated: # check if user is logged in
      return redirect(url_for('login', next=request.url))
    prefix = kwargs.get('prefix', None)
    
    if isAuthorized(g.user, prefix):
      kwargs['can_edit'] = True
    else:
      kwargs['can_edit'] = False
      
    
      
    return f(*args, **kwargs)
    
  return decorated_function
  
  
def must_be_authorized(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not g.user.is_authenticated: # check if user is logged in

      return redirect(url_for('login', next=request.url))
    prefix = kwargs['prefix']
    
    if not isAuthorized(g.user, prefix):
      abort(403)
    
    return f(*args, **kwargs)
    
  return decorated_function
  
def must_be_admin(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not g.user.is_authenticated: # check if user is logged in
      return redirect(url_for('login', next=request.url))
    
    if not g.user.isAdmin:
      abort(403)
    
    return f(*args, **kwargs)
    
  return decorated_function