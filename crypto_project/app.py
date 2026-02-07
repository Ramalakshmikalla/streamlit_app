from flask import Flask, jsonify, render_template
import requests
import pandas as pd
from datetime import datetime

app = Flask(__name__)
def fetch_crypto_data():
    url = f"https://api.coingecko.com/api/v3/coins/markets"
params = {
"vs_currency": "usd",
"order": "market_cap_desc",
"per_page": 5,
"page": 1,
"sparkline": False
}
response = requests.get(url, params=params)
data = response.json()
crypto_list = []
for coin in data:
    crypto_list.append({
"name": coin["name"],
"symbol": coin["symbol"].upper(),
"price": coin["current_price"],
"change": coin["price_change_percentage_24h"],
"volume": coin["total_volume"]
})
    df = pd.DataFrame(crypto_list)
    df.fillna(0, inplace=True)
    df["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv("crypto_data.csv", index=False)
@app.route("/")
def home():
        return render_template("index.html")
@app.route("/data")
def data():
        crypto_data = fetch_crypto_data()
        return jsonify(crypto_data)
if __name__ == "__main__":
    app.run(debug=True)
