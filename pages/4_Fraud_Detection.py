import streamlit as st
import pandas as pd
import joblib
from datetime import datetime, time

from utils import local_css, page_header

local_css()
page_header()

# --- Page Config ---
st.set_page_config(page_title="Fraud Detection", layout="wide")

# --- Load Model ---
try:
    model = joblib.load("credit_fraud_xgboost.pkl")
except FileNotFoundError:
    st.error("Model file 'credit_fraud_xgboost.pkl' not found.")
    st.stop()

# --- Page Title ---
st.markdown("<h1 style='text-align:center; color:#00BFA6;'>💳 Fraud Detection</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:gray;'>Enter transaction details to check fraud risk</h4>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Form for Inputs ---
with st.form("fraud_detection_form"):
    col1, col2 = st.columns(2)

    with col1:
        location = st.text_input("Transaction Location")
        amount = st.number_input("Transaction Amount", min_value=0.0)
        card_type = st.selectbox("Card Type", ["UzCard", "Visa", "MasterCard", "Humo", "Rupay"])
        auth_method = st.selectbox("Authentication Method", ["2FA", "PIN", "Biometric", "None", "Password"])
        prev_tx = st.number_input("Previous Transactions", min_value=0)
        distance = st.number_input("Distance Between Transactions (km)", min_value=0.0)

    with col2:
        velocity = st.number_input("Transaction Velocity", min_value=0.0)
        tx_currency = st.selectbox("Transaction Currency", ["UZS", "USD", "EUR", "INR"])
        tx_status = st.selectbox("Transaction Status", ["Successful", "Failed", "Pending", "Declined"])
        tx_category = st.selectbox("Transaction Category", ["Transfer", "Purchase", "Withdrawal", "Bill Payment", "Online Shopping"])
        tx_date = st.date_input("Transaction Date", datetime.now().date())
        tx_time = st.time_input("Transaction Time", value=time(0, 0))

    submit = st.form_submit_button("🔍 Predict Fraud Risk")

# --- Prediction Logic ---
if submit:
    # Prepare data
    tx_datetime = datetime.combine(tx_date, tx_time)
    single_tx = {
        'Transaction_Amount': amount,
        'Previous_Transaction_Count': prev_tx,
        'Distance_Between_Transactions_km': distance,
        'Time_Since_Last_Transaction_min': 0.0,
        'Transaction_Velocity': velocity,
        'Hour': tx_datetime.hour,
        'Day': tx_datetime.day,
        'Month': tx_datetime.month,
        'Year': tx_datetime.year,
        'Transaction_Location': location,
        'Card_Type': card_type,
        'Transaction_Currency': tx_currency,
        'Transaction_Status': tx_status,
        'Authentication_Method': auth_method,
        'Transaction_Category': tx_category
    }

    input_df = pd.DataFrame([single_tx])

    try:
        prediction = model.predict(input_df)[0]
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        st.stop()

    # --- Result Display ---
    st.markdown("<br>", unsafe_allow_html=True)
    if prediction == 1:
        st.error("🚨 **High Risk Transaction Detected!**\n\nThis transaction is likely **FRAUDULENT.**")
    else:
        st.success("✅ **Low Risk Transaction.**\n\nThis transaction appears **legitimate.**")

# --- Styling ---
st.markdown("""
    <style>
    body { background-color: #0E1117; color: white; }
    .stForm {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00BFA6, #6200EA);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0px 0px 10px #00BFA6;
    }
    </style>
""", unsafe_allow_html=True)
