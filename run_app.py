"""
SIMPLE WORKING AI Healthcare Chatbot
All issues fixed - Just run this file!
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# ============================================
# Database Setup
# ============================================

def setup_database():
    """Setup clean database"""
    conn = sqlite3.connect('healthcare.db')
    c = conn.cursor()
    
    # Users table - SIMPLE
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Appointments table
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        doctor TEXT,
        date TEXT,
        time TEXT,
        reason TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Chat messages table
    c.execute('''CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()
    print("✓ Database ready")

setup_database()

# ============================================
# AI Chat Function
# ============================================

def get_ai_response(message):
    """Simple AI responses"""
    msg = message.lower()
    
    if 'hello' in msg or 'hi' in msg:
        return "Hello! I'm your health assistant. How can I help you today?"
    
    elif 'headache' in msg:
        return """For headaches:
• Rest in a quiet, dark room
• Stay hydrated - drink plenty of water
• Apply a cold compress to your forehead
• Take over-the-counter pain relief if needed
• If severe or persistent, consult a doctor"""
    
    elif 'fever' in msg:
        return """For fever:
• Rest and stay hydrated
• Take fever-reducing medication (acetaminophen or ibuprofen)
• Keep room temperature comfortable
• Monitor your temperature
• Seek medical attention if fever is high (103°F+) or lasts more than 3 days"""
    
    elif 'cough' in msg:
        return """For cough:
• Stay hydrated
• Use honey for soothing (for adults)
• Rest your voice
• Avoid irritants like smoke
• See a doctor if it persists or worsens"""
    
    elif 'appointment' in msg or 'book' in msg:
        return "To schedule an appointment, please go to the Appointments page. I can help answer health questions in the meantime!"
    
    else:
        return "I understand you have a health concern. For specific medical advice, please consult with a healthcare professional. Is there anything else I can help you with?"

# ============================================
# Routes
# ============================================

@app.route('/')
def home():
    """Home page"""
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    if request.method == 'POST':
        try:
            data = request.json
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            phone = data.get('phone', '')
            
            if not all([name, email, password]):
                return jsonify({'error': 'All fields required'}), 400
            
            # Check if email exists
            conn = sqlite3.connect('healthcare.db')
            c = conn.cursor()
            c.execute('SELECT id FROM users WHERE email = ?', (email,))
            if c.fetchone():
                conn.close()
                return jsonify({'error': 'Email already registered'}), 400
            
            # Insert user
            c.execute('INSERT INTO users (name, email, password, phone) VALUES (?, ?, ?, ?)',
                     (name, email, password, phone))
            user_id = c.lastrowid
            conn.commit()
            conn.close()
            
            # Set session
            session['user_id'] = user_id
            session['name'] = name
            session['email'] = email
            
            return jsonify({'success': True, 'redirect': '/dashboard'})
            
        except Exception as e:
            print(f"Registration error: {e}")
            return jsonify({'error': str(e)}), 500
    
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        try:
            data = request.json
            email = data.get('email')
            password = data.get('password')
            
            if not all([email, password]):
                return jsonify({'error': 'Email and password required'}), 400
            
            # Check credentials
            conn = sqlite3.connect('healthcare.db')
            c = conn.cursor()
            c.execute('SELECT id, name, email FROM users WHERE email = ? AND password = ?',
                     (email, password))
            user = c.fetchone()
            conn.close()
            
            if not user:
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Set session
            session['user_id'] = user[0]
            session['name'] = user[1]
            session['email'] = user[2]
            
            return jsonify({'success': True, 'redirect': '/dashboard'})
            
        except Exception as e:
            print(f"Login error: {e}")
            return jsonify({'error': str(e)}), 500
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'user_id' not in session:
        return redirect('/login')
    
    return render_template('dashboard.html', 
                         user_name=session.get('name', 'User'))

@app.route('/chat')
def chat():
    """Chat page"""
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('chat.html')

@app.route('/appointments')
def appointments():
    """Appointments page"""
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('appointments.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect('/')

# ============================================
# API Endpoints
# ============================================

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat API"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message required'}), 400
        
        # Get AI response
        response = get_ai_response(message)
        
        # Save to database
        conn = sqlite3.connect('healthcare.db')
        c = conn.cursor()
        c.execute('INSERT INTO chats (user_id, message, response) VALUES (?, ?, ?)',
                 (session['user_id'], message, response))
        conn.commit()
        conn.close()
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments', methods=['GET', 'POST'])
def api_appointments():
    """Appointments API"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        try:
            data = request.json
            doctor = data.get('doctor')
            date = data.get('date')
            time = data.get('time')
            reason = data.get('reason')
            
            if not all([doctor, date, time, reason]):
                return jsonify({'error': 'All fields required'}), 400
            
            conn = sqlite3.connect('healthcare.db')
            c = conn.cursor()
            c.execute('INSERT INTO appointments (user_id, doctor, date, time, reason) VALUES (?, ?, ?, ?, ?)',
                     (session['user_id'], doctor, date, time, reason))
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Appointment scheduled'})
            
        except Exception as e:
            print(f"Appointment error: {e}")
            return jsonify({'error': str(e)}), 500
    
    else:  # GET
        try:
            conn = sqlite3.connect('healthcare.db')
            c = conn.cursor()
            c.execute('SELECT id, doctor, date, time, reason FROM appointments WHERE user_id = ? ORDER BY date DESC',
                     (session['user_id'],))
            appointments = []
            for row in c.fetchall():
                appointments.append({
                    'id': row[0],
                    'doctor': row[1],
                    'date': row[2],
                    'time': row[3],
                    'reason': row[4]
                })
            conn.close()
            
            return jsonify(appointments)
            
        except Exception as e:
            print(f"Get appointments error: {e}")
            return jsonify({'error': str(e)}), 500

# ============================================
# Run App
# ============================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🏥 AI Healthcare Chatbot - WORKING VERSION")
    print("="*70)
    print("\n✅ All issues fixed!")
    print("✅ Simple database (no username)")
    print("✅ Working registration")
    print("✅ Working login")
    print("✅ Working chat")
    print("✅ Working appointments")
    print("\n📍 Open your browser: http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
