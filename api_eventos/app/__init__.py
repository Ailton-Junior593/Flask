# app/__init__.py
# Criação da aplicação Flask

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Inicializa o SQLAlchemy (banco de dados)
db = SQLAlchemy()

def create_app():
    """
    Função fábrica que cria e configura a aplicação Flask.
    Retorna a instância da app pronta para uso.
    """
    app = Flask(__name__)
    
    # Aplica as configurações da classe Config
    app.config.from_object(Config)
    
    # Inicializa o SQLAlchemy com a app
    db.init_app(app)

    # Importa e registra as rotas da aplicação
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
