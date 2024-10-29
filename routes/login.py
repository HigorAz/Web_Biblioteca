import sqlite3
from dotenv import load_dotenv
from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from . import bp
from db.database import get_db
from datetime import datetime
import pytz
import bcrypt
import re
import os

load_dotenv()

mail = Mail()
s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

now = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')

def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE login = ?", (email,))
        usuario = cursor.fetchone()
        db.close()

        if not usuario:
            flash('E-mail não encontrado no sistema.', category='danger')
            return render_template('forgot_password.html')

        token = s.dumps(email, salt='password_recovery')
        msg = Message('Redefinição de senha', sender=os.getenv("MAIL_USERNAME"), recipients=[email])
        link = url_for('routes.reset_password', token=token, _external=True)
        msg.body = f'Clique no link para redefinir sua senha: {link}'
        mail.send(msg)

        flash('Um link de recuperação de senha foi enviado para o seu email', category='success')
        return redirect(url_for('routes.login'))

    return render_template('forgot_password.html')


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password_recovery', max_age=3600)
    except SignatureExpired:
        return '<h1>O link de redefinição de senha expirou</h1>'
    except BadSignature:
        return '<h1>Token inválido</h1>'

    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE usuarios SET senha = ? WHERE login = ?", (hashed_password, email))
        db.commit()
        db.close()

        flash('Sua senha foi redefinida com sucesso!', category='success')
        return redirect(url_for('routes.login'))
    
    return render_template('reset_password.html')

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

                    session['user_name'] = usuario[3] 
                    
                    return redirect(url_for('index'))
                else:
                    flash('Senha incorreta')
                    return render_template("login.html")
            else:
                flash('Usuário não encontrado')
                return render_template("login.html")
        except sqlite3.Error as e:
            flash(f'Erro ao fazer login: {e}')
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
