# app/config.py
# Configurações da aplicação Flask

import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    # Chave secreta para sessões, cookies e segurança
    SECRET_KEY = os.getenv("SECRET_KEY", "devkey")

    # URL do banco de dados PostgreSQL (Supabase)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    # Desliga o aviso de alterações não rastreadas do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
