# app/models.py
# Modelos da aplicação usando SQLAlchemy

from . import db
from datetime import datetime

class Usuario(db.Model):
    """
    Modelo para a tabela 'usuarios'.
    Cada instância representa um usuário do sistema.
    """
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)  # ID único, autoincrementável
    nome = db.Column(db.String(100), nullable=False)  # Nome obrigatório
    email = db.Column(db.String(150), unique=True, nullable=False)  # Email único
    senha_hash = db.Column(db.String(255), nullable=False)  # Senha (hash)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação

    # Relacionamento com eventos
    eventos = db.relationship("Evento", backref="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario {self.nome}>"


class Evento(db.Model):
    """
    Modelo para a tabela 'eventos'.
    Cada instância representa um evento criado por um usuário.
    """
    __tablename__ = "eventos"

    id = db.Column(db.Integer, primary_key=True)  # ID do evento
    titulo = db.Column(db.String(200), nullable=False)  # Título do evento
    descricao = db.Column(db.Text)  # Descrição opcional
    data_evento = db.Column(db.DateTime, nullable=False)  # Data e hora do evento
    localizacao = db.Column(db.String(200))  # Local opcional
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)  # FK para usuário
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação

    def __repr__(self):
        return f"<Evento {self.titulo}>"
