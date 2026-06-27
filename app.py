"""
AI Healthcare Chatbot - Home Page
Welcome page with navigation to Login/Admin/Patient portals
"""

import streamlit as st
from database import db
import config
import auth


# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
auth.init_session_state()

# Custom CSS for beautiful home page
st.markdown("""
    <style>
    .main-header {
        font-size: 4rem;
        color: #1f77b4;
        text-align: center;
        margin: 2rem 0;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .subtitle {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-10px);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .cta-button {
        background: linear-gradient(90deg, #1f77b4, #2196f3);
        color: white;
        padding: 1rem 3rem;
        border-radius: 2rem;
        font-size: 1.2rem;
        font-weight: bold;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .stat-label {
        font-size: 1rem;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main home page"""
    
    # Check if already logged in - redirect to appropriate page
    if auth.is_authenticated():
        user = auth.get_current_user()
        if user['role'] == 'admin':
            st.switch_page("pages/2_🎛️_Admin_Dashboard.py")
        else:
            st.switch_page("pages/3_🏥_Patient_Portal.py")
        st.stop()
    
    # Hero Section
    st.markdown(f'<h1 class="main-header">{config.APP_ICON} {config.APP_TITLE}</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your 24/7 AI-Powered Healthcare Assistant</p>', 
                unsafe_allow_html=True)
    
    # Call to Action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🚀 Get Started")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔐 Login", use_container_width=True, type="primary"):
                st.switch_page("pages/1_🔐_Login.py")
        with col_b:
            if st.button("📝 Register", use_container_width=True):
                st.session_state.show_register = True
                st.switch_page("pages/1_🔐_Login.py")
    
    st.divider()
    
    # Features Section
    st.markdown("### 🌟 Features")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🩺</div>
            <div class="feature-title">Symptom Checker</div>
            <p>AI-powered analysis with severity assessment and health advice</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📅</div>
            <div class="feature-title">Appointments</div>
            <p>Easy booking with 10+ medical specialties</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">AI Chatbot</div>
            <p>Intelligent assistant available 24/7 for health queries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎛️</div>
            <div class="feature-title">Admin Panel</div>
            <p>Complete management dashboard for healthcare providers</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Statistics Section
    stats = db.get_statistics()
    st.markdown("### 📊 Platform Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stat-number">{stats.get('total_patients', 0)}</div>
            <div class="stat-label">Registered Patients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stat-number">{stats.get('total_appointments', 0)}</div>
            <div class="stat-label">Appointments Booked</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stat-number">{stats.get('total_symptom_checks', 0)}</div>
            <div class="stat-label">Symptom Checks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stat-number">{stats.get('active_users', 0)}</div>
            <div class="stat-label">Active Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # How It Works
    st.markdown("### 📖 How It Works")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Register/Login
        Create your account in seconds. Secure authentication with role-based access.
        """)
    
    with col2:
        st.markdown("""
        #### 2️⃣ Chat with AI
        Describe your symptoms or health concerns to our intelligent chatbot.
        """)
    
    with col3:
        st.markdown("""
        #### 3️⃣ Get Help
        Receive instant analysis, book appointments, and access health information.
        """)
    
    st.divider()
    
    # Medical Specialties
    st.markdown("### 🏥 Available Medical Specialties")
    cols = st.columns(5)
    specialties_with_icons = [
        ("🩺", "General Medicine"),
        ("❤️", "Cardiology"),
        ("🧴", "Dermatology"),
        ("👶", "Pediatrics"),
        ("🦴", "Orthopedics"),
        ("🧠", "Neurology"),
        ("👂", "ENT"),
        ("👁️", "Ophthalmology"),
        ("🧘", "Psychiatry"),
        ("👩", "Gynecology")
    ]
    
    for idx, (icon, specialty) in enumerate(specialties_with_icons):
        with cols[idx % 5]:
            st.markdown(f"**{icon} {specialty}**")
    
    st.divider()
    
    # Disclaimer
    with st.expander("⚠️ Important Medical Disclaimer"):
        st.warning(config.MEDICAL_DISCLAIMER)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p><strong>AI Healthcare Chatbot</strong> | Powered by Advanced AI Technology</p>
        <p>For emergencies, call 911 immediately | Available 24/7</p>
    </div>
    """, unsafe_allow_html=True)


# Old functions removed - now handled in separate pages
if __name__ == "__main__":
    main()


