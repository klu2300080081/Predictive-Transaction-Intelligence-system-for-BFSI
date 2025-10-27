import streamlit as st

# --- Apply global CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")
# --- Page Configuration ---
st.set_page_config(
    page_title="Predictive Transaction Intelligence for BFSI",
    layout="wide",
    page_icon="🛡️"
)

# --- Session ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


# --- Login Page ---
def login_page():
    st.markdown("<h2 style='text-align:center;'>🔐 Login Page</h2>", unsafe_allow_html=True)
    st.markdown("### Please log in to continue.")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if username == "admin" and password == "admin":
                st.session_state.logged_in = True
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")


# --- Logout Button ---
def logout_button():
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()


# --- Main Interface (App Home Page) ---
def main_interface():
    # ✅ Show heading only on app.py page
    st.markdown("""
        <h1 style="
            text-align: center;
            color: #00BFA6;
            margin-top: 200px;
            font-family: 'Segoe UI', sans-serif;
        ">
        🛡️ Predictive Transaction Intelligence for BFSI
        </h1>
    """, unsafe_allow_html=True)

    logout_button()


# --- Entry Point ---
if not st.session_state.logged_in:
    # Hide sidebar completely until login
    st.markdown("""
        <style>[data-testid="stSidebar"] {visibility: hidden;}</style>
    """, unsafe_allow_html=True)
    login_page()
else:
    main_interface()


# --- Sidebar & UI Styling ---
st.markdown("""
    <style>
    /* Hide the default 'app' tab */
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] ul li:first-child {
        display: none !important;
    }

    /* Hide the "Pages" header */
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] > div:first-child {
        display: none !important;
    }

    /* Sidebar dark theme */
    [data-testid="stSidebar"] {
        background-color: #0E1117;
        padding-top: 15px;
    }

    /* Center alignment fix for main heading */
    .stMarkdown {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)
