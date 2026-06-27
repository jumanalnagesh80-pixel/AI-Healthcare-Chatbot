"""
Prescription Management System
Track medications, dosages, refills, and reminders
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
import auth
import utils

st.set_page_config(
    page_title="Prescriptions",
    page_icon="💊",
    layout="wide"
)

auth.init_session_state()

if not auth.is_authenticated():
    st.warning("⚠️ Please log in to access this page")
    st.switch_page("pages/1_🔐_Login.py")
    st.stop()

# Custom CSS
st.markdown("""
    <style>
    .prescription-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .active-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .expired-badge {
        background-color: #dc3545;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    user = auth.get_current_user()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("💊 Prescription Management")
        st.markdown(f"**{user['full_name']}**")
    with col2:
        st.write("")
        if st.button("🔙 Back to Portal", use_container_width=True):
            if user['role'] == 'admin':
                st.switch_page("pages/2_🎛️_Admin_Dashboard.py")
            else:
                st.switch_page("pages/3_🏥_Patient_Portal.py")
    
    st.divider()
    
    # Get patient info
    if user['role'] == 'patient':
        # Patient view - need to get their patient record
        if 'current_patient' not in st.session_state or not st.session_state.current_patient:
            st.warning("⚠️ Please link your patient profile first")
            phone = st.text_input("Enter your phone number:")
            if st.button("Link Profile"):
                patient = db.get_patient_by_phone(phone)
                if patient:
                    st.session_state.current_patient = patient
                    st.success("Profile linked!")
                    st.rerun()
            st.stop()
        
        patient = st.session_state.current_patient
        show_patient_prescriptions(patient['patient_id'])
    
    elif user['role'] == 'admin':
        # Admin view - can manage all prescriptions
        show_admin_prescriptions()


def show_patient_prescriptions(patient_id: int):
    """Show prescriptions for a specific patient"""
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 My Prescriptions", "➕ Add Prescription", "📊 Medication History"])
    
    with tab1:
        st.subheader("📋 Active Prescriptions")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            show_active = st.checkbox("Active Only", value=True)
        with col2:
            if st.button("🔄 Refresh"):
                st.rerun()
        with col3:
            if st.button("📥 Export"):
                st.session_state.show_export = True
        
        # Get prescriptions
        prescriptions = db.get_patient_prescriptions(patient_id, active_only=show_active)
        
        if prescriptions:
            # Export functionality
            if st.session_state.get('show_export', False):
                csv_data = utils.export_to_csv(prescriptions, "prescriptions.csv")
                st.download_button(
                    "📄 Download Prescriptions CSV",
                    data=csv_data,
                    file_name=f"prescriptions_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                if st.button("❌ Close"):
                    st.session_state.show_export = False
                    st.rerun()
            
            st.write(f"**Total prescriptions:** {len(prescriptions)}")
            st.divider()
            
            # Display prescriptions
            for rx in prescriptions:
                # Calculate days remaining
                try:
                    end_date = datetime.strptime(rx['end_date'], "%Y-%m-%d")
                    days_remaining = (end_date - datetime.now()).days
                    
                    status_badge = "active-badge" if rx['status'] == 'Active' else "expired-badge"
                    
                    with st.expander(f"💊 {rx['medication_name']} - {rx['dosage']}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"**Medication:** {rx['medication_name']}")
                            st.markdown(f"**Dosage:** {rx['dosage']}")
                            st.markdown(f"**Frequency:** {rx['frequency']}")
                            st.markdown(f"**Duration:** {rx['duration_days']} days")
                        
                        with col2:
                            st.markdown(f"**Doctor:** {rx['doctor_name']}")
                            st.markdown(f"**Start Date:** {rx['start_date']}")
                            st.markdown(f"**End Date:** {rx['end_date']}")
                            st.markdown(f"**Status:** <span class='{status_badge}'>{rx['status']}</span>", 
                                      unsafe_allow_html=True)
                        
                        with col3:
                            if days_remaining > 0:
                                st.metric("Days Remaining", days_remaining)
                                if days_remaining <= 7:
                                    st.warning("⚠️ Refill needed soon!")
                            else:
                                st.error("❌ Expired")
                            
                            st.markdown(f"**Refills Left:** {rx['refills_remaining']}")
                        
                        if rx['instructions']:
                            st.info(f"📝 **Instructions:** {rx['instructions']}")
                        
                        # Action buttons
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("📅 Request Refill", key=f"refill_{rx['prescription_id']}"):
                                st.success("✅ Refill request sent to pharmacy!")
                        with col_b:
                            if rx['status'] == 'Active' and st.button("🛑 Mark as Completed", 
                                                                       key=f"complete_{rx['prescription_id']}"):
                                db.update_prescription_status(rx['prescription_id'], 'Completed')
                                st.success("Prescription marked as completed")
                                st.rerun()
                except Exception as e:
                    st.error(f"Error processing prescription: {e}")
        else:
            st.info("📋 No prescriptions found")
    
    with tab2:
        st.subheader("➕ Add New Prescription")
        add_prescription_form(patient_id)
    
    with tab3:
        st.subheader("📊 Medication History")
        show_medication_history(patient_id)


def add_prescription_form(patient_id: int):
    """Form to add a new prescription"""
    
    with st.form("add_prescription_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            medication_name = st.text_input("💊 Medication Name *", placeholder="e.g., Aspirin")
            dosage = st.text_input("📏 Dosage *", placeholder="e.g., 100mg")
            frequency = st.selectbox("⏰ Frequency *", 
                                    ["Once daily", "Twice daily", "Three times daily", 
                                     "Four times daily", "As needed", "Every 12 hours"])
            duration_days = st.number_input("📅 Duration (days) *", min_value=1, max_value=365, value=30)
        
        with col2:
            doctor_name = st.text_input("👨‍⚕️ Prescribing Doctor *", placeholder="Dr. John Smith")
            start_date = st.date_input("📆 Start Date *", value=datetime.now())
            refills = st.number_input("🔄 Refills Remaining", min_value=0, max_value=12, value=2)
        
        instructions = st.text_area("📝 Instructions", 
                                   placeholder="Take with food, avoid alcohol, etc.")
        side_effects = st.text_area("⚠️ Possible Side Effects",
                                   placeholder="Nausea, dizziness, etc.")
        
        submit = st.form_submit_button("✅ Add Prescription", use_container_width=True)
        
        if submit:
            if medication_name and dosage and frequency and doctor_name:
                prescription_id = db.add_prescription(
                    patient_id, doctor_name, medication_name, dosage, frequency,
                    duration_days, instructions, str(start_date), refills, side_effects
                )
                
                if prescription_id:
                    st.success(f"✅ Prescription added successfully! ID: {prescription_id}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to add prescription")
            else:
                st.error("❌ Please fill in all required fields (*)")


def show_medication_history(patient_id: int):
    """Show medication history with timeline"""
    
    all_prescriptions = db.get_patient_prescriptions(patient_id, active_only=False)
    
    if all_prescriptions:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        active_count = sum(1 for rx in all_prescriptions if rx['status'] == 'Active')
        completed_count = sum(1 for rx in all_prescriptions if rx['status'] == 'Completed')
        total_medications = len(set([rx['medication_name'] for rx in all_prescriptions]))
        
        with col1:
            st.metric("Total Prescriptions", len(all_prescriptions))
        with col2:
            st.metric("Active", active_count)
        with col3:
            st.metric("Completed", completed_count)
        with col4:
            st.metric("Unique Medications", total_medications)
        
        st.divider()
        
        # Timeline view
        st.write("**📅 Medication Timeline:**")
        
        # Sort by start date
        sorted_rx = sorted(all_prescriptions, key=lambda x: x['start_date'], reverse=True)
        
        for rx in sorted_rx:
            time_ago = utils.format_timestamp(rx['start_date'] + " 00:00:00")
            status_icon = "✅" if rx['status'] == 'Active' else "✓"
            
            st.markdown(f"""
            {status_icon} **{rx['medication_name']}** ({rx['dosage']})  
            📅 Started {time_ago} | Duration: {rx['duration_days']} days | Status: {rx['status']}
            ---
            """)
    else:
        st.info("No medication history found")


def show_admin_prescriptions():
    """Admin view for managing all prescriptions"""
    
    st.subheader("🔧 Prescription Management (Admin)")
    
    # Search patient
    patient_phone = st.text_input("🔍 Search by Patient Phone:", placeholder="+1234567890")
    
    if patient_phone and len(patient_phone) >= 10:
        patient = db.get_patient_by_phone(patient_phone)
        
        if patient:
            st.success(f"✅ Patient found: {patient['name']}")
            show_patient_prescriptions(patient['patient_id'])
        else:
            st.warning("❌ Patient not found")
    else:
        st.info("👆 Enter patient phone number to manage prescriptions")


if __name__ == "__main__":
    main()
