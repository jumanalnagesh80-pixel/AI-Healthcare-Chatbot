#!/usr/bin/env python3
"""
Setup script for AI Healthcare Chatbot
Creates database with sample data for testing
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database tables"""
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            full_name TEXT,
            role TEXT DEFAULT 'patient',
            is_active INTEGER DEFAULT 1,
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
            phone TEXT UNIQUE,
            email TEXT,
            blood_group TEXT,
            allergies TEXT,
            chronic_conditions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Appointments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_name TEXT,
            specialty TEXT,
            appointment_date DATE,
            appointment_time TEXT,
            symptoms TEXT,
            status TEXT DEFAULT 'Scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    
    # Prescriptions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            medication_name TEXT NOT NULL,
            dosage TEXT,
            frequency TEXT,
            start_date DATE,
            end_date DATE,
            status TEXT DEFAULT 'Active',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    
    # Vital signs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vital_signs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            blood_pressure_systolic INTEGER,
            blood_pressure_diastolic INTEGER,
            heart_rate INTEGER,
            temperature REAL,
            oxygen_saturation INTEGER,
            glucose_level INTEGER,
            weight REAL,
            bmi REAL,
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
            test_date DATE,
            result_value TEXT,
            normal_range TEXT,
            status TEXT DEFAULT 'Normal',
            notes TEXT,
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
            message TEXT,
            sender TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()

def create_sample_data():
    """Create sample data for testing"""
    # First initialize database
    init_database()
    
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    print("🏥 Setting up AI Healthcare Chatbot...")
    print("=" * 50)
    
    # Create admin user
    print("✓ Creating admin user...")
    try:
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("""
            INSERT INTO users (username, password_hash, email, full_name, role)
            VALUES (?, ?, ?, ?, ?)
        """, ("admin", password_hash, "admin@healthcare.com", "Admin User", "admin"))
    except sqlite3.IntegrityError:
        print("  → Admin user already exists")
    
    # Create test patient users
    print("✓ Creating test patient users...")
    test_patients = [
        ("patient1", "password123", "patient1@email.com", "John Doe", "patient"),
        ("patient2", "password123", "patient2@email.com", "Jane Smith", "patient"),
        ("doctor1", "password123", "doctor1@email.com", "Dr. Robert Johnson", "doctor"),
    ]
    
    for username, password, email, full_name, role in test_patients:
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("""
                INSERT INTO users (username, password_hash, email, full_name, role)
                VALUES (?, ?, ?, ?, ?)
            """, (username, password_hash, email, full_name, role))
        except sqlite3.IntegrityError:
            pass
    
    # Create patient profiles
    print("✓ Creating patient profiles...")
    patients_data = [
        (1, "John Doe", 35, "Male", "+1-555-0101", "john.doe@email.com", "O+", "Penicillin", "None"),
        (2, "Jane Smith", 28, "Female", "+1-555-0102", "jane.smith@email.com", "A+", "None", "Hypertension"),
    ]
    
    for user_id, name, age, gender, phone, email, blood_group, allergies, conditions in patients_data:
        try:
            cursor.execute("""
                INSERT INTO patients (user_id, name, age, gender, phone, email, blood_group, allergies, chronic_conditions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, name, age, gender, phone, email, blood_group, allergies, conditions))
        except sqlite3.IntegrityError:
            pass
    
    # Create sample appointments
    print("✓ Creating sample appointments...")
    today = datetime.now()
    appointments = [
        (1, "Dr. Sarah Williams", "Cardiology", (today + timedelta(days=2)).strftime("%Y-%m-%d"), "10:00 AM", "Regular checkup", "Scheduled"),
        (1, "Dr. Michael Brown", "General Medicine", (today + timedelta(days=7)).strftime("%Y-%m-%d"), "2:00 PM", "Follow-up consultation", "Scheduled"),
        (2, "Dr. Emily Davis", "Dermatology", (today + timedelta(days=5)).strftime("%Y-%m-%d"), "11:30 AM", "Skin rash", "Confirmed"),
        (1, "Dr. James Wilson", "Orthopedics", (today - timedelta(days=5)).strftime("%Y-%m-%d"), "9:00 AM", "Knee pain", "Completed"),
    ]
    
    for patient_id, doctor, specialty, date, time, symptoms, status in appointments:
        try:
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_name, specialty, appointment_date, appointment_time, symptoms, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, doctor, specialty, date, time, symptoms, status))
        except:
            pass
    
    # Create sample prescriptions
    print("✓ Creating sample prescriptions...")
    prescriptions = [
        (1, "Lisinopril", "10mg", "Once daily", (today - timedelta(days=30)).strftime("%Y-%m-%d"), 
         (today + timedelta(days=60)).strftime("%Y-%m-%d"), "Active", "Take with food"),
        (1, "Metformin", "500mg", "Twice daily", (today - timedelta(days=15)).strftime("%Y-%m-%d"),
         (today + timedelta(days=75)).strftime("%Y-%m-%d"), "Active", "Take with meals"),
        (2, "Ibuprofen", "400mg", "As needed", (today - timedelta(days=7)).strftime("%Y-%m-%d"),
         (today + timedelta(days=23)).strftime("%Y-%m-%d"), "Active", "Max 3 times per day"),
    ]
    
    for patient_id, med, dosage, freq, start, end, status, notes in prescriptions:
        try:
            cursor.execute("""
                INSERT INTO prescriptions (patient_id, medication_name, dosage, frequency, start_date, end_date, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, med, dosage, freq, start, end, status, notes))
        except:
            pass
    
    # Create sample vital signs
    print("✓ Creating sample vital signs...")
    for i in range(10):
        date = today - timedelta(days=i*3)
        for patient_id in [1, 2]:
            try:
                cursor.execute("""
                    INSERT INTO vital_signs (patient_id, blood_pressure_systolic, blood_pressure_diastolic,
                                           heart_rate, temperature, oxygen_saturation, weight)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    patient_id,
                    random.randint(110, 130),
                    random.randint(70, 85),
                    random.randint(65, 85),
                    round(random.uniform(97.5, 99.5), 1),
                    random.randint(95, 99),
                    round(random.uniform(65, 75), 1)
                ))
            except:
                pass
    
    # Create sample lab reports
    print("✓ Creating sample lab reports...")
    lab_tests = [
        (1, "Complete Blood Count (CBC)", (today - timedelta(days=10)).strftime("%Y-%m-%d"), 
         "WBC: 7.5, RBC: 5.2, Hemoglobin: 14.5", "Normal", "Normal", "All values within normal range"),
        (1, "Lipid Profile", (today - timedelta(days=20)).strftime("%Y-%m-%d"),
         "Cholesterol: 185, LDL: 110, HDL: 55", "Normal", "Normal", "Healthy lipid levels"),
        (2, "Blood Glucose", (today - timedelta(days=5)).strftime("%Y-%m-%d"),
         "Fasting: 92 mg/dL", "Normal", "Normal", "Within normal range"),
    ]
    
    for patient_id, test, date, result, range_val, status, notes in lab_tests:
        try:
            cursor.execute("""
                INSERT INTO lab_reports (patient_id, test_name, test_date, result_value, normal_range, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, test, date, result, range_val, status, notes))
        except:
            pass
    
    conn.commit()
    conn.close()
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Test Credentials:")
    print("   Admin:    username='admin'    password='admin123'")
    print("   Patient:  username='patient1' password='password123'")
    print("   Doctor:   username='doctor1'  password='password123'")
    print("\n🚀 Start the server with: python app.py")
    print("🌐 Then open: http://localhost:5000")
    print()

if __name__ == "__main__":
    create_sample_data()
