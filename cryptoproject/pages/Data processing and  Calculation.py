

import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf  # Changed from requests
import plotly.express as px


st.set_page_config(page_title="Crypto Risk Analysis", layout="wide")
# ==================================================
# GLOBAL DASHBOARD STYLES
# ==================================================
st.markdown("""
<style>




/* -------- Sidebar -------- */
[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#020617,#0f172a);
}

/* -------- Headers -------- */
h1,h2,h3,h4{
    color:#38bdf8;
    font-weight:600;
}

/* -------- Buttons -------- */
div.stButton > button{
    background: linear-gradient(135deg,#2563eb,#1e40af);
    color:white;
    border:none;
    border-radius:10px;
    padding:0.6em 1.2em;
    font-weight:600;
    transition:all 0.3s ease;
    box-shadow:0px 4px 10px rgba(0,0,0,0.4);
}

div.stButton > button:hover{
    transform:translateY(-2px);
    background:linear-gradient(135deg,#1e40af,#2563eb);
    box-shadow:0px 6px 18px rgba(37,99,235,0.6);
}

/* -------- DataFrame -------- */
[data-testid="stDataFrame"]{
    background:#020617;
    border-radius:10px;
    padding:10px;
}

[data-testid="stDataFrame"] th{
    background:#1e293b !important;
    color:#38bdf8 !important;
}

[data-testid="stDataFrame"] td{
    background:#020617 !important;
    color:white !important;
}

/* -------- Metric Cards -------- */
[data-testid="metric-container"]{
    background:#020617;
    border-radius:12px;
    padding:15px;
    border:1px solid #1e293b;
}

/* -------- Expander -------- */
.streamlit-expanderHeader{
    font-size:16px;
    font-weight:600;
}

/* -------- Chart Background -------- */
[data-testid="stPlotlyChart"]{
    background:#020617;
    border-radius:12px;
    padding:10px;
}

</style>
""", unsafe_allow_html=True)
# st.title("📊 Crypto Risk Analysis Dashboard")
header1, header2 = st.columns([8,1])

with header1:
  
    st.markdown(
    "<h1 style='text-align:left; font-size:40px; color:lightblue;'>📊 Crypto Risk Analysis Dashboard</h1>",
    unsafe_allow_html=True
)

    


    

# -------------------------------------------------------
# Layout
# -------------------------------------------------------
left_col, right_col = st.columns([4, 1])

with right_col:
    st.subheader("⚙ Controls")
    period_days = st.radio(
        "Select Period",
        [30, 90, 365],
        format_func=lambda x: f"{x} Days" if x != 365 else "1 Year"
    )

# -------------------------------------------------------
# Coin Mapping (yfinance Tickers)
# -------------------------------------------------------
# format is TICKER-USD
coins = {
    "BTC-USD": "BTC",
    "ETH-USD": "ETH",
    "SOL-USD": "SOL",
    "ADA-USD": "ADA",
    "DOGE-USD": "DOGE"
}

# -------------------------------------------------------
# Fetch Historical Data (yfinance VERSION)
# -------------------------------------------------------
@st.cache_data(ttl=3600)
def get_historical_data(ticker, days):
    """
    Fetches data using yfinance. No rate limit delays needed!
    """
    try:
        # yfinance period format: '30d', '90d', '1y'
        period = f"{days}d" if days != 365 else "1y"
        
        # Fetching directly returns a Pandas DataFrame
        data = yf.download(ticker, period=period, interval="1d", progress=False)

        if data.empty:
            st.warning(f"⚠ No data found for {ticker}")
            return pd.DataFrame()

        # yfinance returns MultiIndex if multiple tickers, 
        # but single ticker is straightforward
        df = data[['Close']].reset_index()
        df.columns = ["Date", "price"]
        
        return df

    except Exception as e:
        st.error(f"Error fetching {ticker}: {e}")
        return pd.DataFrame()

# -------------------------------------------------------
# Data Preparation
# -------------------------------------------------------
all_data = []

for ticker, symbol in coins.items():
    df = get_historical_data(ticker, period_days)
    if not df.empty:
        df["Coin"] = symbol
        all_data.append(df)

if len(all_data) == 0:
    st.error("No data available. Check your connection.")
    st.stop()

crypto_df = pd.concat(all_data, ignore_index=True)
crypto_df.sort_values(["Coin", "Date"], inplace=True)
crypto_df.ffill(inplace=True)

st.success(f"✅ Data Prepared via yfinance for Last {period_days} Days")

# -------------------------------------------------------
# Risk Calculations (Remains the same)
# -------------------------------------------------------
crypto_df["Log Return"] = (
    crypto_df.groupby("Coin")["price"]
    .transform(lambda x: np.log(x / x.shift(1)))
)
crypto_df.dropna(inplace=True)

volatility = crypto_df.groupby("Coin")["Log Return"].std()
annual_volatility = volatility * np.sqrt(252)
mean_returns = crypto_df.groupby("Coin")["Log Return"].mean()
sharpe_ratio = mean_returns / volatility

# -------------------------------------------------------
# Metrics & Visualization
# -------------------------------------------------------
benchmark = st.selectbox("Select Benchmark for Beta", list(coins.values()), index=0)
# (Rest of the calculation logic remains identical to your original code)

metrics_df = pd.DataFrame({
    "Volatility": annual_volatility,
    "Sharpe Ratio": sharpe_ratio,
    "Risk Level": annual_volatility.apply(lambda x: "High" if x > 1 else ("Medium" if x > 0.5 else "Low"))
})
metrics_df.reset_index(inplace=True)

st.subheader("📊 Risk Metrics Table")
st.dataframe(metrics_df.round(4), use_container_width=True)


# -------------------------------------------------------
# Volatility Comparison Chart
# -------------------------------------------------------
with st.expander("📊 View Crypto Volatility Comparison"):

    vol_df = metrics_df.sort_values("Volatility", ascending=False)

    fig = px.bar(
        vol_df,
        x="Coin",
        y="Volatility",
        text_auto=".3f",
        title="Annualized Volatility Comparison"
    )

    fig.update_traces(width=0.25)

    fig.update_layout(
        template="plotly_dark",
        bargap=0.7
    )

    st.plotly_chart(fig, use_container_width=True)

 # -------------------------------------------------------
# Correlation with Benchmark
# -------------------------------------------------------
st.subheader("📊 Correlation with Benchmark")

pivot_returns = crypto_df.pivot(
    index="Date",
    columns="Coin",
    values="Log Return"
)

correlation = pivot_returns.corr()
benchmark_corr = correlation[benchmark].drop(benchmark)

corr_df = benchmark_corr.reset_index()
corr_df.columns = ["Coin", "Correlation"]

fig = px.bar(
    corr_df,
    x="Coin",
    y="Correlation",
    text_auto=True,
    title=f"Correlation with {benchmark}"
)

fig.update_layout(
    template="plotly_dark",
    yaxis=dict(range=[-1, 1])
)

st.plotly_chart(fig, use_container_width=True)
# -------------------------------------------------------
# Rolling Volatility
# -------------------------------------------------------
if period_days >= 30:

    crypto_df["30D Rolling Vol"] = (
        crypto_df.groupby("Coin")["Log Return"]
        .transform(lambda x: x.rolling(30).std() * np.sqrt(252))
    )

    st.subheader(f"📈 {period_days}-Day Rolling Volatility")

    rolling_pivot = crypto_df.pivot(
        index="Date",
        columns="Coin",
        values="30D Rolling Vol"
    )

    st.line_chart(rolling_pivot)
    
    # # -------------------------------------------------------
# Interpretation
# -------------------------------------------------------
most_volatile = metrics_df.loc[
    metrics_df["Volatility"].idxmax(), "Coin"
]

best_sharpe = metrics_df.loc[
    metrics_df["Sharpe Ratio"].idxmax(), "Coin"
]

st.subheader("📌 Interpretation")
st.write(f"🔴 Most Volatile Asset: **{most_volatile}**")
st.write(f"🟢 Best Risk-Adjusted Return: **{best_sharpe}**")


    
if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

