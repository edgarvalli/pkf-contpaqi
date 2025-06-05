from functools import wraps
from flask import redirect, url_for, session, request


def protectApi(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(request.path)
        if not request.path.startswith("/api/"):
            return {
                "error": True,
                "message": "API no disponible",
                "data": {},
            }
        
        userSigned = session.get("user_singed", None)

        if userSigned is None:
            return {
                "error": True,
                "message": "No se ha iniciado sesión",
                "data": {},
            }
        return f(*args, **kwargs)
    
    return decorated_function

def checkSession(func):
    @wraps(func)
    def isAllowed(*args, **kwargs):
        if request.path in ["/login", "/logout"]:
            return func(*args, **kwargs)

        if session.get("user_singed") is None:
            if request.path != "/login":
                return redirect(url_for("login.login", msg="Sesión expirada!!!"))
            return func(*args, **kwargs)

        else:

            if request.path == "/login":
                return redirect(url_for("app"))

            return func(*args, **kwargs)

    return isAllowed

def checkSessionLogin(func):
    @wraps(func)
    def isAllowed(*args, **kwargs):

        if session.get("user_singed") is None:
            if request.path.startswith("/login"):
                return func(*args, **kwargs)
            else:
                return redirect("/login")
        else:
            if request.path.startswith("/login"):
                return redirect("/app")
            else:
                return func(*args, **kwargs)

    return isAllowed
