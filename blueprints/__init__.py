from flask import Blueprint, render_template
from .contabilidad import contabilidad_route
from .usuarios import usuarios_route
from middleware.security import checkSession

approute = Blueprint('App Router', __name__, url_prefix='/app')

approute.register_blueprint(contabilidad_route)
approute.register_blueprint(usuarios_route)

@approute.route("/")
@checkSession
def index():
    return render_template('dashboard.html',title='Dashboard')