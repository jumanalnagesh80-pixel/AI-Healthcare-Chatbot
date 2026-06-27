"""
Ultra-Advanced AI Healthcare System - Professional Web Application
Author: Kiro AI Assistant  
Date: June 27, 2026
Description: World-class healthcare platform with modern UI, Chart.js, file uploads, animations
Features: Glassmorphism UI, data visualization, email notifications, dark mode, real-time updates
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for, send_file
from flask_cors import CORS
from functools import wraps
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
import os
import json
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
CORS(app)

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database setup
DATABASE = 'ultra_healthcare.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize comprehensive database with advanced features"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table (patients)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            age INTEGER,
            gender TEXT,
            blood_group TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            doctor_name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            symptoms TEXT,
            diagnosis TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Chats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Medical Records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            record_type TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            doctor_name TEXT,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Prescriptions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            doctor_name TEXT NOT NULL,
            medication TEXT NOT NULL,
            dosage TEXT NOT NULL,
            frequency TEXT NOT NULL,
            duration TEXT NOT NULL,
            instructions TEXT,
            date_prescribed TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Lab Reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lab_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            test_name TEXT NOT NULL,
            test_type TEXT NOT NULL,
            result TEXT NOT NULL,
            reference_range TEXT,
            status TEXT,
            test_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Vital Signs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vital_signs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            blood_pressure TEXT,
            heart_rate INTEGER,
            temperature REAL,
            weight REAL,
            bmi REAL,
            recorded_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create default admin if not exists
    cursor.execute('SELECT COUNT(*) FROM admins')
    if cursor.fetchone()[0] == 0:
        admin_password = hash_password('admin123')
        cursor.execute('''
            INSERT INTO admins (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', ('Admin User', 'admin@healthcare.com', admin_password, 'super_admin'))
        print("✅ Default admin created: admin@healthcare.com / admin123")
    
    conn.commit()
    conn.close()
    print("✅ Advanced database initialized successfully!")

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

# ==================== AUTHENTICATION DECORATORS ====================

def login_required(f):
    """Decorator for routes that require user login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator for routes that require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_ai_response(user_message, user_name="there"):
    """Advanced AI chatbot responses with personalization"""
    message_lower = user_message.lower()
    
    # Emergency detection
    emergency_keywords = ['emergency', 'urgent', 'severe pain', 'chest pain', 'cant breathe', 
                         'suicide', 'heart attack', 'stroke']
    if any(keyword in message_lower for keyword in emergency_keywords):
        return f"""🚨 EMERGENCY ALERT 🚨

{user_name}, this sounds like an emergency!

IMMEDIATE ACTIONS:
1. 🚑 Call 911 NOW
2. 📞 Contact emergency services immediately
3. 🏥 Go to nearest Emergency Room

Emergency Services: 911
Poison Control: 1-800-222-1222

DO NOT WAIT - GET HELP IMMEDIATELY!"""
    
    # Health condition responses
    if any(word in message_lower for word in ['fever', 'temperature', 'hot']):
        return f"""Hi {user_name}! For fever management:

🌡️ **Immediate Steps:**
• Rest in comfortable environment
• Stay well-hydrated (water, clear broths)
• Take acetaminophen (Tylenol) or ibuprofen as directed
• Use cool compresses on forehead

📊 **Monitoring:**
• Check temperature every 4 hours
• Normal: 98.6°F (37°C)
• Fever: > 100.4°F (38°C)

⚠️ **Seek Medical Attention If:**
• Fever > 103°F (39.4°C)
• Lasts more than 3 days
• Accompanied by severe symptoms

Would you like to book an appointment?"""

    elif any(word in message_lower for word in ['headache', 'head pain', 'migraine']):
        return f"""Hi {user_name}! For headache relief:

💊 **Immediate Relief:**
• Rest in quiet, dark room
• Apply cold compress to forehead
• Stay hydrated
• Take OTC pain relievers
• Avoid screens and bright lights

⚠️ **See Doctor If:**
• Sudden, severe headache
• Headache with fever or confusion
• Persistent or worsening

Need to schedule an appointment?"""
    
    elif any(word in message_lower for word in ['cough', 'cold', 'flu']):
        return f"""Hi {user_name}! For cough/cold/flu:

🏠 **Home Care:**
• Get 7-9 hours quality sleep
• Drink warm fluids (tea, soup, honey water)
• Use humidifier
• Gargle with warm salt water
• Take vitamin C and zinc

📞 **Call Doctor If:**
• Symptoms worsen after 7-10 days
• High fever > 103°F
• Difficulty breathing"""
    
    elif any(word in message_lower for word in ['stomach', 'pain', 'ache', 'abdominal']):
        return f"""Hi {user_name}! For stomach issues:

🥤 **Initial Steps:**
• Stop eating solid foods temporarily
• Sip clear liquids
• Try BRAT diet: Bananas, Rice, Applesauce, Toast
• Avoid dairy, caffeine, alcohol
• Rest

⚠️ **EMERGENCY - Go to ER If:**
• Severe, constant pain
• Bloody stools
• Vomiting blood
• Fever with pain"""
    
    elif any(word in message_lower for word in ['stress', 'anxiety', 'worried', 'mental', 'depressed']):
        return f"""Hi {user_name}! Mental health support:

🧠 **Immediate Coping:**
• Deep breathing: Inhale 4 sec, hold 7 sec, exhale 8 sec
• Practice grounding techniques
• Step outside for fresh air
• Listen to calming music

🏃 **Long-term Management:**
• Regular exercise (30 min/day)
• Consistent sleep schedule (7-9 hours)
• Mindfulness or meditation
• Connect with friends/family

📞 **Professional Help:**
• Therapy/Counseling
• Support groups

🆘 **Crisis Resources:**
• 988 Suicide & Crisis Lifeline
• Call or text 988

Would you like to book mental health appointment?"""
    
    elif any(word in message_lower for word in ['diabetes', 'blood sugar', 'glucose']):
        return f"""Hi {user_name}! Diabetes management:

📊 **Blood Sugar Monitoring:**
• Fasting target: 80-130 mg/dL
• After meals: < 180 mg/dL
• HbA1c goal: < 7%

🍽️ **Diet Management:**
• Count carbohydrates (45-60g per meal)
• Choose complex carbs
• Include lean proteins
• Healthy fats in moderation

💊 **Medication:**
• Take as prescribed
• Never skip doses
• Monitor for side effects

Need endocrinologist appointment?"""
    
    elif any(word in message_lower for word in ['blood pressure', 'bp', 'hypertension']):
        return f"""Hi {user_name}! Blood pressure management:

📊 **Understanding BP:**
• Normal: < 120/80 mmHg
• Elevated: 120-129 / < 80
• Hypertension: ≥ 130/80

🧂 **Diet (DASH Diet):**
• Reduce sodium to < 2,300 mg/day
• Eat fruits, vegetables, whole grains
• Limit processed foods

🏃 **Exercise:**
• 30 minutes moderate activity, 5 days/week
• Walking, swimming, cycling

Book cardiology appointment?"""
    
    elif any(word in message_lower for word in ['appointment', 'book', 'schedule', 'doctor']):
        return f"""Hi {user_name}! Ready to book appointment:

📅 **Available Specialties:**
• General Physician
• Cardiology
• Dermatology
• Pediatrics
• Orthopedics
• Neurology
• Gynecology
• Gastroenterology
• Endocrinology
• Psychiatry

Click 'Appointments' tab to book! 🔝"""
    
    elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'start']):
        return f"""Hello {user_name}! 👋 Welcome to AI Healthcare Assistant!

I can help you with:

💬 **Health Consultations**
📅 **Book Appointments**
📊 **Track Health Records**
💊 **Medication Management**
📈 **Vital Signs Monitoring**

Just ask me anything health-related! 💙"""
    
    elif any(word in message_lower for word in ['thank', 'thanks']):
        return f"""You're welcome, {user_name}! 😊

I'm always here to help with your health questions!

Stay healthy and take care! 💚"""
    
    else:
        return f"""Hi {user_name}! I can help with:

🩺 **Common Topics:**
• Fever, headache, cough, cold
• Stomach pain, digestion issues
• Stress, anxiety, mental health
• Diabetes, blood pressure
• Weight management
• Medication information
• Appointment booking

Please describe your concern, and I'll provide detailed guidance!

⚠️ Note: I provide general information. For diagnosis and treatment, please consult a healthcare professional.

**Emergency?** Call 911 immediately."""

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home/Landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    return render_template_string(INDEX_HTML)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and handler"""
    if request.method == 'GET':
        return render_template_string(REGISTER_HTML)

    
    # POST - handle registration
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        phone = data.get('phone', '').strip()
        
        # Validation
        if not name or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        
        # Check if email exists
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Insert new user
        hashed_password = hash_password(password)
        cursor.execute('''
            INSERT INTO users (name, email, password, phone)
            VALUES (?, ?, ?, ?)
        ''', (name, email, hashed_password, phone))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        # Set session
        session['user_id'] = user_id
        session['user_name'] = name
        session['user_email'] = email
        
        return jsonify({'success': True, 'message': 'Registration successful!'}), 200
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

@app.route('/login', methods=['GET', 'POST'])

def login():
    """Login page and handler"""
    if request.method == 'GET':
        return render_template_string(LOGIN_HTML)
    
    # POST - handle login
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        # Check credentials
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, password FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        hashed_password = hash_password(password)
        if user['password'] != hashed_password:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Set session
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        
        return jsonify({'success': True, 'message': 'Login successful!'}), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@app.route('/logout')
def logout():
    """Logout handler"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Modern Dashboard with charts - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get user stats
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM appointments WHERE user_id = ?', (session['user_id'],))
    total_appointments = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM chats WHERE user_id = ?', (session['user_id'],))
    total_chats = cursor.fetchone()[0]
    
    # Get recent appointments
    cursor.execute('''
        SELECT doctor_name, specialty, appointment_date, appointment_time, status
        FROM appointments
        WHERE user_id = ?
        ORDER BY appointment_date DESC, appointment_time DESC
        LIMIT 5
    ''', (session['user_id'],))
    recent_appointments = cursor.fetchall()
    
    conn.close()
    
    # Import modern dashboard
    from modern_templates import MODERN_DASHBOARD_HTML
    
    return render_template_string(MODERN_DASHBOARD_HTML,
                                 user_name=session['user_name'],
                                 total_appointments=total_appointments,
                                 total_chats=total_chats,
                                 recent_appointments=recent_appointments)

@app.route('/chat')
def chat():
    """Chat page - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get chat history
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT message, response, created_at
        FROM chats
        WHERE user_id = ?
        ORDER BY created_at ASC
    ''', (session['user_id'],))
    chat_history = cursor.fetchall()
    conn.close()

    
    return render_template_string(CHAT_HTML, 
                                 user_name=session['user_name'],
                                 chat_history=chat_history)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for chat"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'message': 'Message cannot be empty'}), 400
        
        # Get AI response
        response = get_ai_response(message)
        
        # Save to database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chats (user_id, message, response)
            VALUES (?, ?, ?)
        ''', (session['user_id'], message, response))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'response': response}), 200
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'success': False, 'message': 'Chat failed'}), 500

@app.route('/appointments')
def appointments():
    """Appointments page - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get user appointments
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, doctor_name, specialty, appointment_date, appointment_time, status, symptoms
        FROM appointments

        WHERE user_id = ?
        ORDER BY appointment_date DESC, appointment_time DESC
    ''', (session['user_id'],))
    appointments_list = cursor.fetchall()
    conn.close()
    
    return render_template_string(APPOINTMENTS_HTML,
                                 user_name=session['user_name'],
                                 appointments=appointments_list)

@app.route('/api/appointments', methods=['POST'])
def api_book_appointment():
    """API endpoint to book appointment"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        doctor_name = data.get('doctor_name', '').strip()
        specialty = data.get('specialty', '').strip()
        appointment_date = data.get('appointment_date', '').strip()
        appointment_time = data.get('appointment_time', '').strip()
        symptoms = data.get('symptoms', '').strip()
        
        if not all([doctor_name, specialty, appointment_date, appointment_time]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Insert appointment
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO appointments (user_id, doctor_name, specialty, appointment_date, appointment_time, symptoms)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], doctor_name, specialty, appointment_date, appointment_time, symptoms))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Appointment booked successfully!'}), 200
        
    except Exception as e:
        print(f"Appointment booking error: {e}")
        return jsonify({'success': False, 'message': 'Booking failed'}), 500

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page and handler"""
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'GET':
        return render_template_string(ADMIN_LOGIN_HTML)
    
    # POST - handle admin login
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, password, role FROM admins WHERE email = ?', (email,))
        admin = cursor.fetchone()
        conn.close()
        
        if not admin:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        hashed_password = hash_password(password)
        if admin['password'] != hashed_password:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Set admin session
        session['admin_id'] = admin['id']
        session['admin_name'] = admin['name']
        session['admin_email'] = admin['email']
        session['admin_role'] = admin['role']
        
        return jsonify({'success': True, 'message': 'Login successful!'}), 200
        
    except Exception as e:
        print(f"Admin login error: {e}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard with statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM appointments')
    total_appointments = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status='pending'")
    pending_appointments = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status='confirmed'")
    confirmed_appointments = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM chats')
    total_chats = cursor.fetchone()[0]
    
    # Get recent users
    cursor.execute('''
        SELECT id, name, email, phone, created_at
        FROM users
        ORDER BY created_at DESC
        LIMIT 10
    ''')
    recent_users = cursor.fetchall()
    
    # Get recent appointments
    cursor.execute('''
        SELECT a.id, u.name, a.doctor_name, a.specialty, a.appointment_date, 
               a.appointment_time, a.status
        FROM appointments a
        JOIN users u ON a.user_id = u.id
        ORDER BY a.created_at DESC
        LIMIT 10
    ''')
    recent_appointments = cursor.fetchall()
    
    conn.close()
    
    return render_template_string(ADMIN_DASHBOARD_HTML,
                                 admin_name=session['admin_name'],
                                 total_users=total_users,
                                 total_appointments=total_appointments,
                                 pending_appointments=pending_appointments,
                                 confirmed_appointments=confirmed_appointments,
                                 total_chats=total_chats,
                                 recent_users=recent_users,
                                 recent_appointments=recent_appointments)

@app.route('/admin/users')
@admin_required
def admin_users():
    """Manage users"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, email, phone, age, gender, blood_group, created_at
        FROM users
        ORDER BY created_at DESC
    ''')
    users = cursor.fetchall()
    conn.close()
    
    return render_template_string(ADMIN_USERS_HTML,
                                 admin_name=session['admin_name'],
                                 users=users)

@app.route('/admin/appointments')
@admin_required
def admin_appointments():
    """Manage appointments"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.id, u.name, u.email, a.doctor_name, a.specialty, 
               a.appointment_date, a.appointment_time, a.status, a.symptoms
        FROM appointments a
        JOIN users u ON a.user_id = u.id
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
    ''')
    appointments = cursor.fetchall()
    conn.close()
    
    return render_template_string(ADMIN_APPOINTMENTS_HTML,
                                 admin_name=session['admin_name'],
                                 appointments=appointments)

@app.route('/admin/appointment/update/<int:appointment_id>', methods=['POST'])
@admin_required
def admin_update_appointment(appointment_id):
    """Update appointment status"""
    try:
        data = request.get_json()
        status = data.get('status')
        diagnosis = data.get('diagnosis', '')
        notes = data.get('notes', '')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE appointments
            SET status = ?, diagnosis = ?, notes = ?
            WHERE id = ?
        ''', (status, diagnosis, notes, appointment_id))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Appointment updated!'}), 200
    except Exception as e:
        print(f"Update error: {e}")
        return jsonify({'success': False, 'message': 'Update failed'}), 500

# ==================== USER ADVANCED ROUTES ====================

@app.route('/medical-records')
@login_required
def medical_records():
    """User medical records"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, record_type, title, description, doctor_name, date, created_at
        FROM medical_records
        WHERE user_id = ?
        ORDER BY date DESC
    ''', (session['user_id'],))
    records = cursor.fetchall()
    conn.close()
    
    return render_template_string(MEDICAL_RECORDS_HTML,
                                 user_name=session['user_name'],
                                 records=records)

@app.route('/prescriptions')
@login_required
def prescriptions():
    """User prescriptions"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, doctor_name, medication, dosage, frequency, duration, 
               instructions, date_prescribed, status
        FROM prescriptions
        WHERE user_id = ?
        ORDER BY date_prescribed DESC
    ''', (session['user_id'],))
    prescriptions_list = cursor.fetchall()
    conn.close()
    
    return render_template_string(PRESCRIPTIONS_HTML,
                                 user_name=session['user_name'],
                                 prescriptions=prescriptions_list)

@app.route('/lab-reports')
@login_required
def lab_reports():
    """User lab reports"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, test_name, test_type, result, reference_range, status, test_date
        FROM lab_reports
        WHERE user_id = ?
        ORDER BY test_date DESC
    ''', (session['user_id'],))
    reports = cursor.fetchall()
    conn.close()
    
    return render_template_string(LAB_REPORTS_HTML,
                                 user_name=session['user_name'],
                                 reports=reports)

@app.route('/vital-signs')
@login_required
def vital_signs():
    """User vital signs tracking"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, blood_pressure, heart_rate, temperature, weight, bmi, recorded_date
        FROM vital_signs
        WHERE user_id = ?
        ORDER BY recorded_date DESC
        LIMIT 20
    ''', (session['user_id'],))
    vitals = cursor.fetchall()
    conn.close()
    
    return render_template_string(VITAL_SIGNS_HTML,
                                 user_name=session['user_name'],
                                 vitals=vitals)

@app.route('/api/vital-signs', methods=['POST'])
@login_required
def api_add_vital_signs():
    """Add vital signs"""
    try:
        data = request.get_json()
        blood_pressure = data.get('blood_pressure', '').strip()
        heart_rate = data.get('heart_rate')
        temperature = data.get('temperature')
        weight = data.get('weight')
        bmi = data.get('bmi')
        recorded_date = data.get('recorded_date')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vital_signs (user_id, blood_pressure, heart_rate, temperature, weight, bmi, recorded_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], blood_pressure, heart_rate, temperature, weight, bmi, recorded_date))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Vital signs recorded!'}), 200
    except Exception as e:
        print(f"Vital signs error: {e}")
        return jsonify({'success': False, 'message': 'Failed to record'}), 500

# ==================== FILE UPLOAD ROUTES ====================

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file uploads for medical documents"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'}), 400
    
    file = request.files['file']
    description = request.form.get('description', '')
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{session['user_id']}_{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)
        
        # Save to database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO files (user_id, filename, filepath, file_type, description)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], filename, filepath, file.content_type, description))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'File uploaded successfully!'}), 200
    
    return jsonify({'success': False, 'message': 'Invalid file type'}), 400

@app.route('/files')
@login_required
def user_files():
    """View uploaded files"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, filename, file_type, description, uploaded_at
        FROM files
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
    ''', (session['user_id'],))
    files = cursor.fetchall()
    conn.close()
    
    return render_template_string(FILES_HTML,
                                 user_name=session['user_name'],
                                 files=files)

@app.route('/api/dashboard-stats')
@login_required
def api_dashboard_stats():
    """API endpoint for dashboard statistics with chart data"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get vital signs for last 30 days
    cursor.execute('''
        SELECT recorded_date, blood_pressure, heart_rate, weight
        FROM vital_signs
        WHERE user_id = ?
        ORDER BY recorded_date DESC
        LIMIT 30
    ''', (session['user_id'],))
    vitals_data = cursor.fetchall()
    
    # Get appointments by month
    cursor.execute('''
        SELECT strftime('%Y-%m', appointment_date) as month, COUNT(*) as count
        FROM appointments
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    ''', (session['user_id'],))
    appointments_data = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'success': True,
        'vitals': [dict(row) for row in vitals_data],
        'appointments': [dict(row) for row in appointments_data]
    })

# ==================== HTML TEMPLATES ====================

# Import modern landing page
from modern_templates import MODERN_INDEX_HTML

INDEX_HTML = MODERN_INDEX_HTML

REGISTER_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Healthcare Chatbot - Home</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 60px 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 600px;
            width: 90%;
        }
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .subtitle {
            color: #666;
            font-size: 1.2em;
            margin-bottom: 40px;
        }
        .features {
            text-align: left;
            margin: 30px 0;
        }
        .feature {
            padding: 15px;
            margin: 10px 0;
            background: #f8f9fa;
            border-radius: 10px;
            font-size: 1.1em;
        }
        .feature::before {
            content: "✓ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 10px;
        }
        .buttons {
            margin-top: 40px;

        }
        .btn {
            display: inline-block;
            padding: 15px 40px;
            margin: 10px;
            border: none;
            border-radius: 50px;
            font-size: 1.1em;
            font-weight: bold;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 AI Healthcare Chatbot</h1>
        <p class="subtitle">Your Personal Health Assistant</p>
        
        <div class="features">
            <div class="feature">24/7 AI Health Consultation</div>
            <div class="feature">Book Doctor Appointments</div>
            <div class="feature">Symptom Analysis & Advice</div>
            <div class="feature">Health History Tracking</div>
            <div class="feature">Instant Medical Responses</div>
        </div>
        
        <div class="buttons">
            <a href="/register" class="btn btn-primary">Get Started</a>
            <a href="/login" class="btn btn-secondary">Login</a>
        </div>
    </div>
</body>
</html>
'''

REGISTER_HTML = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - AI Healthcare</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 450px;
            width: 90%;
        }
        h2 {
            color: #667eea;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #333;
            margin-bottom: 8px;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;

            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .btn:hover { transform: translateY(-2px); }
        .message {
            padding: 12px;
            margin-bottom: 20px;
            border-radius: 8px;
            text-align: center;
            display: none;
        }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .link {
            text-align: center;
            margin-top: 20px;
            color: #666;
        }
        .link a {
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🏥 Create Account</h2>
        <div id="message" class="message"></div>
        <form id="registerForm">
            <div class="form-group">
                <label>Full Name *</label>
                <input type="text" id="name" required placeholder="Enter your full name">
            </div>
            <div class="form-group">
                <label>Email *</label>
                <input type="email" id="email" required placeholder="Enter your email">
            </div>
            <div class="form-group">
                <label>Password * (min 6 characters)</label>
                <input type="password" id="password" required placeholder="Create a password">
            </div>
            <div class="form-group">
                <label>Phone Number</label>
                <input type="tel" id="phone" placeholder="Enter your phone number">

            </div>
            <button type="submit" class="btn">Register</button>
        </form>
        <div class="link">
            Already have an account? <a href="/login">Login here</a>
        </div>
    </div>
    
    <script>
        document.getElementById('registerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const phone = document.getElementById('phone').value.trim();
            
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, password, phone })
                });
                
                const data = await response.json();
                const messageDiv = document.getElementById('message');
                messageDiv.style.display = 'block';
                
                if (data.success) {
                    messageDiv.className = 'message success';
                    messageDiv.textContent = data.message;
                    setTimeout(() => { window.location.href = '/dashboard'; }, 1500);
                } else {
                    messageDiv.className = 'message error';
                    messageDiv.textContent = data.message;
                }
            } catch (error) {
                const messageDiv = document.getElementById('message');
                messageDiv.style.display = 'block';
                messageDiv.className = 'message error';
                messageDiv.textContent = 'Registration failed. Please try again.';
            }
        });
    </script>
</body>
</html>
'''

LOGIN_HTML = '''
<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - AI Healthcare</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 450px;
            width: 90%;
        }
        h2 {
            color: #667eea;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #333;
            margin-bottom: 8px;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .btn:hover { transform: translateY(-2px); }
        .message {
            padding: 12px;
            margin-bottom: 20px;
            border-radius: 8px;
            text-align: center;
            display: none;
        }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .link {
            text-align: center;
            margin-top: 20px;
            color: #666;
        }
        .link a {
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🏥 Welcome Back</h2>
        <div id="message" class="message"></div>
        <form id="loginForm">
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="email" required placeholder="Enter your email">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required placeholder="Enter your password">
            </div>
            <button type="submit" class="btn">Login</button>
        </form>

        <div class="link">
            Don't have an account? <a href="/register">Register here</a>
        </div>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                const messageDiv = document.getElementById('message');
                messageDiv.style.display = 'block';
                
                if (data.success) {
                    messageDiv.className = 'message success';
                    messageDiv.textContent = data.message;
                    setTimeout(() => { window.location.href = '/dashboard'; }, 1500);
                } else {
                    messageDiv.className = 'message error';
                    messageDiv.textContent = data.message;
                }
            } catch (error) {
                const messageDiv = document.getElementById('message');
                messageDiv.style.display = 'block';
                messageDiv.className = 'message error';
                messageDiv.textContent = 'Login failed. Please try again.';
            }
        });
    </script>
</body>
</html>
'''

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - AI Healthcare</title>

    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .navbar-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h1 { font-size: 1.5em; }
        .nav-links a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
            padding: 8px 16px;
            border-radius: 8px;
            transition: background 0.3s;
        }
        .nav-links a:hover { background: rgba(255,255,255,0.2); }
        .container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .welcome {
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .welcome h2 { color: #667eea; margin-bottom: 10px; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {

            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-card h3 { color: #667eea; font-size: 2.5em; margin-bottom: 10px; }
        .stat-card p { color: #666; font-size: 1.1em; }
        .section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .section h3 { color: #667eea; margin-bottom: 20px; }
        .appointment-item {
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }
        .appointment-item strong { color: #333; }
        .appointment-item .status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.9em;
            background: #d4edda;
            color: #155724;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="navbar-content">
            <h1>🏥 AI Healthcare</h1>
            <div class="nav-links">
                <a href="/dashboard">Dashboard</a>
                <a href="/chat">Chat</a>
                <a href="/appointments">Appointments</a>
                <a href="/logout">Logout</a>
            </div>
        </div>
    </div>
    
    <div class="container">

        <div class="welcome">
            <h2>Welcome back, {{ user_name }}! 👋</h2>
            <p>Your health is our priority. How can we help you today?</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{{ total_appointments }}</h3>
                <p>Total Appointments</p>
            </div>
            <div class="stat-card">
                <h3>{{ total_chats }}</h3>
                <p>Health Consultations</p>
            </div>
        </div>
        
        <div class="section">
            <h3>Recent Appointments</h3>
            {% if recent_appointments %}
                {% for apt in recent_appointments %}
                <div class="appointment-item">
                    <strong>{{ apt[0] }}</strong> - {{ apt[1] }}
                    <span class="status">{{ apt[4] }}</span>
                    <br>
                    <small>{{ apt[2] }} at {{ apt[3] }}</small>
                </div>
                {% endfor %}
            {% else %}
                <p style="color: #666;">No appointments yet. <a href="/appointments" style="color: #667eea;">Book your first appointment</a></p>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

CHAT_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat - AI Healthcare</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;

            background: #f5f7fa;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            flex-shrink: 0;
        }
        .navbar-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h1 { font-size: 1.5em; }
        .nav-links a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
            padding: 8px 16px;
            border-radius: 8px;
            transition: background 0.3s;
        }
        .nav-links a:hover { background: rgba(255,255,255,0.2); }
        .chat-container {
            flex: 1;
            max-width: 900px;
            width: 100%;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            padding: 20px;
        }
        .chat-messages {
            flex: 1;
            background: white;
            border-radius: 15px;
            padding: 20px;
            overflow-y: auto;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .message {
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
        }
        .message.user { align-items: flex-end; }

        .message.bot { align-items: flex-start; }
        .message-bubble {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        .message.user .message-bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .message.bot .message-bubble {
            background: #e9ecef;
            color: #333;
        }
        .chat-input {
            display: flex;
            gap: 10px;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .chat-input input {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
        }
        .chat-input input:focus {
            outline: none;
            border-color: #667eea;
        }
        .chat-input button {
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .chat-input button:hover { transform: translateY(-2px); }
        .timestamp {
            font-size: 0.75em;
            color: #999;
            margin-top: 5px;
        }
    </style>
</head>

<body>
    <div class="navbar">
        <div class="navbar-content">
            <h1>🏥 AI Healthcare - Chat</h1>
            <div class="nav-links">
                <a href="/dashboard">Dashboard</a>
                <a href="/chat">Chat</a>
                <a href="/appointments">Appointments</a>
                <a href="/logout">Logout</a>
            </div>
        </div>
    </div>
    
    <div class="chat-container">
        <div class="chat-messages" id="chatMessages">
            {% if chat_history %}
                {% for chat in chat_history %}
                <div class="message user">
                    <div class="message-bubble">{{ chat[0] }}</div>
                    <div class="timestamp">{{ chat[2] }}</div>
                </div>
                <div class="message bot">
                    <div class="message-bubble">{{ chat[1] }}</div>
                </div>
                {% endfor %}
            {% else %}
                <div class="message bot">
                    <div class="message-bubble">Hello {{ user_name }}! 👋 I'm your AI Healthcare Assistant. How can I help you today?</div>
                </div>
            {% endif %}
        </div>
        
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Type your health question here..." />
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    
    <script>
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        
        // Auto-scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Send on Enter key
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();

        });
        
        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            messageInput.value = '';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    addMessage(data.response, 'bot');
                } else {
                    addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            } catch (error) {
                addMessage('Connection error. Please check your internet and try again.', 'bot');
            }
        }
        
        function addMessage(text, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            bubble.textContent = text;
            
            messageDiv.appendChild(bubble);
            
            if (type === 'user') {
                const timestamp = document.createElement('div');
                timestamp.className = 'timestamp';
                timestamp.textContent = new Date().toLocaleString();
                messageDiv.appendChild(timestamp);
            }
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    </script>
</body>
</html>
'''

APPOINTMENTS_HTML = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointments - AI Healthcare</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .navbar-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h1 { font-size: 1.5em; }
        .nav-links a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
            padding: 8px 16px;
            border-radius: 8px;
            transition: background 0.3s;
        }
        .nav-links a:hover { background: rgba(255,255,255,0.2); }
        .container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .section h2 { color: #667eea; margin-bottom: 20px; }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            color: #333;
            margin-bottom: 8px;
            font-weight: 500;
        }
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
        }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            padding: 14px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .btn:hover { transform: translateY(-2px); }
        .message {
            padding: 12px;
            margin-bottom: 20px;
            border-radius: 8px;
            text-align: center;
            display: none;
        }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .appointment-list {
            margin-top: 20px;
        }
        .appointment-card {
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }
        .appointment-card h4 { color: #667eea; margin-bottom: 10px; }
        .appointment-card p { color: #666; margin: 5px 0; }
        .status-badge {
            display: inline-block;

            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.9em;
            background: #d4edda;
            color: #155724;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="navbar-content">
            <h1>🏥 AI Healthcare - Appointments</h1>
            <div class="nav-links">
                <a href="/dashboard">Dashboard</a>
                <a href="/chat">Chat</a>
                <a href="/appointments">Appointments</a>
                <a href="/logout">Logout</a>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="section">
            <h2>Book New Appointment</h2>
            <div id="message" class="message"></div>
            <form id="appointmentForm">
                <div class="form-grid">
                    <div class="form-group">
                        <label>Doctor Name *</label>
                        <input type="text" id="doctorName" required placeholder="Dr. Smith">
                    </div>
                    <div class="form-group">
                        <label>Specialty *</label>
                        <select id="specialty" required>
                            <option value="">Select Specialty</option>
                            <option value="General">General Physician</option>
                            <option value="Cardiology">Cardiology</option>
                            <option value="Dermatology">Dermatology</option>
                            <option value="Pediatrics">Pediatrics</option>
                            <option value="Orthopedics">Orthopedics</option>
                            <option value="Neurology">Neurology</option>
                            <option value="Gynecology">Gynecology</option>
                        </select>
                    </div>
                </div>
                <div class="form-grid">

                    <div class="form-group">
                        <label>Date *</label>
                        <input type="date" id="appointmentDate" required>
                    </div>
                    <div class="form-group">
                        <label>Time *</label>
                        <input type="time" id="appointmentTime" required>
                    </div>
                </div>
                <div class="form-group">
                    <label>Symptoms/Reason</label>
                    <textarea id="symptoms" rows="3" placeholder="Describe your symptoms or reason for visit..."></textarea>
                </div>
                <button type="submit" class="btn">Book Appointment</button>
            </form>
        </div>
        
        <div class="section">
            <h2>Your Appointments</h2>
            <div class="appointment-list">
                {% if appointments %}
                    {% for apt in appointments %}
                    <div class="appointment-card">
                        <h4>{{ apt[1] }} - {{ apt[2] }}</h4>
                        <p><strong>Date:</strong> {{ apt[3] }} at {{ apt[4] }}</p>
                        <p><strong>Status:</strong> <span class="status-badge">{{ apt[5] }}</span></p>
                        {% if apt[6] %}
                        <p><strong>Symptoms:</strong> {{ apt[6] }}</p>
                        {% endif %}
                    </div>
                    {% endfor %}
                {% else %}
                    <p style="color: #666;">No appointments yet. Book your first appointment above!</p>
                {% endif %}
            </div>
        </div>
    </div>
    
    <script>
        // Set min date to today
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('appointmentDate').min = today;
        
        document.getElementById('appointmentForm').addEventListener('submit', async function(e) {

            e.preventDefault();
            
            const doctorName = document.getElementById('doctorName').value.trim();
            const specialty = document.getElementById('specialty').value;
            const appointmentDate = document.getElementById('appointmentDate').value;
            const appointmentTime = document.getElementById('appointmentTime').value;
            const symptoms = document.getElementById('symptoms').value.trim();
            
            try {
                const response = await fetch('/api/appointments', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        doctor_name: doctorName,
                        specialty: specialty,
                        appointment_date: appointmentDate,
                        appointment_time: appointmentTime,
                        symptoms: symptoms
                    })
                });
                
                const data = await response.json();
                const messageDiv = document.getElementById('message');
                messageDiv.style.display = 'block';
                
                if (data.success) {
                    messageDiv.className = 'message success';
                    messageDiv.textContent = data.message;
                    setTimeout(() => { location.reload(); }, 2000);
                } else {
                    messageDiv.className = 'message error';
                    messageDiv.textContent = data.message;
                }
            } catch (error) {
                const messageDiv = document.getElementById('message');
                messageDiv.style.display = 'block';
                messageDiv.className = 'message error';
                messageDiv.textContent = 'Booking failed. Please try again.';
            }
        });
    </script>
</body>
</html>
'''

# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 AI Healthcare Chatbot - Starting...")
    print("=" * 60)
    
    # Initialize database

    init_db()
    
    print("\n✅ Server is ready!")
    print("\n📱 Open your browser and go to:")
    print("   http://127.0.0.1:5000")
    print("\n💡 Features:")
    print("   • Register/Login")
    print("   • AI Health Chat")
    print("   • Book Appointments")
    print("   • View Dashboard")
    print("\n⚠️  Press Ctrl+C to stop the server\n")
    print("=" * 60)
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)



# Admin Templates
ADMIN_LOGIN_HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Admin Login</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;align-items:center;justify-content:center}.container{background:white;padding:40px;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,0.3);max-width:450px;width:90%}h2{color:#667eea;text-align:center;margin-bottom:30px;font-size:2em}.form-group{margin-bottom:20px}label{display:block;color:#333;margin-bottom:8px;font-weight:500}input{width:100%;padding:12px;border:2px solid #e0e0e0;border-radius:8px;font-size:1em}input:focus{outline:none;border-color:#667eea}.btn{width:100%;padding:14px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;border-radius:8px;font-size:1.1em;font-weight:bold;cursor:pointer}.message{padding:12px;margin-bottom:20px;border-radius:8px;text-align:center;display:none}.success{background:#d4edda;color:#155724}.error{background:#f8d7da;color:#721c24}</style></head>
<body><div class="container"><h2>🔐 Admin Login</h2><div id="message" class="message"></div>
<form id="loginForm"><div class="form-group"><label>Email</label><input type="email" id="email" required></div>
<div class="form-group"><label>Password</label><input type="password" id="password" required></div>
<button type="submit" class="btn">Login</button></form></div>
<script>document.getElementById('loginForm').addEventListener('submit',async function(e){e.preventDefault();const email=document.getElementById('email').value.trim();const password=document.getElementById('password').value;try{const response=await fetch('/admin/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password})});const data=await response.json();const messageDiv=document.getElementById('message');messageDiv.style.display='block';if(data.success){messageDiv.className='message success';messageDiv.textContent=data.message;setTimeout(()=>{window.location.href='/admin/dashboard'},1500)}else{messageDiv.className='message error';messageDiv.textContent=data.message}}catch(error){const messageDiv=document.getElementById('message');messageDiv.style.display='block';messageDiv.className='message error';messageDiv.textContent='Login failed'}});</script></body></html>'''

ADMIN_DASHBOARD_HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Admin Dashboard</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:#f5f7fa}.navbar{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}.navbar-content{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}.nav-links a{color:white;text-decoration:none;margin-left:20px;padding:8px 16px;border-radius:8px}.nav-links a:hover{background:rgba(255,255,255,0.2)}.container{max-width:1200px;margin:40px auto;padding:0 20px}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-bottom:30px}.stat-card{background:white;padding:25px;border-radius:15px;box-shadow:0 2px 10px rgba(0,0,0,0.1);text-align:center}.stat-card h3{color:#667eea;font-size:2.5em;margin-bottom:10px}.stat-card p{color:#666}.section{background:white;padding:30px;border-radius:15px;box-shadow:0 2px 10px rgba(0,0,0,0.1);margin-bottom:30px}.section h3{color:#667eea;margin-bottom:20px}table{width:100%;border-collapse:collapse}th,td{padding:12px;text-align:left;border-bottom:1px solid #e0e0e0}th{background:#f8f9fa;font-weight:600}</style></head>
<body><div class="navbar"><div class="navbar-content"><h1>🔐 Admin Panel</h1><div class="nav-links">
<a href="/admin/dashboard">Dashboard</a><a href="/admin/users">Users</a><a href="/admin/appointments">Appointments</a>
<a href="/admin/logout">Logout</a></div></div></div>
<div class="container"><h2>Welcome, {{admin_name}}!</h2><div class="stats">
<div class="stat-card"><h3>{{total_users}}</h3><p>Total Users</p></div>
<div class="stat-card"><h3>{{total_appointments}}</h3><p>Total Appointments</p></div>
<div class="stat-card"><h3>{{pending_appointments}}</h3><p>Pending</p></div>
<div class="stat-card"><h3>{{confirmed_appointments}}</h3><p>Confirmed</p></div>
<div class="stat-card"><h3>{{total_chats}}</h3><p>Total Chats</p></div></div>
<div class="section"><h3>Recent Users</h3><table><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Registered</th></tr></thead><tbody>
{%for user in recent_users%}<tr><td>{{user[0]}}</td><td>{{user[1]}}</td><td>{{user[2]}}</td><td>{{user[3]or'-'}}</td><td>{{user[4]}}</td></tr>{%endfor%}</tbody></table></div>
<div class="section"><h3>Recent Appointments</h3><table><thead><tr><th>ID</th><th>Patient</th><th>Doctor</th><th>Specialty</th><th>Date</th><th>Time</th><th>Status</th></tr></thead><tbody>
{%for apt in recent_appointments%}<tr><td>{{apt[0]}}</td><td>{{apt[1]}}</td><td>{{apt[2]}}</td><td>{{apt[3]}}</td><td>{{apt[4]}}</td><td>{{apt[5]}}</td><td>{{apt[6]}}</td></tr>{%endfor%}</tbody></table></div></div></body></html>'''

ADMIN_USERS_HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Manage Users</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:#f5f7fa}.navbar{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:20px}.navbar-content{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}.nav-links a{color:white;text-decoration:none;margin-left:20px;padding:8px 16px;border-radius:8px}.nav-links a:hover{background:rgba(255,255,255,0.2)}.container{max-width:1200px;margin:40px auto;padding:0 20px}.section{background:white;padding:30px;border-radius:15px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}table{width:100%;border-collapse:collapse;margin-top:20px}th,td{padding:12px;text-align:left;border-bottom:1px solid #e0e0e0}th{background:#f8f9fa;font-weight:600}</style></head>
<body><div class="navbar"><div class="navbar-content"><h1>🔐 Admin Panel</h1><div class="nav-links">
<a href="/admin/dashboard">Dashboard</a><a href="/admin/users">Users</a><a href="/admin/appointments">Appointments</a>
<a href="/admin/logout">Logout</a></div></div></div>
<div class="container"><div class="section"><h2>Manage Users ({{users|length}} total)</h2>
<table><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Age</th><th>Gender</th><th>Blood Group</th><th>Registered</th></tr></thead><tbody>
{%for user in users%}<tr><td>{{user[0]}}</td><td>{{user[1]}}</td><td>{{user[2]}}</td><td>{{user[3]or'-'}}</td><td>{{user[4]or'-'}}</td><td>{{user[5]or'-'}}</td><td>{{user[6]or'-'}}</td><td>{{user[7]}}</td></tr>{%endfor%}</tbody></table></div></div></body></html>'''

ADMIN_APPOINTMENTS_HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Manage Appointments</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:#f5f7fa}.navbar{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:20px}.navbar-content{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}.nav-links a{color:white;text-decoration:none;margin-left:20px;padding:8px 16px;border-radius:8px}.nav-links a:hover{background:rgba(255,255,255,0.2)}.container{max-width:1200px;margin:40px auto;padding:0 20px}.section{background:white;padding:30px;border-radius:15px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}table{width:100%;border-collapse:collapse;margin-top:20px;font-size:0.9em}th,td{padding:10px;text-align:left;border-bottom:1px solid #e0e0e0}th{background:#f8f9fa;font-weight:600}.badge{padding:4px 10px;border-radius:12px;font-size:0.85em}.pending{background:#fff3cd;color:#856404}.confirmed{background:#d4edda;color:#155724}.completed{background:#d1ecf1;color:#0c5460}</style></head>
<body><div class="navbar"><div class="navbar-content"><h1>🔐 Admin Panel</h1><div class="nav-links">
<a href="/admin/dashboard">Dashboard</a><a href="/admin/users">Users</a><a href="/admin/appointments">Appointments</a>
<a href="/admin/logout">Logout</a></div></div></div>
<div class="container"><div class="section"><h2>Manage Appointments ({{appointments|length}} total)</h2>
<table><thead><tr><th>ID</th><th>Patient</th><th>Email</th><th>Doctor</th><th>Specialty</th><th>Date</th><th>Time</th><th>Status</th><th>Symptoms</th></tr></thead><tbody>
{%for apt in appointments%}<tr><td>{{apt[0]}}</td><td>{{apt[1]}}</td><td>{{apt[2]}}</td><td>{{apt[3]}}</td><td>{{apt[4]}}</td><td>{{apt[5]}}</td><td>{{apt[6]}}</td><td><span class="badge {{apt[7]}}">{{apt[7]}}</span></td><td>{{apt[8]or'-'}}</td></tr>{%endfor%}</tbody></table></div></div></body></html>'''

MEDICAL_RECORDS_HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Medical Records</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:#f5f7fa}.navbar{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:20px}.navbar-content{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}.nav-links a{color:white;text-decoration:none;margin-left:20px;padding:8px 16px;border-radius:8px}.nav-links a:hover{background:rgba(255,255,255,0.2)}.container{max-width:1200px;margin:40px auto;padding:0 20px}.section{background:white;padding:30px;border-radius:15px;box-shadow:0 2px 10px rgba(0,0,0,0.1);margin-bottom:20px}.record-card{padding:20px;background:#f8f9fa;border-radius:10px;margin-bottom:15px;border-left:4px solid #667eea}.record-card h4{color:#667eea;margin-bottom:10px}.record-card p{color:#666;margin:5px 0}</style></head>
<body><div class="navbar"><div class="navbar-content"><h1>🏥 Medical Records</h1><div class="nav-links">
<a href="/dashboard">Dashboard</a><a href="/chat">Chat</a><a href="/appointments">Appointments</a>
<a href="/medical-records">Records</a><a href="/prescriptions">Prescriptions</a><a href="/lab-reports">Lab Reports</a>
<a href="/vital-signs">Vitals</a><a href="/logout">Logout</a></div></div></div>
<div class="container"><div class="section"><h2>Your Medical Records</h2>
{%if records%}{%for rec in records%}<div class="record-card"><h4>{{rec[2]}} ({{rec[1]}})</h4>
<p><strong>Date:</strong> {{rec[5]}}</p><p><strong>Doctor:</strong> {{rec[4]or'N/A'}}</p>
<p><strong>Description:</strong> {{rec[3]or'No description'}}</p></div>{%endfor%}
{%else%}<p style="color:#666">No medical records found.</p>{%endif%}</div></div></body></html>'''

PRESCRIPTIONS_HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Prescriptions</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:#f5f7fa}.navbar{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:20px}.navbar-content{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}.nav-links a{color:white;text-decoration:none;margin-left:20px;padding:8px 16px;border-radius:8px}.nav-links a:hover{background:rgba(255,255,255,0.2)}.container{max-width:1200px;margin:40px auto;padding:0 20px}.section{background:white;padding:30px;border-radius:15px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}.prescription-card{padding:20px;background:#f8f9fa;border-radius:10px;margin-bottom:15px;border-left:4px solid #28a745}.prescription-card h4{color:#28a745;margin-bottom:10px}.prescription-card p{color:#666;margin:5px 0}.status-badge{padding:4px 10px;border-radius:12px;font-size:0.85em}.active{background:#d4edda;color:#155724}.expired{background:#f8d7da;color:#721c24}</style></head>
<body><div class="navbar"><div class="navbar-content"><h1>💊 Prescriptions</h1><div class="nav-links">
<a href="/dashboard">Dashboard</a><a href="/chat">Chat</a><a href="/appointments">Appointments</a>
<a href="/medical-records">Records</a><a href="/prescriptions">Prescriptions</a><a href="/lab-reports">Lab Reports</a>
<a href="/vital-signs">Vitals</a><a href="/logout">Logout</a></div></div></div>
<div class="container"><div class="section"><h2>Your Prescriptions</h2>
{%if prescriptions%}{%for rx in prescriptions%}<div class="prescription-card">
<h4>{{rx[2]}} <span class="status-badge {{rx[8]}}">{{rx[8]}}</span></h4>
<p><strong>Doctor:</strong> {{rx[1]}}</p><p><strong>Dosage:</strong> {{rx[3]}}</p>
<p><strong>Frequency:</strong> {{rx[4]}}</p><p><strong>Duration:</strong> {{rx[5]}}</p>
<p><strong>Instructions:</strong> {{rx[6]or'Take as directed'}}</p>
<p><strong>Prescribed:</strong> {{rx[7]}}</p></div>{%endfor%}
{%else%}<p style="color:#666">No prescriptions found.</p>{%endif%}</div></div></body></html>'''

LAB_REPORTS_HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Lab Reports</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:#f5f7fa}.navbar{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:20px}.navbar-content{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}.nav-links a{color:white;text-decoration:none;margin-left:20px;padding:8px 16px;border-radius:8px}.nav-links a:hover{background:rgba(255,255,255,0.2)}.container{max-width:1200px;margin:40px auto;padding:0 20px}.section{background:white;padding:30px;border-radius:15px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}table{width:100%;border-collapse:collapse;margin-top:20px}th,td{padding:12px;text-align:left;border-bottom:1px solid #e0e0e0}th{background:#f8f9fa;font-weight:600}.normal{color:#28a745}.abnormal{color:#dc3545}</style></head>
<body><div class="navbar"><div class="navbar-content"><h1>🔬 Lab Reports</h1><div class="nav-links">
<a href="/dashboard">Dashboard</a><a href="/chat">Chat</a><a href="/appointments">Appointments</a>
<a href="/medical-records">Records</a><a href="/prescriptions">Prescriptions</a><a href="/lab-reports">Lab Reports</a>
<a href="/vital-signs">Vitals</a><a href="/logout">Logout</a></div></div></div>
<div class="container"><div class="section"><h2>Your Lab Reports</h2>
{%if reports%}<table><thead><tr><th>Test Name</th><th>Type</th><th>Result</th><th>Reference Range</th><th>Status</th><th>Date</th></tr></thead><tbody>
{%for rep in reports%}<tr><td>{{rep[1]}}</td><td>{{rep[2]}}</td><td>{{rep[3]}}</td><td>{{rep[4]or'N/A'}}</td><td class="{{rep[5]or'normal'}}">{{rep[5]or'Normal'}}</td><td>{{rep[6]}}</td></tr>{%endfor%}</tbody></table>
{%else%}<p style="color:#666">No lab reports found.</p>{%endif%}</div></div></body></html>'''

VITAL_SIGNS_HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Vital Signs</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:#f5f7fa}.navbar{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:20px}.navbar-content{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}.nav-links a{color:white;text-decoration:none;margin-left:20px;padding:8px 16px;border-radius:8px}.nav-links a:hover{background:rgba(255,255,255,0.2)}.container{max-width:1200px;margin:40px auto;padding:0 20px}.section{background:white;padding:30px;border-radius:15px;box-shadow:0 2px 10px rgba(0,0,0,0.1);margin-bottom:20px}.form-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin-bottom:20px}.form-group{margin-bottom:15px}.form-group label{display:block;color:#333;margin-bottom:5px;font-weight:500}.form-group input{width:100%;padding:10px;border:2px solid #e0e0e0;border-radius:8px}.btn{padding:12px 30px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;border-radius:8px;font-size:1em;font-weight:bold;cursor:pointer}table{width:100%;border-collapse:collapse;margin-top:20px}th,td{padding:12px;text-align:left;border-bottom:1px solid #e0e0e0}th{background:#f8f9fa;font-weight:600}</style></head>
<body><div class="navbar"><div class="navbar-content"><h1>📈 Vital Signs</h1><div class="nav-links">
<a href="/dashboard">Dashboard</a><a href="/chat">Chat</a><a href="/appointments">Appointments</a>
<a href="/medical-records">Records</a><a href="/prescriptions">Prescriptions</a><a href="/lab-reports">Lab Reports</a>
<a href="/vital-signs">Vitals</a><a href="/logout">Logout</a></div></div></div>
<div class="container"><div class="section"><h2>Record Vital Signs</h2>
<form id="vitalForm"><div class="form-grid"><div class="form-group"><label>Blood Pressure</label><input type="text" id="bp" placeholder="120/80"></div>
<div class="form-group"><label>Heart Rate (bpm)</label><input type="number" id="hr" placeholder="75"></div>
<div class="form-group"><label>Temperature (°F)</label><input type="number" step="0.1" id="temp" placeholder="98.6"></div>
<div class="form-group"><label>Weight (lbs)</label><input type="number" step="0.1" id="weight" placeholder="150"></div>
<div class="form-group"><label>BMI</label><input type="number" step="0.1" id="bmi" placeholder="22.5"></div>
<div class="form-group"><label>Date</label><input type="date" id="date" required></div></div>
<button type="submit" class="btn">Record Vitals</button></form></div>
<div class="section"><h2>Your Vital Signs History</h2>
{%if vitals%}<table><thead><tr><th>Date</th><th>BP</th><th>HR</th><th>Temp</th><th>Weight</th><th>BMI</th></tr></thead><tbody>
{%for v in vitals%}<tr><td>{{v[6]}}</td><td>{{v[1]or'-'}}</td><td>{{v[2]or'-'}}</td><td>{{v[3]or'-'}}</td><td>{{v[4]or'-'}}</td><td>{{v[5]or'-'}}</td></tr>{%endfor%}</tbody></table>
{%else%}<p style="color:#666">No vital signs recorded yet.</p>{%endif%}</div></div>
<script>document.getElementById('date').value=new Date().toISOString().split('T')[0];document.getElementById('vitalForm').addEventListener('submit',async function(e){e.preventDefault();const data={blood_pressure:document.getElementById('bp').value,heart_rate:document.getElementById('hr').value,temperature:document.getElementById('temp').value,weight:document.getElementById('weight').value,bmi:document.getElementById('bmi').value,recorded_date:document.getElementById('date').value};try{const response=await fetch('/api/vital-signs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const result=await response.json();if(result.success){alert('Vital signs recorded!');location.reload()}else{alert('Failed to record')}}catch(error){alert('Error recording vital signs')}});</script></body></html>'''
