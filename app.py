"""
AI Healthcare Chatbot - Main Application
Streamlit-based web interface for the healthcare chatbot
"""

import streamlit as st
from datetime import datetime, timedelta, date
import uuid
from database import db
from chatbot_engine import chatbot
import config


# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
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
        background-color: #1f77b4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None


def main():
    """Main application function"""
    
    # Header
    st.markdown(f'<h1 class="main-header">{config.APP_ICON} {config.APP_TITLE}</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🏥 Menu")
        
        # Patient Login/Registration
        st.subheader("👤 Patient Login")
        phone_number = st.text_input("Enter your phone number:", 
                                     placeholder="+1234567890",
                                     help="Used for identifying your records")
        
        if st.button("🔍 Login"):
            if phone_number:
                patient = db.get_patient_by_phone(phone_number)
                if patient:
                    st.session_state.current_patient = patient
                    st.success(f"✓ Welcome back, {patient['name']}!")
                else:
                    st.warning("❌ Patient not found. Please register below.")
            else:
                st.error("Please enter a phone number")
        
        # Display current patient info
        if st.session_state.current_patient:
            st.info(f"**Logged in as:** {st.session_state.current_patient['name']}")
            if st.button("🚪 Logout"):
                st.session_state.current_patient = None
                st.rerun()
        
        st.divider()
        
        # Patient Registration
        with st.expander("📝 New Patient Registration"):
            register_patient()
        
        st.divider()
        
        # Appointment Booking
        with st.expander("📅 Book Appointment"):
            book_appointment()
        
        st.divider()
        
        # View Appointments
        with st.expander("📋 View My Appointments"):
            view_appointments()
        
        st.divider()
        
        # Database Statistics
        with st.expander("📊 System Statistics"):
            show_statistics()
    
    # Main chat interface
    st.header("💬 Chat with HealthBot")
    
    # Display disclaimer
    with st.expander("⚠️ Medical Disclaimer", expanded=False):
        st.warning(config.MEDICAL_DISCLAIMER)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
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
            "current_patient": st.session_state.current_patient
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
    
    # Quick action buttons
    st.divider()
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🩺 Check Symptoms"):
            auto_message("I want to check my symptoms")
    
    with col2:
        if st.button("📅 Book Appointment"):
            auto_message("I want to book an appointment")
    
    with col3:
        if st.button("📚 Health Info"):
            auto_message("Give me health information")
    
    with col4:
        if st.button("❓ Help"):
            auto_message("Help me")


def auto_message(message: str):
    """Automatically send a message"""
    st.session_state.chat_history.append({
        "role": "user",
        "content": message,
        "timestamp": datetime.now()
    })
    
    patient_id = st.session_state.current_patient['patient_id'] if st.session_state.current_patient else None
    db.save_chat_message(st.session_state.session_id, "user", message, patient_id)
    
    response, intent = chatbot.process_message(message)
    
    st.session_state.chat_history.append({
        "role": "bot",
        "content": response,
        "timestamp": datetime.now(),
        "intent": intent
    })
    
    db.save_chat_message(st.session_state.session_id, "bot", response, patient_id)
    st.rerun()


def register_patient():
    """Patient registration form"""
    st.write("Fill in your details to register:")
    
    with st.form("registration_form"):
        name = st.text_input("Full Name *", placeholder="John Doe")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age *", min_value=1, max_value=120, value=30)
        with col2:
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        
        phone = st.text_input("Phone Number *", placeholder="+1234567890")
        email = st.text_input("Email", placeholder="john@example.com")
        address = st.text_area("Address", placeholder="123 Main St, City, State")
        
        col3, col4 = st.columns(2)
        with col3:
            blood_group = st.selectbox("Blood Group", 
                                       ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        with col4:
            allergies = st.text_input("Allergies", placeholder="Penicillin, Peanuts")
        
        chronic_conditions = st.text_area("Chronic Conditions", 
                                         placeholder="Diabetes, Hypertension")
        
        submit = st.form_submit_button("📝 Register")
        
        if submit:
            if name and phone and age:
                patient_id = db.add_patient(name, age, gender, phone, email, 
                                           address, blood_group, allergies, chronic_conditions)
                if patient_id:
                    st.success(f"✓ Successfully registered! Patient ID: {patient_id}")
                    patient = db.get_patient_by_phone(phone)
                    st.session_state.current_patient = patient
                    st.balloons()
                else:
                    st.error("❌ Registration failed. Phone number may already exist.")
            else:
                st.error("❌ Please fill in all required fields (*)")


def book_appointment():
    """Appointment booking form"""
    if not st.session_state.current_patient:
        st.warning("⚠️ Please login first to book an appointment")
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
                    
                    You will receive a confirmation shortly.
                    """)
                    st.balloons()
                else:
                    st.error("❌ Failed to book appointment. Please try again.")
            else:
                st.error("❌ This time slot is fully booked. Please choose another time.")


def view_appointments():
    """View patient appointments"""
    if not st.session_state.current_patient:
        st.warning("⚠️ Please login first to view your appointments")
        return
    
    patient = st.session_state.current_patient
    appointments = db.get_patient_appointments(patient['patient_id'])
    
    if appointments:
        st.write(f"**Appointments for {patient['name']}:**")
        
        for apt in appointments:
            status_emoji = "✅" if apt['status'] == "Scheduled" else "❌"
            st.markdown(f"""
            {status_emoji} **{apt['specialty']}**
            - **Date:** {apt['date']} at {apt['time']}
            - **Status:** {apt['status']}
            - **Symptoms:** {apt['symptoms'] or 'N/A'}
            ---
            """)
    else:
        st.info("📋 No appointments found")


def show_statistics():
    """Display system statistics"""
    stats = db.get_statistics()
    
    st.metric("Total Patients", stats.get('total_patients', 0))
    st.metric("Total Appointments", stats.get('total_appointments', 0))
    st.metric("Scheduled Appointments", stats.get('scheduled_appointments', 0))
    st.metric("Symptom Checks", stats.get('total_symptom_checks', 0))


if __name__ == "__main__":
    main()
