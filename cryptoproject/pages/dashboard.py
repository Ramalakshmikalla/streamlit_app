


import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os
import time


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Advanced Crypto Data Acquisition",
    layout="wide"
)

# ==================================================
# GLOBAL DARK FINTECH UI STYLING
# ==================================================
st.markdown("""
<style>
/* App Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
/* Reduce top spacing */
.block-container { padding-top: 2rem; }
/* Modern Gradient Button */
div.stButton > button {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    color: white;
    border: none;
    padding: 0.6em 1.4em;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 6px 18px rgba(37, 99, 235, 0.6);
    background: linear-gradient(135deg, #1e40af, #2563eb);
}
/* DataFrame Styling */
[data-testid="stDataFrame"] { background-color: #0f172a; border-radius: 12px; padding: 10px; }
[data-testid="stDataFrame"] th { background-color: #1e293b !important; color: #38bdf8 !important; font-weight: 600; }
[data-testid="stDataFrame"] td { background-color: #0f172a !important; color: white !important; border-bottom: 1px solid #1e293b; }
[data-testid="stDataFrame"] tr:hover td { background-color: #1e293b !important; }
/* LIVE Indicator */
.live-container { display: flex; align-items: center; gap: 10px; font-weight: 600; }
.live-dot { height: 12px; width: 12px; background-color: #22c55e; border-radius: 50%; box-shadow: 0 0 10px #22c55e; animation: pulse 1.5s infinite; }
@keyframes pulse { 0% { box-shadow: 0 0 5px #22c55e; } 50% { box-shadow: 0 0 20px #22c55e; } 100% { box-shadow: 0 0 5px #22c55e; } }
.offline-dot { height: 12px; width: 12px; background-color: #ef4444; border-radius: 50%; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.title("📊 Advanced Crypto Data Acquisition")

col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("### 📡 Live Crypto Market Snapshot")

# Refresh Control
if "refresh_key" not in st.session_state:
    st.session_state.refresh_key = datetime.now().timestamp()

with col2:
    if st.button("🔄 Refresh"):
        st.session_state.refresh_key = datetime.now().timestamp()
        st.toast("Updating market data...")

# ==================================================
# SETUP
# ==================================================
os.makedirs("data", exist_ok=True)
coins = ["bitcoin", "ethereum", "solana", "cardano", "tron"]
file_path = "data/advanced_crypto_data.csv"

# ==================================================
# CACHED API CALL
# ==================================================
@st.cache_data(ttl=30)
def fetch_all_prices(refresh_key):
    ids = ",".join(coins)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ids,
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }
    headers = {"User-Agent": "CryptoDashboard/1.0"}

    for attempt in range(3):
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 429:
            time.sleep(3)
            continue
        response.raise_for_status()
        return response.json()
    raise Exception("Rate limit exceeded. Try again later.")

# ==================================================
# FETCH DATA
# ==================================================
api_status = True
try:
    with st.spinner("Fetching latest market data..."):
        data = fetch_all_prices(st.session_state.refresh_key)

    rows = []
    for coin in coins:
        coin_data = data.get(coin)
        if coin_data:
            rows.append({
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Coin": coin.capitalize(),
                "Price (USD)": round(coin_data.get("usd", 0), 6),
                "Market Cap (USD)": coin_data.get("usd_market_cap", 0),
                "24H Volume (USD)": coin_data.get("usd_24h_vol", 0),
                "24H Change (%)": round(coin_data.get("usd_24h_change", 0), 4)
            })

    final_df = pd.DataFrame(rows)
    if final_df.empty:
        st.error("No data returned from API.")
        st.stop()

    # ==================================================
    # ADD RISK CLASSIFICATION
    # ==================================================
    def classify_risk(change):
        if -2 <= change <= 2:
            return "🟢 Low"
        elif -5 <= change < -2 or 2 < change <= 5:
            return "🟡 Medium"
        else:
            return "🔴 High"

    final_df["Risk"] = final_df["24H Change (%)"].apply(classify_risk)

except Exception as e:
    api_status = False
    st.error(str(e))
    st.stop()

# ==================================================
# LIVE STATUS INDICATOR
# ==================================================
if api_status:
    st.markdown("""<div class="live-container"><div class="live-dot"></div>LIVE Market Data</div>""", unsafe_allow_html=True)
else:
    st.markdown("""<div class="live-container"><div class="offline-dot"></div>API Connection Failed</div>""", unsafe_allow_html=True)

# ==================================================
# SAVE DATA (APPEND HISTORICAL)
# ==================================================
if os.path.exists(file_path):
    old_df = pd.read_csv(file_path)
    final_df = pd.concat([old_df, final_df], ignore_index=True)

final_df.to_csv(file_path, index=False)
st.success("✅ Data Fetched & Saved Successfully")

# ==================================================
# DISPLAY TABLE
# ==================================================
st.dataframe(final_df.tail(50), use_container_width=True)

# ==================================================
# VISUALIZATIONS
# ==================================================
st.subheader("📊 Price Comparison (USD)")
st.line_chart(final_df.set_index("Coin")["Price (USD)"])

st.subheader("📈 24H Percentage Change")
st.line_chart(final_df.set_index("Coin")["24H Change (%)"])

st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ==================================================
st.title("📈 Visualize Trends & Correlations")
# ==================================================
if os.path.exists(file_path):
    hist_df = pd.read_csv(file_path)
    hist_df['Date'] = pd.to_datetime(hist_df['Date'])

    # Pivot for trend chart (Date vs Coin Prices)
    price_trend_df = hist_df.pivot(index='Date', columns='Coin', values='Price (USD)')

    # ----------------------------
    # Price Trends Line Chart
    # ----------------------------
    st.subheader("📈 Price Trends Over Time")
    fig_trends = px.line(
        price_trend_df,
        x=price_trend_df.index,
        y=price_trend_df.columns,
        labels={"value": "Price (USD)", "Date": "Date"},
        title="Cryptocurrency Price Trends"
    )
    st.plotly_chart(fig_trends, use_container_width=True)

    # ----------------------------
    # Price Correlation Heatmap
    # ----------------------------
    st.subheader("🔗 Price Correlation Between Coins")
    corr_df = price_trend_df.corr()
    fig_corr = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale='Viridis',
        title="Correlation Matrix of Crypto Prices"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

else:
    st.warning("Historical data file not found. Trend and correlation charts require saved data over time.")
if st.button("about"):

    st.info("This dashboard fetches live cryptocurrency data from the CoinGecko API, classifies risk based on 24H price changes, and visualizes trends and correlations. Data is saved locally for historical analysis.")
