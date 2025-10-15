import json
from flask import Flask, Response, request

app = Flask(__name__)

funcionarios = [
    {"id": 1, "nome": "Ana Souza", "cargo": "Desenvolvedora", "salario": 7500},
    {"id": 2, "nome": "Carlos Lima", "cargo": "Designer", "salario": 6200},
    {"id": 3, "nome": "Marcos Silva", "cargo": "Gerente de Projetos", "salario": 9500}
]

# Função que transforma dados em JSON UTF-8
def utf8_json(data, status=200):
    return Response(
        response=json.dumps(data, ensure_ascii=False),  # garante acentos
        status=status,
        mimetype='application/json; charset=utf-8'
    )

@app.route('/')
def home():
    return utf8_json({"message": "API funcionando!"})

@app.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    return utf8_json(funcionarios)

@app.route('/funcionarios/<int:id>', methods=['GET'])
def buscar_funcionario(id):
    funcionario = next((f for f in funcionarios if f["id"] == id), None)
    if not funcionario:
        return utf8_json({"error": "Funcionário não encontrado"}, 404)
    return utf8_json(funcionario, 200)

@app.route('/funcionarios', methods=['POST'])
def adicionar_funcionario():
    dados = request.get_json()

    if 'nome' not in dados or 'cargo' not in dados or 'salario' not in dados:
        return utf8_json({'error': 'É preciso enviar nome, cargo e salario'}, 400)
    
    if len(funcionarios) > 0:
        novo_id = funcionarios[-1]['id'] + 1
    else:
        novo_id = 1
    
    novo_funcionario = {
        'id' : novo_id,
        'nome' : dados['nome'],
        'cargo' : dados['cargo'],
        'salario' : dados['salario'],
    }

    funcionarios.append(novo_funcionario)

    return utf8_json(novo_funcionario, 201)


@app.route('/funcionarios/<int:id>', methods=['PUT'])
def atualizar_funcionario(id):
    # 1️⃣ Pega os dados enviados no corpo da requisição (JSON)
    dados = request.get_json()

    # 2️⃣ Procura o funcionário pelo ID
    funcionario = None
    for f in funcionarios:
        if f["id"] == id:
            funcionario = f
            break

    # 3️⃣ Se não encontrar, retorna erro 404
    if funcionario is None:
        return utf8_json({"error": "Funcionário não encontrado"}, 404)

    # 4️⃣ Atualiza os campos que vierem no JSON
    if "nome" in dados:
        funcionario["nome"] = dados["nome"]
    if "cargo" in dados:
        funcionario["cargo"] = dados["cargo"]
    if "salario" in dados:
        funcionario["salario"] = dados["salario"]

    # 5️⃣ Retorna o funcionário atualizado
    return utf8_json(funcionario, 200)


if __name__== '__main__':
    app.run(debug=True)