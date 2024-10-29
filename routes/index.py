from flask import flash, redirect, render_template, request, jsonify, session, url_for
from . import bp
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github


@bp.route('/')
def index():
    user_name = session.get('user_name')  # Busca o nome do usuário da sessão

    # Verifica se o usuário está logado via Google
    if google.authorized:
        try:
            resp = google.get("/oauth2/v2/userinfo")
            if resp.ok:
                google_data = resp.json()
                user_name = google_data.get("name", "Usuário")
                session['user_name'] = user_name  # Atualiza na sessão
        except Exception as e:
            return f"Erro durante a autenticação: {str(e)}"

    # Verifica se o usuário está autenticado via GitHub
    elif github.authorized:
        try:
            github_data = github.get('/user').json()
            user_name = github_data['login']
            session['user_name'] = user_name  # Atualiza na sessão
        except Exception as e:
            return f"Erro na autenticação com GitHub: {e}"

    # Se nenhum usuário está logado, redireciona para a página de login
    if not user_name:
        flash('Por favor, faça login com Google, GitHub ou suas credenciais.')
        return redirect(url_for('routes.login'))

    return render_template('index.html', user_name=user_name)