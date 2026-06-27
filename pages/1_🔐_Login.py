"""
Login Page for AI Healthcare Chatbot
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
import auth

# Page config
st.set_page_config(
    page_title="Login - Healthcare Chatbot",
    page_icon="🔐",
    layout="centered"
)

# Initialize session state
auth.init_session_state()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .login-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1f77b4, #2196f3);
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 AI Healthcare Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Intelligent Healthcare Assistant</p>', 
                unsafe_allow_html=True)
    
    st.divider()
    
    # Check if already logged in
    if auth.is_authenticated():
        user = auth.get_current_user()
        st.success(f"✓ Already logged in as **{user['username']}** ({user['role']})")
        
        col1, col2 = st.columns(2)
        with col1:
            if user['role'] == 'admin':
                if st.button("🎛️ Go to Admin Dashboard", use_container_width=True):
                    st.switch_page("pages/2_🎛️_Admin_Dashboard.py")
            else:
                if st.button("🏥 Go to Patient Portal", use_container_width=True):
                    st.switch_page("pages/3_🏥_Patient_Portal.py")
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                auth.logout_user()
                st.rerun()
        return
    
    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login to Your Account")
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_button = st.form_submit_button("🔓 Login", use_container_width=True)
            with col_b:
                register_button = st.form_submit_button("📝 Register", use_container_width=True)
            
            if login_button:
                if username and password:
                    with st.spinner("Authenticating..."):
                        user = db.authenticate_user(username, password)
                        if user:
                            auth.login_user(user)
                            st.success(f"✓ Welcome back, {user['full_name'] or user['username']}!")
                            st.balloons()
                            
                            # Redirect based on role
                            if user['role'] == 'admin':
                                st.info("Redirecting to Admin Dashboard...")
                                st.rerun()
                            else:
                                st.info("Redirecting to Patient Portal...")
                                st.rerun()
                        else:
                            st.error("❌ Invalid username or password")
                else:
                    st.error("❌ Please enter both username and password")
            
            if register_button:
                st.session_state.show_register = True
                st.rerun()
        
        # Demo credentials info
        with st.expander("🔑 Demo Credentials"):
            st.markdown("""
            **Admin Account:**
            - Username: `admin`
            - Password: `admin123`
            
            **Test Patient Account:**
            - Create your own account using the Register button
            """)
    
    # Registration form
    if st.session_state.get("show_register", False):
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 📝 Create New Account")
            
            with st.form("register_form", clear_on_submit=True):
                reg_username = st.text_input("👤 Username *", placeholder="Choose a username")
                reg_password = st.text_input("🔒 Password *", type="password", placeholder="Choose a password")
                reg_confirm_password = st.text_input("🔒 Confirm Password *", type="password", 
                                                     placeholder="Confirm your password")
                reg_full_name = st.text_input("📛 Full Name *", placeholder="Enter your full name")
                reg_email = st.text_input("📧 Email", placeholder="Enter your email")
                
                col_x, col_y = st.columns(2)
                with col_x:
                    submit_register = st.form_submit_button("✅ Create Account", use_container_width=True)
                with col_y:
                    cancel_register = st.form_submit_button("❌ Cancel", use_container_width=True)
                
                if submit_register:
                    if not reg_username or not reg_password or not reg_full_name:
                        st.error("❌ Please fill in all required fields (*)")
                    elif reg_password != reg_confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(reg_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        user_id = db.create_user(reg_username, reg_password, reg_email, 
                                                "patient", reg_full_name)
                        if user_id:
                            st.success("✓ Account created successfully! Please login.")
                            st.balloons()
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error("❌ Username already exists. Please choose another.")
                
                if cancel_register:
                    st.session_state.show_register = False
                    st.rerun()
    
    # Features section
    st.divider()
    st.markdown("### 🌟 Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h4>🩺 Symptom Checker</h4>
        <p>AI-powered symptom analysis with severity assessment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h4>📅 Appointments</h4>
        <p>Easy booking and management of medical appointments</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
        <h4>💬 AI Chatbot</h4>
        <p>Intelligent health assistant available 24/7</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
