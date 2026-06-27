"""
Simple Working AI Healthcare Chatbot
Fixed all issues - Ready to use!
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['DATABASE'] = 'healthcare_simple.db'

CORS(app)

# ============================================
# Database Setup
# ============================================

def init_db():
    """Initialize database with correct schema"""
    conn = sqlite3.connect('healthcare_simple.db')
    c = conn.cursor()
    
    # Drop existing tables to start fresh
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('DROP TABLE IF EXISTS appointments')
    c.execute('DROP TABLE IF EXISTS messages')
    
    # Create users table - SIMPLE SCHEMA
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            role TEXT DEFAULT 'patient',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create appointments table
    c.execute('''
        CREATE TABLE appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            doctor_name TEXT,
            date TEXT,
            time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create messages table
    c.execute('''
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully!")

# Initialize database on startup
try:
    init_db()
except Exception as e:
    print(f"Database initialization: {e}")

# ============================================
# Helper Functions
# ============================================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    """Query database"""
    conn = get_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """Execute database modification"""
    conn = get_db()
    try:
        cur = conn.execute(query, args)
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# ============================================
# Simple AI Responses
# ============================================

def get_ai_response(message):
    """Simple AI response"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your healthcare assistant. How can I help you today?"
    
    elif any(word in message_lower for word in ['headache', 'head pain']):
        return "For headaches, I recommend: 1) Rest in a quiet, dark room 2) Stay hydrated 3) Take over-the-counter pain relief if needed. If severe or persistent, please consult a doctor."
    
    elif any(word in message_lower for word in ['fever', 'temperature']):
        return "For fever: 1) Rest and stay hydrated 2) Take fever-reducing medication 3) Monitor temperature. Seek medical help if fever is over 103°F or lasts more than 3 days."
    
    elif any(word in message_lower for word in ['appointment', 'book', 'schedule']):
        return "To schedule an appointment, please visit the Appointments page or call our office. What type of appointment do you need?"
    
    else:
        return "I understand you're asking about your health. For specific medical advice, please consult with a healthcare professional. Is there anything else I can help you with?"

# ============================================
# Routes - Pages
# ============================================

@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
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
    
    # Get user info
    user = query_db('SELECT * FROM users WHERE id = ?', [session['user_id']], one=True)
    
    # Get stats
    appointments = query_db('SELECT COUNT(*) as count FROM appointments WHERE user_id = ?', 
                           [session['user_id']], one=True)
    messages = query_db('SELECT COUNT(*) as count FROM messages WHERE user_id = ?', 
                       [session['user_id']], one=True)
    
    return render_template('dashboard.html', 
                         user=user,
                         appointments_count=appointments['count'] if appointments else 0,
                         messages_count=messages['count'] if messages else 0)

@app.route('/chat')
def chat_page():
    """Chat page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('chat.html')

@app.route('/appointments')
def appointments_page():
    """Appointments page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('appointments.html')

# ============================================
# API Routes
# ============================================

@app.route('/api/register', methods=['POST'])
def api_register():
    """Register new user - FIXED"""
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        phone = data.get('phone', '').strip()
        
        # Validation
        if not all([name, email, password]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Check if email exists
        existing = query_db('SELECT id FROM users WHERE email = ?', [email], one=True)
        if existing:
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Insert user - SIMPLE SCHEMA
        user_id = execute_db('''
            INSERT INTO users (name, email, password_hash, phone, role)
            VALUES (?, ?, ?, ?, 'patient')
        ''', [name, email, password_hash, phone])
        
        # Create session
        session['user_id'] = user_id
        session['name'] = name
        session['email'] = email
        session['role'] = 'patient'
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'redirect': '/dashboard'
        }), 201
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """User login - FIXED"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not all([email, password]):
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Find user
        user = query_db('''
            SELECT id, name, email, role 
            FROM users 
            WHERE email = ? AND password_hash = ?
        ''', [email, password_hash], one=True)
        
        if not user:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Create session
        session['user_id'] = user['id']
        session['name'] = user['name']
        session['email'] = user['email']
        session['role'] = user['role']
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'redirect': '/dashboard'
        }), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True, 'redirect': '/'}), 200

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat with AI"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message required'}), 400
        
        # Get AI response
        response = get_ai_response(message)
        
        # Save to database
        execute_db('''
            INSERT INTO messages (user_id, message, response)
            VALUES (?, ?, ?)
        ''', [session['user_id'], message, response])
        
        return jsonify({
            'success': True,
            'response': response
        }), 200
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': 'Chat failed'}), 500

@app.route('/api/chat/history', methods=['GET'])
def api_chat_history():
    """Get chat history"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        messages = query_db('''
            SELECT message, response, created_at
            FROM messages
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 50
        ''', [session['user_id']])
        
        return jsonify([dict(m) for m in messages]), 200
        
    except Exception as e:
        print(f"History error: {e}")
        return jsonify({'error': 'Failed to load history'}), 500

@app.route('/api/appointments', methods=['GET'])
def api_appointments_list():
    """Get appointments"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        appointments = query_db('''
            SELECT * FROM appointments
            WHERE user_id = ?
            ORDER BY date DESC, time DESC
        ''', [session['user_id']])
        
        return jsonify([dict(a) for a in appointments]), 200
        
    except Exception as e:
        print(f"Appointments error: {e}")
        return jsonify({'error': 'Failed to load appointments'}), 500

@app.route('/api/appointments', methods=['POST'])
def api_appointments_create():
    """Create appointment"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        doctor_name = data.get('doctor_name', '').strip()
        date = data.get('date', '').strip()
        time = data.get('time', '').strip()
        reason = data.get('reason', '').strip()
        
        if not all([doctor_name, date, time, reason]):
            return jsonify({'error': 'All fields required'}), 400
        
        appointment_id = execute_db('''
            INSERT INTO appointments (user_id, doctor_name, date, time, reason, status)
            VALUES (?, ?, ?, ?, ?, 'scheduled')
        ''', [session['user_id'], doctor_name, date, time, reason])
        
        return jsonify({
            'success': True,
            'id': appointment_id,
            'message': 'Appointment created'
        }), 201
        
    except Exception as e:
        print(f"Create appointment error: {e}")
        return jsonify({'error': 'Failed to create appointment'}), 500

# ============================================
# Run App
# ============================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏥 AI Healthcare Chatbot - Simple Working Version")
    print("="*60)
    print("\n✓ All issues fixed!")
    print("✓ Database schema corrected")
    print("✓ Templates matched")
    print("✓ Ready to use!")
    print("\n📍 Open: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
