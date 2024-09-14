from flask import Flask
from db.database import init_app, init_db
from routes import bp as routes_bp

app = Flask(__name__, template_folder= "templates")

# Inicializar o banco de dados
init_app(app)

# Registrar o Blueprint das rotas
app.register_blueprint(routes_bp)

@app.route('/initdb')
def initialize_db():
    init_db()
    return 'Banco de dados inicializado!'

if __name__ == '__main__':
    app.run(debug=True)
