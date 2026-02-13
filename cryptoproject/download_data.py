import yfinance as yf
import os

# Create folder if not exists
os.makedirs("data", exist_ok=True)

# Download Bitcoin data
data = yf.download("BTC-USD", period="1y")

# Save to CSV file
data.to_csv("data/btc_data.csv")

print("Data saved successfully inside 'data' folder.")
