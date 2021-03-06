from flask import session
from random import choice
from string import ascii_letters, digits
from .filters import *
from .. import Config

def autenticado():
    tem_user_id = session.get('id') is not None

    expira = session.get('expiration') or 0
    nao_expirado = expira > datetime.now().timestamp()
    _autenticado = tem_user_id and nao_expirado
    if _autenticado:
        now = int(datetime.now().timestamp())
        session['expiration'] = now + Config.session_duration
    return nao_expirado and tem_user_id

def admin_autenticado():
    return autenticado() and session.get('admin') == True

def random_string(n):
    alfabeto = ascii_letters + digits
    return ''.join(choice(alfabeto) for i in range(n))
