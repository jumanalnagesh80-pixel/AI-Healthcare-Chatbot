"""
Patient Portal for AI Healthcare Chatbot
Enhanced version of the main chatbot interface with authentication
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta, date
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from chatbot_engine import chatbot
import config
import auth

# Page configuration
st.set_page_config(
    page_title="Patient Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
auth.init_session_state()

# Check authentication
if not auth.is_authenticated():
    st.warning("⚠️ Please log in to access this page")
    st.switch_page("pages/1_🔐_Login.py")
    st.stop()

# Check if admin trying to access patient portal
if auth.is_admin():
    st.info("You're logged in as admin. Redirecting to admin dashboard...")
    st.switch_page("pages/2_🎛️_Admin_Dashboard.py")
    st.stop()

# Initialize chat session
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None



# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-left: 4px solid #667eea;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .info-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1f77b4, #2196f3);
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .quick-action {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    user = auth.get_current_user()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<h1 class="main-header">🏥 {config.APP_TITLE}</h1>', 
                    unsafe_allow_html=True)
        st.markdown(f"**Welcome, {user['full_name']}!** 👋")
    with col2:
        st.write("")
        st.write("")
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout_user()
            st.switch_page("pages/1_🔐_Login.py")
    
    # Sidebar
    with st.sidebar:
        st.header("🏥 Patient Portal")

        
        # Patient Profile Section
        st.subheader("👤 My Profile")
        
        # Check if user has a patient profile
        if not st.session_state.current_patient:
            phone_number = st.text_input("📱 Enter your phone number:", 
                                         placeholder="+1234567890",
                                         help="Link your account to patient records")
            
            if st.button("🔗 Link Profile"):
                if phone_number:
                    patient = db.get_patient_by_phone(phone_number)
                    if patient:
                        st.session_state.current_patient = patient
                        st.success(f"✓ Profile linked!")
                        st.rerun()
                    else:
                        st.warning("❌ No patient record found. Please register below.")
                else:
                    st.error("Please enter a phone number")
        
        # Display current patient info
        if st.session_state.current_patient:
            patient = st.session_state.current_patient
            st.success(f"**{patient['name']}**")
            st.write(f"📧 {patient.get('email', 'N/A')}")
            st.write(f"📱 {patient['phone']}")
            st.write(f"🩸 Blood Group: {patient.get('blood_group', 'N/A')}")
            
            if st.button("🔄 Unlink Profile"):
                st.session_state.current_patient = None
                st.rerun()
        
        st.divider()
        
        # Patient Registration
        if not st.session_state.current_patient:
            with st.expander("📝 Create Patient Profile"):
                register_patient()
        
        st.divider()
        
        # Appointment Booking
        with st.expander("📅 Book Appointment"):
            book_appointment()
        
        st.divider()
        
        # View Appointments
        with st.expander("📋 My Appointments"):
            view_appointments()
        
        st.divider()
        
        # Health History
        if st.session_state.current_patient:
            with st.expander("🩺 Symptom History"):
                view_symptom_history()
    
    # Main chat interface
    st.header("💬 Chat with HealthBot")
    
    # Display disclaimer
    with st.expander("⚠️ Medical Disclaimer", expanded=False):
        st.warning(config.MEDICAL_DISCLAIMER)
    
    # Chat container
    chat_container = st.container()

    
    with chat_container:
        # Display chat history
        if not st.session_state.chat_history:
            st.info("👋 Start a conversation! Try asking about symptoms, booking appointments, or health information.")
        
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">👤 **You:** {message["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message">🤖 **{config.BOT_NAME}:** {message["content"]}</div>', 
                           unsafe_allow_html=True)
    
    # Chat input
    st.divider()
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("Type your message here:", 
                                   placeholder="e.g., I have a headache and fever",
                                   label_visibility="collapsed",
                                   key="user_input")
    
    with col2:
        send_button = st.button("📤 Send", use_container_width=True)
    
    # Process user input
    if send_button and user_input:
        process_message(user_input)
    
    # Quick action buttons
    st.divider()
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🩺 Check Symptoms", use_container_width=True):
            auto_message("I want to check my symptoms")
    
    with col2:
        if st.button("📅 Book Appointment", use_container_width=True):
            auto_message("I want to book an appointment")
    
    with col3:
        if st.button("📚 Health Info", use_container_width=True):
            auto_message("Give me health information")
    
    with col4:
        if st.button("❓ Help", use_container_width=True):
            auto_message("Help me")


def process_message(user_input: str):
    """Process user message and generate bot response"""
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    # Save to database
    patient_id = st.session_state.current_patient['patient_id'] if st.session_state.current_patient else None
    db.save_chat_message(st.session_state.session_id, "user", user_input, patient_id)
    
    # Get bot response
    session_context = {
        "current_patient": st.session_state.current_patient,
        "user": auth.get_current_user()
    }
    response, intent = chatbot.process_message(user_input, session_context)

    
    # Add bot response to history
    st.session_state.chat_history.append({
        "role": "bot",
        "content": response,
        "timestamp": datetime.now(),
        "intent": intent
    })
    
    # Save to database
    db.save_chat_message(st.session_state.session_id, "bot", response, patient_id)
    
    # Log symptoms if symptom check
    if intent == "symptom_check":
        symptoms = chatbot._extract_symptoms(user_input)
        if symptoms:
            severity = chatbot._assess_severity(symptoms)
            possible_conditions = chatbot._analyze_symptoms(symptoms)
            advice = chatbot._generate_advice(symptoms, severity)
            db.log_symptoms(', '.join(symptoms), severity, possible_conditions, advice, patient_id)
    
    st.rerun()


def auto_message(message: str):
    """Automatically send a message"""
    process_message(message)


def register_patient():
    """Patient registration form"""
    st.write("Create your patient profile:")
    
    user = auth.get_current_user()
    
    with st.form("registration_form"):
        name = st.text_input("Full Name *", value=user.get('full_name', ''))
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age *", min_value=1, max_value=120, value=30)
        with col2:
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        
        phone = st.text_input("Phone Number *", placeholder="+1234567890")
        email = st.text_input("Email", value=user.get('email', ''))
        address = st.text_area("Address", placeholder="123 Main St, City, State")
        
        col3, col4 = st.columns(2)
        with col3:
            blood_group = st.selectbox("Blood Group", 
                                       ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        with col4:
            allergies = st.text_input("Allergies", placeholder="Penicillin, Peanuts")
        
        chronic_conditions = st.text_area("Chronic Conditions", 
                                         placeholder="Diabetes, Hypertension")
        
        submit = st.form_submit_button("📝 Create Profile")
        
        if submit:
            if name and phone and age:
                patient_id = db.add_patient(name, age, gender, phone, email, 
                                           address, blood_group, allergies, chronic_conditions, 
                                           user['user_id'])
                if patient_id:
                    st.success(f"✓ Profile created successfully!")
                    patient = db.get_patient_by_phone(phone)
                    st.session_state.current_patient = patient
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Phone number already exists.")
            else:
                st.error("❌ Please fill in all required fields (*)")


def book_appointment():
    """Appointment booking form"""
    if not st.session_state.current_patient:
        st.warning("⚠️ Please create/link your profile first")
        return

    
    patient = st.session_state.current_patient
    
    st.write(f"Booking for: **{patient['name']}**")
    
    with st.form("appointment_form"):
        specialty = st.selectbox("Medical Specialty *", config.MEDICAL_SPECIALTIES)
        
        col1, col2 = st.columns(2)
        with col1:
            appointment_date = st.date_input("Appointment Date *",
                                            min_value=date.today(),
                                            max_value=date.today() + timedelta(days=90))
        with col2:
            appointment_time = st.selectbox("Appointment Time *", config.TIME_SLOTS)
        
        symptoms = st.text_area("Describe your symptoms", 
                               placeholder="e.g., Chest pain and difficulty breathing")
        
        submit = st.form_submit_button("📅 Book Appointment")
        
        if submit:
            # Check availability
            if db.check_appointment_availability(str(appointment_date), appointment_time):
                appointment_id = db.book_appointment(
                    patient['patient_id'],
                    patient['name'],
                    specialty,
                    str(appointment_date),
                    appointment_time,
                    symptoms
                )
                
                if appointment_id:
                    st.success(f"""
                    ✓ **Appointment Booked Successfully!**
                    
                    **Appointment ID:** {appointment_id}
                    **Date:** {appointment_date}
                    **Time:** {appointment_time}
                    **Specialty:** {specialty}
                    """)
                    st.balloons()
                else:
                    st.error("❌ Failed to book appointment. Please try again.")
            else:
                st.error("❌ This time slot is fully booked. Please choose another time.")


def view_appointments():
    """View patient appointments"""
    if not st.session_state.current_patient:
        st.warning("⚠️ Please create/link your profile first")
        return
    
    patient = st.session_state.current_patient
    appointments = db.get_patient_appointments(patient['patient_id'])
    
    if appointments:
        st.write(f"**Your Appointments:**")
        
        for apt in appointments:
            status_emoji = "✅" if apt['status'] == "Scheduled" else "❌" if apt['status'] == "Cancelled" else "✓"
            st.markdown(f"""
            {status_emoji} **{apt['specialty']}**
            - **Date:** {apt['date']} at {apt['time']}
            - **Status:** {apt['status']}
            - **Symptoms:** {apt['symptoms'] or 'N/A'}
            ---
            """)
    else:
        st.info("📋 No appointments found")


def view_symptom_history():
    """View patient symptom history"""
    if not st.session_state.current_patient:
        st.warning("⚠️ Please create/link your profile first")
        return
    
    patient = st.session_state.current_patient
    history = db.get_patient_symptom_history(patient['patient_id'])
    
    if history:
        st.write(f"**Your Symptom History:**")
        
        for entry in history[:10]:  # Show last 10 entries
            st.markdown(f"""
            **{entry['logged_at']}**
            - **Symptoms:** {entry['symptoms']}
            - **Severity:** {entry['severity']}
            - **Possible Conditions:** {entry['possible_conditions']}
            ---
            """)
    else:
        st.info("🩺 No symptom history found")


if __name__ == "__main__":
    main()
