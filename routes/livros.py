import sqlite3
from flask import redirect, render_template, request, jsonify, url_for, flash
from flask_login import current_user
from . import bp
from db.database import get_db
from datetime import datetime
import pytz
import re

now = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')

@bp.route('/livros', methods=['POST', 'GET'])
def handle_livros():
    if request.method == 'GET':
        return get_livros()
    elif request.method == 'POST':
        return add_livro()

def get_livros():
    # Parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = 8  # Número de registros por página
    offset = (page - 1) * per_page
    try:
        db = get_db()
        cursor = db.cursor()
        # Consultar o total de registros
        cursor.execute("SELECT COUNT(*) AS total FROM livros")
        total_records = cursor.fetchone()['total']
        cursor.execute(
            'SELECT * FROM livros LIMIT ? OFFSET ?', 
            (per_page, offset)
        )
        dados = cursor.fetchall()

        # Calcular o total de páginas
        total_pages = (total_records + per_page - 1) // per_page

        return render_template("livros.html", dados=dados, page=page, total_pages=total_pages)
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def add_livro():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    genero = request.form.get('genero')
    paginas = request.form.get('paginas')

    if not titulo or not autor or not genero or not paginas:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO livros (titulo, autor, genero, paginas, created) VALUES (?, ?, ?, ?, ?)', 
            (titulo, autor, genero, paginas, now)
        )
        db.commit()
        return jsonify({'message': 'Livro adicionado com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/livro/<int:livro_id>', methods=['DELETE', 'POST', 'GET', 'PUT'])
def handle_livro(livro_id):
    if getattr(current_user, 'cargo', '') != 'admin':
        flash("Acesso negado: Apenas administradores podem acessar esta página.", "danger")
        return redirect(url_for('routes.forbidden'))
    if request.method == 'GET':
        return get_livro(livro_id)
    
    elif request.method == 'POST':
        if request.form.get('_method') == 'DELETE':
            return delete_livro(livro_id)
        elif request.form.get('_method') == 'PUT':
            return update_livro(livro_id)

    elif request.method == 'PUT':
        return update_livro(livro_id)
    
    elif request.method == 'DELETE':
        return delete_livro(livro_id)

def get_livro(livro_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM livros WHERE id = ?', (livro_id,))
        livro = cursor.fetchone()
        if livro:
            return render_template("edit_livro.html", livro=livro)
        else:
            return jsonify({'error': 'Livro não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def delete_livro(livro_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM livros WHERE id = ?', (livro_id,))
        livro = cursor.fetchone()
        if livro:
            cursor.execute('DELETE FROM livros WHERE id = ?', (livro_id,))
            db.commit()
            return jsonify({'message': 'Livro excluído com sucesso'})
        else:
            return jsonify({'error': 'Livro não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def update_livro(livro_id):
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    genero = request.form.get('genero')
    paginas = request.form.get('paginas')

    if not titulo or not autor or not genero or not paginas:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM livros WHERE id = ?', (livro_id,))
        livro = cursor.fetchone()

        if not livro:
            return jsonify({'error': 'Livro não encontrado'}), 404

        cursor.execute(
            'UPDATE livros SET titulo = ?, autor = ?, genero = ?, paginas = ?, modified = ? WHERE id = ?',
            (titulo, autor, genero, paginas, now, livro_id)
        )
        db.commit()
        return jsonify({'message': 'Livro atualizado com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/livros/create', methods=['GET'])
def create_livro():
    return render_template('create_livro.html')
