from functools import wraps
from flask import g
from app.models import Term

def define_term_code_and_prefix(f):
    @wraps(f)
    def set_tId_and_prefix(*args, **kwargs):
        #Set default values if no values were found
        if not 'prefix' in kwargs:
            last_visited = g.user.lastVisited
            if g.user.lastVisited is not None:
                kwargs['prefix'] = last_visited.prefix
            else:
                kwargs['prefix'] = Subject.get().prefix
        if not 'tID' in kwargs:
            termCode = (Term.select(Term.termCode).where(Term.state == 0))[0].termCode
            kwargs['tID'] = termCode
        print kwargs
            
        return f(*args, **kwargs)
    return set_tId_and_prefix


''' Author-> CDM 20160728
Purpose: we store the prefix as lastVisted and 
call function with after saving last visited
@param -tid      {{integer}} -> term identification number
@param -prefix   {{string}}  -> course prefix
@param -username {{string}}  -> unique id for users

@return -list [tid,prefix]   -> contains the value sets
'''
def save_last_visited(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.user.lastVisited = kwargs['prefix']
        g.user.save()
        return f(*args, **kwargs)
        
    return decorated_function