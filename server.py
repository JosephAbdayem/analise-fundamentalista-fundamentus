#!/usr/bin/env python3

import os
from flask import Flask, jsonify
from fundamentus import get_data
from datetime import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

def get_current_day():
    return datetime.strftime(datetime.today(), '%d')


def fetch_stock_data():
    data = dict(get_data())
    formatted_data = {
        outer_key: {
            inner_key: float(inner_value) for inner_key, inner_value in outer_value.items()
        } for outer_key, outer_value in data.items()
    }
    return formatted_data


@app.route("/")
def json_api():
    global stock_data, last_update_day

    current_day = get_current_day()

    # Then only update once a day
    if last_update_day == current_day:
        return jsonify(stock_data)
    else:
        stock_data, last_update_day = fetch_stock_data(), current_day
        return jsonify(stock_data)


def main():
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

# First update
stock_data, last_update_day = fetch_stock_data(), get_current_day()

if __name__ == "__main__":
    main()
