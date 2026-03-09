import pandas as pd
import numpy as np
import yfinance as yf

# Select coins
coins = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "SOL": "SOL-USD",
    "ADA": "ADA-USD"
}

all_data = []

for name, ticker in coins.items():
    df = yf.download(ticker, start="2023-01-01")

    df["Returns"] = df["Close"].pct_change()
    df["Volatility"] = df["Returns"].rolling(30).std()

    risk_free_rate = 0.01 / 252
    df["Sharpe_Ratio"] = (df["Returns"] - risk_free_rate) / df["Volatility"]

    df = df.reset_index()
    df["Crypto"] = name

    all_data.append(df[["Date", "Crypto", "Close", "Returns", "Volatility", "Sharpe_Ratio"]])

final_df = pd.concat(all_data)

# Save CSV
final_df.to_csv("crypto_processed.csv", index=False)

print("✅ crypto_processed.csv created successfully!")