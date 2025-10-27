import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import local_css, page_header

local_css()
page_header()


# --- Page Config ---
st.set_page_config(page_title="Risk Analysis", layout="wide")

# --- Title ---
st.title("📉 Risk Analysis Dashboard")

# --- Load Data ---
df = pd.read_csv("card_fraud_processed.csv")

# --- Matplotlib dark style ---
plt.style.use("dark_background")

def make_plot(plot_func):
    """Helper to render compact charts with transparent background"""
    fig, ax = plt.subplots(figsize=(5, 3), facecolor='none')
    plot_func(ax)
    ax.set_facecolor("none")
    for spine in ax.spines.values():
        spine.set_visible(False)
    st.pyplot(fig, use_container_width=True)

# --- Total Fraud Transactions ---
st.markdown("#### 🚨 Total Fraudulent Transactions")
if 'isFraud' in df.columns:
    fraud_count = df[df['isFraud'] == 1].shape[0]
    total_tx = len(df)
    fraud_percent = (fraud_count / total_tx) * 100 if total_tx > 0 else 0
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Fraudulent Transactions", value=f"{fraud_count:,}")
    with col2:
        st.metric(label="Fraud Percentage", value=f"{fraud_percent:.2f}%")
else:
    st.error("Column 'isFraud' not found in dataset.")
st.divider()

# --- Two-column layout for charts ---
col1, col2 = st.columns(2)

# FRAUD BY CARD TYPE
with col1:
    st.markdown("#### 💳 Fraud Transactions by Card Type")
    if 'Card_Type' in df.columns and 'isFraud' in df.columns:
        fraud_card = df[df['isFraud'] == 1]['Card_Type'].value_counts()
        if not fraud_card.empty:
            make_plot(lambda ax: fraud_card.plot(kind='bar', ax=ax, color='#42A5F5', edgecolor='none'))
            ax = plt.gca()
            ax.set_xlabel('')
            ax.set_ylabel('Count')
        else:
            st.info("No fraudulent transactions found for any Card Type.")
    else:
        st.warning("Columns 'Card_Type' or 'isFraud' not found.")

# FRAUD BY CURRENCY
with col2:
    st.markdown("#### 💰 Fraud Transactions by Currency")
    if 'Transaction_Currency' in df.columns and 'isFraud' in df.columns:
        fraud_currency = df[df['isFraud'] == 1]['Transaction_Currency'].value_counts()
        if not fraud_currency.empty:
            make_plot(lambda ax: fraud_currency.plot(
                kind='pie', autopct='%1.1f%%', ax=ax,
                colors=['#66BB6A','#FFA726','#AB47BC','#29B6F6','#EC407A'])
            )
            ax = plt.gca()
            ax.set_ylabel('')
        else:
            st.info("No fraudulent transactions found for any Currency type.")
    else:
        st.warning("Columns 'Transaction_Currency' or 'isFraud' not found.")

# --- Second row of charts ---
col3, col4 = st.columns(2)

# FRAUD BY LOCATION
with col3:
    st.markdown("#### 📍 Top 10 Fraud Locations")
    if 'Transaction_Location' in df.columns and 'isFraud' in df.columns:
        fraud_location = df[df['isFraud'] == 1]['Transaction_Location'].value_counts().head(10)
        if not fraud_location.empty:
            make_plot(lambda ax: fraud_location.plot(
                kind='barh', ax=ax, color='#FF7043', edgecolor='none')
            )
            ax = plt.gca()
            ax.set_xlabel('Fraud Count')
            ax.set_ylabel('')
        else:
            st.info("No fraudulent transactions by location found.")
    else:
        st.warning("Columns 'Transaction_Location' or 'isFraud' not found.")

# FRAUD BY TRANSACTION CATEGORY
with col4:
    st.markdown("#### 🧾 Fraud Transactions by Category")
    if 'Transaction_Category' in df.columns and 'isFraud' in df.columns:
        fraud_cat = df[df['isFraud'] == 1]['Transaction_Category'].value_counts()
        if not fraud_cat.empty:
            make_plot(lambda ax: fraud_cat.plot(kind='bar', ax=ax, color='#AB47BC', edgecolor='none'))
            ax = plt.gca()
            ax.set_xlabel('')
            ax.set_ylabel('Count')
        else:
            st.info("No fraudulent transactions found for any Category.")
    else:
        st.warning("Columns 'Transaction_Category' or 'isFraud' not found.")

st.markdown("---")
st.caption("🕒 Data analyzed and visualized dynamically from card_fraud_processed.csv")
