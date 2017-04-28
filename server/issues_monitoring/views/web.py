from flask import render_template, request, redirect, url_for, session
from datetime import datetime
from ..common.utils import autenticado, admin_autenticado
from .. import app, Config, controllers

@app.route('/')
def gerenciar():
    if not autenticado():
        return redirect(url_for('login'))

    admin = admin_autenticado()
    laboratorios = controllers.obter_informacoes_labs(session['id'])
    return render_template('gerenciar.html',
                           admin=admin,
                           laboratorios=laboratorios)

@app.route('/', methods=["POST"])
def gerenciar_post():
    if not autenticado():
        return redirect(url_for('login'))

    user_id = session["id"]
    nome = request.form.get("nome-lab") or ''
    endereco = request.form.get("endereco-lab") or ''
    intervalo_parser = request.form.get("intervalo-parser") or ''
    intervalo_arduino = request.form.get("intervalo-arduino") or ''
    args = [user_id,
            nome,
            endereco,
            intervalo_parser,
            intervalo_arduino]
    if "" not in args:
        controllers.atualizar_informacoes_lab(*args)

    return redirect(url_for("gerenciar"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
 
@app.route('/login')
def login():
    session['id'] = 1
    session['expiration'] = datetime.now().timestamp() + 10000
    session['admin'] = True
    if autenticado():
        return redirect(url_for('gerenciar'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if autenticado():
        return redirect(url_for('gerenciar'))

    usuario = request.form.get('login') or ''
    senha = request.form.get('senha') or ''
    if '' in [usuario, senha]:
        return redirect(url_for('login'))

    (session['id'],
     session['admin']) = controllers.autenticar(usuario, senha)

    if session['id'] is not None:
        now = int(datetime.now().timestamp())
        session['expiration'] = now + Config.session_duration
    else:
        session.pop('id', None)
    return redirect(url_for('login'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro_usuario_sistema.html',
                           autenticado=autenticado())

@app.route('/cadastro', methods=['POST'])
def cadastro_post():
    login = request.form.get('login') or ''
    senha = request.form.get('senha') or ''
    email = request.form.get('email') or ''
    nome = request.form.get('nome') or ''
    args = [login, senha, email, nome]

    if '' not in args:
        controllers.cadastrar_usuario_sistema(login, senha, email, nome)
    return redirect(url_for('login'))

@app.route('/cadastro-usuario-lab')
def cadastro_usuario_lab():
    laboratorios = controllers.listar_laboratorios()
    return render_template('cadastro_usuario_lab.html',
                           laboratorios=laboratorios,
                           autenticado=autenticado())

@app.route('/cadastro-usuario-lab', methods=['POST'])
def cadastro_usuario_lab_post():
    lab_id = request.form.get('id-lab') or ''
    user_id = request.form.get('id-user') or ''
    nome = request.form.get('nome') or ''
    email = request.form.get('email') or ''

    aprovar = admin_autenticado() and request.form.get('aprovar') == 'on'
    args = [lab_id, user_id, nome, email, aprovar]

    if "" not in args:
        controllers.cadastrar_usuario_lab(*args)

    if autenticado():
        url = 'gerenciar'
    else:
        url = 'cadastro_lab_post'
    return redirect(url_for(url))

@app.route('/remover-usuario-lab', methods=["POST"])
def remover_usuario_lab():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    id_lab = request.form.get('id-lab')
    user_id = request.form.get('id-user')
    args = [id_lab, user_id]
    if "" not in args:
        controllers.remover_usuario_lab(*args)

    return redirect(url_for('gerenciar'))

@app.route('/cadastrar-equipamento', methods=["POST"])
def cadastrar_equipamento():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    temp_min = request.form.get('temp-min')
    temp_max = request.form.get('temp-max')
    MAC = request.form.get('endereco-mac')
    args = [temp_min, temp_max, MAC]
    if "" not in args:
        controllers.cadastrar_equipamento(*args)

    return redirect(url_for('gerenciar'))

@app.route('/remover-equipamento', methods=["POST"])
def remover_equipamento():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    _id = request.form.get('id-equipamento')
    if _id != "":
        controllers.remover_equipamento(_id)
    return redirect(url_for('gerenciar'))

@app.route('/robots.txt')
def robots_txt():
    return "User-Agent: *\nDisallow: /"
