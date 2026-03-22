

from numpy.strings import title

import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.express as px

# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(page_title="Crypto Risk Dashboard", layout="wide")

# ---------------------------------------
# Custom CSS Styling
# ---------------------------------------
st.markdown("""
<style>

/* -------- Sidebar -------- */
[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#020617,#0f172a);
}

.main-title{
font-size:60px;
font-weight:900;
text-align:center;
color:#4CAF50;
margin-bottom:5px;
letter-spacing:1px;
}

.subtitle{
text-align:center;
color:#9e9e9e;
margin-bottom:35px;
font-size:18px;
}

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


.card{
padding:22px;
border-radius:14px;
color:white;
font-weight:600;
margin-bottom:14px;
box-shadow:0 6px 18px rgba(0,0,0,0.35);
transition:0.3s;
font-size:12px;
}

.card:hover{
transform:translateY(-6px);
box-shadow:0 12px 28px rgba(0,0,0,0.5);
}

/* Risk Colors */

.high{background: linear-gradient(90deg,#ff4b4b,#b30000);}
.medium{background: linear-gradient(90deg,#f7b733,#fc4a1a);}
.low{background: linear-gradient(90deg,#00c853,#009624);}

/* Section Titles */

.section-title{
font-size:22px;
font-weight:600;
margin-top:30px;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# Title
# ---------------------------------------
st.markdown(
    "<h1 style='text-align:center; font-size:40px; color:lightblue;'>📊 Crypto Volatility & Risk Reporting</h1>",
    unsafe_allow_html=True
)
st.markdown('<p class="subtitle">Live Market Data | Volatility Analysis | Sharpe Ratio Evaluation</p>', unsafe_allow_html=True)


# ---------------------------------------
# Refresh Button (Right Side)
# ---------------------------------------
col_title, col_refresh = st.columns([8,1])

with col_refresh:
    if st.button("🔄 Refresh"):
        st.rerun()

# ---------------------------------------
# Crypto List
# ---------------------------------------
crypto_ids = ["bitcoin","ethereum","cardano","solana","dogecoin"]

# ---------------------------------------
# Fetch Live Data from CoinGecko
# ---------------------------------------
url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": ",".join(crypto_ids),
    "vs_currencies": "usd",
    "include_24hr_change": "true"
}

response = requests.get(url, params=params)
data = response.json()

crypto=[]
price=[]
volatility=[]

for coin in crypto_ids:
    crypto.append(coin.capitalize())
    price.append(data[coin]["usd"])
    volatility.append(abs(data[coin]["usd_24h_change"]))

df = pd.DataFrame({
"Crypto":crypto,
"Price":price,
"Volatility":volatility
})

# ---------------------------------------
# Calculate Returns
# ---------------------------------------
df["Returns"] = df["Volatility"] / 100

# ---------------------------------------
# Sharpe Ratio Calculation
# ---------------------------------------
risk_free_rate = 0.01

df["Sharpe_Ratio"] = (df["Returns"] - risk_free_rate) / (df["Volatility"]/100)

df["Sharpe_Ratio"] = df["Sharpe_Ratio"].replace([np.inf,-np.inf],0).fillna(0)

# ---------------------------------------
# Risk Classification
# ---------------------------------------
def classify(vol):

    if vol > 5:
        return "High"
    elif vol > 2:
        return "Medium"
    else:
        return "Low"

df["Risk"] = df["Volatility"].apply(classify)

# ---------------------------------------
# Layout Columns
# ---------------------------------------
col1,col2,col3 = st.columns(3)

high=df[df["Risk"]=="High"]
medium=df[df["Risk"]=="Medium"]
low=df[df["Risk"]=="Low"]

# ---------------------------------------
# High Risk
# ---------------------------------------
with col1:

    st.subheader("🔴 High Risk")

    for i in range(len(high)):

        st.markdown(f"""
        <div class="card high">
        {high.iloc[i]['Crypto']} <br>
        Price: ${high.iloc[i]['Price']} <br>
        Volatility: {high.iloc[i]['Volatility']:.2f}% <br>
        Sharpe Ratio: {high.iloc[i]['Sharpe_Ratio']:.2f}
        </div>
        """,unsafe_allow_html=True)

# ---------------------------------------
# Medium Risk
# ---------------------------------------
with col2:

    st.subheader("🟡 Medium Risk")

    for i in range(len(medium)):

        st.markdown(f"""
        <div class="card medium">
        {medium.iloc[i]['Crypto']} <br>
        Price: ${medium.iloc[i]['Price']} <br>
        Volatility: {medium.iloc[i]['Volatility']:.2f}% <br>
        Sharpe Ratio: {medium.iloc[i]['Sharpe_Ratio']:.2f}
        </div>
        """,unsafe_allow_html=True)

# ---------------------------------------
# Low Risk
# ---------------------------------------
with col3:

    st.subheader("🟢 Low Risk")

    for i in range(len(low)):

        st.markdown(f"""
        <div class="card low">
        {low.iloc[i]['Crypto']} <br>
        Price: ${low.iloc[i]['Price']} <br>
        Volatility: {low.iloc[i]['Volatility']:.2f}% <br>
        Sharpe Ratio: {low.iloc[i]['Sharpe_Ratio']:.2f}
        </div>
        """,unsafe_allow_html=True)

# ---------------------------------------
# Risk Summary Section
# ---------------------------------------
st.markdown('<div class="section-title">📑 Risk Summary Report</div>', unsafe_allow_html=True)

colA,colB,colC,colD = st.columns(4)

colA.metric("Total Cryptos",len(df))
colB.metric("Average Volatility",f"{df['Volatility'].mean():.2f}%")
colC.metric("Average Sharpe Ratio",f"{df['Sharpe_Ratio'].mean():.2f}")
colD.metric("High Risk Coins",len(high))


    # ---------------------------------------
# Donut Chart
# ---------------------------------------
risk_counts = df["Risk"].value_counts().reset_index()
risk_counts.columns = ["Risk","Count"]

fig = px.pie(
    risk_counts,
    values="Count",
    names="Risk",
    hole=0.6,
    color="Risk",
    title="Risk Distribution",
    color_discrete_map={
        "High":"#e63946",     # Red
        "Medium":"#ffb703",   # Yellow
        "Low":"#06d6a0"       # Green
    }
)

fig.update_layout(
template="plotly_dark",
title_x=0.35,
font=dict(size=14)
)

st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------
# Data Table
# ---------------------------------------
st.markdown('<div class="section-title">📋 Live Crypto Data</div>', unsafe_allow_html=True)

st.dataframe(df)
# ---------------------------------------
# Download Report Section
# ---------------------------------------
st.markdown('<div class="section-title">⬇ Download Risk Report</div>', unsafe_allow_html=True)

# Select columns for report
report_df = df[["Crypto","Price","Volatility","Sharpe_Ratio","Risk"]]

# Convert dataframe to CSV
csv = report_df.to_csv(index=False).encode("utf-8")

# Download Button
st.download_button(
    label="📥 Download Crypto Risk Report (CSV)",
    data=csv,
    file_name="crypto_risk_report.csv",
    mime="text/csv"
)


if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()
