
from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")


api.register_blueprint(__import__("blueprints.api.common", fromlist=["common"]).common)
api.register_blueprint(__import__("blueprints.api.apicontabilidad", fromlist=["apicontabilidad"]).apicontabilidad)


@api.route("/")
def index():
    return {
        "error": False,
        "message": "API is running",
        "data": {
            "version": "1.0.0",
            "status": "OK"
        }
    }
