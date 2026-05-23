from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/prices")
def get_prices():
    try:
        # CoinCap - tüm kripto fiyatları, bloke yok
        resp = requests.get(
            "https://api.coincap.io/v2/assets?limit=2000",
            timeout=15
        )
        if resp.status_code != 200:
            return jsonify({"status": "error", "code": resp.status_code}), 500
        data = resp.json().get("data", [])
        prices = {}
        for item in data:
            symbol = (item.get("symbol") or "").upper() + "USDT"
            price = item.get("priceUsd")
            if price:
                prices[symbol] = float(price)
        return jsonify({"status": "ok", "prices": prices})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route("/")
def index():
    return "Binance Proxy OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
