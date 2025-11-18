import streamlit as st
import pandas as pd
import joblib
import sklearn.compose._column_transformer
import plotly.graph_objects as go
from utils import local_css, page_header  # if you have your shared styling file

# --- Global CSS ---
local_css()

# --- Page Header ---
page_header("Customer Churn Prediction", "🔮")

# --- Compatibility Fix for sklearn >= 1.3 ---
if not hasattr(sklearn.compose._column_transformer, "_RemainderColsList"):
    class _RemainderColsList(list):
        pass
    sklearn.compose._column_transformer._RemainderColsList = _RemainderColsList


# --- Load Model ---
@st.cache_resource
def load_model():
    try:
        model = joblib.load("churn_prediction_rfp.pkl")
        st.success("✅ Model loaded successfully!")
        return model
    except FileNotFoundError:
        st.error("❌ Model file 'churn_prediction_rfp.pkl' not found.")
        return None
    except Exception as e:
        st.error(f"⚠️ Error loading model: {e}")
        return None


model = load_model()


# --- If Model Loaded, Show Input Form ---
if model:
    st.markdown("### 🧾 Enter Customer Details for Prediction")

    with st.form("churn_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=670)
            geography = st.text_input("Geography")
            gender = st.selectbox("Gender", ["Male", "Female"])
            age = st.slider("Age", 18, 100, 45)

        with col2:
            tenure = st.number_input("Tenure (Years)", min_value=0, max_value=10, value=5)
            balance = st.number_input("Account Balance", min_value=0.0, value=125000.0, step=1000.0)
            num_products = st.selectbox("Number of Products", [1, 2, 3, 4], index=1)
            has_card = st.selectbox("Has Credit Card?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")

        with col3:
            is_active = st.selectbox("Is Active Member?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
            salary = st.number_input("Estimated Salary", min_value=0.0, value=60000.0, step=500.0)

        submit = st.form_submit_button("🔍 Predict Churn")

    # --- Prediction Logic ---
    if submit:
        new_customer = pd.DataFrame({
            'CreditScore': [credit_score],
            'Geography': [geography],
            'Gender': [gender],
            'Age': [age],
            'Tenure': [tenure],
            'Balance': [balance],
            'NumOfProducts': [num_products],
            'HasCrCard': [has_card],
            'IsActiveMember': [is_active],
            'EstimatedSalary': [salary]
        })

        try:
            churn_pred = model.predict(new_customer)[0]
            churn_prob = model.predict_proba(new_customer)[:, 1][0]

            st.markdown("---")
            st.subheader("📊 Prediction Results")

            col1, col2 = st.columns([1, 1])

            with col1:
                st.metric("Churn Prediction", "Yes" if churn_pred == 1 else "No")
                if churn_pred == 1:
                    st.error("⚠️ This customer is **likely to churn.** Take proactive measures.")
                else:
                    st.success("✅ This customer is **not likely to churn.**")

            with col2:
                st.metric("Churn Probability", f"{churn_prob * 100:.2f}%")

            # --- Gauge Chart ---
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=churn_prob * 100,
                title={'text': "Churn Probability (%)", 'font': {'size': 18}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#00BFA6" if churn_pred == 0 else "#FF4B4B"},
                    'steps': [
                        {'range': [0, 30], 'color': '#1E3D59'},
                        {'range': [30, 60], 'color': '#32527B'},
                        {'range': [60, 100], 'color': '#7B1E1E'},
                    ],
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")
else:
    st.warning("⚠️ Please ensure the model file exists and is valid.")
