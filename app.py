from flask import Flask, redirect, request, url_for, session, render_template, jsonify, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from datetime import datetime, timedelta
from routes import bp as routes_bp 
import os
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv()

app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

google_blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"), 
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to='index', 
    scope=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"] 
)
app.register_blueprint(google_blueprint, url_prefix="/login")

github_blueprint = make_github_blueprint(
    client_id=os.getenv("GITHUB_CLIENT_ID"), 
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    scope="user:email"
)
app.register_blueprint(github_blueprint, url_prefix="/login")

app.register_blueprint(routes_bp)

@app.route("/")
def index():
    
    if google.authorized:
        print("Usuário está autorizado via Google")
        try:
            resp = google.get("/oauth2/v2/userinfo")
            if resp.ok:
                google_data = resp.json()
                user_name = google_data.get("name", "Usuário")
                print(f"Nome do usuário: {user_name}")
                return render_template('index.html', user_name=user_name)
            else:
                print(f"Erro ao obter dados do Google: {resp.status_code}")
                return f"Erro ao obter dados do Google: {resp.status_code} {resp.text}"
        except Exception as e:
            print(f"Erro durante a autenticação: {str(e)}")
            return f"Erro durante a autenticação: {str(e)}"

    elif github.authorized:
        try:
            github_data = github.get('/user').json()
            user_name = github_data['login'] 
            print(f"Usuário GitHub logado: {user_name}")
        except Exception as e:
            print(f"Erro na autenticação com GitHub: {e}")

    if not google_data and not github_data:
        print("Usuário não está logado, redirecionando para a página de login...")
        flash('Por favor, faça login com Google ou GitHub.')
        return redirect(url_for('routes.login'))

    print(f"Renderizando a página para o usuário: {user_name}")
    return render_template('index.html', user_name=user_name)

@app.route("/logout")
def logout():
    session.clear() 
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
