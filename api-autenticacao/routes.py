from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from utils import hash_password, verify_password, generate_reset_code
from flask_mail import Message

# cria o blueprint 'auth' — as rotas serão registradas como /api/...
auth_bp = Blueprint("auth", __name__)

# -------------------------
# ROTA: /register
# -------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Cria um novo usuário.
    Espera JSON: { "email": "...", "password": "..." }
    """
    # pega o JSON do corpo da requisição (se vier vazio, usa dict vazio)
    payload = request.get_json() or {}

    # extrai email e password do payload
    email = payload.get("email")
    password = payload.get("password")

    # validação básica: ambos campos são obrigatórios
    if not email or not password:
        return jsonify({"msg": "email e password são obrigatórios"}), 400

    # acessa o cliente supabase configurado em app.py via current_app
    supabase = current_app.supabase

    # 1) checa se já existe um usuário com esse email (evita duplicidade)
    # usamos limit(1) para otimizar
    resp = supabase.table("usuarios").select("id").eq("email", email).limit(1).execute()

    # resp.data contém a lista de resultados; se houver elemento, email já existe
    if resp.data and len(resp.data) > 0:
        return jsonify({"msg": "Email já cadastrado"}), 409

    # 2) cria o hash da senha (nunca salvar senha em texto plano)
    hashed = hash_password(password)

    # 3) insere o usuário no Supabase
    insert_data = {"email": email, "senha": hashed}
    insert_resp = supabase.table("usuarios").insert(insert_data).execute()

    # tratamento simples de erro: verifica status code (supabase-py expõe status_code)
    if hasattr(insert_resp, "status_code") and insert_resp.status_code not in (200, 201):
        # em caso de erro, devolver detalhe para debugging (sem vazar secrets)
        return jsonify({"msg": "Erro ao criar usuário", "detail": insert_resp.data}), 500

    # sucesso
    return jsonify({"msg": "Usuário criado com sucesso"}), 201


# -------------------------
# ROTA: /login
# -------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Autentica o usuário e retorna um access_token JWT.
    Espera JSON: { "email": "...", "password": "..." }
    """
    payload = request.get_json() or {}
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        return jsonify({"msg": "email e password são obrigatórios"}), 400

    supabase = current_app.supabase

    # busca usuário pelo email; selecionamos id, senha (hash) e email
    resp = supabase.table("usuarios").select("id, senha, email").eq("email", email).limit(1).execute()
    rows = resp.data or []

    # se não encontrou, credenciais inválidas
    if not rows or len(rows) == 0:
        return jsonify({"msg": "Credenciais inválidas"}), 401

    user = rows[0]

    # verifica a senha recebida com o hash salvo
    if not verify_password(user["senha"], password):
        return jsonify({"msg": "Credenciais inválidas"}), 401

    # se chegou aqui, credenciais ok -> cria JWT
    # identity armazenará o id do usuário (pode ser email se preferir)
    access_token = create_access_token(identity=user["id"], expires_delta=timedelta(hours=8))

    # retorna o token para o cliente
    return jsonify({"access_token": access_token}), 200


# -------------------------
# Exemplo: rota protegida de teste
# -------------------------
@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    Exemplo simples para testar se o token funciona.
    Deve enviar header: Authorization: Bearer <token>
    """
    identity = get_jwt_identity()  # recupera o identity que armazenamos no token
    return jsonify({"msg": f"Você está autenticado como {identity}"}), 200



@auth_bp.route("/request-reset", methods=["POST"])
def request_reset():
    """
    Solicita redefinição de senha.
    Espera JSON: { "email": "..." }
    Gera um código, salva no Supabase e envia por e-mail.
    """
    payload = request.get_json() or {}
    email = payload.get("email")

    # validação
    if not email:
        return jsonify({"msg": "E-mail é obrigatório"}), 400

    supabase = current_app.supabase
    mail = current_app.mail

    # verifica se o e-mail existe
    user_resp = supabase.table("usuarios").select("id").eq("email", email).limit(1).execute()
    if not user_resp.data or len(user_resp.data) == 0:
        return jsonify({"msg": "E-mail não encontrado"}), 404

    # gera o código (ex: A7D4K2)
    reset_code = generate_reset_code()

    # atualiza o código no banco
    supabase.table("usuarios").update({"reset_code": reset_code}).eq("email", email).execute()

    # cria e envia o e-mail
    try:
        msg = Message(
            subject="Código para redefinir senha 🔐",
            sender="seuemail@gmail.com",
            recipients=[email],
            body=f"Olá! Aqui está seu código de redefinição: {reset_code}\n\nEle expira em 15 minutos."
        )
        mail.send(msg)

    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return jsonify({"msg": "Erro ao enviar e-mail"}), 500

    return jsonify({"msg": "Código enviado para o e-mail informado"}), 200

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """
    Rota para redefinir senha após receber o código de verificação.
    Espera JSON: { "email": "...", "code": "...", "new_password": "..." }
    """
    payload = request.get_json() or {}
    email = payload.get("email")
    code = payload.get("code")
    new_password = payload.get("new_password")

    # validações básicas
    if not email or not code or not new_password:
        return jsonify({"msg": "email, code e new_password são obrigatórios"}), 400

    supabase = current_app.supabase

    # busca usuário pelo email
    user_resp = supabase.table("usuarios").select("id, reset_code").eq("email", email).limit(1).execute()
    if not user_resp.data:
        return jsonify({"msg": "Usuário não encontrado"}), 404

    user = user_resp.data[0]

    # confere se o código bate com o que foi salvo no banco
    if user.get("reset_code") != code:
        return jsonify({"msg": "Código inválido ou expirado"}), 400

    # faz o hash da nova senha
    hashed_password = hash_password(new_password)

    # atualiza a senha e limpa o código de redefinição
    update_resp = (
        supabase.table("usuarios")
        .update({"senha": hashed_password, "reset_code": None})
        .eq("email", email)
        .execute()
    )

    if hasattr(update_resp, "status_code") and update_resp.status_code not in (200, 201):
        return jsonify({"msg": "Erro ao atualizar senha"}), 500

    return jsonify({"msg": "Senha redefinida com sucesso!"}), 200
