import sqlite3
from flask import flash, redirect, render_template, request, url_for
from . import bp
from db.database import get_db
from datetime import datetime
import pytz
import bcrypt
import re

now = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')

def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        senha = request.form.get('senha')

        if not login:
            flash('Login é obrigatório')
            return render_template("login.html")
        if not senha:
            flash('Senha é obrigatória')
            return render_template("login.html")

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE login = ?', (login,))
            usuario = cursor.fetchone()

            if usuario:
                if usuario[4] == 0: 
                    flash('Usuário está bloqueado')
                    return render_template("login.html")

                if bcrypt.checkpw(senha.encode('utf-8'), usuario[2]):
                    flash('Login bem-sucedido')
                    return redirect(url_for('routes.handle_usuarios'))
                else:
                    flash('Senha incorreta')
                    return render_template("login.html")
            else:
                flash('Usuário não encontrado')
                return render_template("login.html")
        except sqlite3.Error as e:
            flash('Erro ao fazer login: {}'.format(e))
            return render_template("login.html")
        finally:
            db.close()

    return render_template("login.html")

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        senha = request.form.get('senha')
        nome_real = request.form.get("nome_real")

        if not login:
            flash('Login é obrigatório')
            return render_template("register.html")
        if not senha:
            flash('Senha é obrigatória')
            return render_template("register.html")
        if not nome_real:
            flash('Nome real é obrigatório')
            return render_template("register.html")
        if not validar_email(login):
            flash('Login deve ser um e-mail válido')
            return render_template("register.html")

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE login = ?', (login,))
            ver_login = cursor.fetchone()
            if ver_login:
                flash('Login já existe')
                return render_template("register.html")
            else:
                hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                cursor.execute('INSERT INTO usuarios (login, senha, nome_real, created) VALUES (?, ?, ?, ?)', 
                               (login, hashed_senha, nome_real, now))
                db.commit()
                flash('Usuário registrado com sucesso')
                return render_template("login.html")
        except sqlite3.Error as e:
            flash('Erro ao registrar o usuário: {}'.format(e))
            return render_template("register.html")
        finally:
            db.close()

    return render_template("register.html")
