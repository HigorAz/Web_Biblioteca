Guia de Instalação:

1. Através de uma IDE, é necessário que você possua o SQLite e Python instalados;
2. Agora que você baixou este repositório, dentro do VSCODE, abra a pasta do projeto;
3. Instale os seguintes módulos:
	- pip install flask
	- pip install pysqlite3
	- pip install bcrypt
  	- pip install python-dotenv
4. Adicione as suas credenciais Google, GitHub e de e-mail no arquivo .env, conforme o modelo abaixo:
	
 	GOOGLE_CLIENT_ID="" 
	
 	GOOGLE_CLIENT_SECRET=""
	
	GITHUB_CLIENT_ID=""
	
	GITHUB_CLIENT_SECRET=""
	
	MAIL_USERNAME=""
	
	MAIL_PASSWORD=""
	
	SECRET_KEY="123"
 
5. Vá ao arquivo app.py e clique na opção "Run Code";
6. No terminal você terá o link de acesso ao projeto, que será uma rota direcionando para uma rota padrão do seu computador (normalmente na porta 3000 ou 5000);
7. Vá para a rota /initdb e então seu banco será criado, após isso você poderá utilizar as funções do sistema normalmente.
