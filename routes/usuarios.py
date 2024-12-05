import sqlite3
from flask import redirect, render_template, request, jsonify, url_for
import jwt
from . import bp
from db.database import get_db
from datetime import datetime
import pytz
import bcrypt
import re

def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

now = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')

@bp.route('/usuarios', methods=['POST', 'GET'])
def handle_usuarios():
    if request.method == 'GET':
        return get_usuarios()
    elif request.method == 'POST':
        return add_usuario()

def get_usuarios():
    # Parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = 8  # Número de registros por página
    offset = (page - 1) * per_page
    try:
        db = get_db()
        cursor = db.cursor()
        # Consultar o total de registros
        cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
        total_records = cursor.fetchone()['total']
        cursor.execute('SELECT *, CASE WHEN status = 1 THEN \'Ativo\' WHEN status = 0 THEN \'Bloqueado\' END AS status_label, CASE WHEN cargo = 1 THEN \'Administrador\' WHEN cargo = 0 THEN \'Membro\' END AS cargo_label FROM usuarios LIMIT ? OFFSET ?', (per_page, offset))
        dados = cursor.fetchall()

        # Calcular o total de páginas
        total_pages = (total_records + per_page - 1) // per_page

        return render_template("usuarios.html", dados = dados, page=page, total_pages=total_pages)
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def add_usuario():
    login = request.json.get('login')
    senha = request.json.get('senha')
    nome_real = request.json.get("nome_real")
    cargo = request.json.get('cargo')

    if not login:
        return jsonify({'error': 'login é obrigatório'})
    if not senha:
        return jsonify({'error': 'senha é obrigatória'})
    if not nome_real:
        return jsonify({'error': 'nome_real é obrigatório'})
    if not validar_email(login):
        return jsonify({'error': 'login deve ser um e-mail válido'})
    
    try: 
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE login = ?', (login,))
        ver_login = cursor.fetchone()
        if ver_login: 
            return jsonify({'error': 'Login já existe'})
        else:
            hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO usuarios (login, senha, nome_real, cargo) VALUES (?, ?, ?, ?)', (login, hashed_senha, nome_real, cargo))
            db.commit()
            return jsonify({'message': 'Dados inseridos com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

#========================================================================================================================================

@bp.route('/usuario/<int:usuario_id>', methods=['DELETE', 'POST', 'GET', 'PUT', 'PATCH'])
def handle_usuario(usuario_id):
    if request.method == 'GET':
        return get_usuario(usuario_id)
    
    elif request.method == 'POST':
        if request.form.get('_method') == 'DELETE':
            return delete_usuario(usuario_id)
        elif request.form.get('_method') == 'PUT':
            return update_usuario(usuario_id)

    elif request.method == 'PUT':
        return update_usuario(usuario_id)
    
    elif request.method == 'DELETE':
        return delete_usuario(usuario_id)
    
    elif request.method == 'PATCH':
        return ativar_usuario(usuario_id)


def get_usuario(usuario_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT *, CASE WHEN status = 1 THEN \'Ativo\' WHEN status = 0 THEN \'Bloqueado\' END AS status_label, CASE WHEN cargo = 1 THEN \'Administrador\' WHEN cargo = 0 THEN \'Membro\' END AS cargo_label FROM usuarios WHERE id = ?', (usuario_id,))
        usuario = cursor.fetchone()
        if usuario: 
            return render_template("edit_usuario.html", usuario=usuario)
        else:
            return jsonify({'error': 'ID não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def delete_usuario(usuario_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
        usuario = cursor.fetchone()
        if usuario: 
            cursor.execute('UPDATE usuarios set status = 0, modified = ? WHERE id = ?', (now, usuario_id,))
            db.commit()
            cursor.execute('SELECT *, CASE WHEN status = 1 THEN \'Ativo\' WHEN status = 0 THEN \'Bloqueado\' END AS status_label FROM usuarios WHERE id = ?', (usuario_id,))
            usuario_atualizado = cursor.fetchone()
            return render_template("usuario.html", usuario=usuario_atualizado)
        else:
            return jsonify({'error': 'ID não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def ativar_usuario(usuario_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
        dado = cursor.fetchone()
        if dado: 
            cursor.execute('UPDATE usuarios set status = 1, modified = ? WHERE id = ?', (now,usuario_id,))
            db.commit()
            return jsonify({'message': 'Usuário ativado com sucesso'})
        else:
            return jsonify({'error': 'ID não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def update_usuario(usuario_id):
    login = request.form.get('login')
    senha = request.form.get('senha') 
    nome_real = request.form.get('nome_real')
    status = request.form.get('status')
    cargo = request.form.get('cargo')

    if not validar_email(login):
        return jsonify({'error': 'login deve ser um e-mail válido'}), 400

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({'error': 'ID não encontrado'}), 404

        cursor.execute('SELECT * FROM usuarios WHERE login = ? AND id != ?', (login, usuario_id))
        if cursor.fetchone():
            return jsonify({'error': 'Login já existe'}), 409

        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('UPDATE usuarios SET login = ?, senha = ?, nome_real = ?, status = ?, cargo = ?, modified = ? WHERE id = ?', 
                       (login, hashed_senha, nome_real, status, cargo, now, usuario_id))
        db.commit()

        cursor.execute('SELECT *, CASE WHEN status = 1 THEN \'Ativo\' WHEN status = 0 THEN \'Bloqueado\' END AS status_label, CASE WHEN cargo = 1 THEN \'Administrador\' WHEN cargo = 0 THEN \'Membro\' END AS cargo_label FROM usuarios WHERE id = ?', (usuario_id,))
        usuario_atualizado = cursor.fetchone()

        return render_template("usuario.html", usuario=usuario_atualizado)

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()