import streamlit as st

st.title("📊 Crypto Volatility and Risk Analyzer")

crypto_name = st.text_input("Enter Cryptocurrency Name")
price_change = st.number_input("Enter Daily Price Change (%)", 0.0, 100.0)

if st.button("Analyze Risk"):
    if price_change > 10:
        risk = "🔴 High Risk"
    elif price_change > 5:
        risk = "🟠 Medium Risk"
    else:
        risk = "🟢 Low Risk"

    st.success(f"{crypto_name} Risk Level: {risk}")
