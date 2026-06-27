"""
Doctor Directory and Profiles
Browse doctors, view specialties, ratings, and book consultations
"""

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
import auth
import config

st.set_page_config(page_title="Doctors", page_icon="👨‍⚕️", layout="wide")

auth.init_session_state()

if not auth.is_authenticated():
    st.warning("⚠️ Please log in")
    st.switch_page("pages/1_🔐_Login.py")
    st.stop()

st.markdown("""<style>
.doctor-card {
    background: white;
    padding: 1.5rem;
    border-radius: 1rem;
    border: 2px solid #e0e0e0;
    margin-bottom: 1rem;
}
</style>""", unsafe_allow_html=True)


def main():
    st.title("👨‍⚕️ Doctor Directory")
    
    tab1, tab2 = st.tabs(["🔍 Find Doctors", "➕ Add Doctor (Admin)"])
    
    with tab1:
        show_doctor_directory()
    
    with tab2:
        if auth.is_admin():
            add_doctor_form()
        else:
            st.warning("⚠️ Admin access required")


def show_doctor_directory():
    st.subheader("🔍 Browse Doctors by Specialty")
    
    # Specialty filter
    specialty_filter = st.selectbox(
        "Filter by Specialty:",
        ["All Specialties"] + config.MEDICAL_SPECIALTIES
    )
    
    # Get doctors
    if specialty_filter == "All Specialties":
        doctors = db.get_all_doctors()
    else:
        doctors = db.get_all_doctors(specialty=specialty_filter)
    
    if doctors:
        st.write(f"**Found {len(doctors)} doctor(s):**")
        st.divider()
        
        for doc in doctors:
            with st.container():
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    st.markdown("### 👨‍⚕️")
                    st.markdown(f"**{doc['full_name']}**")
                    st.caption(doc['specialty'])
                
                with col2:
                    st.markdown(f"**Qualification:** {doc['qualification']}")
                    st.markdown(f"**Experience:** {doc['experience_years']} years")
                    if doc['bio']:
                        st.caption(doc['bio'][:100] + "...")
                    
                    # Rating
                    rating_stars = "⭐" * int(doc['rating'])
                    st.markdown(f"{rating_stars} {doc['rating']}/5.0 ({doc['total_reviews']} reviews)")
                
                with col3:
                    st.markdown(f"**Fee:** ${doc['consultation_fee']}")
                    
                    if st.button("📅 Book Appointment", key=f"book_{doc['doctor_id']}"):
                        st.session_state.selected_doctor = doc
                        st.success(f"✅ Selected Dr. {doc['full_name']}")
                        st.info("Go to Appointments page to complete booking")
                
                st.divider()
    else:
        st.info("No doctors found matching your criteria")
    
    # Add sample doctors button
    if auth.is_admin():
        if st.button("➕ Add Sample Doctors"):
            add_sample_doctors()
            st.success("✅ Sample doctors added!")
            st.rerun()


def add_doctor_form():
    st.subheader("➕ Add New Doctor")
    
    with st.form("add_doctor_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", placeholder="Dr. John Smith")
            specialty = st.selectbox("Specialty *", config.MEDICAL_SPECIALTIES)
            qualification = st.text_input("Qualification *", placeholder="MD, MBBS")
            experience = st.number_input("Experience (years) *", min_value=0, max_value=60, value=5)
        
        with col2:
            license_number = st.text_input("License Number *", placeholder="MED12345")
            phone = st.text_input("Phone", placeholder="+1234567890")
            email = st.text_input("Email", placeholder="doctor@hospital.com")
            consultation_fee = st.number_input("Consultation Fee ($)", min_value=0.0, value=100.0)
        
        available_days = st.multiselect(
            "Available Days",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
        
        bio = st.text_area("Bio/About", placeholder="Brief professional biography...")
        
        submit = st.form_submit_button("✅ Add Doctor", use_container_width=True)
        
        if submit:
            if full_name and specialty and qualification and license_number:
                doctor_id = db.add_doctor(
                    full_name, specialty, qualification, experience,
                    license_number, phone, email, consultation_fee,
                    ", ".join(available_days), bio
                )
                
                if doctor_id:
                    st.success(f"✅ Doctor added successfully! ID: {doctor_id}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to add doctor (license number may already exist)")
            else:
                st.error("❌ Please fill all required fields")


def add_sample_doctors():
    """Add sample doctors for demonstration"""
    sample_doctors = [
        ("Dr. Sarah Johnson", "Cardiology", "MD, FACC", 15, "CARD001", "+1234567891", 
         "sarah.j@hospital.com", 150.0, "Mon, Wed, Fri", 
         "Specialist in heart disease and preventive cardiology"),
        ("Dr. Michael Chen", "Pediatrics", "MD, FAAP", 12, "PED001", "+1234567892",
         "michael.c@hospital.com", 120.0, "Tue, Thu, Sat",
         "Board-certified pediatrician with expertise in child development"),
        ("Dr. Emily Roberts", "Dermatology", "MD, Board Certified", 8, "DERM001", "+1234567893",
         "emily.r@hospital.com", 130.0, "Mon, Tue, Wed, Thu",
         "Specialist in skin conditions and cosmetic dermatology"),
        ("Dr. James Wilson", "Neurology", "MD, PhD", 20, "NEUR001", "+1234567894",
         "james.w@hospital.com", 180.0, "Mon, Wed, Thu, Fri",
         "Expert in neurological disorders and brain health")
    ]
    
    for doctor_data in sample_doctors:
        try:
            db.add_doctor(*doctor_data)
        except:
            pass  # Doctor may already exist


if __name__ == "__main__":
    main()
