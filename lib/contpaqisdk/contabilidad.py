from lib.databases import Databases, DBConfig
from .contaqpi_types import Empresa
from .utils import eliminarDuplicados


class ContabilidadSDK:

    sqlconfig: DBConfig

    def __init__(self, dbconfig: DBConfig):
        self.sqlconfig = dbconfig

    def listaEmpresas(self) -> list[Empresa]:
        query = (
            "SELECT Nombre empresa,AliasBDD dbname FROM GeneralesSQL.dbo.ListaEmpresas;"
        )
        return Databases.fetchall(dbconfig=self.sqlconfig, query=query)

    def cuentasGlobales(self, empresa: str) -> dict:
        query = (
            "SELECT Id id, Codigo cuenta, Nombre nombre "
            f"FROM {empresa}.dbo.Cuentas where LOWER(Nombre) IN ('activo','pasivo','capital');"
        )

        self.sqlconfig.database = empresa
        _cuentasGlobales = Databases.fetchall(dbconfig=self.sqlconfig, query=query)

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

        return data

    def saldoSubCuentas(
        self, dbname, idCuenta: int, ejercicio: int = None
    ) -> list[dict]:

        self.sqlconfig.database = dbname

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

        resultado: list[dict] = Databases.fetchall(dbconfig=self.sqlconfig, query=query)

        saldoCuentas = []

        if len(resultado) > 0:
            for sc in resultado:
                saldo = 0
                for key in sc.keys():
                    if key.startswith("Importes"):
                        saldo += sc[key]

                if saldo != 0:
                    saldoCuentas.append(sc)

        return eliminarDuplicados(saldoCuentas, ejercicio)

    def subcuentas(self, dbname: str, cuentaid: int) -> list[dict]:
        """
        Obtiene las subcuentas de una cuenta específica.

        Args:
            dbname (str): Nombre de la base de datos.
            cuenta (str): Código de la cuenta para buscar sus subcuentas.

        Returns:
            list[dict]: Lista de subcuentas encontradas.
        """
        self.sqlconfig.database = dbname

        query = f"""
                SELECT
                    c.Id idCuenta, c.Codigo cuenta, c.Nombre nombre,
                    a.IdCtaSup cuentaPadre
                FROM Asociaciones a
                INNER JOIN Cuentas c ON a.IdSubCtade=c.id
                WHERE a.IdCtaSup={cuentaid};
            """
        return Databases.fetchall(dbconfig=self.sqlconfig, query=query)
