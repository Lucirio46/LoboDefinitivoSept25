import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from bybit import bybit

load_dotenv()

api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")

client = bybit(test=False, api_key=api_key, api_secret=api_secret)
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Webhook recibido:", data)

    side = data.get("side")  # "Buy" o "Sell"
    symbol = "BTCUSDT"
    qty = 0.01  # ajusta según tu capital

    try:
        order = client.Order.Order_new(
            side=side,
            symbol=symbol,
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel"
        ).result()
        return jsonify({"success": True, "order": str(order)})
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
