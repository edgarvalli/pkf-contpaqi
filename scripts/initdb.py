from common import set_root_path

set_root_path()
from lib.sqlitedb import SQLiteDB
from utils.encrypt import encrypt_password

queries = [
    # Tabla de usuarios
    """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        displayname TEXT NOT NULL,
        profile_id INTEGER,
        FOREIGN KEY (profile_id) REFERENCES profiles(id)
    );""",
    # Tabla de perfiles
    """CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        descripcion TEXT
    );""",
    # Tabla de menú
    """CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT,
        icon TEXT,
        parent_id INTEGER,
        sequence INTEGER,
        FOREIGN KEY (parent_id) REFERENCES menu(id)
    );""",
    # Tabla de relación perfiles-menu
    """CREATE TABLE IF NOT EXISTS profile_menu (
        profile_id INTEGER,
        menu_id INTEGER,
        PRIMARY KEY (profile_id, menu_id),
        FOREIGN KEY (profile_id) REFERENCES profiles(id),
        FOREIGN KEY (menu_id) REFERENCES menu(id)
    );""",
]

users = [
    ("admin", encrypt_password("admin"), "evalli@pkf.com.mx", "PKF Admin", 1),
]

menu_options = [("Root", "/app", "", 0, 0)]

db = SQLiteDB("data.db")
db.connect()

for query in queries:
    print(query)
    db.execute_query(query=query)


for user in users:
    db.execute_query(
        "INSERT INTO users (username, password, email, displayname, profile_id) VALUES (?, ?, ?, ?,?)",
        user,
    )

    db.connection.commit()

menu = menu_options[0]
query = "INSERT INTO menu (name,path,icon,parent_id,sequence) VALUES (?,?,?,?,?)"
db.execute_query(query=query, params=menu)
db.connection.commit()

del menu_options[0]

for menu in menu_options:
    query = "INSERT INTO menu (name,path,icon,parent_id,sequence) VALUES (?,?,?,?,?)"
    db.execute_query(query=query, params=menu)
    db.connection.commit()
