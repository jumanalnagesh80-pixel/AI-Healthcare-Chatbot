#!/usr/bin/env python3
"""
Enhanced Setup Script for AI Healthcare Chatbot v2.0
Creates database with comprehensive sample data
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize all database tables"""
    conn = sqlite3.connect('healthcare_enhanced.db')
    cursor = conn.cursor()
    
    print("🏥 AI Healthcare Chatbot - Enhanced Setup")
    print("=" * 60)
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE,
            full_name TEXT,
            phone TEXT,
            role TEXT DEFAULT 'patient',
            is_active INTEGER DEFAULT 1,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            email TEXT,
            blood_group TEXT,
            height REAL,
            weight REAL,
            bmi REAL,
            allergies TEXT,
            chronic_conditions TEXT,
            emergency_contact TEXT,
            emergency_phone TEXT,
            insurance_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Appointments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            patient_name TEXT,
            doctor_name TEXT,
            specialty TEXT,
            appointment_date DATE,
            appointment_time TEXT,
            reason TEXT,
            symptoms TEXT,
            notes TEXT,
            status TEXT DEFAULT 'Scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    
    # Prescriptions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_name TEXT,
            medication_name TEXT NOT NULL,
            dosage TEXT,
            frequency TEXT,
            duration TEXT,
            instructions TEXT,
            start_date DATE,
            end_date DATE,
            refills_remaining INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    
    # Vital signs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vital_signs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            blood_pressure TEXT,
            blood_pressure_systolic INTEGER,
            blood_pressure_diastolic INTEGER,
            heart_rate INTEGER,
            temperature REAL,
            oxygen_saturation INTEGER,
            respiratory_rate INTEGER,
            glucose_level INTEGER,
            weight REAL,
            bmi REAL,
            notes TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    
    # Lab reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            test_name TEXT NOT NULL,
            test_type TEXT,
            test_date DATE,
            result_value TEXT,
            reference_range TEXT,
            unit TEXT,
            status TEXT DEFAULT 'Pending',
            doctor_comments TEXT,
            abnormal_flag INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    
    # Chat history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_id INTEGER,
            patient_id INTEGER,
            message TEXT,
            response TEXT,
            sender TEXT,
            intent TEXT,
            sentiment TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    
    # Medical records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            record_type TEXT,
            diagnosis TEXT,
            treatment TEXT,
            doctor_name TEXT,
            record_date DATE,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    
    # Activity logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            description TEXT,
            ip_address TEXT,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database tables created")

def create_sample_data():
    """Create comprehensive sample data"""
    conn = sqlite3.connect('healthcare_enhanced.db')
    cursor = conn.cursor()
    
    today = datetime.now()
    
    # Create users
    print("✅ Creating users...")
    users_data = [
        ('admin', 'admin123', 'admin@healthcare.com', 'Dr. Admin', '+1-555-0100', 'admin'),
        ('patient1', 'password123', 'john.doe@email.com', 'John Doe', '+1-555-0101', 'patient'),
        ('patient2', 'password123', 'jane.smith@email.com', 'Jane Smith', '+1-555-0102', 'patient'),
        ('patient3', 'password123', 'bob.wilson@email.com', 'Bob Wilson', '+1-555-0103', 'patient'),
        ('doctor1', 'password123', 'dr.williams@healthcare.com', 'Dr. Sarah Williams', '+1-555-0201', 'doctor'),
        ('doctor2', 'password123', 'dr.johnson@healthcare.com', 'Dr. Michael Johnson', '+1-555-0202', 'doctor'),
    ]
    
    for username, password, email, full_name, phone, role in users_data:
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("""
                INSERT INTO users (username, password_hash, email, full_name, phone, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, password_hash, email, full_name, phone, role))
        except:
            pass
    
    # Create patients
    print("✅ Creating patient profiles...")
    patients_data = [
        (2, 'John Doe', 35, 'Male', '+1-555-0101', 'john.doe@email.com', 'O+', 175, 75, 24.5, 
         'Penicillin', 'None', 'Mary Doe', '+1-555-0111', 'INS-12345'),
        (3, 'Jane Smith', 28, 'Female', '+1-555-0102', 'jane.smith@email.com', 'A+', 165, 60, 22.0,
         'None', 'Hypertension', 'Tom Smith', '+1-555-0112', 'INS-12346'),
        (4, 'Bob Wilson', 52, 'Male', '+1-555-0103', 'bob.wilson@email.com', 'B+', 180, 85, 26.2,
         'Aspirin, Shellfish', 'Diabetes Type 2', 'Alice Wilson', '+1-555-0113', 'INS-12347'),
    ]
    
    for user_id, name, age, gender, phone, email, blood_group, height, weight, bmi, allergies, conditions, emergency, emerg_phone, insurance in patients_data:
        try:
            cursor.execute("""
                INSERT INTO patients (user_id, name, age, gender, phone, email, blood_group, 
                                    height, weight, bmi, allergies, chronic_conditions,
                                    emergency_contact, emergency_phone, insurance_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, name, age, gender, phone, email, blood_group, height, weight, bmi,
                  allergies, conditions, emergency, emerg_phone, insurance))
        except:
            pass
    
    # Create appointments
    print("✅ Creating appointments...")
    appointments_data = [
        (1, 'John Doe', 'Dr. Sarah Williams', 'Cardiology', (today + timedelta(days=3)).strftime("%Y-%m-%d"), 
         '10:00 AM', 'Annual Checkup', 'No specific symptoms', 'Routine physical examination', 'Scheduled'),
        (1, 'John Doe', 'Dr. Michael Johnson', 'General Medicine', (today + timedelta(days=7)).strftime("%Y-%m-%d"),
         '2:00 PM', 'Follow-up', 'None', 'Follow-up for blood pressure', 'Confirmed'),
        (2, 'Jane Smith', 'Dr. Emily Davis', 'Dermatology', (today + timedelta(days=5)).strftime("%Y-%m-%d"),
         '11:30 AM', 'Skin Condition', 'Rash on arms', 'Possible allergic reaction', 'Scheduled'),
        (1, 'John Doe', 'Dr. James Wilson', 'Orthopedics', (today - timedelta(days=10)).strftime("%Y-%m-%d"),
         '9:00 AM', 'Knee Pain', 'Chronic knee pain', 'X-ray and assessment completed', 'Completed'),
        (3, 'Bob Wilson', 'Dr. Sarah Williams', 'Endocrinology', (today + timedelta(days=2)).strftime("%Y-%m-%d"),
         '3:30 PM', 'Diabetes Management', 'Blood sugar monitoring', 'A1C test recommended', 'Confirmed'),
    ]
    
    for patient_id, patient_name, doctor, specialty, date, time, reason, symptoms, notes, status in appointments_data:
        try:
            cursor.execute("""
                INSERT INTO appointments (patient_id, patient_name, doctor_name, specialty, 
                                        appointment_date, appointment_time, reason, symptoms, notes, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, patient_name, doctor, specialty, date, time, reason, symptoms, notes, status))
        except:
            pass
    
    # Create prescriptions
    print("✅ Creating prescriptions...")
    prescriptions_data = [
        (1, 'Dr. Sarah Williams', 'Lisinopril', '10mg', 'Once daily', '90 days', 
         'Take in the morning with or without food', (today - timedelta(days=30)).strftime("%Y-%m-%d"),
         (today + timedelta(days=60)).strftime("%Y-%m-%d"), 2, 'Active'),
        (1, 'Dr. Sarah Williams', 'Aspirin', '81mg', 'Once daily', '365 days',
         'Take with food to reduce stomach irritation', (today - timedelta(days=60)).strftime("%Y-%m-%d"),
         (today + timedelta(days=305)).strftime("%Y-%m-%d"), 3, 'Active'),
        (2, 'Dr. Michael Johnson', 'Ibuprofen', '400mg', 'As needed (max 3x daily)', '30 days',
         'Take with food. Do not exceed 3 doses per day', (today - timedelta(days=5)).strftime("%Y-%m-%d"),
         (today + timedelta(days=25)).strftime("%Y-%m-%d"), 1, 'Active'),
        (3, 'Dr. Emily Davis', 'Metformin', '500mg', 'Twice daily', '90 days',
         'Take with meals. Monitor blood sugar regularly', (today - timedelta(days=45)).strftime("%Y-%m-%d"),
         (today + timedelta(days=45)).strftime("%Y-%m-%d"), 1, 'Active'),
        (3, 'Dr. Emily Davis', 'Atorvastatin', '20mg', 'Once daily', '90 days',
         'Take in the evening', (today - timedelta(days=45)).strftime("%Y-%m-%d"),
         (today + timedelta(days=45)).strftime("%Y-%m-%d"), 1, 'Active'),
    ]
    
    for patient_id, doctor, medication, dosage, frequency, duration, instructions, start_date, end_date, refills, status in prescriptions_data:
        try:
            cursor.execute("""
                INSERT INTO prescriptions (patient_id, doctor_name, medication_name, dosage, frequency, 
                                         duration, instructions, start_date, end_date, refills_remaining, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, doctor, medication, dosage, frequency, duration, instructions, start_date, end_date, refills, status))
        except:
            pass
    
    # Create vital signs
    print("✅ Creating vital signs records...")
    for i in range(30):
        date = today - timedelta(days=i)
        for patient_id in [1, 2, 3]:
            try:
                systolic = random.randint(110, 135)
                diastolic = random.randint(70, 90)
                bp = f"{systolic}/{diastolic}"
                hr = random.randint(60, 90)
                temp = round(random.uniform(97.5, 99.2), 1)
                o2 = random.randint(95, 100)
                resp = random.randint(12, 20)
                glucose = random.randint(80, 120)
                weight = round(random.uniform(60, 90), 1)
                
                cursor.execute("""
                    INSERT INTO vital_signs (patient_id, blood_pressure, blood_pressure_systolic, 
                                           blood_pressure_diastolic, heart_rate, temperature, 
                                           oxygen_saturation, respiratory_rate, glucose_level, weight,
                                           recorded_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (patient_id, bp, systolic, diastolic, hr, temp, o2, resp, glucose, weight, date))
            except:
                pass
    
    # Create lab reports
    print("✅ Creating lab reports...")
    lab_reports_data = [
        (1, 'Complete Blood Count (CBC)', 'Hematology', (today - timedelta(days=15)).strftime("%Y-%m-%d"),
         'WBC: 7.5, RBC: 5.2, Hgb: 14.5, Hct: 42', '4.5-11.0, 4.7-6.1, 14-18, 42-52', 'K/µL, M/µL, g/dL, %',
         'Completed', 'All values within normal range', 0),
        (1, 'Lipid Profile', 'Chemistry', (today - timedelta(days=20)).strftime("%Y-%m-%d"),
         'Total Chol: 185, LDL: 110, HDL: 55, Triglycerides: 100', '<200, <100, >40, <150', 'mg/dL',
         'Completed', 'Healthy lipid levels', 0),
        (2, 'Blood Glucose (Fasting)', 'Chemistry', (today - timedelta(days=7)).strftime("%Y-%m-%d"),
         '92', '70-100', 'mg/dL', 'Completed', 'Normal fasting glucose', 0),
        (3, 'Hemoglobin A1C', 'Chemistry', (today - timedelta(days=30)).strftime("%Y-%m-%d"),
         '6.8', '<5.7', '%', 'Completed', 'Elevated - consistent with prediabetes. Recommend lifestyle modifications', 1),
        (3, 'Comprehensive Metabolic Panel', 'Chemistry', (today - timedelta(days=30)).strftime("%Y-%m-%d"),
         'Na: 140, K: 4.2, Cl: 102, CO2: 24, BUN: 18, Creat: 1.0, Glucose: 105',
         '136-145, 3.5-5.0, 96-106, 23-29, 7-20, 0.7-1.3, 70-100', 'mEq/L, mEq/L, mEq/L, mEq/L, mg/dL, mg/dL, mg/dL',
         'Completed', 'Slightly elevated glucose - monitor', 0),
        (1, 'Thyroid Panel', 'Endocrinology', (today - timedelta(days=45)).strftime("%Y-%m-%d"),
         'TSH: 2.5, Free T4: 1.2, Free T3: 3.2', '0.4-4.0, 0.9-1.7, 2.3-4.2', 'mIU/L, ng/dL, pg/mL',
         'Completed', 'Normal thyroid function', 0),
    ]
    
    for patient_id, test_name, test_type, test_date, result, ref_range, unit, status, comments, abnormal in lab_reports_data:
        try:
            cursor.execute("""
                INSERT INTO lab_reports (patient_id, test_name, test_type, test_date, result_value,
                                       reference_range, unit, status, doctor_comments, abnormal_flag)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, test_name, test_type, test_date, result, ref_range, unit, status, comments, abnormal))
        except:
            pass
    
    # Create medical records
    print("✅ Creating medical records...")
    medical_records_data = [
        (1, 'Visit', 'Essential Hypertension', 'Antihypertensive medication started', 
         'Dr. Sarah Williams', (today - timedelta(days=90)).strftime("%Y-%m-%d"),
         'Patient counseled on lifestyle modifications including diet and exercise'),
        (2, 'Visit', 'Allergic Dermatitis', 'Topical corticosteroid prescribed',
         'Dr. Emily Davis', (today - timedelta(days=60)).strftime("%Y-%m-%d"),
         'Patient advised to avoid known allergens'),
        (3, 'Visit', 'Type 2 Diabetes Mellitus', 'Oral hypoglycemic therapy initiated',
         'Dr. Michael Johnson', (today - timedelta(days=45)).strftime("%Y-%m-%d"),
         'Patient educated on diet, exercise, and blood glucose monitoring'),
    ]
    
    for patient_id, record_type, diagnosis, treatment, doctor, record_date, notes in medical_records_data:
        try:
            cursor.execute("""
                INSERT INTO medical_records (patient_id, record_type, diagnosis, treatment, 
                                           doctor_name, record_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, record_type, diagnosis, treatment, doctor, record_date, notes))
        except:
            pass
    
    conn.commit()
    conn.close()
    
    print("=" * 60)
    print("✅ Setup completed successfully!")
    print()
    print("📋 Test Credentials:")
    print("   👤 Admin:    username='admin'    password='admin123'")
    print("   👤 Patient:  username='patient1' password='password123'")
    print("   👤 Patient:  username='patient2' password='password123'")
    print("   👤 Patient:  username='patient3' password='password123'")
    print("   👤 Doctor:   username='doctor1'  password='password123'")
    print()
    print("📊 Sample Data Created:")
    print("   • 6 Users (1 admin, 3 patients, 2 doctors)")
    print("   • 3 Patient Profiles with full details")
    print("   • 5 Appointments (past and upcoming)")
    print("   • 5 Active Prescriptions")
    print("   • 90 Vital Signs Records (30 days × 3 patients)")
    print("   • 6 Lab Reports with detailed results")
    print("   • 3 Medical Records with visit history")
    print()
    print("🚀 Start the server with: python app_enhanced.py")
    print("🌐 Then open: http://localhost:5000")
    print("=" * 60)

if __name__ == "__main__":
    init_database()
    create_sample_data()
