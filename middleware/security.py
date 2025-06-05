from functools import wraps
from flask import redirect, url_for, session, request


def apiAllowed(func):
    @wraps(func)
    def isAllowed(*args, **kwargs):
        print("API Allowed Middleware Loaded")
        if request.path.startswith("/api/"):
            if session.get("user_singed") is None:
                return {
                    "error": True,
                    "message": "No tienes permisos para acceder a esta API",
                    "data": {},
                }
            return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return isAllowed

def isSignedIn(func):
    @wraps(func)
    def isAllowed(*args, **kwargs):
        if request.path in ["/login", "/logout"]:
            return func(*args, **kwargs)

        if session.get("user_singed"):
            if request.path == "/login":
                return redirect(url_for("app"))
            return func(*args, **kwargs)

        else:

            if request.path != "/login":
                return redirect(url_for("login", msg="Sesión expirada!!!"))
            return func(*args, **kwargs)

    return isAllowed


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
