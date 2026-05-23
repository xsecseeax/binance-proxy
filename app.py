from flask import Flask, jsonify
import requests
import traceback

app = Flask(__name__)

@app.route("/prices")
def get_prices():
    try:
        resp = requests.get(
            "https://api.coincap.io/v2/assets?limit=2000",
            timeout=15
        )
        if resp.status_code != 200:
            return jsonify({"status": "error", "code": resp.status_code, "body": resp.text[:200]}), 500
        data = resp.json().get("data", [])
        prices = {}
        for item in data:
            symbol = (item.get("symbol") or "").upper() + "USDT"
            price = item.get("priceUsd")
            if price:
                prices[symbol] = float(price)
        return jsonify({"status": "ok", "count": len(prices), "prices": prices})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e), "trace": traceback.format_exc()}), 500

@app.route("/test")
def test():
    try:
        resp = requests.get("https://api.coincap.io/v2/assets?limit=5", timeout=10)
        return jsonify({"http": resp.status_code, "body": resp.text[:500]})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/")
def index():
    return "Binance Proxy OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
