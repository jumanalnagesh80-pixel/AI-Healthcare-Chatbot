"""
AI Healthcare Chatbot - Simple Working Version for Mac M2
Author: Kiro AI Assistant
Date: June 27, 2026
Description: Complete healthcare chatbot with Flask, SQLite, AI responses
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
import os
import json

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
CORS(app)

# Database setup
DATABASE = 'healthcare_simple.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table - SIMPLE, no username required
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
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
            status TEXT DEFAULT 'scheduled',
            symptoms TEXT,
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
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_ai_response(user_message):
    """Simple AI chatbot responses for healthcare"""
    message_lower = user_message.lower()
    
    # Health condition responses
    if any(word in message_lower for word in ['fever', 'temperature', 'hot']):
        return """For fever:
        • Rest and stay hydrated
        • Take acetaminophen (Tylenol) or ibuprofen
        • Monitor temperature every 4 hours
        • Seek medical attention if fever > 103°F (39.4°C)
        • Or if fever lasts more than 3 days"""

    
    elif any(word in message_lower for word in ['headache', 'head pain', 'migraine']):
        return """For headaches:
        • Rest in a quiet, dark room
        • Apply cold compress to forehead
        • Stay hydrated - drink plenty of water
        • Take over-the-counter pain relievers
        • Avoid screens and bright lights
        • Seek doctor if severe or persistent"""
    
    elif any(word in message_lower for word in ['cough', 'cold', 'flu']):
        return """For cough/cold:
        • Get plenty of rest (7-9 hours)
        • Drink warm fluids (tea, soup, warm water)
        • Use humidifier in your room
        • Gargle with salt water
        • Take vitamin C
        • See doctor if symptoms worsen or last > 10 days"""
    
    elif any(word in message_lower for word in ['stomach', 'pain', 'ache', 'abdominal']):
        return """For stomach pain:
        • Avoid solid foods initially
        • Drink clear liquids (water, broth)
        • Try BRAT diet (Bananas, Rice, Applesauce, Toast)
        • Avoid dairy, caffeine, alcohol
        • Rest and avoid strenuous activity
        • Seek immediate care if severe, persistent, or with fever"""
    
    elif any(word in message_lower for word in ['stress', 'anxiety', 'worried', 'mental']):
        return """For stress/anxiety:
        • Practice deep breathing exercises
        • Try meditation or yoga
        • Regular physical exercise (30 min/day)
        • Maintain regular sleep schedule

        • Talk to friends/family
        • Consider professional counseling
        • Limit caffeine and alcohol"""
    
    elif any(word in message_lower for word in ['diabetes', 'blood sugar', 'glucose']):
        return """For diabetes management:
        • Monitor blood sugar regularly
        • Follow prescribed medication schedule
        • Eat balanced meals at regular times
        • Exercise regularly (consult doctor first)
        • Stay hydrated
        • Regular check-ups with your doctor"""
    
    elif any(word in message_lower for word in ['blood pressure', 'bp', 'hypertension']):
        return """For blood pressure:
        • Reduce sodium intake
        • Exercise regularly (30 minutes, 5 days/week)
        • Maintain healthy weight
        • Limit alcohol consumption
        • Manage stress effectively
        • Take medications as prescribed
        • Regular monitoring recommended"""
    
    elif any(word in message_lower for word in ['appointment', 'book', 'schedule', 'doctor']):
        return """To book an appointment:
        • Click on 'Appointments' tab
        • Select your preferred doctor and specialty
        • Choose date and time
        • Describe your symptoms
        • Confirm your booking
        
        Available specialties: General, Cardiology, Dermatology, Pediatrics, Orthopedics"""
    
    elif any(word in message_lower for word in ['hello', 'hi', 'hey']):

        return """Hello! 👋 I'm your AI Healthcare Assistant.

I can help you with:
• Health symptoms and advice
• Booking appointments
• General medical information
• Medication guidance
• Lifestyle recommendations

How can I assist you today?"""
    
    else:
        return """I'm here to help with your health concerns. I can provide information about:

• Common symptoms (fever, headache, cough, stomach pain)
• General health advice
• Booking appointments with doctors
• Managing chronic conditions (diabetes, blood pressure)
• Mental health support
• Emergency guidance

Please describe your symptoms or health concern, and I'll do my best to assist you.

⚠️ Note: This is not a substitute for professional medical advice. For emergencies, call 911 or visit the nearest hospital."""

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
    """Dashboard page - requires login"""

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
    
    return render_template_string(DASHBOARD_HTML,
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

# ==================== HTML TEMPLATES ====================


INDEX_HTML = '''
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
