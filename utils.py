import streamlit as st

def local_css(file_name="style.css"):
    """Applies the shared CSS file globally."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"⚠️ CSS file '{file_name}' not found.")

def page_header(title: str = "Predictive Transaction Intelligence for BFSI", emoji: str = "🛡️"):
    """Displays a consistent page heading with default title."""
    st.markdown(f"""
        <h2 style='
            text-align: center;
            color: #00BFA6;
            font-family: "Segoe UI", sans-serif;
            margin-top: -10px;
        '>
            {emoji} {title}
        </h2>
        <hr style='
            border: 1px solid #00BFA6;
            margin-top: -5px;
            margin-bottom: 25px;
        ' />
    """, unsafe_allow_html=True)
