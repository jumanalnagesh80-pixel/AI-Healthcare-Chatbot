"""
Real-Time Vital Signs Monitoring Dashboard
Track blood pressure, heart rate, temperature, glucose, and more
"""

import streamlit as st
import sys
import os
from datetime import datetime
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
import auth
import utils

st.set_page_config(page_title="Vital Signs", page_icon="❤️", layout="wide")

auth.init_session_state()

if not auth.is_authenticated():
    st.warning("⚠️ Please log in to access this page")
    st.switch_page("pages/1_🔐_Login.py")
    st.stop()

st.markdown("""<style>
.vital-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 1rem;
    text-align: center;
}
</style>""", unsafe_allow_html=True)


def main():
    user = auth.get_current_user()
    
    st.title("❤️ Vital Signs Monitoring")
    st.markdown(f"**{user['full_name']}**")
    
    if user['role'] == 'patient':
        if 'current_patient' not in st.session_state or not st.session_state.current_patient:
            st.warning("⚠️ Please link your patient profile first")
            st.stop()
        patient = st.session_state.current_patient
        show_vital_signs_dashboard(patient['patient_id'])
    else:
        show_admin_vitals()


def show_vital_signs_dashboard(patient_id: int):
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "➕ Add Reading", "📈 History & Trends"])
    
    with tab1:
        st.subheader("📊 Latest Vital Signs")
        
        vitals = db.get_patient_vital_signs(patient_id, limit=1)
        
        if vitals:
            latest = vitals[0]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if latest['bp_systolic'] and latest['bp_diastolic']:
                    bp_value = f"{latest['bp_systolic']}/{latest['bp_diastolic']}"
                    bp_status = "🟢" if latest['bp_systolic'] < 130 else "🟡" if latest['bp_systolic'] < 140 else "🔴"
                    st.metric("Blood Pressure", bp_value, bp_status)
            
            with col2:
                if latest['heart_rate']:
                    hr_status = "🟢" if 60 <= latest['heart_rate'] <= 100 else "🟡"
                    st.metric("Heart Rate", f"{latest['heart_rate']} bpm", hr_status)
            
            with col3:
                if latest['temperature']:
                    temp_status = "🟢" if 36.5 <= latest['temperature'] <= 37.5 else "🔴"
                    st.metric("Temperature", f"{latest['temperature']}°C", temp_status)
            
            with col4:
                if latest['oxygen_saturation']:
                    o2_status = "🟢" if latest['oxygen_saturation'] >= 95 else "🔴"
                    st.metric("O₂ Saturation", f"{latest['oxygen_saturation']}%", o2_status)
            
            st.divider()
            
            col5, col6, col7 = st.columns(3)
            
            with col5:
                if latest['glucose_level']:
                    glucose_status = "🟢" if 70 <= latest['glucose_level'] <= 140 else "🟡"
                    st.metric("Glucose", f"{latest['glucose_level']} mg/dL", glucose_status)
            
            with col6:
                if latest['weight']:
                    st.metric("Weight", f"{latest['weight']} kg")
            
            with col7:
                if latest['bmi']:
                    bmi_status = "🟢" if 18.5 <= latest['bmi'] <= 24.9 else "🟡" if latest['bmi'] < 30 else "🔴"
                    st.metric("BMI", f"{latest['bmi']}", bmi_status)
            
            time_ago = utils.format_timestamp(latest['recorded_at'])
            st.info(f"📅 Last recorded: {time_ago}")
        else:
            st.info("📊 No vital signs recorded yet. Add your first reading!")
    
    with tab2:
        st.subheader("➕ Record Vital Signs")
        add_vital_signs_form(patient_id)
    
    with tab3:
        st.subheader("📈 Vital Signs History")
        show_vitals_history(patient_id)


def add_vital_signs_form(patient_id: int):
    with st.form("add_vitals_form"):
        st.write("**Enter your measurements:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            bp_sys = st.number_input("Blood Pressure (Systolic)", min_value=0, max_value=300, value=120)
            bp_dia = st.number_input("Blood Pressure (Diastolic)", min_value=0, max_value=200, value=80)
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, max_value=300, value=75)
            temperature = st.number_input("Temperature (°C)", min_value=30.0, max_value=45.0, value=37.0, step=0.1)
        
        with col2:
            oxygen_sat = st.number_input("Oxygen Saturation (%)", min_value=0, max_value=100, value=98)
            glucose = st.number_input("Glucose (mg/dL)", min_value=0, max_value=500, value=100)
            weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, value=70.0, step=0.1)
            height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, value=170.0, step=0.1)
        
        notes = st.text_area("Notes", placeholder="Any observations or symptoms...")
        
        submit = st.form_submit_button("✅ Save Vital Signs", use_container_width=True)
        
        if submit:
            vital_id = db.add_vital_signs(
                patient_id, bp_sys, bp_dia, heart_rate, temperature,
                oxygen_sat, glucose, weight, height, notes
            )
            
            if vital_id:
                st.success("✅ Vital signs recorded successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Failed to record vital signs")


def show_vitals_history(patient_id: int):
    vitals = db.get_patient_vital_signs(patient_id, limit=30)
    
    if vitals:
        st.write(f"**Showing last {len(vitals)} readings:**")
        
        # Blood Pressure Chart
        if any(v['bp_systolic'] for v in vitals):
            st.subheader("📊 Blood Pressure Trends")
            bp_data = []
            for v in reversed(vitals):
                if v['bp_systolic'] and v['bp_diastolic']:
                    bp_data.append({
                        'Date': v['recorded_at'][:10],
                        'Systolic': v['bp_systolic'],
                        'Diastolic': v['bp_diastolic']
                    })
            
            if bp_data:
                df = pd.DataFrame(bp_data)
                st.line_chart(df.set_index('Date'))
        
        # Heart Rate Chart
        if any(v['heart_rate'] for v in vitals):
            st.subheader("💓 Heart Rate Trends")
            hr_data = [{'Date': v['recorded_at'][:10], 'BPM': v['heart_rate']} 
                      for v in reversed(vitals) if v['heart_rate']]
            if hr_data:
                df = pd.DataFrame(hr_data)
                st.line_chart(df.set_index('Date'))
        
        # Export button
        if st.button("📥 Export Vital Signs"):
            csv_data = utils.export_to_csv(vitals, "vital_signs.csv")
            st.download_button(
                "Download CSV",
                data=csv_data,
                file_name=f"vitals_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No vital signs history found")


def show_admin_vitals():
    st.subheader("🔧 Vital Signs Management (Admin)")
    patient_phone = st.text_input("🔍 Search Patient:", placeholder="+1234567890")
    
    if patient_phone and len(patient_phone) >= 10:
        patient = db.get_patient_by_phone(patient_phone)
        if patient:
            st.success(f"✅ {patient['name']}")
            show_vital_signs_dashboard(patient['patient_id'])
        else:
            st.warning("❌ Patient not found")


if __name__ == "__main__":
    main()
