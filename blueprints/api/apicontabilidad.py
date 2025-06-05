from flask import Blueprint, current_app
from middleware.security import protectApi
from datetime import datetime
from lib.contpaqisdk import ContpaqISDK

apicontabilidad = Blueprint("apicontabilidad", __name__, url_prefix="/contabilidad")

def sqlconfig() -> dict:
    return current_app.config["appconfig"]["database"]

@apicontabilidad.route("/empresas")
@protectApi
def listado_empresas():
    sdk = ContpaqISDK(sqlconfig())
    empresas = sdk.contabilidad.listaEmpresas()
    return {"error": False, "message": "In Test", "empresas": empresas}


@apicontabilidad.route("/<dbname>/cuentasGlobales")
@protectApi
def cuentas_globales(dbname: str):
    sdk = ContpaqISDK(sqlconfig())
    empresas = sdk.contabilidad.cuentasGlobales(empresa=dbname)
    return {"error": False, "message": "", "empresas": empresas}


@apicontabilidad.route("/<dbname>/balanceGeneral/<ejercicio>")
@protectApi
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
            saldos: list[dict] = sdk.contabilidad.saldoSubCuentas(
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


@apicontabilidad.route("/<dbname>/analisisBalanceGeneral/<ejercicio>")
@protectApi
def analisisBalanceGeneral(dbname, ejercicio: int = None):
    if ejercicio is None:
        ejercicio = datetime.now().year
        ejercicio = int(ejercicio)
    else:
        ejercicio = int(ejercicio)

    sdk = ContpaqISDK(sqlconfig())

    data = sdk.contabilidad.cuentasGlobales(empresa=dbname)
    cuentasContables = []

    for key in data.keys():
        for subcuenta in data[key]["subcuentas"]:

            subcuentas = sdk.contabilidad.subcuentas(dbname=dbname,cuentaid=subcuenta['idCuenta'])
            
            for sc in subcuentas:
                saldos: dict = sdk.contabilidad.saldoSubCuentas(
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

    return {"error": False, "data": cuentasContables}

