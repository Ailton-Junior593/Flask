from app import create_app  # importa a função que cria a app Flask

app = create_app()  # cria a aplicação usando a fábrica

if __name__ == "__main__":
    # verifica se o arquivo está sendo executado diretamente
    # e não importado por outro módulo
    # inicia o servidor Flask no host 0.0.0.0 e porta 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
