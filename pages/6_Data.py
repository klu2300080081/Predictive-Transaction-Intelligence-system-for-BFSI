import streamlit as st
import pandas as pd
from utils import local_css, page_header

# --- Apply Global CSS ---
local_css()

# --- Page Title ---
page_header("Dataset Viewer", "📂")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("card_fraud.csv")
        return df
    except FileNotFoundError:
        st.error("❌ The file 'card_fraud.csv' was not found in the root directory.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- Search Input (styled & functional) ---
    st.markdown("""
        <style>
        .search-box {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        search_query = st.text_input(
            " ", placeholder="🔍 Search by Transaction_ID", label_visibility="collapsed"
        )

    # --- Filter Data ---
    if search_query:
        filtered_df = df[df['Transaction_ID'].astype(str).str.contains(search_query, case=False, na=False)]
        if filtered_df.empty:
            st.warning("No matching Transaction_ID found.")
        else:
            st.markdown(f"### 🔎 Showing results for `{search_query}`")
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
    else:
        st.markdown("### 📋 Complete Dataset")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
else:
    st.warning("⚠️ No data available to display.")
