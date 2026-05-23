from flask import Flask, jsonify
import requests

app = Flask(__name__)

BINANCE_URL = "https://fapi.binance.com/fapi/v1/ticker/price"

@app.route("/prices")
def get_prices():
    try:
        resp = requests.get(BINANCE_URL, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            prices = {item["symbol"]: float(item["price"]) for item in data}
            return jsonify({"status": "ok", "prices": prices})
        else:
            return jsonify({"status": "error", "code": resp.status_code}), 500
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route("/")
def index():
    return "Binance Proxy OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
