from common import set_root_path

set_root_path()
from lib.databases import Databases
from sys import argv


kwargs = {"uuid": None}

for i, arg in enumerate(argv[1:]):
    if arg.startswith("--"):
        arg = arg[2:]
        kwargs[arg] = argv[i + 2]

if kwargs.get("uuid") is None:
    raise ValueError("Debe especificar el UUID del documento a buscar con --uuid")


db = Databases(
    username="sa",
    password="324Xy371",
    database="DB_Directory",
    instance="COMPAC",
    hostname="10.1.10.6",
    driver="ODBC Driver 17 for SQL Server",
)

db.connect()


uuid = kwargs.get("uuid")
query = (
    "SELECT NombreEmpresa empresa, DB_DocumentsMetadata metadata FROM DatabaseDirectory"
)

empresas: list[dict] = db.query(query)

for empresa in empresas:

    print("Buscando en los documentos de la empresa {}".format(empresa["empresa"]))
    queryparams = (uuid,)
    query = f"SELECT * FROM [{empresa["metadata"]}].dbo.Comprobante WHERE UUID = ?"

    result = db.query(query, queryparams)

    if len(result) > 0:
        
        print("\n")
        print(
            f"El archivo {uuid} se encontro en {empresa['empresa']} con ADD {empresa['metadata']} "
        )
        print("\n")

        break
