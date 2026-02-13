

# import streamlit as st
# import yfinance as yf
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# import hashlib

# # ==================================================
# # ================= PAGE CONFIG ====================
# # ==================================================

# st.set_page_config(
#     page_title="Crypto Volatility & Risk Analyzer",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ==================================================
# # ============== SESSION STATE INIT ===============
# # ==================================================

# if "users" not in st.session_state:
#     st.session_state.users = {}

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if "page" not in st.session_state:
#     st.session_state.page = "login"

# # ==================================================
# # ============== PASSWORD HASH FUNCTION ============
# # ==================================================

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # ==================================================
# # ================= REGISTER PAGE ==================
# # ==================================================

# def register():
#     st.title("📝 Register")

#     with st.form("register_form"):
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         confirm = st.text_input("Confirm Password", type="password")
#         submit = st.form_submit_button("Register")

#         if submit:
#             if not username or not password:
#                 st.error("All fields are required!")
#             elif username in st.session_state.users:
#                 st.error("Username already exists!")
#             elif password != confirm:
#                 st.error("Passwords do not match!")
#             else:
#                 st.session_state.users[username] = hash_password(password)
#                 st.success("Registration successful! Please login.")
#                 st.session_state.page = "login"
#                 st.rerun()

#     if st.button("Go to Login"):
#         st.session_state.page = "login"
#         st.rerun()

# # ==================================================
# # ================= LOGIN PAGE =====================
# # ==================================================

# def login():
#     st.title("🔐 Login")

#     with st.form("login_form"):
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         submit = st.form_submit_button("Login")

#         if submit:
#             hashed = hash_password(password)
#             stored = st.session_state.users.get(username)

#             if stored and stored == hashed:
#                 st.session_state.logged_in = True
#                 st.session_state.page = "dashboard"
#                 st.success("Login successful!")
#                 st.rerun()
#             else:
#                 st.error("Invalid username or password")

#     if st.button("Create New Account"):
#         st.session_state.page = "register"
#         st.rerun()


        

# # ==================================================
# # ================= DASHBOARD ======================
# # ==================================================

# def dashboard():

#     st.title("📊 Crypto Volatility & Risk Analyzer")
#     st.markdown("### Analyzing Cryptocurrency Risk Through Automated Data Acquisition")

#     # Sidebar
#     st.sidebar.header("Settings")
#     ticker = st.sidebar.selectbox(
#         "Select Coin",
#         ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "TRX-USD"]
#     )

#     days = st.sidebar.slider("Select Days", 30, 180, 90)

#     if st.sidebar.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.page = "login"
#         st.rerun()

#     # Fetch Data
#     data = yf.download(ticker, period=f"{days}d", interval="1d")

#     # Fix MultiIndex issue
#     if isinstance(data.columns, pd.MultiIndex):
#         data.columns = data.columns.get_level_values(0)

#     if data.empty:
#         st.error("No data found.")
#         return

#     # Calculations
#     data["Returns"] = data["Close"].pct_change()

#     volatility = data["Returns"].std() * np.sqrt(252) * 100

#     if data["Returns"].std() != 0:
#         sharpe = (data["Returns"].mean() / data["Returns"].std()) * np.sqrt(252)
#     else:
#         sharpe = 0

#     current_price = data["Close"].iloc[-1]

#     # Risk Level (Dynamic)
#     if volatility < 40:
#         risk_level = "Low Risk"
#         risk_value = [70, 20, 10]
#     elif volatility < 80:
#         risk_level = "Medium Risk"
#         risk_value = [30, 50, 20]
#     else:
#         risk_level = "High Risk"
#         risk_value = [15, 25, 60]

#     # Metrics
#     m1, m2, m3 = st.columns(3)
#     m1.metric("Annualized Volatility", f"{volatility:.2f}%")
#     m2.metric("Sharpe Ratio", f"{sharpe:.2f}")
#     m3.metric("Current Price", f"${current_price:,.2f}")

#     st.success(f"Detected Risk Level: {risk_level}")

#     st.divider()

#     left, right = st.columns([2, 1])

#     with left:
#         fig_line = px.line(data, y="Close", title=f"{ticker} Price Trend")
#         fig_line.update_layout(template="plotly_dark")
#         st.plotly_chart(fig_line, use_container_width=True)

#         fig_bar = px.bar(data, y="Volume", title="Trading Volume")
#         fig_bar.update_layout(template="plotly_dark")
#         st.plotly_chart(fig_bar, use_container_width=True)

#     with right:
#         labels = ["Low Risk", "Medium Risk", "High Risk"]

#         fig_pie = go.Figure(
#             data=[go.Pie(labels=labels, values=risk_value, hole=.4)]
#         )
#         fig_pie.update_layout(template="plotly_dark")
#         st.plotly_chart(fig_pie, use_container_width=True)

#         if st.button("Go to Dashboard", key="dashboard_button"):
#             st.switch_page("pages/dashboard.py")
            
        
#         if st.button("Go to About", key="about_button"):
#             st.switch_page("pages/About.py")
# # # ==================================================
# # ================= PAGE ROUTER ====================
# # ==================================================

# if st.session_state.page == "login":
#     login()

# elif st.session_state.page == "register":
#     register()

# elif st.session_state.page == "dashboard":
#     if st.session_state.logged_in:
#         dashboard()
#     else:
#         st.session_state.page = "login"
#         st.rerun()


import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import hashlib
import requests
from datetime import datetime

# ==================================================
# ================= PAGE CONFIG ====================
# ==================================================
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# ============== SESSION STATE INIT ===============
# ==================================================
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ==================================================
# ============== PASSWORD HASH FUNCTION ===========
# ==================================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ==================================================
# ================= REGISTER PAGE ==================
# ==================================================
def register():
    st.title("📝 Register")
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Register")

        if submit:
            if not username or not password:
                st.error("All fields are required!")
            elif username in st.session_state.users:
                st.error("Username already exists!")
            elif password != confirm:
                st.error("Passwords do not match!")
            else:
                st.session_state.users[username] = hash_password(password)
                st.success("Registration successful! Please login.")
                st.session_state.page = "login"
                st.rerun()

    if st.button("Go to Login"):
        st.session_state.page = "login"
        st.rerun()

# ==================================================
# ================= LOGIN PAGE =====================
# ==================================================
def login():
    st.title("🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            hashed = hash_password(password)
            stored = st.session_state.users.get(username)
            if stored and stored == hashed:
                st.session_state.logged_in = True
                st.session_state.page = "dashboard"
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    if st.button("Create New Account"):
        st.session_state.page = "register"
        st.rerun()

# ==================================================
# ================= DASHBOARD ======================
# ==================================================
def dashboard():
    st.title("📊 Crypto Volatility & Risk Analyzer")
    st.markdown("### Analyzing Cryptocurrency Risk Through Automated Data Acquisition")

    # Sidebar
    st.sidebar.header("Settings")
    ticker = st.sidebar.selectbox(
        "Select Coin",
        ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "TRX-USD"]
    )
    days = st.sidebar.slider("Select Days", 30, 180, 90)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

    # --------------------------
    # Fetch Historical Data via yfinance
    # --------------------------
    data = yf.download(ticker, period=f"{days}d", interval="1d")

    # Fix MultiIndex issue
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    if data.empty:
        st.error("No historical data found.")
        return

    # Calculations
    data["Returns"] = data["Close"].pct_change()
    volatility = data["Returns"].std() * np.sqrt(252) * 100
    sharpe = (data["Returns"].mean() / data["Returns"].std() * np.sqrt(252)
              if data["Returns"].std() != 0 else 0)
    current_price = data["Close"].iloc[-1]

    # Risk Level (Dynamic)
    if volatility < 40:
        risk_level = "Low Risk"
        risk_value = [70, 20, 10]
    elif volatility < 80:
        risk_level = "Medium Risk"
        risk_value = [30, 50, 20]
    else:
        risk_level = "High Risk"
        risk_value = [15, 25, 60]

    # --------------------------
    # Live Data via CoinGecko API
    # --------------------------
    coins_api_map = {
        "BTC-USD": "bitcoin",
        "ETH-USD": "ethereum",
        "SOL-USD": "solana",
        "ADA-USD": "cardano",
        "TRX-USD": "tron"
    }

    live_data = {}
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coins_api_map[ticker],
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        live_data = response.json()[coins_api_map[ticker]]
    except Exception as e:
        st.warning(f"Could not fetch live data: {e}")

    # --------------------------
    # Display Metrics
    # --------------------------
    m1, m2, m3 = st.columns(3)
    m1.metric("Annualized Volatility", f"{volatility:.2f}%")
    m2.metric("Sharpe Ratio", f"{sharpe:.2f}")
    m3.metric("Current Price", f"${live_data.get('usd', current_price):,.2f}")

    st.success(f"Detected Risk Level: {risk_level}")

    st.divider()
    left, right = st.columns([2, 1])

    # --------------------------
    # Graphs: Price Trend & Volume
    # --------------------------
    with left:
        st.subheader(f"📈 {ticker} Price Trend (Historical)")
        fig_line = px.line(data, y="Close", title=f"{ticker} Price Trend", labels={"Close": "Price (USD)"})
        fig_line.update_layout(template="plotly_dark")
        st.plotly_chart(fig_line, use_container_width=True)

        st.subheader(f"📊 {ticker} Trading Volume")
        fig_bar = px.bar(data, y="Volume", title=f"{ticker} Trading Volume", labels={"Volume": "Volume"})
        fig_bar.update_layout(template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

    # --------------------------
    # Risk Pie Chart
    # --------------------------
    with right:
        st.subheader("⚠️ Risk Distribution")
        labels = ["Low Risk", "Medium Risk", "High Risk"]
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=risk_value, hole=.4)])
        fig_pie.update_layout(template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

        # Navigation buttons
        if st.button("Go to Dashboard", key="dashboard_button"):
            st.switch_page("pages/dashboard.py")

        if st.button("Go to About", key="about_button"):
            st.switch_page("pages/About.py")


# ==================================================
# ================= PAGE ROUTER ====================
# ==================================================
if st.session_state.page == "login":
    login()
elif st.session_state.page == "register":
    register()
elif st.session_state.page == "dashboard":
    if st.session_state.logged_in:
        dashboard()
    else:
        st.session_state.page = "login"
        st.rerun()
