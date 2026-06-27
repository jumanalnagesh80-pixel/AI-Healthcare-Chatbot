"""
Enhanced AI Healthcare Chatbot - Flask Backend
Version 2.0 with Advanced Features
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
import json
import os
import re
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['DATABASE'] = 'healthcare_enhanced.db'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ============================================
# Advanced AI Healthcare Knowledge Base
# ============================================

MEDICAL_KNOWLEDGE = {
    'symptoms': {
        'fever': {
            'conditions': ['Flu', 'COVID-19', 'Common Cold', 'Infection'],
            'advice': 'Rest, stay hydrated, monitor temperature. Seek medical help if fever exceeds 103°F or lasts more than 3 days.',
            'severity': 'moderate'
        },
        'headache': {
            'conditions': ['Migraine', 'Tension Headache', 'Dehydration', 'Stress'],
            'advice': 'Rest in a quiet, dark room. Stay hydrated. Try over-the-counter pain relief. See a doctor if severe or persistent.',
            'severity': 'low'
        },
        'chest pain': {
            'conditions': ['Heart Attack', 'Angina', 'Anxiety', 'GERD'],
            'advice': 'SEEK IMMEDIATE MEDICAL ATTENTION! Call 911 if severe, especially with shortness of breath or arm pain.',
            'severity': 'critical'
        },
        'cough': {
            'conditions': ['Common Cold', 'Bronchitis', 'Allergies', 'COVID-19'],
            'advice': 'Rest, stay hydrated, use honey or cough drops. See a doctor if persistent for more than 2 weeks or with blood.',
            'severity': 'low'
        },
        'shortness of breath': {
            'conditions': ['Asthma', 'COPD', 'Heart Failure', 'Pneumonia'],
            'advice': 'SEEK IMMEDIATE MEDICAL ATTENTION if severe! Could be a medical emergency.',
            'severity': 'critical'
        },
        'nausea': {
            'conditions': ['Gastroenteritis', 'Food Poisoning', 'Migraine', 'Pregnancy'],
            'advice': 'Sip clear fluids, eat bland foods. Rest. See a doctor if persistent or with severe abdominal pain.',
            'severity': 'moderate'
        },
        'dizziness': {
            'conditions': ['Vertigo', 'Dehydration', 'Low Blood Pressure', 'Inner Ear Problem'],
            'advice': 'Sit or lie down immediately. Stay hydrated. Avoid sudden movements. Consult a doctor if persistent.',
            'severity': 'moderate'
        },
        'fatigue': {
            'conditions': ['Anemia', 'Depression', 'Thyroid Issues', 'Sleep Disorders'],
            'advice': 'Ensure adequate sleep, maintain healthy diet, exercise regularly. See a doctor if persistent.',
            'severity': 'low'
        }
    },
    'medications': {
        'aspirin': 'Pain reliever and fever reducer. Also used for heart health. Take with food to avoid stomach upset.',
        'ibuprofen': 'Anti-inflammatory pain reliever. Reduces fever and inflammation. Do not exceed recommended dose.',
        'acetaminophen': 'Pain reliever and fever reducer. Gentler on stomach than NSAIDs. Do not mix with alcohol.',
        'lisinopril': 'Blood pressure medication (ACE inhibitor). Take at the same time daily. Monitor blood pressure regularly.',
        'metformin': 'Diabetes medication. Take with meals. Monitor blood sugar levels regularly.',
        'omeprazole': 'Reduces stomach acid production. Take before meals. Used for GERD and ulcers.',
        'atorvastatin': 'Cholesterol-lowering medication (statin). Take in evening. Regular liver function tests needed.',
        'levothyroxine': 'Thyroid hormone replacement. Take on empty stomach in morning. Regular blood tests needed.'
    },
    'health_tips': [
        'Drink at least 8 glasses of water daily',
        'Get 7-9 hours of quality sleep each night',
        'Exercise for at least 30 minutes, 5 days a week',
        'Eat a balanced diet with fruits and vegetables',
        'Manage stress through meditation or relaxation',
        'Wash hands frequently to prevent infections',
        'Schedule regular health checkups',
        'Maintain a healthy weight',
        'Avoid smoking and excessive alcohol',
        'Practice good hygiene and oral care'
    ]
}

# ============================================
# Database Management
# ============================================

def init_db():
    """Initialize enhanced database with all tables"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
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
    
    # Patients table with enhanced fields
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
    
    # Appointments table with enhanced fields
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
    
    # Chat history table with enhanced fields
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
    
    # Medical records table (new)
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
    
    # Activity logs table (new)
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

def get_db():
    """Get database connection with row factory"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def log_activity(user_id, action, description):
    """Log user activity"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO activity_logs (user_id, action, description, ip_address)
            VALUES (?, ?, ?, ?)
        """, (user_id, action, description, request.remote_addr))
        conn.commit()
        conn.close()
    except:
        pass

# ============================================
# Authentication Decorators
# ============================================

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        if session.get('role') != 'admin':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# ============================================
# Advanced AI Chatbot Engine
# ============================================

class AdvancedHealthChatbot:
    """Enhanced AI Healthcare Chatbot with NLP capabilities"""
    
    def __init__(self):
        self.context = {}
        
    def analyze_sentiment(self, message):
        """Analyze message sentiment"""
        positive_words = ['good', 'great', 'better', 'fine', 'excellent', 'happy', 'thank']
        negative_words = ['bad', 'worse', 'terrible', 'awful', 'pain', 'hurt', 'worried', 'scared']
        
        message_lower = message.lower()
        pos_count = sum(1 for word in positive_words if word in message_lower)
        neg_count = sum(1 for word in negative_words if word in message_lower)
        
        if neg_count > pos_count:
            return 'negative'
        elif pos_count > neg_count:
            return 'positive'
        return 'neutral'
    
    def extract_intent(self, message):
        """Extract user intent from message"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['appointment', 'book', 'schedule', 'visit']):
            return 'appointment'
        elif any(word in message_lower for word in ['prescription', 'medication', 'medicine', 'drug']):
            return 'prescription'
        elif any(word in message_lower for word in ['symptom', 'pain', 'hurt', 'feel', 'sick', 'ill']):
            return 'symptoms'
        elif any(word in message_lower for word in ['vital', 'blood pressure', 'temperature', 'heart rate']):
            return 'vitals'
        elif any(word in message_lower for word in ['test', 'lab', 'report', 'result']):
            return 'lab_results'
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greet']):
            return 'greeting'
        elif any(word in message_lower for word in ['help', 'assist', 'support']):
            return 'help'
        elif any(word in message_lower for word in ['thank', 'thanks']):
            return 'gratitude'
        return 'general'
    
    def find_symptoms(self, message):
        """Find mentioned symptoms in message"""
        found_symptoms = []
        message_lower = message.lower()
        
        for symptom in MEDICAL_KNOWLEDGE['symptoms'].keys():
            if symptom in message_lower:
                found_symptoms.append(symptom)
        
        return found_symptoms
    
    def generate_response(self, message, user_context=None):
        """Generate intelligent response based on message and context"""
        message_lower = message.lower()
        intent = self.extract_intent(message)
        sentiment = self.analyze_sentiment(message)
        
        # Handle different intents
        if intent == 'greeting':
            return self._greeting_response()
        
        elif intent == 'symptoms':
            return self._symptom_response(message)
        
        elif intent == 'appointment':
            return self._appointment_response()
        
        elif intent == 'prescription':
            return self._prescription_response(message)
        
        elif intent == 'vitals':
            return self._vitals_response()
        
        elif intent == 'lab_results':
            return self._lab_results_response()
        
        elif intent == 'help':
            return self._help_response()
        
        elif intent == 'gratitude':
            return "You're welcome! I'm always here to help with your health concerns. Feel free to ask anything! 😊"
        
        else:
            return self._general_response(message)
    
    def _greeting_response(self):
        """Generate greeting response"""
        greetings = [
            "Hello! 👋 I'm your AI Healthcare Assistant. How can I help you today?",
            "Hi there! 🏥 I'm here to assist with your health questions. What can I do for you?",
            "Welcome! 😊 I'm your personal health assistant. How may I help you?",
            "Hello! I'm here to help with appointments, symptoms, medications, and more. What do you need?"
        ]
        import random
        return random.choice(greetings)
    
    def _symptom_response(self, message):
        """Generate symptom-related response"""
        symptoms = self.find_symptoms(message)
        
        if not symptoms:
            return """I understand you're not feeling well. To help you better, please describe your symptoms in detail:
            
• When did the symptoms start?
• How severe are they (mild, moderate, severe)?
• Any other symptoms you're experiencing?
• Have you taken any medication?

**⚠️ IMPORTANT:** If you're experiencing severe chest pain, difficulty breathing, or sudden severe symptoms, please call 911 or visit the nearest emergency room immediately!"""
        
        response = "Based on your symptoms, here's what I found:\n\n"
        
        for symptom in symptoms:
            info = MEDICAL_KNOWLEDGE['symptoms'][symptom]
            response += f"**{symptom.title()}:**\n"
            response += f"• Possible conditions: {', '.join(info['conditions'])}\n"
            response += f"• Advice: {info['advice']}\n"
            
            if info['severity'] == 'critical':
                response += "\n🚨 **URGENT: This could be a medical emergency! Seek immediate medical attention!** 🚨\n"
            response += "\n"
        
        response += "\n**Remember:** This is not a diagnosis. Please consult with a healthcare professional for proper medical advice."
        return response
    
    def _appointment_response(self):
        """Generate appointment-related response"""
        return """📅 **Book an Appointment**

I can help you schedule an appointment! Here's what you can do:

1. Go to the **Appointments** page from the menu
2. Click **"Book New Appointment"**
3. Fill in the details:
   • Choose your doctor or specialty
   • Select preferred date and time
   • Describe reason for visit
   
4. You'll receive a confirmation once booked!

**Available Specialties:**
• General Medicine
• Cardiology
• Dermatology
• Pediatrics
• Orthopedics
• And more...

Would you like me to guide you through the booking process?"""
    
    def _prescription_response(self, message):
        """Generate prescription-related response"""
        # Check if specific medication is mentioned
        mentioned_meds = []
        for med in MEDICAL_KNOWLEDGE['medications'].keys():
            if med in message.lower():
                mentioned_meds.append(med)
        
        if mentioned_meds:
            response = "💊 **Medication Information:**\n\n"
            for med in mentioned_meds:
                response += f"**{med.title()}:**\n{MEDICAL_KNOWLEDGE['medications'][med]}\n\n"
            response += "\n⚠️ Always take medications as prescribed by your doctor. Never adjust dosage without consulting your healthcare provider."
            return response
        
        return """💊 **Prescription Management**

I can help you with:
• View your active prescriptions
• Check medication details and instructions
• Get refill reminders
• Understand drug interactions

**To view your prescriptions:**
Go to the **Prescriptions** page from the menu.

**Need information about a specific medication?**
Just tell me the medication name, and I'll provide details!

⚠️ **Important:** Never stop taking prescribed medications without consulting your doctor."""
    
    def _vitals_response(self):
        """Generate vitals-related response"""
        return """❤️ **Vital Signs Monitoring**

I can help you track your health metrics:

📊 **What you can monitor:**
• Blood Pressure (normal: 120/80 mmHg)
• Heart Rate (normal: 60-100 bpm)
• Temperature (normal: 97-99°F / 36-37°C)
• Oxygen Saturation (normal: 95-100%)
• Weight and BMI
• Blood Glucose levels

**To record vital signs:**
1. Go to **Vital Signs** page
2. Click **"Add Vital Signs"**
3. Enter your measurements
4. View trends with interactive charts!

**Tips for accurate readings:**
• Measure at the same time each day
• Rest for 5 minutes before measuring BP
• Use calibrated equipment
• Record immediately

Would you like help recording your vitals?"""
    
    def _lab_results_response(self):
        """Generate lab results response"""
        return """🔬 **Lab Reports & Test Results**

I can help you with:
• View your test results
• Understand what the numbers mean
• Track test history
• Schedule upcoming tests

**To view your lab reports:**
Go to the **Lab Reports** page from the menu.

**Common tests:**
• Complete Blood Count (CBC)
• Metabolic Panel
• Lipid Profile
• Thyroid Function
• Glucose/A1C
• Liver Function
• Kidney Function

**📊 Understanding your results:**
• Green = Within normal range
• Yellow = Borderline
• Red = Abnormal (needs attention)

**Note:** Always discuss your results with your doctor for proper interpretation and treatment plans."""
    
    def _help_response(self):
        """Generate help response"""
        return """🆘 **How I Can Help You**

I'm your AI Healthcare Assistant! Here's what I can do:

**💬 Answer Questions:**
• Symptom information
• Medication details
• Health tips and advice
• General medical information

**📋 Manage Healthcare:**
• Book and track appointments
• View prescriptions
• Monitor vital signs
• Access lab reports

**🏥 Emergency Guidance:**
• Identify urgent symptoms
• Provide first aid tips
• Direct to appropriate care

**💡 Health & Wellness:**
• Daily health tips
• Exercise guidance
• Nutrition advice
• Preventive care

**Just ask me anything about:**
"I have a headache"
"What is aspirin used for?"
"Book an appointment"
"Show my vital signs"
"Health tips for sleep"

**⚠️ Emergency? Call 911!**

How can I assist you today?"""
    
    def _general_response(self, message):
        """Generate general response"""
        # Check for specific keywords
        if 'health tip' in message.lower() or 'wellness' in message.lower():
            import random
            tip = random.choice(MEDICAL_KNOWLEDGE['health_tips'])
            return f"💡 **Health Tip:**\n\n{tip}\n\nWant another tip or have any health questions? Just ask!"
        
        return """I'm here to help with your healthcare needs! I can assist with:

• **Symptom checking** - Tell me how you're feeling
• **Appointments** - Schedule or manage visits
• **Prescriptions** - View or inquire about medications
• **Vital signs** - Track your health metrics
• **Lab results** - Understand your test results
• **Health tips** - Daily wellness advice

What would you like help with today? 😊"""

# Initialize chatbot
chatbot = AdvancedHealthChatbot()

# Initialize database on startup
init_db()

# ============================================
# Routes - Authentication
# ============================================

@app.route('/')
def index():
    """Home page"""
    return render_template('index_enhanced.html')

@app.route('/login')
def login_page():
    """Login page"""
    return render_template('login_enhanced.html')

@app.route('/register')
def register_page():
    """Registration page"""
    return render_template('login_enhanced.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page"""
    return render_template('dashboard_enhanced.html')

@app.route('/chat')
@login_required
def chat():
    """Chat page"""
    return render_template('chat_enhanced.html')

@app.route('/appointments')
@login_required
def appointments():
    """Appointments page"""
    return render_template('appointments_enhanced.html')

@app.route('/prescriptions')
@login_required
def prescriptions():
    """Prescriptions page"""
    return render_template('prescriptions_enhanced.html')

@app.route('/vital-signs')
@login_required
def vital_signs():
    """Vital signs page"""
    return render_template('vital_signs_enhanced.html')

@app.route('/lab-reports')
@login_required
def lab_reports():
    """Lab reports page"""
    return render_template('lab_reports_enhanced.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    """Enhanced registration endpoint"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password')
        email = data.get('email', '').strip()
        full_name = data.get('full_name', '').strip()
        phone = data.get('phone', '').strip()
        role = data.get('role', 'patient')
        
        # Validation
        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password are required'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400
        
        if email and '@' not in email:
            return jsonify({'success': False, 'error': 'Invalid email address'}), 400
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Insert user
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (username, password_hash, email, full_name, phone, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, password_hash, email, full_name, phone, role))
        
        user_id = cursor.lastrowid
        
        # Create patient profile if role is patient
        if role == 'patient':
            cursor.execute("""
                INSERT INTO patients (user_id, name, email, phone)
                VALUES (?, ?, ?, ?)
            """, (user_id, full_name, email, phone))
        
        conn.commit()
        conn.close()
        
        log_activity(user_id, 'register', f'New user registered: {username}')
        
        return jsonify({
            'success': True,
            'message': 'Registration successful! Please login.',
            'user_id': user_id
        })
        
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return jsonify({'success': False, 'error': 'Username already exists'}), 409
        elif 'email' in str(e):
            return jsonify({'success': False, 'error': 'Email already registered'}), 409
        return jsonify({'success': False, 'error': 'Registration failed'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """Enhanced login endpoint"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password required'}), 400
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        conn = get_db()
        cursor = conn.cursor()
        
        user = cursor.execute("""
            SELECT * FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        """, (username, password_hash)).fetchone()
        
        if not user:
            conn.close()
            return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
        
        # Update last login
        cursor.execute("""
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
        """, (user['id'],))
        
        # Get patient ID if exists
        patient = cursor.execute("""
            SELECT id FROM patients WHERE user_id = ?
        """, (user['id'],)).fetchone()
        
        patient_id = patient['id'] if patient else None
        
        conn.commit()
        conn.close()
        
        # Set session
        session.permanent = True
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['full_name'] = user['full_name']
        session['patient_id'] = patient_id
        
        log_activity(user['id'], 'login', f'User logged in: {username}')
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'full_name': user['full_name'],
                'email': user['email'],
                'role': user['role'],
                'patient_id': patient_id
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Logout endpoint"""
    if 'user_id' in session:
        log_activity(session['user_id'], 'logout', 'User logged out')
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'username': session['username'],
                'role': session['role'],
                'full_name': session.get('full_name'),
                'patient_id': session.get('patient_id')
            }
        })
    return jsonify({'authenticated': False})

# Continue in next part due to length...



# ============================================
# Routes - Dashboard & Pages
# ============================================

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard_enhanced.html')

@app.route('/appointments')
def appointments_page():
    """Appointments page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('appointments_enhanced.html')

@app.route('/prescriptions')
def prescriptions_page():
    """Prescriptions page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('prescriptions_enhanced.html')

@app.route('/vital-signs')
def vital_signs_page():
    """Vital Signs page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('vital_signs_enhanced.html')

@app.route('/lab-reports')
def lab_reports_page():
    """Lab Reports page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('lab_reports_enhanced.html')

@app.route('/chat')
def chat_page():
    """AI Chat page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('chat_enhanced.html')

@app.route('/profile')
def profile_page():
    """Profile page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('profile_enhanced.html')

# ============================================
# API Routes - Dashboard Stats
# ============================================

@app.route('/api/dashboard/stats', methods=['GET'])
@login_required
def dashboard_stats():
    """Get dashboard statistics"""
    try:
        patient_id = session.get('patient_id')
        user_role = session.get('role')
        
        conn = get_db()
        
        if user_role == 'admin':
            stats = {
                'total_patients': conn.execute('SELECT COUNT(*) as count FROM patients').fetchone()['count'],
                'total_appointments': conn.execute('SELECT COUNT(*) as count FROM appointments').fetchone()['count'],
                'pending_appointments': conn.execute("SELECT COUNT(*) as count FROM appointments WHERE status='Scheduled'").fetchone()['count'],
                'active_prescriptions': conn.execute("SELECT COUNT(*) as count FROM prescriptions WHERE status='Active'").fetchone()['count'],
                'recent_reports': conn.execute('SELECT COUNT(*) as count FROM lab_reports WHERE date(created_at) >= date("now", "-30 days")').fetchone()['count'],
                'vital_records': conn.execute('SELECT COUNT(*) as count FROM vital_signs').fetchone()['count']
            }
        else:
            if not patient_id:
                return jsonify({'success': False, 'error': 'Patient ID not found'}), 400
            
            stats = {
                'total_appointments': conn.execute('SELECT COUNT(*) as count FROM appointments WHERE patient_id=?', (patient_id,)).fetchone()['count'],
                'pending_appointments': conn.execute("SELECT COUNT(*) as count FROM appointments WHERE patient_id=? AND status='Scheduled'", (patient_id,)).fetchone()['count'],
                'active_prescriptions': conn.execute("SELECT COUNT(*) as count FROM prescriptions WHERE patient_id=? AND status='Active'", (patient_id,)).fetchone()['count'],
                'recent_reports': conn.execute('SELECT COUNT(*) as count FROM lab_reports WHERE patient_id=? AND date(test_date) >= date("now", "-30 days")', (patient_id,)).fetchone()['count']
            }
        
        conn.close()
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# API Routes - Appointments
# ============================================

@app.route('/api/appointments', methods=['GET'])
@login_required
def api_appointments_list():
    """Get appointments list"""
    try:
        patient_id = session.get('patient_id')
        role = session.get('role')
        status_filter = request.args.get('status')
        limit = request.args.get('limit', 100, type=int)
        
        conn = get_db()
        
        if role == 'admin':
            query = 'SELECT * FROM appointments'
            params = []
        else:
            query = 'SELECT * FROM appointments WHERE patient_id = ?'
            params = [patient_id]
        
        if status_filter:
            query += ' AND status = ?' if 'WHERE' in query else ' WHERE status = ?'
            params.append(status_filter)
        
        query += ' ORDER BY appointment_date DESC, appointment_time DESC LIMIT ?'
        params.append(limit)
        
        appointments = conn.execute(query, params).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'appointments': [dict(apt) for apt in appointments]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments', methods=['POST'])
@login_required
def api_appointments_create():
    """Create new appointment"""
    try:
        data = request.json
        patient_id = session.get('patient_id') or data.get('patient_id')
        
        if not patient_id:
            return jsonify({'success': False, 'error': 'Patient ID required'}), 400
        
        # Get patient name
        conn = get_db()
        patient = conn.execute('SELECT name FROM patients WHERE id = ?', (patient_id,)).fetchone()
        patient_name = patient['name'] if patient else 'Unknown'
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (
                patient_id, patient_name, doctor_name, specialty, 
                appointment_date, appointment_time, reason, symptoms, notes, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            patient_name,
            data.get('doctor_name'),
            data.get('specialty'),
            data.get('appointment_date'),
            data.get('appointment_time'),
            data.get('reason'),
            data.get('symptoms'),
            data.get('notes'),
            data.get('status', 'Scheduled')
        ))
        
        appointment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'appointment_create', f'Created appointment #{appointment_id}')
        
        return jsonify({
            'success': True,
            'message': 'Appointment booked successfully!',
            'appointment_id': appointment_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
@login_required
def api_appointment_update(appointment_id):
    """Update appointment"""
    try:
        data = request.json
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Build update query dynamically
        fields = []
        values = []
        
        for field in ['doctor_name', 'specialty', 'appointment_date', 'appointment_time', 'reason', 'symptoms', 'notes', 'status']:
            if field in data:
                fields.append(f"{field} = ?")
                values.append(data[field])
        
        if not fields:
            return jsonify({'success': False, 'error': 'No fields to update'}), 400
        
        fields.append('updated_at = CURRENT_TIMESTAMP')
        values.append(appointment_id)
        
        query = f"UPDATE appointments SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'appointment_update', f'Updated appointment #{appointment_id}')
        
        return jsonify({'success': True, 'message': 'Appointment updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
@login_required
def api_appointment_delete(appointment_id):
    """Cancel/delete appointment"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE appointments SET status = ? WHERE id = ?', ('Cancelled', appointment_id))
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'appointment_cancel', f'Cancelled appointment #{appointment_id}')
        
        return jsonify({'success': True, 'message': 'Appointment cancelled successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# API Routes - Prescriptions
# ============================================

@app.route('/api/prescriptions', methods=['GET'])
@login_required
def api_prescriptions_list():
    """Get prescriptions list"""
    try:
        patient_id = session.get('patient_id')
        role = session.get('role')
        status_filter = request.args.get('status')
        
        conn = get_db()
        
        if role == 'admin':
            query = 'SELECT * FROM prescriptions'
            params = []
        else:
            query = 'SELECT * FROM prescriptions WHERE patient_id = ?'
            params = [patient_id]
        
        if status_filter:
            query += ' AND status = ?' if 'WHERE' in query else ' WHERE status = ?'
            params.append(status_filter)
        
        query += ' ORDER BY created_at DESC'
        
        prescriptions = conn.execute(query, params).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'prescriptions': [dict(rx) for rx in prescriptions]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/prescriptions', methods=['POST'])
@login_required
def api_prescriptions_create():
    """Create new prescription"""
    try:
        data = request.json
        patient_id = session.get('patient_id') or data.get('patient_id')
        
        if not patient_id:
            return jsonify({'success': False, 'error': 'Patient ID required'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO prescriptions (
                patient_id, doctor_name, medication_name, dosage, frequency, 
                duration, instructions, start_date, end_date, refills_remaining, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            data.get('doctor_name'),
            data.get('medication_name'),
            data.get('dosage'),
            data.get('frequency'),
            data.get('duration'),
            data.get('instructions'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('refills_remaining', 0),
            data.get('status', 'Active')
        ))
        
        prescription_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'prescription_create', f'Created prescription #{prescription_id}')
        
        return jsonify({
            'success': True,
            'message': 'Prescription added successfully!',
            'prescription_id': prescription_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# API Routes - Vital Signs
# ============================================

@app.route('/api/vital-signs', methods=['GET'])
@login_required
def api_vital_signs_list():
    """Get vital signs list"""
    try:
        patient_id = session.get('patient_id')
        role = session.get('role')
        limit = request.args.get('limit', 30, type=int)
        
        conn = get_db()
        
        if role == 'admin':
            query = 'SELECT * FROM vital_signs ORDER BY recorded_at DESC LIMIT ?'
            params = [limit]
        else:
            query = 'SELECT * FROM vital_signs WHERE patient_id = ? ORDER BY recorded_at DESC LIMIT ?'
            params = [patient_id, limit]
        
        vital_signs = conn.execute(query, params).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'vital_signs': [dict(vs) for vs in vital_signs]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/vital-signs', methods=['POST'])
@login_required
def api_vital_signs_create():
    """Record new vital signs"""
    try:
        data = request.json
        patient_id = session.get('patient_id') or data.get('patient_id')
        
        if not patient_id:
            return jsonify({'success': False, 'error': 'Patient ID required'}), 400
        
        # Parse blood pressure if provided as string
        bp = data.get('blood_pressure', '')
        bp_systolic = data.get('blood_pressure_systolic')
        bp_diastolic = data.get('blood_pressure_diastolic')
        
        if bp and '/' in bp:
            parts = bp.split('/')
            bp_systolic = int(parts[0])
            bp_diastolic = int(parts[1])
        
        # Calculate BMI if height and weight provided
        weight = data.get('weight')
        height = data.get('height')
        bmi = None
        if weight and height:
            bmi = round(weight / ((height/100) ** 2), 2)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vital_signs (
                patient_id, blood_pressure, blood_pressure_systolic, blood_pressure_diastolic,
                heart_rate, temperature, oxygen_saturation, respiratory_rate,
                glucose_level, weight, bmi, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            bp,
            bp_systolic,
            bp_diastolic,
            data.get('heart_rate'),
            data.get('temperature'),
            data.get('oxygen_saturation'),
            data.get('respiratory_rate'),
            data.get('glucose_level'),
            weight,
            bmi,
            data.get('notes')
        ))
        
        vital_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'vital_signs_record', f'Recorded vital signs #{vital_id}')
        
        return jsonify({
            'success': True,
            'message': 'Vital signs recorded successfully!',
            'vital_id': vital_id,
            'bmi': bmi
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# API Routes - Lab Reports
# ============================================

@app.route('/api/lab-reports', methods=['GET'])
@login_required
def api_lab_reports_list():
    """Get lab reports list"""
    try:
        patient_id = session.get('patient_id')
        role = session.get('role')
        status_filter = request.args.get('status')
        
        conn = get_db()
        
        if role == 'admin':
            query = 'SELECT * FROM lab_reports'
            params = []
        else:
            query = 'SELECT * FROM lab_reports WHERE patient_id = ?'
            params = [patient_id]
        
        if status_filter:
            query += ' AND status = ?' if 'WHERE' in query else ' WHERE status = ?'
            params.append(status_filter)
        
        query += ' ORDER BY test_date DESC, created_at DESC'
        
        lab_reports = conn.execute(query, params).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'lab_reports': [dict(report) for report in lab_reports]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/lab-reports', methods=['POST'])
@login_required
def api_lab_reports_create():
    """Create new lab report"""
    try:
        data = request.json
        patient_id = session.get('patient_id') or data.get('patient_id')
        
        if not patient_id:
            return jsonify({'success': False, 'error': 'Patient ID required'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO lab_reports (
                patient_id, test_name, test_type, test_date, result_value,
                reference_range, unit, status, doctor_comments, abnormal_flag
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            data.get('test_name'),
            data.get('test_type'),
            data.get('test_date'),
            data.get('result_value'),
            data.get('reference_range'),
            data.get('unit'),
            data.get('status', 'Pending'),
            data.get('doctor_comments'),
            data.get('abnormal_flag', 0)
        ))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'lab_report_create', f'Created lab report #{report_id}')
        
        return jsonify({
            'success': True,
            'message': 'Lab report added successfully!',
            'report_id': report_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# API Routes - AI Chat
# ============================================

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """Handle chat message and generate AI response"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400
        
        # Generate AI response
        response = chatbot.generate_response(message, {
            'user_id': session.get('user_id'),
            'patient_id': session.get('patient_id')
        })
        
        intent = chatbot.extract_intent(message)
        sentiment = chatbot.analyze_sentiment(message)
        
        # Save to database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_history (
                session_id, user_id, patient_id, message, response, 
                sender, intent, sentiment
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.sid if hasattr(request, 'sid') else 'http',
            session.get('user_id'),
            session.get('patient_id'),
            message,
            response,
            'user',
            intent,
            sentiment
        ))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'response': response,
            'intent': intent,
            'sentiment': sentiment
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat/history', methods=['GET'])
@login_required
def api_chat_history():
    """Get chat history"""
    try:
        user_id = session.get('user_id')
        limit = request.args.get('limit', 50, type=int)
        
        conn = get_db()
        history = conn.execute("""
            SELECT * FROM chat_history 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (user_id, limit)).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'history': [dict(h) for h in history]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# WebSocket Events for Real-time Chat
# ============================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'Client connected: {request.sid}')
    emit('connected', {'message': 'Connected to AI Healthcare Assistant'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f'Client disconnected: {request.sid}')

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle incoming chat message via WebSocket"""
    try:
        message = data.get('message', '').strip()
        
        if not message:
            emit('chat_error', {'error': 'Message is required'})
            return
        
        # Generate AI response
        response = chatbot.generate_response(message)
        intent = chatbot.extract_intent(message)
        sentiment = chatbot.analyze_sentiment(message)
        
        # Send response back
        emit('chat_response', {
            'message': message,
            'response': response,
            'intent': intent,
            'sentiment': sentiment,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        emit('chat_error', {'error': str(e)})

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    emit('user_typing', {'typing': data.get('typing', False)}, broadcast=True, include_self=False)

# ============================================
# Additional API Routes
# ============================================

@app.route('/api/profile', methods=['GET'])
@login_required
def api_profile_get():
    """Get user profile"""
    try:
        user_id = session.get('user_id')
        patient_id = session.get('patient_id')
        
        conn = get_db()
        
        # Get user data
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        
        # Get patient data if exists
        patient = None
        if patient_id:
            patient = conn.execute('SELECT * FROM patients WHERE id = ?', (patient_id,)).fetchone()
        
        conn.close()
        
        return jsonify({
            'success': True,
            'user': dict(user) if user else None,
            'patient': dict(patient) if patient else None
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/profile', methods=['PUT'])
@login_required
def api_profile_update():
    """Update user profile"""
    try:
        data = request.json
        user_id = session.get('user_id')
        patient_id = session.get('patient_id')
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Update user data
        user_fields = []
        user_values = []
        for field in ['full_name', 'email', 'phone']:
            if field in data:
                user_fields.append(f"{field} = ?")
                user_values.append(data[field])
        
        if user_fields:
            user_values.append(user_id)
            cursor.execute(f"UPDATE users SET {', '.join(user_fields)} WHERE id = ?", user_values)
        
        # Update patient data if exists
        if patient_id:
            patient_fields = []
            patient_values = []
            for field in ['name', 'age', 'gender', 'blood_group', 'height', 'weight', 'allergies', 'chronic_conditions', 'emergency_contact', 'emergency_phone']:
                if field in data:
                    patient_fields.append(f"{field} = ?")
                    patient_values.append(data[field])
            
            # Calculate BMI
            if 'height' in data and 'weight' in data:
                height = float(data['height'])
                weight = float(data['weight'])
                bmi = round(weight / ((height/100) ** 2), 2)
                patient_fields.append('bmi = ?')
                patient_values.append(bmi)
            
            if patient_fields:
                patient_values.append(patient_id)
                cursor.execute(f"UPDATE patients SET {', '.join(patient_fields)} WHERE id = ?", patient_values)
        
        conn.commit()
        conn.close()
        
        log_activity(user_id, 'profile_update', 'Profile updated')
        
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/activity-logs', methods=['GET'])
@login_required
def api_activity_logs():
    """Get activity logs"""
    try:
        user_id = session.get('user_id')
        role = session.get('role')
        limit = request.args.get('limit', 100, type=int)
        
        conn = get_db()
        
        if role == 'admin':
            logs = conn.execute("""
                SELECT al.*, u.username, u.full_name
                FROM activity_logs al
                LEFT JOIN users u ON al.user_id = u.id
                ORDER BY al.timestamp DESC
                LIMIT ?
            """, (limit,)).fetchall()
        else:
            logs = conn.execute("""
                SELECT * FROM activity_logs
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, limit)).fetchall()
        
        conn.close()
        
        return jsonify({
            'success': True,
            'logs': [dict(log) for log in logs]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# Error Handlers
# ============================================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Endpoint not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

# ============================================
# Main Application Entry Point
# ============================================

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/img', exist_ok=True)
    
    print("=" * 60)
    print("🏥 AI Healthcare Chatbot - Enhanced Version 2.0")
    print("=" * 60)
    print("✅ Database initialized")
    print("✅ AI Chatbot engine ready")
    print("✅ WebSocket server configured")
    print("✅ Security features enabled")
    print("=" * 60)
    print("🚀 Starting server...")
    print("🌐 Access at: http://localhost:5000")
    print("=" * 60)
    
    # Run with SocketIO
    socketio.run(
        app,
        debug=True,
        host='0.0.0.0',
        port=5000,
        allow_unsafe_werkzeug=True
    )
