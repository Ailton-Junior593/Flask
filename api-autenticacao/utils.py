from werkzeug.security import generate_password_hash, check_password_hash
import random
import string


# -------------------------
# 1️⃣ Criptografar senha
# -------------------------
def hash_password(password: str) -> str:
    """
    Recebe uma senha em texto plano e retorna um hash seguro.
    O hash é irreversível (não dá pra descobrir a senha original).
    """
    return generate_password_hash(password)


# -------------------------
# 2️⃣ Verificar senha
# -------------------------
def verify_password(hashed_password: str, plain_password: str) -> bool:
    """
    Compara a senha digitada com o hash armazenado.
    Retorna True se forem equivalentes, False caso contrário.
    """
    return check_password_hash(hashed_password, plain_password)


# -------------------------
# 3️⃣ Gerar código de redefinição de senha (para etapa 3)
# -------------------------
def generate_reset_code(length: int = 6) -> str:
    """
    Gera um código aleatório com letras e números (ex: 'A9B3D2')
    que será enviado por e-mail para o usuário.
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))
