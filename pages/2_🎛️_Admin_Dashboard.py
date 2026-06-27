"""
Admin Dashboard for AI Healthcare Chatbot
"""

import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
import auth

# Page config
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🎛️",
    layout="wide"
)

# Initialize session state
auth.init_session_state()

# Check authentication and admin role
if not auth.is_authenticated():
    st.warning("⚠️ Please log in to access this page")
    st.switch_page("pages/1_🔐_Login.py")
    st.stop()

if not auth.is_admin():
    st.error("❌ You don't have permission to access this page")
    st.switch_page("pages/3_🏥_Patient_Portal.py")
    st.stop()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .stButton>button {
        width: 100%;
    }
    .dataframe {
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    # Header with logout
    col1, col2 = st.columns([3, 1])
    with col1:
        user = auth.get_current_user()
        st.markdown(f'<h1 class="main-header">🎛️ Admin Dashboard</h1>', unsafe_allow_html=True)
        st.markdown(f"**Welcome, {user['full_name']}** ({user['username']})")
    with col2:
        st.write("")
        st.write("")
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout_user()
            st.switch_page("pages/1_🔐_Login.py")
    
    st.divider()
    
    # Tabs for different admin sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "👥 Patients", 
        "📅 Appointments", 
        "👤 Users",
        "⚙️ Settings"
    ])

    
    # Tab 1: Dashboard Overview
    with tab1:
        show_dashboard()
    
    # Tab 2: Patient Management
    with tab2:
        show_patients()
    
    # Tab 3: Appointment Management
    with tab3:
        show_appointments()
    
    # Tab 4: User Management
    with tab4:
        show_users()
    
    # Tab 5: Settings
    with tab5:
        show_settings()


def show_dashboard():
    """Display dashboard overview with statistics"""
    st.subheader("📊 System Overview")
    
    # Get statistics
    stats = db.get_statistics()
    
    # Display metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Patients",
            value=stats.get('total_patients', 0),
            delta=f"+{stats.get('recent_patients', 0)} this week"
        )

    
    with col2:
        st.metric(
            label="📅 Total Appointments",
            value=stats.get('total_appointments', 0),
            delta=f"{stats.get('todays_appointments', 0)} today"
        )
    
    with col3:
        st.metric(
            label="🩺 Symptom Checks",
            value=stats.get('total_symptom_checks', 0),
            delta="Health monitoring"
        )
    
    with col4:
        st.metric(
            label="👤 Active Users",
            value=stats.get('active_users', 0),
            delta=f"{stats.get('total_users', 0)} total"
        )
    
    st.divider()
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Recent Appointments")
        appointments = db.get_all_appointments()[:10]
        if appointments:
            df = pd.DataFrame(appointments)
            df = df[['patient_name', 'specialty', 'date', 'time', 'status']]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No appointments found")

    
    with col2:
        st.subheader("👥 Recent Patients")
        patients = db.get_all_patients()[:10]
        if patients:
            df = pd.DataFrame(patients)
            df = df[['name', 'age', 'gender', 'phone', 'blood_group']]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No patients found")


def show_patients():
    """Patient management section"""
    st.subheader("👥 Patient Management")
    
    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("🔍 Search patients", placeholder="Search by name or phone")
    with col2:
        gender_filter = st.selectbox("Gender", ["All", "Male", "Female", "Other"])
    with col3:
        st.write("")
        st.write("")
        refresh = st.button("🔄 Refresh", use_container_width=True)
    
    # Get all patients
    patients = db.get_all_patients()
    
    if patients:
        # Apply filters
        if search_query:
            patients = [p for p in patients if search_query.lower() in p['name'].lower() 
                       or search_query in p['phone']]
        if gender_filter != "All":
            patients = [p for p in patients if p['gender'] == gender_filter]

        
        st.write(f"**Total patients:** {len(patients)}")
        
        # Display patients in a table with actions
        for patient in patients:
            with st.expander(f"👤 {patient['name']} - {patient['phone']}"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Age:** {patient['age']}")
                    st.write(f"**Gender:** {patient['gender']}")
                    st.write(f"**Phone:** {patient['phone']}")
                
                with col2:
                    st.write(f"**Email:** {patient.get('email', 'N/A')}")
                    st.write(f"**Blood Group:** {patient.get('blood_group', 'N/A')}")
                
                with col3:
                    if st.button("🗑️ Delete", key=f"del_patient_{patient['patient_id']}"):
                        if db.delete_patient(patient['patient_id']):
                            st.success("Patient deleted")
                            st.rerun()
                        else:
                            st.error("Failed to delete")
    else:
        st.info("No patients found")


def show_appointments():
    """Appointment management section"""
    st.subheader("📅 Appointment Management")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Scheduled", "Completed", "Cancelled"])
    with col2:
        date_filter = st.date_input("Date", value=None)
    with col3:
        st.write("")
        st.write("")
        refresh = st.button("🔄 Refresh", key="refresh_appointments", use_container_width=True)

    
    # Get appointments
    if status_filter == "All":
        appointments = db.get_all_appointments()
    else:
        appointments = db.get_all_appointments(status_filter)
    
    # Apply date filter
    if date_filter:
        appointments = [a for a in appointments if a['date'] == str(date_filter)]
    
    st.write(f"**Total appointments:** {len(appointments)}")
    
    if appointments:
        for apt in appointments:
            status_emoji = "✅" if apt['status'] == "Scheduled" else "❌" if apt['status'] == "Cancelled" else "✓"
            
            with st.expander(f"{status_emoji} {apt['patient_name']} - {apt['specialty']} ({apt['date']})"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Patient:** {apt['patient_name']}")
                    st.write(f"**Specialty:** {apt['specialty']}")
                    st.write(f"**Symptoms:** {apt.get('symptoms', 'N/A')}")
                
                with col2:
                    st.write(f"**Date:** {apt['date']}")
                    st.write(f"**Time:** {apt['time']}")
                    st.write(f"**Status:** {apt['status']}")
                
                with col3:
                    new_status = st.selectbox(
                        "Change Status",
                        ["Scheduled", "Completed", "Cancelled"],
                        key=f"status_{apt['appointment_id']}"
                    )
                    if st.button("💾 Update", key=f"update_{apt['appointment_id']}"):
                        if db.update_appointment_status(apt['appointment_id'], new_status):
                            st.success("Updated!")
                            st.rerun()
                    
                    if st.button("🗑️ Delete", key=f"del_apt_{apt['appointment_id']}"):
                        if db.delete_appointment(apt['appointment_id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("No appointments found")




def show_users():
    """User management section"""
    st.subheader("👤 User Management")
    
    # Add new user button
    if st.button("➕ Create New User"):
        st.session_state.show_create_user = True
    
    # Create user form
    if st.session_state.get("show_create_user", False):
        with st.form("create_user_form"):
            st.write("**Create New User**")
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_email = st.text_input("Email")
            new_full_name = st.text_input("Full Name")
            new_role = st.selectbox("Role", ["patient", "admin"])
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("✅ Create")
            with col2:
                cancel = st.form_submit_button("❌ Cancel")
            
            if submit and new_username and new_password:
                user_id = db.create_user(new_username, new_password, new_email, new_role, new_full_name)
                if user_id:
                    st.success("User created successfully!")
                    st.session_state.show_create_user = False
                    st.rerun()
                else:
                    st.error("Username already exists")
            
            if cancel:
                st.session_state.show_create_user = False
                st.rerun()
    
    st.divider()

    
    # Display all users
    users = db.get_all_users()
    
    if users:
        st.write(f"**Total users:** {len(users)}")
        
        for user in users:
            status_color = "🟢" if user['is_active'] else "🔴"
            role_emoji = "👑" if user['role'] == 'admin' else "👤"
            
            with st.expander(f"{status_color} {role_emoji} {user['username']} - {user['full_name']}"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Username:** {user['username']}")
                    st.write(f"**Email:** {user['email'] or 'N/A'}")
                    st.write(f"**Role:** {user['role']}")
                
                with col2:
                    st.write(f"**Status:** {'Active' if user['is_active'] else 'Inactive'}")
                    st.write(f"**Created:** {user['created_at']}")
                    st.write(f"**Last Login:** {user.get('last_login', 'Never')}")
                
                with col3:
                    # Can't modify current logged in user
                    current_user = auth.get_current_user()
                    if user['user_id'] != current_user['user_id']:
                        if user['is_active']:
                            if st.button("🔒 Deactivate", key=f"deact_{user['user_id']}"):
                                if db.update_user_status(user['user_id'], 0):
                                    st.success("User deactivated")
                                    st.rerun()
                        else:
                            if st.button("🔓 Activate", key=f"act_{user['user_id']}"):
                                if db.update_user_status(user['user_id'], 1):
                                    st.success("User activated")
                                    st.rerun()
                    else:
                        st.info("(You)")
    else:
        st.info("No users found")


def show_settings():
    """Settings section"""
    st.subheader("⚙️ System Settings")
    
    st.info("🔧 Settings functionality coming soon!")
    
    # Database info
    st.write("**Database Information:**")
    stats = db.get_statistics()
    st.json(stats)


if __name__ == "__main__":
    main()
