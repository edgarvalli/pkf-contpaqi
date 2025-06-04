from functools import wraps
from datetime import datetime
from lib.databases import Databases
from lib.sqlitedb import SQLiteDB
from lib.contpaqisdk import ContpaqISDK
from utils.func import eliminarDuplicados
from utils.encrypt import encrypt_password
from flask import Blueprint, current_app, request, session, redirect, url_for

api = Blueprint("api", __name__, url_prefix="/api")


def sqlconfig() -> dict:
    return current_app.config["appconfig"]["database"]


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


def saldoSubCuentas(dbname, idCuenta: int, ejercicio):

    sql = Databases(**current_app.config["appconfig"]["database"])
    sql.database = dbname
    sql.connect()

    query = f"""
            SELECT
                sc.IdCuenta idCuenta, e.Ejercicio ejercicio,c.Codigo cuenta,c.Nombre nombre,
                sc.Importes1,sc.Importes2,sc.Importes3,sc.Importes4,
                sc.Importes5,sc.Importes6,sc.Importes7,sc.Importes8,
                sc.Importes9,sc.Importes10,sc.Importes11,sc.Importes12
            FROM SaldosCuentas sc
            INNER JOIN Ejercicios e ON e.Id=sc.Ejercicio
            INNER JOIN Cuentas c ON c.Id = sc.IdCuenta
            INNER JOIN Asociaciones a ON a.IdSubCtade=c.Id
            WHERE e.Ejercicio IN ({ejercicio}, {ejercicio - 1})
            AND sc.Tipo=1 AND a.IdCtaSup={idCuenta};
        """

    resultado = sql.query(query)

    saldoCuentas = []

    if len(resultado) > 0:
        for sc in resultado:
            saldo = 0
            for key in sc.keys():
                if key.startswith("Importes"):
                    saldo += sc[key]

            if saldo != 0:
                saldoCuentas.append(sc)

    sql.close()

    return eliminarDuplicados(saldoCuentas, ejercicio)


@isSignedIn
@api.route("/")
def index():
    return "API Index Page"


@isSignedIn
@api.route("/empresas")
def listado_empresas():
    sdk = ContpaqISDK(sqlconfig())
    empresas = sdk.contabilidad.listaEmpresas()
    return {"error": False, "message": "In Test", "empresas": empresas}


@isSignedIn
@api.route("/<dbname>/cuentasGlobales")
def cuentas_globales(dbname: str):
    sdk = ContpaqISDK(sqlconfig())
    empresas = sdk.contabilidad.cuentasGlobales(empresa=dbname)
    return {"error": False, "message": "", "empresas": empresas}


@isSignedIn
@api.route("/<dbname>/balanceGeneral/<ejercicio>")
def balanceGeneral(dbname, ejercicio: int = None):

    dbconfig = sqlconfig()

    if ejercicio is None:
        ejercicio = datetime.now().year
        ejercicio = int(ejercicio)
    else:
        ejercicio = int(ejercicio)

    sdk = ContpaqISDK(dbconfig)

    data = sdk.contabilidad.cuentasGlobales(empresa=dbname)

    for key in data.keys():

        # Subcuentas de las cuentas globales
        subcuentas: list[dict] = data[key]["subcuentas"]

        # De cada subcuenta se sacan los saldos
        for idx, subcuenta in enumerate(subcuentas):
            saldos: list[dict] = saldoSubCuentas(
                dbname=dbname, idCuenta=subcuenta["idCuenta"], ejercicio=ejercicio
            )
            data[key]["subcuentas"][idx]["saldos"] = {}

            # Se comprueba que las cuentas tengan subcuentas
            if len(saldos) > 0:
                data[key]["subcuentas"][idx]["subcuentas"] = saldos

            # Se obtienen los saldos de cada subcuenta
            totalSaldos = {}
            for s in saldos:
                for saldoKey in s.keys():
                    # Si el saldo del importe no existe en el total se crea si no se suma
                    if saldoKey.startswith("Importes"):
                        if not saldoKey in totalSaldos:
                            totalSaldos[saldoKey] = 0

                        totalSaldos[saldoKey] += s[saldoKey]

                data[key]["subcuentas"][idx]["saldos"] = totalSaldos

        data[key]["subcuentas"] = [
            item for item in data[key]["subcuentas"] if "subcuentas" in item
        ]

    return {"error": False, "data": data}


@isSignedIn
@api.route("/<dbname>/analisisBalanceGeneral/<ejercicio>")
def analisisBalanceGeneral(dbname, ejercicio: int = None):
    if ejercicio is None:
        ejercicio = datetime.now().year
        ejercicio = int(ejercicio)
    else:
        ejercicio = int(ejercicio)

    sdk = ContpaqISDK(sqlconfig())

    data = sdk.contabilidad.cuentasGlobales(empresa=dbname)

    sql = Databases(**current_app.config["appconfig"]["database"])
    sql.database = dbname
    sql.connect()

    cuentasContables = []

    for key in data.keys():
        for subcuenta in data[key]["subcuentas"]:
            query = f"""
                SELECT
                    c.Id idCuenta, c.Codigo cuenta, c.Nombre nombre,
                    a.IdCtaSup cuentaPadre
                FROM Asociaciones a
                INNER JOIN Cuentas c ON a.IdSubCtade=c.id
                WHERE a.IdCtaSup={subcuenta['idCuenta']};
            """

            subcuentas = sql.query(query)

            for sc in subcuentas:
                saldos = saldoSubCuentas(
                    dbname=dbname, idCuenta=sc["idCuenta"], ejercicio=ejercicio
                )

                if len(saldos) > 0:

                    sc["subcuentas"] = saldos
                    totalSaldos = {}
                    for s in saldos:
                        for saldoKey in s.keys():
                            # Si el saldo del importe no existe en el total se crea si no se suma
                            if saldoKey.startswith("Importes"):
                                if not saldoKey in totalSaldos:
                                    totalSaldos[saldoKey] = 0

                                totalSaldos[saldoKey] += s[saldoKey]

                    sc["saldos"] = totalSaldos
                    cuentasContables.append(sc)

    sql.close()

    return {"error": False, "data": cuentasContables}

@isSignedIn
@api.route("/common/<model>/")
def commonSearch(model: str):

    db = SQLiteDB()
    db.connect()

    params = {
        "table": model,
        "conditions": request.args.to_dict()
    }

    reserved_keywords = ["limit","orderby"]

    for key in reserved_keywords:
        if key in params["conditions"]:
            params[key] = params["conditions"][key]
            del params["conditions"][key]

    return db.fetchall(**params)

@isSignedIn
@api.route("/common/<model>/save", methods=["POST"])
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


@isSignedIn
@api.route("/common/<model>/update/<id>", methods=["POST", "UPDATE"])
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


@isSignedIn
@api.route("/users/changePassword/<id>", methods=["POST", "UPDATE"])
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


@isSignedIn
@api.route("/users/delete/<id>", methods=["GET", "DELETE"])
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
    