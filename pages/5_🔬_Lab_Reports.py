"""
Lab Reports and Test Results Management
Upload, track, and analyze laboratory test results
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
from advanced_ai import medical_ai

st.set_page_config(
    page_title="Lab Reports",
    page_icon="🔬",
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
    .report-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
    }
    .normal-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
    }
    .abnormal-badge {
        background-color: #dc3545;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    user = auth.get_current_user()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🔬 Lab Reports & Test Results")
        st.markdown(f"**{user['full_name']}**")
    with col2:
        st.write("")
        if st.button("🔙 Back", use_container_width=True):
            if user['role'] == 'admin':
                st.switch_page("pages/2_🎛️_Admin_Dashboard.py")
            else:
                st.switch_page("pages/3_🏥_Patient_Portal.py")
    
    st.divider()
    
    # Get patient
    if user['role'] == 'patient':
        if 'current_patient' not in st.session_state or not st.session_state.current_patient:
            st.warning("⚠️ Please link your patient profile first")
            st.stop()
        patient = st.session_state.current_patient
        show_patient_lab_reports(patient['patient_id'])
    else:
        show_admin_lab_reports()


def show_patient_lab_reports(patient_id: int):
    """Show lab reports for a patient"""
    
    tab1, tab2, tab3 = st.tabs(["📊 My Reports", "➕ Add Report", "📈 Trends Analysis"])
    
    with tab1:
        st.subheader("📊 Laboratory Test Results")
        
        # Get reports
        reports = db.get_patient_lab_reports(patient_id)
        
        if reports:
            # Summary
            col1, col2, col3 = st.columns(3)
            normal_count = sum(1 for r in reports if r['status'] == 'Normal')
            abnormal_count = sum(1 for r in reports if r['status'] == 'Abnormal')
            
            with col1:
                st.metric("Total Reports", len(reports))
            with col2:
                st.metric("Normal Results", normal_count)
            with col3:
                st.metric("Abnormal Results", abnormal_count)
            
            st.divider()
            
            # Display reports
            for report in reports:
                status_badge = "normal-badge" if report['status'] == 'Normal' else "abnormal-badge"
                status_icon = "✅" if report['status'] == 'Normal' else "⚠️"
                
                with st.expander(f"{status_icon} {report['test_name']} - {report['test_date']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Test Name:** {report['test_name']}")
                        st.markdown(f"**Report Type:** {report['report_type']}")
                        st.markdown(f"**Test Date:** {report['test_date']}")
                        st.markdown(f"**Status:** <span class='{status_badge}'>{report['status']}</span>",
                                  unsafe_allow_html=True)
                    
                    with col2:
                        if report['result_value']:
                            st.markdown(f"**Result Value:** {report['result_value']}")
                        if report['normal_range']:
                            st.markdown(f"**Normal Range:** {report['normal_range']}")
                        
                        time_ago = utils.format_timestamp(report['created_at'])
                        st.markdown(f"*Added {time_ago}*")
                    
                    if report['notes']:
                        st.info(f"📝 **Notes:** {report['notes']}")
                    
                    # AI Analysis button
                    if st.button("🤖 AI Analysis", key=f"ai_{report['report_id']}"):
                        with st.spinner("Analyzing report..."):
                            # Simulate report analysis
                            analysis_text = f"{report['test_name']}: {report['result_value']} ({report['status']})"
                            analysis = medical_ai.analyze_medical_report(analysis_text)
                            
                            st.success("✅ AI Analysis Complete!")
                            st.json(analysis)
        else:
            st.info("📋 No lab reports found")
    
    with tab2:
        st.subheader("➕ Add New Lab Report")
        add_lab_report_form(patient_id)
    
    with tab3:
        st.subheader("📈 Test Results Trends")
        show_trends_analysis(patient_id)


def add_lab_report_form(patient_id: int):
    """Form to add a new lab report"""
    
    with st.form("add_lab_report_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.selectbox("📋 Report Type *", [
                "Blood Test", "Urine Test", "X-Ray", "CT Scan", "MRI",
                "Ultrasound", "ECG", "Blood Sugar", "Lipid Profile", "Liver Function",
                "Kidney Function", "Thyroid Function", "Other"
            ])
            
            test_name = st.text_input("🔬 Test Name *", placeholder="e.g., Complete Blood Count")
            test_date = st.date_input("📅 Test Date *", value=datetime.now())
        
        with col2:
            result_value = st.text_input("📊 Result Value", placeholder="e.g., 120 mg/dL")
            normal_range = st.text_input("📏 Normal Range", placeholder="e.g., 70-100 mg/dL")
            status = st.selectbox("🎯 Status", ["Normal", "Abnormal", "Critical", "Pending"])
        
        notes = st.text_area("📝 Notes/Interpretation", placeholder="Doctor's notes or interpretation")
        
        # File upload (placeholder - would need actual file handling)
        uploaded_file = st.file_uploader("📎 Upload Report (PDF/Image)", type=['pdf', 'jpg', 'png'])
        
        submit = st.form_submit_button("✅ Add Lab Report", use_container_width=True)
        
        if submit:
            if report_type and test_name and test_date:
                file_path = ""
                if uploaded_file:
                    file_path = f"uploads/{uploaded_file.name}"
                    # In production, save file to storage
                
                report_id = db.add_lab_report(
                    patient_id, report_type, test_name, str(test_date),
                    result_value, normal_range, status, notes, file_path
                )
                
                if report_id:
                    st.success(f"✅ Lab report added successfully! ID: {report_id}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to add lab report")
            else:
                st.error("❌ Please fill in all required fields (*)")


def show_trends_analysis(patient_id: int):
    """Show trends analysis of lab results"""
    
    reports = db.get_patient_lab_reports(patient_id)
    
    if len(reports) < 2:
        st.info("📊 Need at least 2 reports to show trends")
        return
    
    # Group reports by test type
    test_types = {}
    for report in reports:
        test_name = report['test_name']
        if test_name not in test_types:
            test_types[test_name] = []
        test_types[test_name].append(report)
    
    # Display trends for each test type
    for test_name, test_reports in test_types.items():
        if len(test_reports) > 1:
            st.markdown(f"### 📈 {test_name} Trends")
            
            # Create DataFrame for charting
            df_data = []
            for report in sorted(test_reports, key=lambda x: x['test_date']):
                try:
                    # Try to extract numeric value
                    result_str = report['result_value']
                    if result_str:
                        # Extract first number from string
                        import re
                        numbers = re.findall(r'\d+\.?\d*', result_str)
                        if numbers:
                            df_data.append({
                                'Date': report['test_date'],
                                'Value': float(numbers[0]),
                                'Status': report['status']
                            })
                except:
                    pass
            
            if df_data:
                df = pd.DataFrame(df_data)
                st.line_chart(df.set_index('Date')['Value'])
                
                # Show data table
                with st.expander("📊 View Data Table"):
                    st.dataframe(df, use_container_width=True)
            
            st.divider()
    
    # Overall health score (simple calculation)
    normal_percentage = (sum(1 for r in reports if r['status'] == 'Normal') / len(reports)) * 100
    
    st.metric("Overall Health Score", f"{normal_percentage:.1f}%")
    
    if normal_percentage >= 80:
        st.success("🎉 Excellent! Most of your tests are normal.")
    elif normal_percentage >= 60:
        st.warning("⚠️ Some tests need attention. Consult your doctor.")
    else:
        st.error("🚨 Multiple abnormal results. Please consult your doctor immediately.")


def show_admin_lab_reports():
    """Admin view for lab reports"""
    
    st.subheader("🔧 Lab Reports Management (Admin)")
    
    patient_phone = st.text_input("🔍 Search by Patient Phone:", placeholder="+1234567890")
    
    if patient_phone and len(patient_phone) >= 10:
        patient = db.get_patient_by_phone(patient_phone)
        
        if patient:
            st.success(f"✅ Patient found: {patient['name']}")
            show_patient_lab_reports(patient['patient_id'])
        else:
            st.warning("❌ Patient not found")
    else:
        st.info("👆 Enter patient phone number to manage lab reports")


if __name__ == "__main__":
    main()
