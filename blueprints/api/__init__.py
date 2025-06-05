
from flask import Blueprint
from middleware.security import isSignedIn

api = Blueprint("api", __name__, url_prefix="/api")


api.register_blueprint(__import__("blueprints.api.common", fromlist=["common"]).common)
api.register_blueprint(__import__("blueprints.api.apicontabilidad", fromlist=["apicontabilidad"]).apicontabilidad)

@isSignedIn
@api.route("/")
def index():
    return "API Index Page"
