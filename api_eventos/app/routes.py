# # app/routes.py
# # Rotas principais da API de Eventos

# from flask import Blueprint, jsonify, request
# from .models import Usuario
# from . import db
# # 🎉 Rotas para EVENTOS
# from .models import Evento


# # Cria o Blueprint principal
# main_routes = Blueprint("main_routes", __name__)

# # 🏠 Rota inicial
# @main_routes.route("/")
# def home():
#     return jsonify({
#         "mensagem": "🚀 API de Eventos funcionando com sucesso!",
#         "status": "ok"
#     })


# # 👥 Rota para listar todos os usuários
# @main_routes.route("/usuarios", methods=["GET"])
# def listar_usuarios():
#     usuarios = Usuario.query.all()
#     lista = [
#         {
#             "id": u.id,
#             "nome": u.nome,
#             "email": u.email,
#             "criado_em": u.criado_em
#         }
#         for u in usuarios
#     ]
#     return jsonify(lista),200


# # ➕ Rota para criar um novo usuário
# @main_routes.route("/usuarios", methods=["POST"])
# def criar_usuario():
#     dados = request.get_json()
#     # Validação simples
#     if not dados or "nome" not in dados or "email" not in dados or "senha" not in dados:
#         return jsonify({"erro": "Campos obrigatórios: nome, email, senha"}), 400

#     # Criação e inserção
#     novo_usuario = Usuario(
#         nome=dados["nome"],
#         email=dados["email"],
#         senha=dados["senha"]
#     )

#     db.session.add(novo_usuario)
#     db.session.commit()

#     return jsonify({"mensagem": "Usuário criado com sucesso!"}), 201


# # 🔍 Rota para buscar um usuário por ID
# @main_routes.route("/usuarios/<int:id>", methods=["GET"])
# def obter_usuario(id):
#     usuario = Usuario.query.get(id)
#     if not usuario:
#         return jsonify({"erro": "Usuário não encontrado"}), 404

#     return jsonify({
#         "id": usuario.id,
#         "nome": usuario.nome,
#         "email": usuario.email,
#         "criado_em": usuario.criado_em
#     })


# # ✏️ Rota para atualizar um usuário
# @main_routes.route("/usuarios/<int:id>", methods=["PUT"])
# def atualizar_usuario(id):
#     usuario = Usuario.query.get(id)
#     if not usuario:
#         return jsonify({"erro": "Usuário não encontrado"}), 404

#     dados = request.get_json()
#     usuario.nome = dados.get("nome", usuario.nome)
#     usuario.email = dados.get("email", usuario.email)
#     usuario.senha = dados.get("senha", usuario.senha)

#     db.session.commit()
#     return jsonify({"mensagem": "Usuário atualizado com sucesso!"},200)


# # ❌ Rota para deletar um usuário
# @main_routes.route("/usuarios/<int:id>", methods=["DELETE"])
# def deletar_usuario(id):
#     usuario = Usuario.query.get(id)
#     if not usuario:
#         return jsonify({"erro": "Usuário não encontrado"}), 404

#     db.session.delete(usuario)
#     db.session.commit()
#     return jsonify({"mensagem": "Usuário deletado com sucesso!"},200)














# # ➕ Criar um novo evento
# @main_routes.route("/eventos", methods=["POST"])
# def criar_evento():
#     dados = request.get_json()

#     if not dados or "titulo" not in dados or "data_evento" not in dados or "usuario_id" not in dados:
#         return jsonify({"erro": "Campos obrigatórios: titulo, data_evento, usuario_id"}), 400

#     novo_evento = Evento(
#         titulo=dados["titulo"],
#         descricao=dados.get("descricao"),
#         data_evento=dados["data_evento"],
#         localizacao=dados.get("localizacao"),
#         usuario_id=dados["usuario_id"]
#     )

#     db.session.add(novo_evento)
#     db.session.commit()

#     return jsonify({"mensagem": "Evento criado com sucesso!"}), 201


# # 📋 Listar todos os eventos
# @main_routes.route("/eventos", methods=["GET"])
# def listar_eventos():
#     eventos = Evento.query.all()
#     lista = [
#         {
#             "id": e.id,
#             "titulo": e.titulo,
#             "descricao": e.descricao,
#             "data_evento": e.data_evento,
#             "localizacao": e.localizacao,
#             "usuario_id": e.usuario_id,
#             "criado_em": e.criado_em
#         }
#         for e in eventos
#     ]
#     return jsonify(lista),200


# # 🔍 Obter um evento pelo ID
# @main_routes.route("/eventos/<int:id>", methods=["GET"])
# def obter_evento(id):
#     evento = Evento.query.get(id)
#     if not evento:
#         return jsonify({"erro": "Evento não encontrado"}), 404

#     return jsonify({
#         "id": evento.id,
#         "titulo": evento.titulo,
#         "descricao": evento.descricao,
#         "data_evento": evento.data_evento,
#         "localizacao": evento.localizacao,
#         "usuario_id": evento.usuario_id,
#         "criado_em": evento.criado_em
#     },200)


# # ✏️ Atualizar um evento
# @main_routes.route("/eventos/<int:id>", methods=["PUT"])
# def atualizar_evento(id):
#     evento = Evento.query.get(id)
#     if not evento:
#         return jsonify({"erro": "Evento não encontrado"}), 404

#     dados = request.get_json()
#     evento.titulo = dados.get("titulo", evento.titulo)
#     evento.descricao = dados.get("descricao", evento.descricao)
#     evento.data_evento = dados.get("data_evento", evento.data_evento)
#     evento.localizacao = dados.get("localizacao", evento.localizacao)
#     evento.usuario_id = dados.get("usuario_id", evento.usuario_id)

#     db.session.commit()
#     return jsonify({"mensagem": "Evento atualizado com sucesso!"},200)


# # ❌ Deletar um evento
# @main_routes.route("/eventos/<int:id>", methods=["DELETE"])
# def deletar_evento(id):
#     evento = Evento.query.get(id)
#     if not evento:
#         return jsonify({"erro": "Evento não encontrado"}), 404

#     db.session.delete(evento)
#     db.session.commit()
#     return jsonify({"mensagem": "Evento deletado com sucesso!"},200)

# app/routes.py
# Rotas principais da API de Eventos (usando Supabase REST API)

from flask import Blueprint, jsonify, request
import requests
import datetime

# 🔑 Credenciais reais do Supabase
SUPABASE_URL = "https://nuxrdhgdwqqinsrmqyfi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51eHJkaGdkd3FxaW5zcm1xeWZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExNDE4NjEsImV4cCI6MjA3NjcxNzg2MX0.hgaOSCexbZsdP9a64MhiZc_CdJpr5juSOD1SdRRb8Fk"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
        "Prefer": "return=representation"  # 👈 ESSA LINHA FAZ O SUPABASE DEVOLVER JSON

}

# Cria o Blueprint principal
main_routes = Blueprint("main_routes", __name__)

# 🏠 Rota inicial
@main_routes.route("/")
def home():
    return jsonify({
        "mensagem": "🚀 API de Eventos funcionando com sucesso (via Supabase REST API)!",
        "status": "ok"
    })


# ======================================================
# 👥 ROTAS DE USUÁRIOS
# ======================================================

# 📋 Listar todos os usuários
@main_routes.route("/usuarios", methods=["GET"])
def listar_usuarios():
    url = f"{SUPABASE_URL}/rest/v1/usuarios?select=*"
    r = requests.get(url, headers=HEADERS)
    return jsonify(r.json()), r.status_code


# ➕ Criar um novo usuário
@main_routes.route("/usuarios", methods=["POST"])
def criar_usuario():
    dados = request.get_json()
    if not dados or "nome" not in dados or "email" not in dados or "senha" not in dados:
        return jsonify({"erro": "Campos obrigatórios: nome, email, senha"}), 400

    novo_usuario = {
        "nome": dados["nome"],
        "email": dados["email"],
        "senha": dados["senha"],
        "criado_em": datetime.datetime.utcnow().isoformat()
    }

    r = requests.post(f"{SUPABASE_URL}/rest/v1/usuarios", headers=HEADERS, json=novo_usuario)
    return jsonify({"mensagem": "Usuário criado com sucesso!", "detalhes": r.json()}), r.status_code


# 🔍 Buscar usuário por ID
@main_routes.route("/usuarios/<int:id>", methods=["GET"])
def obter_usuario(id):
    r = requests.get(f"{SUPABASE_URL}/rest/v1/usuarios?id=eq.{id}&select=*", headers=HEADERS)
    data = r.json()
    if not data:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    return jsonify(data[0]), 200


# ✏️ Atualizar usuário
@main_routes.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    dados = request.get_json()
    r = requests.patch(f"{SUPABASE_URL}/rest/v1/usuarios?id=eq.{id}", headers=HEADERS, json=dados)
    if r.status_code >= 400:
        return jsonify({"erro": "Falha ao atualizar usuário", "detalhes": r.text}), r.status_code
    return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200


# ❌ Deletar usuário
@main_routes.route("/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    r = requests.delete(f"{SUPABASE_URL}/rest/v1/usuarios?id=eq.{id}", headers=HEADERS)
    if r.status_code >= 400:
        return jsonify({"erro": "Falha ao deletar usuário", "detalhes": r.text}), r.status_code
    return jsonify({"mensagem": "Usuário deletado com sucesso!"}), 200


# ======================================================
# 🎉 ROTAS DE EVENTOS
# ======================================================

# ➕ Criar evento
@main_routes.route("/eventos", methods=["POST"])
def criar_evento():
    dados = request.get_json()
    if not dados or "titulo" not in dados or "data_evento" not in dados or "usuario_id" not in dados:
        return jsonify({"erro": "Campos obrigatórios: titulo, data_evento, usuario_id"}), 400

    novo_evento = {
        "titulo": dados["titulo"],
        "descricao": dados.get("descricao"),
        "data_evento": dados["data_evento"],
        "localizacao": dados.get("localizacao"),
        "usuario_id": dados["usuario_id"],
        "criado_em": datetime.datetime.utcnow().isoformat()
    }

    r = requests.post(f"{SUPABASE_URL}/rest/v1/eventos", headers=HEADERS, json=novo_evento)
    return jsonify({"mensagem": "Evento criado com sucesso!", "detalhes": r.json()}), r.status_code


# 📋 Listar todos os eventos
@main_routes.route("/eventos", methods=["GET"])
def listar_eventos():
    url = f"{SUPABASE_URL}/rest/v1/eventos?select=*"
    r = requests.get(url, headers=HEADERS)
    return jsonify(r.json()), r.status_code


# 🔍 Obter evento por ID
@main_routes.route("/eventos/<int:id>", methods=["GET"])
def obter_evento(id):
    r = requests.get(f"{SUPABASE_URL}/rest/v1/eventos?id=eq.{id}&select=*", headers=HEADERS)
    data = r.json()
    if not data:
        return jsonify({"erro": "Evento não encontrado"}), 404
    return jsonify(data[0]), 200


# ✏️ Atualizar evento
@main_routes.route("/eventos/<int:id>", methods=["PUT"])
def atualizar_evento(id):
    dados = request.get_json()
    r = requests.patch(f"{SUPABASE_URL}/rest/v1/eventos?id=eq.{id}", headers=HEADERS, json=dados)
    if r.status_code >= 400:
        return jsonify({"erro": "Falha ao atualizar evento", "detalhes": r.text}), r.status_code
    return jsonify({"mensagem": "Evento atualizado com sucesso!"}), 200


# ❌ Deletar evento
@main_routes.route("/eventos/<int:id>", methods=["DELETE"])
def deletar_evento(id):
    r = requests.delete(f"{SUPABASE_URL}/rest/v1/eventos?id=eq.{id}", headers=HEADERS)
    if r.status_code >= 400:
        return jsonify({"erro": "Falha ao deletar evento", "detalhes": r.text}), r.status_code
    return jsonify({"mensagem": "Evento deletado com sucesso!"}), 200
