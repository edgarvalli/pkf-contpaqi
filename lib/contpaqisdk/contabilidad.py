from lib.databases import Databases, DBConfig
from .contaqpi_types import Empresa

class ContabilidadSDK:

    sqlconfig: DBConfig

    def __init__(self, dbconfig: DBConfig):
        self.sqlconfig = dbconfig

    def listaEmpresas(self) -> list[Empresa]:
        query = "SELECT Nombre empresa,AliasBDD dbname FROM GeneralesSQL.dbo.ListaEmpresas;"
        return Databases.fetchall(dbconfig=self.sqlconfig,query=query)
    
    def cuentasGlobales(self, empresa: str) -> dict:
        query = "SELECT Id id, Codigo cuenta, Nombre nombre " \
                f"FROM {empresa}.dbo.Cuentas where LOWER(Nombre) IN ('activo','pasivo','capital');"

        self.sqlconfig.database = empresa
        _cuentasGlobales = Databases.fetchall(dbconfig=self.sqlconfig,query=query)

        data = {}

        # De cada cuenta global se busca sus cuentas de balance
        for cuenta in _cuentasGlobales:

            query = f"""
                SELECT
                    a.idCtaSup idCuentaPadre,a.idSubCtade idCuenta,
                    a.CtaSup cuentaPadre, a.SubCtade cuenta, c.Nombre nombre
                FROM Asociaciones a
                INNER JOIN Cuentas c ON c.Id=a.IdSubCtade
                WHERE CtaSup = '{cuenta["cuenta"]}'
            """

            data[cuenta["cuenta"]] = {
                "cuenta": cuenta["cuenta"],
                "nombre": cuenta["nombre"],
                "saldo": False,
                "subcuentas": Databases.fetchall(self.sqlconfig, query=query),
            }

        return  data
