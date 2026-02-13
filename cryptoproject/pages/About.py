import streamlit as st

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

**Author:** Ramalakshmi Kalla  
**Purpose:** To help crypto traders and enthusiasts make data-driven decisions.
""")

# Optional: add an image or logo

cols = st.columns(5)
with cols[0]:   
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg", caption="Bitcoin", use_container_width=True)

with cols[1]:
    st.image("https://cryptologos.cc/logos/ethereum-eth-logo.png?v=014", caption="Ethereum", use_container_width=True)

# Solana
with cols[2]:
    st.image("https://cryptologos.cc/logos/solana-sol-logo.png?v=014", caption="Solana", use_container_width=True)

# Cardano
with cols[3]:
    st.image("https://cryptologos.cc/logos/cardano-ada-logo.png?v=014", caption="Cardano", use_container_width=True)

# Tron
with cols[4]:
    st.image("https://cryptologos.cc/logos/tron-trx-logo.png?v=014", caption="Tron", use_container_width=True)

if st.button("Go to Dashboard"):
    st.switch_page("pages/dashboard.py")
if st.button("Go to Home"):
    st.switch_page("app.py")

    


