from flask import render_template, current_app, request


def init_db_local():

    from lib.sqlitedb import SQLiteDB
    from utils.encrypt import encrypt_password

    print("Initializing local database...")
    db = SQLiteDB(None)
    db.connect()

    print(db.db_path)

    querys = [
        "CREATE TABLE IF NOT Exists empresas (id INTEGER PRIMARY KEY AUTOINCREMENT, dbname TEXT, empresa TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT, displayname TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS categorias (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, seccion INTEGER,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS cuentas (id INTEGER PRIMARY KEY AUTOINCREMENT, cuenta TEXT, nombre TEXT,bd TEXT,categoriaid INTEGER,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
    ]

    users = [
        ("admin", encrypt_password("admin"), "evalli@pkf.com.mx", "PKF Admin"),
    ]

    categorias = [
        ("ACTIVOS", 1),
        ("PASIVOS", 2),
        ("ACTIVO FIJO", 1),
    ]

    cuentas = [
        {
            "cuenta": "110200000",
            "nombre": "BANCOS",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 1,
        },
        {
            "cuenta": "110800000",
            "nombre": "INVERSIONES EN VALORES",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 1,
        },
        {
            "cuenta": "110300000",
            "nombre": "DEUDORES DIVERSOS",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 1,
        },
        {
            "cuenta": "110400000",
            "nombre": "CLIENTES",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 1,
        },
        {
            "cuenta": "110500000",
            "nombre": "IVA ACREDITABLE",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 1,
        },
        {
            "cuenta": "130100000",
            "nombre": "IMPUESTOS A FAVOR",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 1,
        },
        {
            "cuenta": "110700000",
            "nombre": "DEPOSITOS EN GARANTIA",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 1,
        },
        {
            "cuenta": "210100000",
            "nombre": "PROVEEDORES",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 2,
        },
        {
            "cuenta": "210200000",
            "nombre": "ACREEDORES DIVERSOS",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 2,
        },
        {
            "cuenta": "210300000",
            "nombre": "IMPUESTOS POR PAGAR",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 2,
        },
        {
            "cuenta": "210400000",
            "nombre": "IVA POR PAGAR",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 2,
        },
        {
            "cuenta": "210600000",
            "nombre": "PRESTAMO BANCARIO",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 2,
        },
        {
            "cuenta": "123000000",
            "nombre": "MOBILIARIO Y EQUIPO DE OFICINA",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 3,
        },
        {
            "cuenta": "124000000",
            "nombre": "DEP. ACUM. EQUIPO DE OFICINA",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 3,
        },
        {
            "cuenta": "125000000",
            "nombre": "EQUIPO DE COMPUTO",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 3,
        },
        {
            "cuenta": "126000000",
            "nombre": "DEP. ACUM. EQUIPO DE COMPUTO",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 3,
        },
        {
            "cuenta": "121000000",
            "nombre": "EQUIPO DE TRANSPORTE",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 3,
        },
        {
            "cuenta": "122000000",
            "nombre": "DEP.  ACUM. EQUIPO DE TRANSPORTE",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 3,
        },
        {
            "cuenta": "127000000",
            "nombre": "MEJORAS A LOCALES ARRENDADOS",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 3,
        },
        {
            "cuenta": "128000000",
            "nombre": "AMORTIZACION MEJORAS LOC. ARREENDADOS",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 3,
        },
        {
            "cuenta": "130300000",
            "nombre": "GASTOS DE INSTALACION",
            "bd": "ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL",
            "categoriaid": 3,
        },
    ]

    for query in querys:
        db.execute_query(query)

    for user in users:
        db.execute_query(
            "INSERT INTO users (username, password, email, displayname) VALUES (?, ?, ?, ?)",
            user,
        )

        db.connection.commit()

    for categoria in categorias:
        db.execute_query(
            "INSERT INTO categorias (categoria, seccion) VALUES (?, ?)", categoria
        )

        db.connection.commit()

    for cuenta in cuentas:
        db.execute_query(
            "INSERT INTO cuentas (cuenta, nombre, bd, categoriaid) VALUES (?, ?, ?, ?)",
            (cuenta["cuenta"], cuenta["nombre"], cuenta["bd"], cuenta["categoriaid"]),
        )

        db.connection.commit()

    db.execute_query(
        """
        INSERT INTO empresas (dbname, empresa) VALUES
        ('ct2018_TRILLO_ESTRATEGIAS_EMPRESARIAL', 'TRILLO ESTRATEGIAS EMPRESARIALES S.A. DE C.V.'),
        ('ctF1_DE_MONTERREY_CONTA', 'F1 DE MONTERREY'),
        ('ctJOSE_ANGEL_TRILLO_VILLASENOR', 'JOSE ANGEL TRILLO VILLASEÑOR'),
        ('ctPKFMONTERREY', 'PKF MONTERREY SC');
    """
    )

    db.connection.commit()

    db.close()


def obtenerMeses(limit):
    meses = [
        "ENERO",
        "FEBRERO",
        "MARZO",
        "ABRIL",
        "MAYO",
        "JUNIO",
        "JULIO",
        "AGOSTO",
        "SEPTIEMBRE",
        "OCTUBRE",
        "NOVIEMBRE",
        "DICIEMBRE",
    ]
    return meses[:limit]


def eliminarDuplicados(lista_cuentas, año_prioritario=None):
    """
    Elimina cuentas duplicadas (mismo código) priorizando:
    1. El año_prioritario si se especifica
    2. El año más reciente si no se especifica año_prioritario

    Args:
        lista_cuentas: Lista de diccionarios con información de cuentas
        año_prioritario: Año que debe tener prioridad (opcional)

    Returns:
        Lista filtrada sin cuentas duplicadas
    """
    cuentas_por_codigo = {}

    for cuenta in lista_cuentas:
        codigo = cuenta["cuenta"]
        ejercicio = cuenta["ejercicio"]

        if codigo not in cuentas_por_codigo:
            cuentas_por_codigo[codigo] = cuenta
        else:
            actual = cuentas_por_codigo[codigo]

            # Priorizar el año específico si se proporciona
            if año_prioritario is not None:
                if (
                    ejercicio == año_prioritario
                    and actual["ejercicio"] != año_prioritario
                ):
                    cuentas_por_codigo[codigo] = cuenta
            else:
                # Si no hay año prioritario, usar el más reciente
                if ejercicio > actual["ejercicio"]:
                    cuentas_por_codigo[codigo] = cuenta

    return list(cuentas_por_codigo.values())


def render_template_module(template: str, **args):

    module = current_app.blueprints[request.blueprint].url_prefix

    if not module:
        module = ""

    if not template.endswith(".html"):
        template += ".html"

    return render_template(f"{module}/{template}", **args)
