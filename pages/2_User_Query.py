import streamlit as st


from utils import local_css, page_header

local_css()
page_header()

st.set_page_config(page_title="User Query", layout="wide")

st.title("💬 User Query Interface")
st.markdown("Simulated chatbot frontend (backend can be added later).")

prompt = st.text_input("Ask something...")
if st.button("Send"):
    st.write("🤖 (Future backend response will appear here)")
