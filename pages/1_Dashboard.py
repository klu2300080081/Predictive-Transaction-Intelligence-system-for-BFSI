import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import local_css, page_header

local_css()
page_header()


# --- Page Config ---
st.set_page_config(page_title="Dashboard", layout="wide")

# --- Title ---
st.title("📊 Dashboard")
st.markdown("### Fraud Data Overview")

# --- Load Data ---
df = pd.read_csv("card_fraud_processed.csv")

# --- Matplotlib global style (dark transparent background) ---
plt.style.use("dark_background")

def make_plot(plot_func):
    """Helper to render compact charts without white background"""
    fig, ax = plt.subplots(figsize=(5, 3), facecolor='none')
    plot_func(ax)
    ax.set_facecolor("none")
    for spine in ax.spines.values():
        spine.set_visible(False)
    st.pyplot(fig, use_container_width=True)


# ---------- ROW 1 ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🧾 Transaction Categories")
    make_plot(lambda ax: df['Transaction_Category'].value_counts().plot(
        kind='bar', ax=ax, color='#00BCD4', edgecolor='none')
    )
    ax = plt.gca()
    ax.set_xlabel('')
    ax.set_ylabel('Count')

with col2:
    st.markdown("#### 🔐 Authentication Methods")
    make_plot(lambda ax: df['Authentication_Method'].value_counts().plot(
        kind='pie', autopct='%1.1f%%', ax=ax,
        colors=['#42A5F5', '#66BB6A', '#FFA726', '#AB47BC', '#EC407A'])
    )
    ax = plt.gca()
    ax.set_ylabel('')


# ---------- ROW 2 ----------
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 💰 Transaction Type Summary (Cash in / Cash out / Transfer / Payment)")
    if 'Transaction_Category' in df.columns:
        tx_summary = df['Transaction_Category'].value_counts()
        make_plot(lambda ax: tx_summary.plot(
            kind='bar', ax=ax, color=['#9C27B0', '#2196F3', '#4CAF50', '#FFC107'])
        )
        ax = plt.gca()
        ax.set_xlabel('')
        ax.set_ylabel('Count')
    else:
        st.info("Column 'Transaction_Category' not found.")

with col4:
    st.markdown("#### 📅 Weekly Transactions")
    if 'Transaction_Date' in df.columns:
        df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')
        weekly = df.groupby(df['Transaction_Date'].dt.isocalendar().week).size()
        make_plot(lambda ax: weekly.plot(kind='line', marker='o', color='#29B6F6', ax=ax))
        ax = plt.gca()
        ax.set_xlabel('Week Number')
        ax.set_ylabel('Transactions')
