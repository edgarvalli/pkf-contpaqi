from lib.sqlitedb import SQLiteDB
from flask import Blueprint, request
from middleware.security import protectApi
from utils.encrypt import encrypt_password

common = Blueprint("common", __name__, url_prefix="/common")
unprotected_routes = ["/common/<model>/"]


@common.route("/<model>/")
@protectApi
def commonSearch(model: str):

    db = SQLiteDB()
    db.connect()

    params = {"table": model, "conditions": request.args.to_dict()}

    reserved_keywords = ["limit", "orderby"]

    for key in reserved_keywords:
        if key in params["conditions"]:
            params[key] = params["conditions"][key]
            del params["conditions"][key]

    return db.fetchall(**params)

@common.route("/<model>/save", methods=["POST"])
def commonSave(model: str):
    data = request.get_json()

    if not "data" in data:
        return {
            "error": True,
            "message": "Debe de enviar la propiedad data",
            "data": {},
        }

    db = SQLiteDB()
    db.connect()

    if "password" in data["data"]:
        data["data"]["password"] = encrypt_password(data["data"]["password"])

    return db.save(table=model, data=data["data"])

@common.route("/<model>/update/<id>", methods=["POST", "UPDATE"])
def commonUpdate(model: str, id: int = None):
    data = request.get_json()

    if not "data" in data or id is None:
        return {
            "error": True,
            "message": "Debe de enviar la propiedad data o el id",
            "data": {},
        }

    db = SQLiteDB()
    db.connect()

    return db.update(table=model, record_id=id, data=data["data"])

@common.route("/users/changePassword/<id>", methods=["POST", "UPDATE"])
def userChangePassword(id: int = None):
    if id is None:
        return {
            "error": True,
            "message": "Debe de enviar la propiedad data o el id",
            "data": {},
        }

    data = {"password": encrypt_password(request.get_json()["password"])}

    db = SQLiteDB()
    db.connect()

    return db.update(table="users", record_id=id, data=data)

@common.route("/users/delete/<id>", methods=["GET", "DELETE"])
def usersDelete(id: int = None):
    if id is None:
        return {
            "error": True,
            "message": "Debe de enviar la propiedad data o el id",
            "data": {},
        }

    db = SQLiteDB()
    db.connect()

    return db.delete(table="users", id=id)
