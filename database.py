"""
Database management module for AI Healthcare Chatbot
Handles SQLite database operations for patients, appointments, and chat history
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import config


class HealthcareDatabase:
    """Manages all database operations for the healthcare chatbot"""
    
    def __init__(self, db_name: str = config.DATABASE_NAME):
        """Initialize database connection and create tables"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cursor = self.connection.cursor()
            print(f"✓ Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"✗ Database connection error: {e}")
    
    def create_tables(self):
        """Create all necessary tables if they don't exist"""
        try:
            # Users table (for authentication - both admin and patient users)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    email TEXT,
                    role TEXT NOT NULL DEFAULT 'patient',
                    full_name TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            
            # Patients table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    email TEXT,
                    address TEXT,
                    blood_group TEXT,
                    allergies TEXT,
                    chronic_conditions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            # Appointments table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    patient_name TEXT NOT NULL,
                    specialty TEXT NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TEXT NOT NULL,
                    symptoms TEXT,
                    status TEXT DEFAULT 'Scheduled',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            """)
            
            # Chat history table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    patient_id INTEGER,
                    message_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            """)
            
            # Symptoms log table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS symptoms_log (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    symptoms TEXT NOT NULL,
                    severity TEXT,
                    possible_conditions TEXT,
                    advice TEXT,
                    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            """)
            
            self.connection.commit()
            print("✓ Database tables created successfully")
            
            # Create default admin user if not exists
            self._create_default_admin()
        except sqlite3.Error as e:
            print(f"✗ Error creating tables: {e}")
    
    def _create_default_admin(self):
        """Create default admin user if not exists"""
        try:
            import hashlib
            # Check if admin exists
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            admin_count = self.cursor.fetchone()[0]
            
            if admin_count == 0:
                # Create default admin: username=admin, password=admin123
                password_hash = hashlib.sha256("admin123".encode()).hexdigest()
                self.cursor.execute("""
                    INSERT INTO users (username, password_hash, email, role, full_name)
                    VALUES (?, ?, ?, ?, ?)
                """, ("admin", password_hash, "admin@healthcare.com", "admin", "System Administrator"))
                self.connection.commit()
                print("✓ Default admin user created (username: admin, password: admin123)")
        except sqlite3.Error as e:
            print(f"✗ Error creating default admin: {e}")
    
    # ===== USER/AUTHENTICATION OPERATIONS =====
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user with username and password"""
        try:
            import hashlib
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            self.cursor.execute("""
                SELECT user_id, username, email, role, full_name, is_active 
                FROM users 
                WHERE username = ? AND password_hash = ? AND is_active = 1
            """, (username, password_hash))
            
            row = self.cursor.fetchone()
            if row:
                # Update last login
                self.cursor.execute("""
                    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?
                """, (row[0],))
                self.connection.commit()
                
                return {
                    "user_id": row[0],
                    "username": row[1],
                    "email": row[2],
                    "role": row[3],
                    "full_name": row[4],
                    "is_active": row[5]
                }
            return None
        except sqlite3.Error as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def create_user(self, username: str, password: str, email: str, 
                   role: str = "patient", full_name: str = "") -> Optional[int]:
        """Create a new user account"""
        try:
            import hashlib
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            self.cursor.execute("""
                INSERT INTO users (username, password_hash, email, role, full_name)
                VALUES (?, ?, ?, ?, ?)
            """, (username, password_hash, email, role, full_name))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Username {username} already exists")
            return None
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        try:
            self.cursor.execute("""
                SELECT user_id, username, email, role, full_name, is_active, created_at
                FROM users WHERE username = ?
            """, (username,))
            row = self.cursor.fetchone()
            if row:
                return {
                    "user_id": row[0],
                    "username": row[1],
                    "email": row[2],
                    "role": row[3],
                    "full_name": row[4],
                    "is_active": row[5],
                    "created_at": row[6]
                }
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving user: {e}")
            return None
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        try:
            self.cursor.execute("""
                SELECT user_id, username, email, role, full_name, is_active, created_at, last_login
                FROM users ORDER BY created_at DESC
            """)
            rows = self.cursor.fetchall()
            users = []
            for row in rows:
                users.append({
                    "user_id": row[0],
                    "username": row[1],
                    "email": row[2],
                    "role": row[3],
                    "full_name": row[4],
                    "is_active": row[5],
                    "created_at": row[6],
                    "last_login": row[7]
                })
            return users
        except sqlite3.Error as e:
            print(f"Error retrieving users: {e}")
            return []
    
    def update_user_status(self, user_id: int, is_active: int) -> bool:
        """Activate or deactivate a user"""
        try:
            self.cursor.execute("""
                UPDATE users SET is_active = ? WHERE user_id = ?
            """, (is_active, user_id))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating user status: {e}")
            return False
    
    def change_password(self, user_id: int, new_password: str) -> bool:
        """Change user password"""
        try:
            import hashlib
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            self.cursor.execute("""
                UPDATE users SET password_hash = ? WHERE user_id = ?
            """, (password_hash, user_id))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error changing password: {e}")
            return False
    
    # ===== PATIENT OPERATIONS =====
    
    def add_patient(self, name: str, age: int, gender: str, phone: str, 
                    email: str = "", address: str = "", blood_group: str = "",
                    allergies: str = "", chronic_conditions: str = "", user_id: int = None) -> Optional[int]:
        """Add a new patient to the database"""
        try:
            self.cursor.execute("""
                INSERT INTO patients (user_id, name, age, gender, phone, email, address, 
                                     blood_group, allergies, chronic_conditions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, name, age, gender, phone, email, address, blood_group, allergies, chronic_conditions))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Patient with phone {phone} already exists")
            return None
        except sqlite3.Error as e:
            print(f"Error adding patient: {e}")
            return None
    
    def get_patient_by_phone(self, phone: str) -> Optional[Dict]:
        """Retrieve patient information by phone number"""
        try:
            self.cursor.execute("SELECT * FROM patients WHERE phone = ?", (phone,))
            row = self.cursor.fetchone()
            if row:
                return {
                    "patient_id": row[0],
                    "name": row[1],
                    "age": row[2],
                    "gender": row[3],
                    "phone": row[4],
                    "email": row[5],
                    "address": row[6],
                    "blood_group": row[7],
                    "allergies": row[8],
                    "chronic_conditions": row[9],
                    "created_at": row[10]
                }
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving patient: {e}")
            return None
    
    def get_all_patients(self) -> List[Dict]:
        """Get all patients from database"""
        try:
            self.cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
            rows = self.cursor.fetchall()
            patients = []
            for row in rows:
                patients.append({
                    "patient_id": row[0],
                    "name": row[1],
                    "age": row[2],
                    "gender": row[3],
                    "phone": row[4],
                    "email": row[5],
                    "blood_group": row[7]
                })
            return patients
        except sqlite3.Error as e:
            print(f"Error retrieving patients: {e}")
            return []
    
    # ===== APPOINTMENT OPERATIONS =====
    
    def book_appointment(self, patient_id: int, patient_name: str, specialty: str,
                        appointment_date: str, appointment_time: str, symptoms: str = "") -> Optional[int]:
        """Book a new appointment"""
        try:
            self.cursor.execute("""
                INSERT INTO appointments (patient_id, patient_name, specialty, 
                                         appointment_date, appointment_time, symptoms)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (patient_id, patient_name, specialty, appointment_date, appointment_time, symptoms))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error booking appointment: {e}")
            return None
    
    def get_patient_appointments(self, patient_id: int) -> List[Dict]:
        """Get all appointments for a specific patient"""
        try:
            self.cursor.execute("""
                SELECT * FROM appointments 
                WHERE patient_id = ? 
                ORDER BY appointment_date DESC, appointment_time DESC
            """, (patient_id,))
            rows = self.cursor.fetchall()
            appointments = []
            for row in rows:
                appointments.append({
                    "appointment_id": row[0],
                    "specialty": row[3],
                    "date": row[4],
                    "time": row[5],
                    "symptoms": row[6],
                    "status": row[7]
                })
            return appointments
        except sqlite3.Error as e:
            print(f"Error retrieving appointments: {e}")
            return []
    
    def get_all_appointments(self, status: str = None) -> List[Dict]:
        """Get all appointments, optionally filtered by status"""
        try:
            if status:
                self.cursor.execute("""
                    SELECT * FROM appointments 
                    WHERE status = ?
                    ORDER BY appointment_date DESC, appointment_time DESC
                """, (status,))
            else:
                self.cursor.execute("""
                    SELECT * FROM appointments 
                    ORDER BY appointment_date DESC, appointment_time DESC
                """)
            rows = self.cursor.fetchall()
            appointments = []
            for row in rows:
                appointments.append({
                    "appointment_id": row[0],
                    "patient_name": row[2],
                    "specialty": row[3],
                    "date": row[4],
                    "time": row[5],
                    "symptoms": row[6],
                    "status": row[7]
                })
            return appointments
        except sqlite3.Error as e:
            print(f"Error retrieving appointments: {e}")
            return []
    
    def check_appointment_availability(self, date: str, time: str) -> bool:
        """Check if a time slot is available"""
        try:
            self.cursor.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE appointment_date = ? AND appointment_time = ? AND status != 'Cancelled'
            """, (date, time))
            count = self.cursor.fetchone()[0]
            # Allow up to 5 appointments per time slot
            return count < 5
        except sqlite3.Error as e:
            print(f"Error checking availability: {e}")
            return False
    
    # ===== CHAT HISTORY OPERATIONS =====
    
    def save_chat_message(self, session_id: str, message_type: str, 
                         message: str, patient_id: Optional[int] = None):
        """Save a chat message to history"""
        try:
            self.cursor.execute("""
                INSERT INTO chat_history (session_id, patient_id, message_type, message)
                VALUES (?, ?, ?, ?)
            """, (session_id, patient_id, message_type, message))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error saving chat message: {e}")
    
    def get_chat_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Retrieve chat history for a session"""
        try:
            self.cursor.execute("""
                SELECT message_type, message, timestamp 
                FROM chat_history 
                WHERE session_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (session_id, limit))
            rows = self.cursor.fetchall()
            history = []
            for row in reversed(rows):  # Reverse to get chronological order
                history.append({
                    "type": row[0],
                    "message": row[1],
                    "timestamp": row[2]
                })
            return history
        except sqlite3.Error as e:
            print(f"Error retrieving chat history: {e}")
            return []
    
    # ===== SYMPTOMS LOG OPERATIONS =====
    
    def log_symptoms(self, symptoms: str, severity: str, possible_conditions: str,
                    advice: str, patient_id: Optional[int] = None) -> Optional[int]:
        """Log symptom check to database"""
        try:
            self.cursor.execute("""
                INSERT INTO symptoms_log (patient_id, symptoms, severity, 
                                         possible_conditions, advice)
                VALUES (?, ?, ?, ?, ?)
            """, (patient_id, symptoms, severity, possible_conditions, advice))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error logging symptoms: {e}")
            return None
    
    def get_patient_symptom_history(self, patient_id: int) -> List[Dict]:
        """Get symptom history for a patient"""
        try:
            self.cursor.execute("""
                SELECT symptoms, severity, possible_conditions, logged_at 
                FROM symptoms_log 
                WHERE patient_id = ? 
                ORDER BY logged_at DESC
            """, (patient_id,))
            rows = self.cursor.fetchall()
            history = []
            for row in rows:
                history.append({
                    "symptoms": row[0],
                    "severity": row[1],
                    "possible_conditions": row[2],
                    "logged_at": row[3]
                })
            return history
        except sqlite3.Error as e:
            print(f"Error retrieving symptom history: {e}")
            return []
    
    # ===== UTILITY OPERATIONS =====
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        try:
            stats = {}
            
            # Total patients
            self.cursor.execute("SELECT COUNT(*) FROM patients")
            stats['total_patients'] = self.cursor.fetchone()[0]
            
            # Total appointments
            self.cursor.execute("SELECT COUNT(*) FROM appointments")
            stats['total_appointments'] = self.cursor.fetchone()[0]
            
            # Scheduled appointments
            self.cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'Scheduled'")
            stats['scheduled_appointments'] = self.cursor.fetchone()[0]
            
            # Total symptom checks
            self.cursor.execute("SELECT COUNT(*) FROM symptoms_log")
            stats['total_symptom_checks'] = self.cursor.fetchone()[0]
            
            # Total users
            self.cursor.execute("SELECT COUNT(*) FROM users")
            stats['total_users'] = self.cursor.fetchone()[0]
            
            # Active users
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            stats['active_users'] = self.cursor.fetchone()[0]
            
            # Today's appointments
            self.cursor.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE appointment_date = DATE('now') AND status = 'Scheduled'
            """)
            stats['todays_appointments'] = self.cursor.fetchone()[0]
            
            # Recent patients (last 7 days)
            self.cursor.execute("""
                SELECT COUNT(*) FROM patients 
                WHERE created_at >= DATE('now', '-7 days')
            """)
            stats['recent_patients'] = self.cursor.fetchone()[0]
            
            return stats
        except sqlite3.Error as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """Update appointment status"""
        try:
            self.cursor.execute("""
                UPDATE appointments SET status = ? WHERE appointment_id = ?
            """, (status, appointment_id))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating appointment status: {e}")
            return False
    
    def delete_appointment(self, appointment_id: int) -> bool:
        """Delete an appointment"""
        try:
            self.cursor.execute("DELETE FROM appointments WHERE appointment_id = ?", (appointment_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting appointment: {e}")
            return False
    
    def delete_patient(self, patient_id: int) -> bool:
        """Delete a patient and all related records"""
        try:
            # Delete related appointments
            self.cursor.execute("DELETE FROM appointments WHERE patient_id = ?", (patient_id,))
            # Delete related symptoms log
            self.cursor.execute("DELETE FROM symptoms_log WHERE patient_id = ?", (patient_id,))
            # Delete related chat history
            self.cursor.execute("DELETE FROM chat_history WHERE patient_id = ?", (patient_id,))
            # Delete patient
            self.cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting patient: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")


# Initialize database instance
db = HealthcareDatabase()
