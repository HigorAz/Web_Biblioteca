import sqlite3
from flask import current_app, g

DATABASE = 'db/database.db'

def get_db():
    if 'db' not in g:
        print("Criando nova conexão com o banco de dados.")
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        print("Fechando conexão com o banco de dados.")
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('db/usuarios_bd.sql', mode='rb') as f:
        db.cursor().executescript(f.read().decode('utf-8'))
    db.commit()

def init_app(app):
    app.teardown_appcontext(close_db)
