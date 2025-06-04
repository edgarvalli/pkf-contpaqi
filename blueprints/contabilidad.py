from flask import Blueprint
from middleware.security import checkSession
from utils.func import render_template_module

contabilidad_route = Blueprint("contabilidad", __name__, url_prefix="/contabilidad")

@contabilidad_route.route("/balanceGeneral")
@checkSession
def balance_general():
    return render_template_module('balance_general.html', title='Balance General')

@contabilidad_route.route('/analisisBalanceGeneral')
@checkSession
def analisis_balance_general():
    return render_template_module('analisis_balance_general.html', title='AnaliticaBG')