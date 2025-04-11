import streamlit as st
from main import ann_app

@st.cache_resource
def load_keras_model():
    return tf.keras.models.load_model('model.h5')

import tensorflow as tf
loaded_model = tf.keras.models.load_model('model.h5')

from auth import register_user, authenticate_user  # Import authentication functions
import os  # For file existence checking

# Initialize session state for login status and user data
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
if "risk_level" not in st.session_state:
    st.session_state.risk_level = None
if "diet_preference" not in st.session_state:
    st.session_state.diet_preference = None

def main():
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-title {
            font-size: 34px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(to right, #1E88E5, #1565C0);
            color: white;
            border-radius: 10px;
        }
        .section-header {
            font-size: 24px;
            font-weight: bold;
            color: #1E88E5;
            margin: 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #1E88E5;
        }
        .sidebar-header {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }
        .about-box {
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #1E88E5;
            margin: 10px 0;
        }
        .diet-plan {
            padding: 20px;
            background-color: #f0f8ff;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="main-title">HEART WISE: AI-DRIVEN HEART DISEASE PREDICTION USING NEURAL NETWORKS</p>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<p class="sidebar-header">Navigation Menu</p>', unsafe_allow_html=True)
        menu = ["Login", "Register", "Home", "Model", "Metrics", "About"]
        if st.session_state.logged_in:
            menu.remove("Login")
            menu.remove("Register")
        choice = st.selectbox('', menu)

    if choice == "Login":
        st.title("🔐 User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

    elif choice == "Register":
        st.title("🔑 User Registration")

        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords do not match! 🔴")
            elif register_user(new_username, new_password):
                st.success("✅ Registration successful! Please go to the Login page.")
            else:
                st.error("❌ Username already exists. Try a different one.")

    elif choice == 'Home':
        if not st.session_state.logged_in:
            st.warning("⚠ Please login to access the Home page.")
            st.stop()

        st.markdown('<p class="section-header">Heart Disease Prediction</p>', unsafe_allow_html=True)
        st.write(f"👤 Logged in as: *{st.session_state.username}*")

        home_tabs = st.tabs(["📖 Overview", "📊 Dataset Features", "🚪 Logout"])
        with home_tabs[0]:
            st.markdown("""
            ### Overview
            This application leverages Artificial Neural Networks (ANN) to predict the likelihood of heart disease based on patient health data. 
            It provides a user-friendly interface and actionable health insights to help users take control of their heart health.
            """)
            st.info("📊 Our model analyzes various patient health parameters to assess their risk of heart disease.")

        with home_tabs[1]:
            st.markdown("### Dataset Features")
            st.write("""
            - *AGE*: Patient's age.
            - *GENDER*: Patient's gender.
            - *RESTING_BP*: Resting blood pressure (mm Hg).
            - *SERUM_CHOLESTEROL*: Serum cholesterol in mg/dl.
            - *TRI_GLYCERIDE*: Triglyceride levels.
            - *LDL*: Low-density lipoprotein cholesterol.
            - *HDL*: High-density lipoprotein cholesterol.
            - *FBS*: Fasting blood sugar (mg/dl).
            - *CHEST_PAIN*: Type and severity of chest pain.
            - *RESTING_ECG*: Resting electrocardiogram results.
            - *TMT*: Treadmill Test results.
            - *ECHO*: Echocardiogram findings.
            - *MAX_HEART_RATE*: Maximum heart rate achieved.
            """)

        with home_tabs[2]:
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.username = ""

    elif choice == 'Model':
        if not st.session_state.logged_in:
            st.warning("⚠ Please login to access the Model page.")
            st.stop()
        ann_app()

    elif choice == "Metrics":
        if not st.session_state.logged_in:
            st.warning("⚠ Please login to access the Metrics page.")
            st.stop()
    
        st.markdown('<p class="section-header">📊 Model Metrics and Performance</p>', unsafe_allow_html=True)
    
        try:
            with open(r"C:\Users\Deepika\OneDrive\Desktop\final_year_project-main\exp.html", "r", encoding='utf-8') as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=800)
        except FileNotFoundError:
            st.error("🚫 Metrics file not found. Please check the file path.")
        except Exception as e:
            st.error(f"⚠ Error loading metrics: {e}")


    else:
        if not st.session_state.logged_in:
            st.warning("⚠ Please login to access the About page.")
            st.stop()

        st.markdown('<p class="section-header">About the Project</p>', unsafe_allow_html=True)
        with st.expander("🎯 Project Significance", expanded=True):
            st.markdown("""
            <div class="about-box">
            This project represents a significant contribution to healthcare technology by:
            - 🏥 Addressing a leading global health concern
            - 🔍 Enabling early detection of heart disease
            - 💻 Leveraging advanced machine learning techniques
            - 🤝 Bridging healthcare and technology
            - 📈 Providing data-driven insights for medical professionals
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<p class="section-header">Future Scope</p>', unsafe_allow_html=True)
        future_scope_items = [
            ("Model Enhancement", "Refining the predictive model with advanced ANN architectures and optimization techniques"),
            ("Healthcare Integration", "Seamless integration with existing healthcare systems and EHR"),
            ("Mobile Solutions", "Development of mobile applications and wearable device integration"),
            ("Advanced Analytics", "Incorporation of genetic data and advanced imaging analysis"),
            ("Clinical Support", "Enhanced decision support tools for healthcare professionals"),
            ("Outcome Prediction", "Long-term outcome predictions and risk assessment"),
            ("Data Integration", "Integration with multiple data sources for comprehensive analysis")
        ]
        cols = st.columns(2)
        for i, (title, description) in enumerate(future_scope_items):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="future-scope-item">
                    <h4>{title}</h4>
                    <p>{description}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        #### Key Features:
        - *Prediction*: AI-powered predictions based on health metrics.
        - *Diet and Lifestyle Advice*: Personalized tips to improve heart health.
        - *Interactive Visuals*: Explore model metrics with detailed charts and graphs.
        """)

        with st.expander("🫀 Heart-Healthy Lifestyle Tips", expanded=True):
            st.markdown("""
            - *Morning Routine*: Start your day with a healthy breakfast, such as oatmeal 🥣, fresh fruits 🍎, and nuts 🥜.
            - *Exercise Daily*: Engage in at least 30 minutes of physical activity, like walking 🚶‍♀, running 🏃‍♂, or cycling 🚴‍♀.
            - *Limit Sodium*: Reduce salt intake 🧂 for better blood pressure control.
            - *Quit Smoking*: Avoid smoking 🚭 as it's a leading cause of heart disease.
            - *Regular Check-Ups*: Monitor your cholesterol 🩺 and blood pressure regularly for early detection.
            """)

main()
