from flask import Blueprint, redirect, request, json
from lib.sqlitedb import SQLiteDB
from middleware.security import checkSession
from utils.func import render_template_module

usuarios_route = Blueprint('Usuarios', __name__, url_prefix='/usuarios')


@usuarios_route.route('/')
@checkSession
def usuarios():
    db = SQLiteDB()
    db.connect()
    users = db.execute_query("SELECT id,displayname,username,email FROM users")

    def parse_dict_to_json(data: dict):
        return json.dumps(data)

    return render_template_module('usuarios', users=users, title='Usuarios', tojsonstr = parse_dict_to_json)

    data = request.form
    

    important_fields = ['username', 'email']

    for field in important_fields:
        if not data[field]:
            return render_template_module('usuarios_error', message=f'El campo {field} es obligatorio')
    
    values = [v for v in data.values()]
    values = tuple(values)

    if id is not None:
        query = "UPDATE users SET "
        params = [f"{key}=?" for key in data.keys()]
        query += ",".join(params)
    
    else:
        values = []
        keys = []

        for key in data.keys():
            keys.append(key)
            values.append("?")

        query = f"INSERT INTO users ({','.join(keys)}) VALUES ({','.join(values)})"

    db = SQLiteDB()
    db.connect()
    db.execute_query(query=query, params=values)
    db.connection.commit()

    return redirect("/app/usuarios")