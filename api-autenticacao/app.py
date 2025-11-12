import os                              # trabalhar com variáveis de ambiente
from dotenv import load_dotenv         # carregar .env automaticamente
from flask import Flask                # microframework web
from flask_jwt_extended import JWTManager  # gerencia JWTs (tokens)
from supabase import create_client     # cliente supabase-py
from flask_mail import Mail
# carrega variáveis do arquivo .env para process.env (sempre no topo)
load_dotenv()

# Lê as variáveis necessárias do ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
FLASK_ENV = os.getenv("FLASK_ENV", "development")  # opcional: ambiente

# cria o cliente global do Supabase para ser usado pelas rotas
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_app():
    """
    Factory function — cria e retorna a aplicação Flask configurada.
    Usar factory facilita testes e evita import cycles com blueprints.
    """
    app = Flask(__name__)                 # instancia a app Flask

    # configurações básicas do Flask/JWT
    app.config["ENV"] = FLASK_ENV
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY  # chave para assinar tokens
    app.config["PROPAGATE_EXCEPTIONS"] = True      # deixa erros subirem (útil em dev)
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

    mail = Mail(app)
    # inicializa o gerenciador de JWT com a app
    jwt = JWTManager(app)

    # registrar blueprints (import local para evitar circular imports)
    # routes.py vai importar 'supabase' e por isso importamos aqui depois da criação
    from routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api")

    # expor o cliente supabase via app (opcional) para facilitar acesso em outros módulos:
    app.supabase = supabase

    return app

# ponto de entrada quando executado diretamente
if __name__ == "__main__":
    # cria a app e roda em modo debug por padrão (não usar debug em produção)
    application = create_app()
    application.run(debug=True, host="127.0.0.1", port=5000)


