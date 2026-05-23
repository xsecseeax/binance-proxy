from flask import Flask, jsonify
import requests

app = Flask(__name__)

ENDPOINTS = [
    "https://fapi.binance.com/fapi/v1/ticker/price",
    "https://api.binance.com/api/v3/ticker/price",
]

@app.route("/prices")
def get_prices():
    for url in ENDPOINTS:
        try:
            resp = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0"
            })
            if resp.status_code == 200:
                data = resp.json()
                prices = {item["symbol"]: float(item["price"]) for item in data}
                return jsonify({"status": "ok", "prices": prices, "source": url})
        except Exception as e:
            continue
    return jsonify({"status": "error", "msg": "All endpoints failed"}), 500

@app.route("/")
def index():
    return "Binance Proxy OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
