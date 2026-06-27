"""
Flask Backend API for AI Healthcare Chatbot
Modern web application with REST API endpoints
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

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['DATABASE'] = 'healthcare.db'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database initialization
def init_db():
    """Initialize database with all tables"""
    conn = sqlite3.connect(app.config['DATABASE'])
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
    
    # Create default admin user
    try:
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("""
            INSERT INTO users (username, password_hash, email, full_name, role)
            VALUES (?, ?, ?, ?, ?)
        """, ("admin", password_hash, "admin@healthcare.com", "Admin User", "admin"))
    except:
        pass  # Admin already exists
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Authentication Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login')
def login_page():
    """Login page"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html')

@app.route('/appointments')
def appointments_page():
    """Appointments page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('appointments.html')

@app.route('/prescriptions')
def prescriptions_page():
    """Prescriptions page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('prescriptions.html')

@app.route('/vital-signs')
def vital_signs_page():
    """Vital Signs page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('vital_signs.html')

@app.route('/lab-reports')
def lab_reports_page():
    """Lab Reports page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('lab_reports.html')

@app.route('/chat')
def chat_page():
    """AI Chat page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('chat.html')

@app.route('/profile')
def profile_page():
    """Profile page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('profile.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    """Login API endpoint"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password_hash = ? AND is_active = 1',
        (username, password_hash)
    ).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['full_name'] = user['full_name']
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'full_name': user['full_name'],
                'role': user['role']
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    """Registration API endpoint"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    full_name = data.get('full_name')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password_hash, email, full_name, role) VALUES (?, ?, ?, ?, ?)',
            (username, password_hash, email, full_name, 'patient')
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'success': True, 'message': 'Registration successful', 'user_id': user_id})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Username already exists'}), 409

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Logout API endpoint"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# Patient Routes
@app.route('/api/patients', methods=['GET', 'POST'])
def api_patients():
    """Get all patients or create new patient"""
    if request.method == 'GET':
        conn = get_db()
        patients = conn.execute('SELECT * FROM patients ORDER BY created_at DESC').fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'patients': [dict(p) for p in patients]
        })
    
    elif request.method == 'POST':
        data = request.json
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO patients (user_id, name, age, gender, phone, email, blood_group, allergies, chronic_conditions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.get('user_id'),
                data.get('name'),
                data.get('age'),
                data.get('gender'),
                data.get('phone'),
                data.get('email'),
                data.get('blood_group'),
                data.get('allergies'),
                data.get('chronic_conditions')
            ))
            conn.commit()
            patient_id = cursor.lastrowid
            conn.close()
            
            return jsonify({'success': True, 'message': 'Patient created', 'patient_id': patient_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['GET', 'PUT', 'DELETE'])
def api_patient_detail(patient_id):
    """Get, update, or delete specific patient"""
    if request.method == 'GET':
        conn = get_db()
        patient = conn.execute('SELECT * FROM patients WHERE id = ?', (patient_id,)).fetchone()
        conn.close()
        
        if patient:
            return jsonify({'success': True, 'patient': dict(patient)})
        else:
            return jsonify({'success': False, 'message': 'Patient not found'}), 404

@app.route('/api/appointments', methods=['GET', 'POST'])
def api_appointments():
    """Get all appointments or create new appointment"""
    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        
        conn = get_db()
        if patient_id:
            appointments = conn.execute(
                'SELECT * FROM appointments WHERE patient_id = ? ORDER BY appointment_date DESC',
                (patient_id,)
            ).fetchall()
        else:
            appointments = conn.execute(
                'SELECT * FROM appointments ORDER BY appointment_date DESC'
            ).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'appointments': [dict(a) for a in appointments]
        })
    
    elif request.method == 'POST':
        data = request.json
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_name, specialty, appointment_date, appointment_time, symptoms, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('patient_id'),
                data.get('doctor_name'),
                data.get('specialty'),
                data.get('appointment_date'),
                data.get('appointment_time'),
                data.get('symptoms'),
                data.get('status', 'Scheduled')
            ))
            conn.commit()
            appointment_id = cursor.lastrowid
            conn.close()
            
            return jsonify({'success': True, 'message': 'Appointment booked', 'appointment_id': appointment_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/prescriptions', methods=['GET', 'POST'])
def api_prescriptions():
    """Get all prescriptions or create new prescription"""
    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        
        conn = get_db()
        if patient_id:
            prescriptions = conn.execute(
                'SELECT * FROM prescriptions WHERE patient_id = ? ORDER BY created_at DESC',
                (patient_id,)
            ).fetchall()
        else:
            prescriptions = conn.execute(
                'SELECT * FROM prescriptions ORDER BY created_at DESC'
            ).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'prescriptions': [dict(p) for p in prescriptions]
        })
    
    elif request.method == 'POST':
        data = request.json
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO prescriptions (patient_id, medication_name, dosage, frequency, start_date, end_date, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('patient_id'),
                data.get('medication_name'),
                data.get('dosage'),
                data.get('frequency'),
                data.get('start_date'),
                data.get('end_date'),
                data.get('status', 'Active'),
                data.get('notes')
            ))
            conn.commit()
            prescription_id = cursor.lastrowid
            conn.close()
            
            return jsonify({'success': True, 'message': 'Prescription added', 'prescription_id': prescription_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/vital-signs', methods=['GET', 'POST'])
def api_vital_signs():
    """Get all vital signs or add new reading"""
    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        
        conn = get_db()
        if patient_id:
            vital_signs = conn.execute(
                'SELECT * FROM vital_signs WHERE patient_id = ? ORDER BY recorded_at DESC LIMIT 30',
                (patient_id,)
            ).fetchall()
        else:
            vital_signs = conn.execute(
                'SELECT * FROM vital_signs ORDER BY recorded_at DESC LIMIT 100'
            ).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'vital_signs': [dict(v) for v in vital_signs]
        })
    
    elif request.method == 'POST':
        data = request.json
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vital_signs (patient_id, blood_pressure_systolic, blood_pressure_diastolic,
                                        heart_rate, temperature, oxygen_saturation, glucose_level, weight, bmi)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('patient_id'),
                data.get('blood_pressure_systolic'),
                data.get('blood_pressure_diastolic'),
                data.get('heart_rate'),
                data.get('temperature'),
                data.get('oxygen_saturation'),
                data.get('glucose_level'),
                data.get('weight'),
                data.get('bmi')
            ))
            conn.commit()
            vital_id = cursor.lastrowid
            conn.close()
            
            return jsonify({'success': True, 'message': 'Vital signs recorded', 'vital_id': vital_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/lab-reports', methods=['GET', 'POST'])
def api_lab_reports():
    """Get all lab reports or add new report"""
    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        
        conn = get_db()
        if patient_id:
            reports = conn.execute(
                'SELECT * FROM lab_reports WHERE patient_id = ? ORDER BY test_date DESC',
                (patient_id,)
            ).fetchall()
        else:
            reports = conn.execute(
                'SELECT * FROM lab_reports ORDER BY test_date DESC'
            ).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'lab_reports': [dict(r) for r in reports]
        })
    
    elif request.method == 'POST':
        data = request.json
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO lab_reports (patient_id, test_name, test_date, result_value, normal_range, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('patient_id'),
                data.get('test_name'),
                data.get('test_date'),
                data.get('result_value'),
                data.get('normal_range'),
                data.get('status', 'Normal'),
                data.get('notes')
            ))
            conn.commit()
            report_id = cursor.lastrowid
            conn.close()
            
            return jsonify({'success': True, 'message': 'Lab report added', 'report_id': report_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/statistics')
def api_statistics():
    """Get system statistics"""
    conn = get_db()
    
    stats = {
        'total_patients': conn.execute('SELECT COUNT(*) as count FROM patients').fetchone()['count'],
        'total_appointments': conn.execute('SELECT COUNT(*) as count FROM appointments').fetchone()['count'],
        'active_prescriptions': conn.execute("SELECT COUNT(*) as count FROM prescriptions WHERE status='Active'").fetchone()['count'],
        'total_vital_records': conn.execute('SELECT COUNT(*) as count FROM vital_signs').fetchone()['count'],
        'lab_reports': conn.execute('SELECT COUNT(*) as count FROM lab_reports').fetchone()['count']
    }
    
    conn.close()
    
    return jsonify({'success': True, 'statistics': stats})

# WebSocket for real-time chat
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connected', {'data': 'Connected to AI Healthcare Chatbot'})

@socketio.on('send_message')
def handle_message(data):
    """Handle incoming chat message"""
    message = data.get('message', '')
    user_id = session.get('user_id', 'anonymous')
    
    # Save to database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_history (session_id, user_id, message, sender)
        VALUES (?, ?, ?, ?)
    """, (request.sid, user_id, message, 'user'))
    conn.commit()
    conn.close()
    
    # Simple AI response (you can integrate advanced AI here)
    ai_response = generate_ai_response(message)
    
    # Save AI response
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_history (session_id, user_id, message, sender)
        VALUES (?, ?, ?, ?)
    """, (request.sid, user_id, ai_response, 'bot'))
    conn.commit()
    conn.close()
    
    # Send response back
    emit('receive_message', {
        'message': ai_response,
        'sender': 'bot',
        'timestamp': datetime.now().strftime('%H:%M')
    })

def generate_ai_response(message):
    """Generate AI response (simplified)"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your AI Healthcare Assistant. How can I help you today?"
    elif any(word in message_lower for word in ['symptom', 'pain', 'hurt', 'sick']):
        return "I understand you're experiencing symptoms. Can you describe them in more detail? This will help me provide better guidance."
    elif any(word in message_lower for word in ['appointment', 'book', 'schedule']):
        return "I can help you book an appointment. Please go to the Appointments section to schedule with your preferred doctor."
    elif any(word in message_lower for word in ['prescription', 'medication', 'medicine']):
        return "I can help with prescription information. Check the Prescriptions section to manage your medications."
    else:
        return "I'm here to help with your healthcare needs. You can ask about symptoms, book appointments, manage prescriptions, or track your vital signs."

if __name__ == '__main__':
    # Ensure templates and static directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/img', exist_ok=True)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
