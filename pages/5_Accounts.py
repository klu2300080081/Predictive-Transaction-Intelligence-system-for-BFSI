import streamlit as st


from utils import local_css, page_header

local_css()
page_header()


st.set_page_config(page_title="Accounts", layout="wide")

st.title("👤 Account Information")
st.write("**Name:** Admin")
st.write("**Email:** admin@gmail.com")
