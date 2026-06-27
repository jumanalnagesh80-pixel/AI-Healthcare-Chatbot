"""
Emergency Alert System
Quick access to emergency contacts, services, and SOS features
"""

import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
import auth

st.set_page_config(page_title="Emergency", page_icon="🚨", layout="wide")

auth.init_session_state()

if not auth.is_authenticated():
    st.warning("⚠️ Please log in")
    st.switch_page("pages/1_🔐_Login.py")
    st.stop()

# Emergency styling
st.markdown("""<style>
.emergency-button {
    background-color: #dc3545;
    color: white;
    padding: 2rem;
    border-radius: 1rem;
    text-align: center;
    font-size: 2rem;
    font-weight: bold;
}
.warning-box {
    background-color: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1rem;
    border-radius: 0.5rem;
}
</style>""", unsafe_allow_html=True)


def main():
    st.title("🚨 Emergency Services")
    
    user = auth.get_current_user()
    
    # Emergency alert banner
    st.error("""
    ⚠️ **FOR LIFE-THREATENING EMERGENCIES:**
    - **Call 911 immediately** (USA)
    - **Go to nearest Emergency Room**
    - **Do not wait - Act Now!**
    """)
    
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["🚨 Emergency", "📞 Contacts", "🆘 Resources"])
    
    with tab1:
        show_emergency_services()
    
    with tab2:
        if user['role'] == 'patient':
            if 'current_patient' in st.session_state and st.session_state.current_patient:
                show_emergency_contacts(st.session_state.current_patient['patient_id'])
            else:
                st.warning("⚠️ Link your patient profile to manage emergency contacts")
        else:
            st.info("Emergency contacts management for patients")
    
    with tab3:
        show_emergency_resources()


def show_emergency_services():
    st.subheader("🚨 Emergency Hotlines")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚑 Medical Emergency
        - **Call: 911** (USA/Canada)
        - **Emergency Room**: Nearest hospital
        - **Available:** 24/7
        
        ### ☎️ Other Emergency Numbers
        - **Poison Control:** 1-800-222-1222
        - **Suicide Prevention:** 988
        - **Domestic Violence:** 1-800-799-7233
        """)
    
    with col2:
        st.markdown("""
        ### 🏥 When to Call 911
        - ✅ Chest pain or pressure
        - ✅ Difficulty breathing
        - ✅ Severe bleeding
        - ✅ Loss of consciousness
        - ✅ Stroke symptoms (FAST)
        - ✅ Severe allergic reaction
        - ✅ Major trauma/injury
        """)
    
    st.divider()
    
    # Quick action buttons
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚨 CALL 911", use_container_width=True, type="primary"):
            st.error("☎️ **DIAL 911 ON YOUR PHONE NOW!**")
            st.write("📍 Share your location with emergency services")
    
    with col2:
        if st.button("🏥 Find Nearest Hospital", use_container_width=True):
            st.info("""
            **Nearest Hospitals:**
            - City General Hospital (2.3 mi)
            - Memorial Medical Center (3.1 mi)
            - St. Mary's Hospital (4.5 mi)
            """)
    
    with col3:
        if st.button("📋 My Medical Info", use_container_width=True):
            if 'current_patient' in st.session_state and st.session_state.current_patient:
                patient = st.session_state.current_patient
                st.success(f"""
                **Emergency Medical Information:**
                - **Name:** {patient['name']}
                - **Age:** {patient['age']}
                - **Blood Type:** {patient.get('blood_group', 'N/A')}
                - **Allergies:** {patient.get('allergies', 'None')}
                - **Conditions:** {patient.get('chronic_conditions', 'None')}
                """)


def show_emergency_contacts(patient_id: int):
    st.subheader("📞 Emergency Contacts")
    
    contacts = db.get_patient_emergency_contacts(patient_id)
    
    if contacts:
        for contact in contacts:
            is_primary = "⭐ PRIMARY" if contact['is_primary'] else ""
            
            with st.expander(f"👤 {contact['contact_name']} {is_primary}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Name:** {contact['contact_name']}")
                    st.markdown(f"**Relationship:** {contact['relationship']}")
                    st.markdown(f"**Phone:** {contact['phone']}")
                
                with col2:
                    if contact['email']:
                        st.markdown(f"**Email:** {contact['email']}")
                    if contact['address']:
                        st.markdown(f"**Address:** {contact['address']}")
                
                if st.button(f"📞 Call {contact['contact_name']}", 
                           key=f"call_{contact['contact_id']}"):
                    st.info(f"📱 Call: {contact['phone']}")
    else:
        st.info("No emergency contacts added")
    
    st.divider()
    
    # Add new contact
    with st.expander("➕ Add Emergency Contact"):
        with st.form("add_emergency_contact"):
            contact_name = st.text_input("Name *", placeholder="John Doe")
            relationship = st.selectbox("Relationship *", 
                ["Spouse", "Parent", "Sibling", "Child", "Friend", "Other"])
            phone = st.text_input("Phone *", placeholder="+1234567890")
            email = st.text_input("Email", placeholder="contact@email.com")
            address = st.text_area("Address")
            is_primary = st.checkbox("Set as primary contact")
            
            submit = st.form_submit_button("✅ Add Contact")
            
            if submit and contact_name and phone:
                contact_id = db.add_emergency_contact(
                    patient_id, contact_name, relationship, phone,
                    email, address, 1 if is_primary else 0
                )
                
                if contact_id:
                    st.success("✅ Emergency contact added!")
                    st.rerun()


def show_emergency_resources():
    st.subheader("🆘 Emergency Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏥 Medical Resources
        - [CDC Emergency Preparedness](https://www.cdc.gov/cpr/)
        - [Red Cross Emergency App](https://www.redcross.org/get-help/how-to-prepare-for-emergencies/mobile-apps.html)
        - [FEMA Preparedness](https://www.ready.gov/)
        
        ### 🧠 Mental Health
        - **Crisis Text Line:** Text HOME to 741741
        - **SAMHSA Helpline:** 1-800-662-4357
        - **Veterans Crisis:** 988 then press 1
        """)
    
    with col2:
        st.markdown("""
        ### 📱 Safety Apps
        - Medical ID (iOS/Android)
        - ICE (In Case of Emergency)
        - Emergency SOS
        
        ### 📋 Prepare Emergency Kit
        - ✅ First aid supplies
        - ✅ Medications (7-day supply)
        - ✅ Medical documents
        - ✅ Emergency contacts list
        - ✅ Flashlight & batteries
        - ✅ Water & non-perishable food
        """)
    
    st.divider()
    
    st.markdown("""
    ### 🔍 Recognize Emergency Symptoms
    
    **FAST for Stroke:**
    - **F**ace drooping
    - **A**rm weakness
    - **S**peech difficulty
    - **T**ime to call 911
    
    **Heart Attack Signs:**
    - Chest pain or discomfort
    - Upper body pain (arms, back, neck, jaw)
    - Shortness of breath
    - Cold sweat, nausea
    """)


if __name__ == "__main__":
    main()
