from flask import Blueprint, request, redirect, session, url_for
from lib.sqlitedb import SQLiteDB
from utils.encrypt import encrypt_password
from middleware.security import checkSessionLogin
from utils.func import render_template_module

login_blueprint = Blueprint("login", __name__, url_prefix="/login")

@login_blueprint.route("/")
@checkSessionLogin
def login():
    return render_template_module("login_page")

@login_blueprint.route("/singin", methods=["POST"])
def signin():
    username = request.form.get("username")
    password = request.form.get("password")

    db = SQLiteDB()
    db.connect()

    query = f"""
        SELECT * FROM users
        WHERE 
            username = '{username}'
            or email = '{username}'
    """
    user = db.execute_query(query=query)

    if len(user) == 0:
        return redirect(url_for('/login', msg='El usuario o correo no existe!!!'))
    
    password = encrypt_password(password=password)
    user = user[0]
    if user['password'] != password:
        return redirect(url_for('/login', msg='El password esincorrecto!!!'))

    del user["password"]
    session['user_info'] = user
    session['user_singed'] = True

    return redirect('/app')

@login_blueprint.route('/singout')
def singout():
    session.clear()
    return redirect('/login')