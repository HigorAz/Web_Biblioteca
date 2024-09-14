import sqlite3
from flask import render_template, request, jsonify
from . import bp
from db.database import get_db
from datetime import datetime
import pytz # type: ignore
import bcrypt
import re

def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

now = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')

@bp.route('/usuarios', methods=['POST', 'GET'])

def handle__usuarios():
    if request.method == 'GET':
        return get_usuarios()
    elif request.method == 'POST':
        return add_usuario()


def get_usuarios():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT *, CASE WHEN status = 1 THEN \'Ativo\' WHEN status = 0 THEN \'Bloqueado\' END AS status_label FROM usuarios')
        dados = cursor.fetchall()
        return render_template("usuarios.html", dados = dados)
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def add_usuario():
    login = request.json.get('login')
    senha = request.json.get('senha')
    nome_real = request.json.get("nome_real")

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
            cursor.execute('INSERT INTO usuarios (login, senha, nome_real) VALUES (?, ?, ?)', (login, hashed_senha, nome_real))
            db.commit()
            return jsonify({'message': 'Dados inseridos com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

#========================================================================================================================================

@bp.route('/usuario/<int:usuario_id>', methods=['DELETE', 'GET', 'PUT', 'PATCH'])

def handle_usuario (usuario_id):
    if request.method == 'GET':
        return get_usuario(usuario_id)
    elif request.method == 'DELETE':
        return delete_usuario(usuario_id)
    elif request.method == 'PUT':
        return update_usuario(usuario_id)
    elif request.method == 'PATCH':
        return ativar_usuario(usuario_id)

def get_usuario(usuario_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT *, CASE WHEN status = 1 THEN \'Ativo\' WHEN status = 0 THEN \'Bloqueado\' END AS status_label FROM usuarios WHERE id = ?', (usuario_id,))
        id = cursor.fetchone()
        if id: 
            return render_template("usuario.html", id = id)
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
        dado = cursor.fetchone()
        if dado: 
            cursor.execute('UPDATE usuarios set status = 0, modified = ? WHERE id = ?', (now, usuario_id,))
            db.commit()
            return jsonify({'message': 'Usuário bloqueado com sucesso'})
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
    login = request.json.get('login')
    senha = request.json.get('senha')
    nome_real = request.json.get("nome_real")
    status = request.json.get("status")


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
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
        id = cursor.fetchone()
        if id:
            cursor.execute('SELECT * FROM usuarios WHERE login = ?', (login,))
            ver_login = cursor.fetchone()
            if ver_login: 
                return jsonify({'error': 'Login já existe'})
            else:
                hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                cursor.execute('UPDATE usuarios set login = ?, senha = ?, nome_real = ?, status = ?, modified = ? WHERE id = ?', (login, hashed_senha, nome_real, status, now, usuario_id,))
                db.commit()
                return jsonify({'message': 'Dados alterados com sucesso!'}), 200
        else:
            return jsonify({'error': 'ID não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()