# import yfinance as yf
# import os

# # Create folder if not exists
# os.makedirs("data", exist_ok=True)

# # Download Bitcoin data
# data = yf.download("BTC-USD", period="1y")
# data =yf.download("ETH-USD", period="1y", interval="1d")
# data = yf.download("ADA-USD", period="1y", interval="1d")
# data = yf.download("BNB-USD", period="1y", interval="1d")
# data = yf.download("XRP-USD", period="1y", interval="1d")

# # Save to CSV file
# data.to_csv("data/btc_data.csv")
# data.to_csv("data/advanced_crypto_data.csv", mode='a', header=not os.path.exists("data/advanced_crypto_data.csv"))

# print("Data saved successfully inside 'data' folder.")


import requests
import pandas as pd

def get_historical_data(coin_id="bitcoin", days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }

    response = requests.get(url, params=params)
    data = response.json()

    prices = data["prices"]

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["Date", "price"]]

    return df

btc_df = get_historical_data("bitcoin", 90)
print(btc_df.head())
