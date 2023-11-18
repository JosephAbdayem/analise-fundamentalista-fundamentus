import os
from flask import Flask, jsonify
from fundamentus import get_data
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_current_day():
    """
    Obtém o dia atual no formato 'dd'.

    :return: String representando o dia atual.
    """
    return datetime.today().strftime('%d')


def fetch_stock_data():
    """
    Busca e formata os dados das ações obtidos pelo módulo fundamentus.

    :return: Dicionário com os dados formatados das ações.
    """
    data = get_data()
    formatted_data = {key: {inner_key: float(value) for inner_key, value in val.items()}
                      for key, val in data.items()}
    return formatted_data


@app.route("/")
def json_api():
    """
    Rota principal da API. Retorna os dados das ações.
    Verifica se os dados já foram atualizados no dia atual; se não, atualiza.

    :return: JSON com os dados das ações.
    """
    global stock_data, last_update_day

    if get_current_day() != last_update_day:
        stock_data, last_update_day = fetch_stock_data(), get_current_day()
    return jsonify(stock_data)


def main():
    """
    Configura e inicia o servidor Flask.
    """
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


# Atualização inicial dos dados
stock_data, last_update_day = fetch_stock_data(), get_current_day()

if __name__ == "__main__":
    main()
