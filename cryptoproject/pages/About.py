import streamlit as st
import pandas as pd
import requests         

# Page config (optional)
st.set_page_config(page_title="About")
st.title("**Crypto Volatility & Risk Analyzer**! 🚀")
# Description



st.markdown("""
         

The **Crypto Volatility & Risk Analyzer** is a tool designed to help cryptocurrency traders and enthusiasts **understand market fluctuations** and make informed investment decisions.

Cryptocurrencies are highly volatile, with prices that can change rapidly. This dashboard allows you to:

- **Track price movements** of popular cryptocurrencies in real time.
- **Analyze historical volatility** to identify patterns and trends.
- **Assess investment risk** using metrics like standard deviation, historical returns, and drawdowns.
- **Compare multiple coins** side by side to make data-driven decisions.

By combining real-time data, historical analysis, and interactive visualizations, the Crypto Volatility & Risk Analyzer provides a **comprehensive view of market dynamics**, helping users minimize risk and maximize opportunities in the crypto space.
""")
st.title("About This Crypto Dashboard")

st.markdown("""
Welcome to the **Crypto Volatility & Risk Analyzer**! 🚀
            

This dashboard allows you to:
- Track real-time cryptocurrency prices.
- Analyze historical price volatility.
- Calculate risk metrics for different coins.
- Visualize trends and correlations.
    

**Built With:**
- Python 3.14
- Streamlit
- Pandas & NumPy
- Plotly for interactive charts
- yFinance for crypto data


**Purpose:** To help crypto traders and enthusiasts make data-driven decisions.
""")

# Optional: add an image or logo
cols = st.columns(6)

coins = [
    ("Bitcoin", "https://assets.coingecko.com/coins/images/1/large/bitcoin.png"),
    ("Ethereum", "https://assets.coingecko.com/coins/images/279/large/ethereum.png"),
    ("Solana", "https://assets.coingecko.com/coins/images/4128/large/solana.png"),
    ("Cardano", "https://assets.coingecko.com/coins/images/975/large/cardano.png"),
    ("Tron", "https://assets.coingecko.com/coins/images/1094/large/tron-logo.png"),
     ("Dogecoin", "https://assets.coingecko.com/coins/images/5/large/dogecoin.png"),
]

for col, (name, url) in zip(cols, coins):
    with col:
        st.image(url, caption=name, use_container_width=True)
if st.sidebar.button("Logout", key="logout_about"):
    st.switch_page("Login.py")   # or your login page path

if st.button("Go to Dashboard"):
    st.switch_page("pages/dashboard.py")
if st.button("Go to Home"):
    st.switch_page("app.py")

    


