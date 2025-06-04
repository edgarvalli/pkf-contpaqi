from databases import Databases

db = Databases(
    username="sa",
    password="324Xy371",
    database="DB_Directory",
    instance="COMPAC",
    hostname="10.1.10.6",
    driver='ODBC Driver 17 for SQL Server'
)

db.connect()


uuid = '80F97899'
query = "SELECT NombreEmpresa empresa, DB_DocumentsMetadata metadata FROM DatabaseDirectory"

empresas: list[dict] = db.query(query)

for empresa in empresas:

    print("Buscando en los documentos del GUID {} de la empresa {}".format(
        empresa['metadata'],
        empresa['empresa']
    ))
    query = "SELECT * FROM [{}].dbo.Comprobante WHERE UUID LIKE '{}%'".format(
        empresa.get('metadata'),
        uuid
    )

    result = db.query(query)

    if len(result) > 0:
        print(f"El archivo {uuid} se encontro en {empresa['empresa']} con ADD {empresa['metadata']} ")
        break
