

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -------------------------------------------
# Page Config
# -------------------------------------------
st.set_page_config(page_title="Crypto Risk Dashboard", layout="wide")

# -------------------------------------------
# Custom Styles
# -------------------------------------------
st.markdown("""
<style>

.main-title{
font-size:38px;
font-weight:700;
text-align:center;
color:#4CAF50;
}

.subtitle{
text-align:center;
color:gray;
margin-bottom:30px;
}

.kpi-container{
display:flex;
gap:20px;
margin-top:20px;
}

.kpi-card{
flex:1;
padding:25px;
border-radius:12px;
background: linear-gradient(135deg,#1e1e2f,#2c2c3c);
box-shadow:0 6px 16px rgba(0,0,0,0.35);
transition:0.3s;
text-align:center;
color:white;
}

.kpi-card:hover{
transform:translateY(-6px);
box-shadow:0 10px 25px rgba(0,0,0,0.45);
}

.kpi-title{
font-size:16px;
color:#bbbbbb;
}

.kpi-value{
font-size:32px;
font-weight:700;
margin-top:10px;
}

.return{border-left:6px solid #00c853;}
.volatility{border-left:6px solid #ff9800;}
.sharpe{border-left:6px solid #03a9f4;}

</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📊 Cryptocurrency Risk & Return Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Risk Analytics | Volatility Study | Sharpe Ratio Evaluation</p>', unsafe_allow_html=True)

# -------------------------------------------
# Load Data
# -------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("data/crypto_processed.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    # ensure numeric columns
    numeric_cols = ["Close","Returns","Volatility","Sharpe_Ratio"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values("Date")

    return df

df = load_data()

# -------------------------------------------
# Coin Selector
# -------------------------------------------
crypto_list = df["Crypto"].unique()

selected_crypto = st.selectbox(
    "🪙 Select Cryptocurrency",
    crypto_list
)

# -------------------------------------------
# Date Range Selector
# -------------------------------------------
min_date = df["Date"].min()
max_date = df["Date"].max()

start_date, end_date = st.date_input(
    "📅 Select Date Range",
    [min_date, max_date]
)

# -------------------------------------------
# Filter Data
# -------------------------------------------
filtered_df = df[
    (df["Crypto"] == selected_crypto) &
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
].copy()

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ===========================================
# MAIN TABS
# ===========================================
main_tab1, main_tab2, main_tab3 = st.tabs([
    "📊 Overview",
    "📈 Market Trends",
    "⚖ Risk Analytics"
])

# ===========================================
# TAB 1 : OVERVIEW
# ===========================================
with main_tab1:

    summary = filtered_df.groupby("Crypto").agg({
        "Returns":"mean",
        "Volatility":"mean",
        "Sharpe_Ratio":"mean"
    }).reset_index()

    st.subheader("📌 Portfolio KPI Summary")

    row = summary.iloc[0]

    st.markdown(f"""
    <div class="kpi-container">

    <div class="kpi-card return">
    <div class="kpi-title">Average Return</div>
    <div class="kpi-value">{row['Returns']:.4f}</div>
    </div>

    <div class="kpi-card volatility">
    <div class="kpi-title">Average Volatility</div>
    <div class="kpi-value">{row['Volatility']:.4f}</div>
    </div>

    <div class="kpi-card sharpe">
    <div class="kpi-title">Sharpe Ratio</div>
    <div class="kpi-value">{row['Sharpe_Ratio']:.2f}</div>
    </div>

    </div>
    """, unsafe_allow_html=True)

# ===========================================
# TAB 2 : MARKET TRENDS
# ===========================================
with main_tab2:

    sub_tab1, sub_tab2 = st.tabs([
        "📈 Price Trend",
        "📉 Volatility Trend"
    ])

    # ---------------------------
    # PRICE TREND
    # ---------------------------
    with sub_tab1:

        filtered_df["MA_30"] = filtered_df["Close"].rolling(window=30).mean()

        fig_price = px.line(
            filtered_df,
            x="Date",
            y=["Close","MA_30"],
            labels={"value":"Price (USD)", "variable":"Indicator"},
            title=f"{selected_crypto} Price Trend Analysis"
        )

        fig_price.update_layout(
            template="plotly_dark",
            hovermode="x unified",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            legend_title="Indicators",
            title_x=0.35,
            xaxis=dict(rangeslider=dict(visible=True))
        )

        st.plotly_chart(fig_price, use_container_width=True)

    # ---------------------------
    # VOLATILITY TREND
    # ---------------------------
    with sub_tab2:

        fig_vol = px.line(
            filtered_df,
            x="Date",
            y="Volatility",
            title=f"{selected_crypto} Volatility Trend"
        )

        fig_vol.update_layout(template="plotly_dark")

        st.plotly_chart(fig_vol, use_container_width=True)

# ===========================================
# TAB 3 : RISK ANALYTICS
# ===========================================
with main_tab3:

    sub_tab3, sub_tab4 = st.tabs([
        "⚖ Risk–Return Scatter",
        "📊 Risk Interpretation"
    ])

    with sub_tab3:

        summary = filtered_df.groupby("Crypto").agg({
            "Returns":"mean",
            "Volatility":"mean",
            "Sharpe_Ratio":"mean"
        }).reset_index()

        summary["Sharpe_Ratio"] = (
            summary["Sharpe_Ratio"]
            .replace([np.inf,-np.inf],np.nan)
            .fillna(0)
        )

        scatter = px.scatter(
            summary,
            x="Volatility",
            y="Returns",
            size="Sharpe_Ratio",
            color="Crypto",
            title="Risk vs Return"
        )

        scatter.update_layout(template="plotly_dark")

        st.plotly_chart(scatter, use_container_width=True)

    with sub_tab4:

        st.markdown("""
### 📘 Risk–Return Interpretation Guide

🔵 **Low Risk + High Return → Best Investment**

🔴 **High Risk + Low Return → Poor Asset**

🟡 **High Risk + High Return → Speculative Asset**

🟢 **Low Risk + Low Return → Stable Asset**

---

### Sharpe Ratio Insight

Higher Sharpe Ratio means **better risk-adjusted performance**.
""")