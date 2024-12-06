# Biblioteca Virtual

Documentação do projeto

---

## Recursos do Sistema

- **Autenticação:**
  - Login com Google e GitHub via OAuth.
  - Login e registro convencionais com validação de senha.
  - Recuperação de senha com envio de e-mail.
- **Gerenciamento de Usuários:**
  - Adicionar, editar e excluir usuários com controle de permissões (admin e usuário).
- **Gerenciamento de Livros:**
  - Adicionar, editar e excluir livros com paginação eficiente.
- **Internacionalização:**
  - Suporte a múltiplos idiomas (Português, Inglês e Espanhol).
- **Segurança:**
  - Proteção de rotas, senhas criptografadas e uso de variáveis de ambiente para dados sensíveis.

---

## Pré-requisitos

- Python 3.8 ou superior
- SQLite 3
- Pip (gerenciador de pacotes do Python)
- IDE (recomendado: VS Code ou PyCharm)

---

## Guia de Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate # No Windows: venv\Scripts\activate

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt

4. Adicione suas credenciais ao arquivo .env: Crie um arquivo .env na raiz do projeto e preencha as variáveis de ambiente:
   ```bash
   GOOGLE_CLIENT_ID="sua_google_client_id"
   GOOGLE_CLIENT_SECRET="seu_google_client_secret"
   GITHUB_CLIENT_ID="seu_github_client_id"
   GITHUB_CLIENT_SECRET="seu_github_client_secret"
   MAIL_USERNAME="seu_email"
   MAIL_PASSWORD="sua_senha"
   SECRET_KEY="uma_chave_secreta"

5. Inicie o servidor e configure o banco de dados:
   ```bash
   python app.py

6. Acesse o sistema:

- http://127.0.0.1:5000/login - Página de login
- http://127.0.0.1:5000/usuarios - Gerenciamento de usuários
- http://127.0.0.1:5000/livros - Gerenciamento de livros

## Comandos úteis

### Gerenciar traduções

- Extrair mensagens:
   ```bash
   pybabel extract -F babel.cfg -o messages.pot .

- Inicializar idioma (es)
   ```bash
   pybabel init -i messages.pot -d translations -l es

- Inicializar idioma (en)
   ```bash
   pybabel init -i messages.pot -d translations -l en

- Compilar traduções:
   ```bash
   pybabel compile -d translations

## Tecnologias Utilizadas

### As principais tecnologias utilizadas neste projeto são:

- Backend: Flask (Python)
- Banco de Dados: SQLite
- Autenticação: Flask-Login, Flask-Dance, OAuth
- Internacionalização: Flask-Babel
- Outras Bibliotecas: Bcrypt, Flask-Principal, Flask-Mail

## Licença

Este projeto é open-source e está disponível sob a licença MIT.
