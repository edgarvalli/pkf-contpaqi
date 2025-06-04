from flask import redirect,url_for, session, request,current_app
from functools import wraps

def checkSession(func):
    @wraps(func)

    def isAllowed(*args, **kwargs):
        if request.path in ['/login', '/logout']:
            return func(*args, **kwargs)
        
        if session.get('user_singed') is None:
            if request.path != '/login':
                return redirect(url_for('login.login', msg='Sesión expirada!!!'))
            return func(*args, **kwargs)

        else:
            
            if request.path == '/login':
                return redirect(url_for('app'))

            return func(*args, **kwargs)


    return isAllowed

def checkSessionLogin(func):
    @wraps(func)
    def isAllowed(*args, **kwargs):
        
        if session.get('user_singed') is None:
            if request.path.startswith('/login'):
                return func(*args, **kwargs)
            else:
                return redirect('/login')
        else:
            if request.path.startswith('/login'):
                return redirect('/app')
            else:
                return func(*args, **kwargs)
    
    return isAllowed