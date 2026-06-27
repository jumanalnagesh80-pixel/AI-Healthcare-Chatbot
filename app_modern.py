"""
HealthAI - Modern AI Healthcare Chatbot Backend v3.0
Complete redesign with OpenAI integration, WebSocket chat, and Admin Panel
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
import json
import os
import re
from functools import wraps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['DATABASE'] = 'healthcare_enhanced.db'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')  # Set via environment variable

CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

# OpenAI Integration (optional - falls back to local AI if not configured)
try:
    if app.config['OPENAI_API_KEY']:
        import openai
        openai.api_key = app.config['OPENAI_API_KEY']
        OPENAI_ENABLED = True
        logger.info("OpenAI integration enabled")
    else:
        OPENAI_ENABLED = False
        logger.info("OpenAI not configured, using local AI")
except ImportError:
    OPENAI_ENABLED = False
    logger.warning("OpenAI package not installed, using local AI")

# ============================================
# Database Helper Functions
# ============================================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    """Query the database"""
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
# Authentication Decorator
# ============================================

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        user = query_db('SELECT role FROM users WHERE id = ?', [session['user_id']], one=True)
        if not user or user['role'] != 'admin':
            return jsonify({'error': 'Forbidden - Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

# ============================================
# Enhanced AI Engine with OpenAI
# ============================================

MEDICAL_INTENTS = {
    'symptom_check': {
        'keywords': ['symptom', 'feel', 'pain', 'hurt', 'ache', 'sick', 'ill', 'fever', 'cough', 'headache'],
        'response': 'I understand you\'re experiencing symptoms. Can you describe them in more detail? When did they start?'
    },
    'medication_info': {
        'keywords': ['medicine', 'medication', 'drug', 'pill', 'prescription', 'dose', 'dosage'],
        'response': 'I can help with medication information. Which medication would you like to know about?'
    },
    'appointment': {
        'keywords': ['appointment', 'book', 'schedule', 'doctor', 'visit', 'consultation'],
        'response': 'I can help you schedule an appointment. Would you like to book one now?'
    },
    'health_tips': {
        'keywords': ['tip', 'advice', 'healthy', 'wellness', 'improve', 'better', 'diet', 'exercise'],
        'response': 'I\'d be happy to share health tips! What area are you interested in?'
    },
    'emergency': {
        'keywords': ['emergency', 'urgent', 'severe', 'chest pain', 'can\'t breathe', 'bleeding', 'unconscious'],
        'response': '⚠️ THIS SOUNDS LIKE AN EMERGENCY! Please call 911 or go to the nearest emergency room immediately!'
    }
}

MEDICAL_KNOWLEDGE = {
    'symptoms': {
        'fever': {
            'info': 'Elevated body temperature, often indicating infection',
            'advice': 'Rest, drink fluids, monitor temperature. Seek help if over 103°F or lasting 3+ days.',
            'severity': 'moderate'
        },
        'headache': {
            'info': 'Pain in the head or face region',
            'advice': 'Rest, hydrate, try OTC pain relief. See doctor if severe or persistent.',
            'severity': 'low'
        },
        'chest pain': {
            'info': 'Discomfort in the chest area - could be serious',
            'advice': '⚠️ SEEK IMMEDIATE MEDICAL ATTENTION! Call 911 if severe.',
            'severity': 'critical'
        },
        'cough': {
            'info': 'Reflex to clear airways',
            'advice': 'Rest, hydrate, use honey. See doctor if persistent 2+ weeks or with blood.',
            'severity': 'low'
        }
    },
    'medications': {
        'aspirin': 'Pain reliever, fever reducer, blood thinner. Take with food.',
        'ibuprofen': 'Anti-inflammatory pain reliever. Reduces fever and inflammation.',
        'acetaminophen': 'Pain reliever and fever reducer. Gentler on stomach.',
        'metformin': 'Diabetes medication. Take with meals.',
        'lisinopril': 'Blood pressure medication. Take at same time daily.'
    },
    'health_tips': [
        'Drink 8 glasses of water daily for optimal hydration',
        'Get 7-9 hours of quality sleep each night',
        'Exercise 30 minutes daily, 5 days a week',
        'Eat a balanced diet rich in fruits and vegetables',
        'Practice stress management through meditation',
        'Wash hands frequently to prevent infections',
        'Schedule regular health checkups',
        'Maintain healthy weight through diet and exercise',
        'Avoid smoking and limit alcohol consumption',
        'Practice good oral hygiene'
    ]
}

def detect_intent(message):
    """Detect user intent from message"""
    message_lower = message.lower()
    
    for intent, data in MEDICAL_INTENTS.items():
        if any(keyword in message_lower for keyword in data['keywords']):
            return intent
    
    return 'general'

def get_local_ai_response(message, intent):
    """Generate response using local AI logic"""
    message_lower = message.lower()
    
    # Emergency detection
    if intent == 'emergency':
        return {
            'response': '⚠️ **MEDICAL EMERGENCY DETECTED!**\n\nPlease call 911 or go to the nearest emergency room immediately!\n\nDo not wait for symptoms to worsen. Your safety is the priority.',
            'intent': intent,
            'confidence': 0.95,
            'suggestions': ['Call 911', 'Go to ER', 'Contact emergency services']
        }
    
    # Symptom checking
    if intent == 'symptom_check':
        for symptom, info in MEDICAL_KNOWLEDGE['symptoms'].items():
            if symptom in message_lower:
                return {
                    'response': f"**About {symptom.title()}:**\n\n{info['info']}\n\n**Recommendation:** {info['advice']}\n\nWould you like to schedule an appointment or learn more?",
                    'intent': intent,
                    'confidence': 0.85,
                    'suggestions': ['Book Appointment', 'More Information', 'Other Symptoms']
                }
        
        return {
            'response': "I'd like to help you with your symptoms. Can you describe what you're experiencing? Include:\n- What symptoms you have\n- When they started\n- How severe they are (1-10)\n- Any other relevant details",
            'intent': intent,
            'confidence': 0.7,
            'suggestions': ['Describe Symptoms', 'Book Appointment']
        }
    
    # Medication information
    if intent == 'medication_info':
        for med, info in MEDICAL_KNOWLEDGE['medications'].items():
            if med in message_lower:
                return {
                    'response': f"**{med.title()} Information:**\n\n{info}\n\n*Note: Always follow your doctor's instructions and read the medication guide.*",
                    'intent': intent,
                    'confidence': 0.85,
                    'suggestions': ['Side Effects', 'Dosage Info', 'Ask Doctor']
                }
        
        return {
            'response': "I can provide information about medications. Which medication would you like to know about?\n\nPlease note: Always consult your healthcare provider for personalized medical advice.",
            'intent': intent,
            'confidence': 0.7,
            'suggestions': ['Common Medications', 'My Prescriptions']
        }
    
    # Health tips
    if intent == 'health_tips':
        import random
        tips = random.sample(MEDICAL_KNOWLEDGE['health_tips'], 3)
        return {
            'response': f"**Here are some health tips for you:**\n\n• {tips[0]}\n• {tips[1]}\n• {tips[2]}\n\nWould you like more personalized health advice?",
            'intent': intent,
            'confidence': 0.8,
            'suggestions': ['More Tips', 'Personalized Plan', 'Track Health']
        }
    
    # Appointment booking
    if intent == 'appointment':
        return {
            'response': "I can help you schedule an appointment! \n\nYou can:\n• Book a new appointment\n• View upcoming appointments\n• Reschedule existing appointments\n\nWould you like to proceed with booking?",
            'intent': intent,
            'confidence': 0.85,
            'suggestions': ['Book Now', 'View Appointments', 'Find Doctor']
        }
    
    # General conversation
    return {
        'response': "I'm your AI health assistant. I can help you with:\n\n• **Symptom checking** and health advice\n• **Medication** information\n• **Appointment** scheduling\n• **Health tips** and wellness guidance\n• **Vital signs** tracking\n\nHow can I assist you today?",
        'intent': 'general',
        'confidence': 0.6,
        'suggestions': ['Check Symptoms', 'Book Appointment', 'Health Tips', 'Track Vitals']
    }

async def get_openai_response(message, user_context=None):
    """Generate response using OpenAI GPT"""
    try:
        system_prompt = """You are HealthAI, an intelligent and empathetic healthcare assistant. 

Your role is to:
- Provide accurate health information and guidance
- Help users understand symptoms and when to seek medical care
- Offer general wellness advice and health tips
- Assist with medication information (always note to consult healthcare provider)
- Recognize medical emergencies and advise immediate action

Guidelines:
- Be professional, clear, and compassionate
- Always recommend professional medical evaluation for serious concerns
- Never diagnose conditions - only provide general information
- Recognize emergencies (chest pain, difficulty breathing, severe bleeding) and urge immediate medical attention
- Keep responses concise but informative
- Include markdown formatting for better readability

Remember: You supplement, not replace, professional healthcare."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        # Add context if available
        if user_context:
            context_msg = f"User context: {json.dumps(user_context)}"
            messages.insert(1, {"role": "system", "content": context_msg})
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        intent = detect_intent(message)
        
        return {
            'response': ai_response,
            'intent': intent,
            'confidence': 0.9,
            'suggestions': generate_suggestions(intent),
            'source': 'openai'
        }
    
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        # Fallback to local AI
        return None

def generate_suggestions(intent):
    """Generate contextual suggestions"""
    suggestions_map = {
        'symptom_check': ['Book Appointment', 'More Info', 'Track Symptoms'],
        'medication_info': ['View Prescriptions', 'Set Reminder', 'Ask Doctor'],
        'appointment': ['Book Now', 'View Schedule', 'Find Doctor'],
        'health_tips': ['Create Goal', 'Track Progress', 'More Tips'],
        'emergency': ['Call 911', 'Find ER', 'Emergency Contacts'],
        'general': ['Check Symptoms', 'Book Appointment', 'Health Dashboard']
    }
    return suggestions_map.get(intent, ['Help', 'Dashboard', 'Contact Support'])

# ============================================
# Routes - Modern Templates
# ============================================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index_enhanced.html')

@app.route('/login')
def login():
    """Login/Register page"""
    return render_template('login_enhanced.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page"""
    return render_template('dashboard_enhanced.html')

@app.route('/chat')
@login_required
def chat():
    """AI Chat page"""
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
    return render_template('prescriptions_modern.html')

@app.route('/vital-signs')
@login_required
def vital_signs():
    """Vital signs page"""
    return render_template('vital_signs_modern.html')

@app.route('/lab-reports')
@login_required
def lab_reports():
    """Lab reports page"""
    return render_template('lab_reports_modern.html')

@app.route('/health-goals')
@login_required
def health_goals():
    """Health goals page"""
    return render_template('health_goals_modern.html')

@app.route('/admin')
@admin_required
def admin_panel():
    """Admin panel page"""
    return render_template('admin_modern.html')

# ============================================
# Authentication API
# ============================================

@app.route('/api/register', methods=['POST'])
def api_register():
    """Register new user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        
        if not all([email, password, full_name]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate username from email (required by database)
        username = email.split('@')[0]
        
        # Check if username exists
        existing_username = query_db('SELECT id FROM users WHERE username = ?', [username], one=True)
        if existing_username:
            # Make username unique by adding number
            counter = 1
            while existing_username:
                new_username = f"{username}{counter}"
                existing_username = query_db('SELECT id FROM users WHERE username = ?', [new_username], one=True)
                counter += 1
            username = new_username
        
        # Check if user exists
        existing = query_db('SELECT id FROM users WHERE email = ?', [email], one=True)
        if existing:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Create user - NOW INCLUDING USERNAME
        user_id = execute_db(
            'INSERT INTO users (username, email, password_hash, full_name, role, created_at) VALUES (?, ?, ?, ?, ?, ?)',
            [username, email, password_hash, full_name, 'patient', datetime.now()]
        )
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user_id': user_id,
            'username': username
        }), 201
    
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """User login"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'error': 'Missing credentials'}), 400
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = query_db(
            'SELECT id, full_name, email, role FROM users WHERE email = ? AND password_hash = ?',
            [email, password_hash],
            one=True
        )
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create session
        session.permanent = True
        session['user_id'] = user['id']
        session['user_name'] = user['full_name']
        session['user_role'] = user['role']
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'name': user['full_name'],
                'email': user['email'],
                'role': user['role']
            }
        })
    
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """User logout"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/check-auth', methods=['GET'])
def api_check_auth():
    """Check if user is authenticated"""
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'name': session.get('user_name'),
                'role': session.get('user_role', 'patient')
            }
        })
    return jsonify({'authenticated': False}), 401

# ============================================
# Chat API with OpenAI Integration
# ============================================

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """Handle chat message and generate AI response"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        user_id = session['user_id']
        
        # Get user context for better responses
        user_context = {
            'user_id': user_id,
            'recent_vitals': None,  # Could fetch recent vital signs
            'active_prescriptions': None  # Could fetch active prescriptions
        }
        
        # Try OpenAI first, fallback to local AI
        ai_response = None
        if OPENAI_ENABLED:
            try:
                import asyncio
                ai_response = asyncio.run(get_openai_response(message, user_context))
            except Exception as e:
                logger.warning(f"OpenAI failed, using local AI: {e}")
        
        if not ai_response:
            intent = detect_intent(message)
            ai_response = get_local_ai_response(message, intent)
        
        # Save chat history
        execute_db(
            'INSERT INTO chat_history (user_id, user_message, bot_response, intent, timestamp) VALUES (?, ?, ?, ?, ?)',
            [user_id, message, ai_response['response'], ai_response['intent'], datetime.now()]
        )
        
        return jsonify({
            'success': True,
            'response': ai_response['response'],
            'intent': ai_response['intent'],
            'confidence': ai_response.get('confidence', 0.8),
            'suggestions': ai_response.get('suggestions', []),
            'source': ai_response.get('source', 'local')
        })
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': 'Failed to process message'}), 500

@app.route('/api/chat/history', methods=['GET'])
@login_required
def api_chat_history():
    """Get chat history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        user_id = session['user_id']
        
        history = query_db(
            'SELECT * FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
            [user_id, limit]
        )
        
        return jsonify({
            'success': True,
            'history': [dict(row) for row in history]
        })
    
    except Exception as e:
        logger.error(f"Chat history error: {e}")
        return jsonify({'error': 'Failed to fetch history'}), 500

# ============================================
# WebSocket Handlers - Fixed Implementation
# ============================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f'Client connected: {request.sid}')
    emit('connected', {
        'message': 'Connected to HealthAI Assistant',
        'sid': request.sid,
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f'Client disconnected: {request.sid}')

@socketio.on('join_chat')
def handle_join_chat(data):
    """Join user's chat room"""
    user_id = data.get('user_id')
    if user_id:
        room = f'user_{user_id}'
        join_room(room)
        logger.info(f'User {user_id} joined room {room}')
        emit('joined_chat', {'room': room})

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle incoming chat message via WebSocket"""
    try:
        message = data.get('message', '').strip()
        user_id = data.get('user_id')
        
        if not message:
            emit('chat_error', {'error': 'Empty message'})
            return
        
        logger.info(f'Received message from user {user_id}: {message[:50]}...')
        
        # Detect intent
        intent = detect_intent(message)
        
        # Generate response
        ai_response = None
        if OPENAI_ENABLED:
            try:
                import asyncio
                ai_response = asyncio.run(get_openai_response(message))
            except Exception as e:
                logger.warning(f"OpenAI failed in WebSocket: {e}")
        
        if not ai_response:
            ai_response = get_local_ai_response(message, intent)
        
        # Save to database if user_id provided
        if user_id:
            try:
                execute_db(
                    'INSERT INTO chat_history (user_id, user_message, bot_response, intent, timestamp) VALUES (?, ?, ?, ?, ?)',
                    [user_id, message, ai_response['response'], ai_response['intent'], datetime.now()]
                )
            except Exception as e:
                logger.error(f"Failed to save chat: {e}")
        
        # Send response back
        emit('chat_response', {
            'message': ai_response['response'],
            'intent': ai_response['intent'],
            'confidence': ai_response.get('confidence', 0.8),
            'suggestions': ai_response.get('suggestions', []),
            'timestamp': datetime.now().isoformat(),
            'source': ai_response.get('source', 'local')
        })
        
        logger.info(f'Sent response to user {user_id}')
    
    except Exception as e:
        logger.error(f"WebSocket chat error: {e}")
        emit('chat_error', {'error': str(e)})

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    user_id = data.get('user_id')
    is_typing = data.get('is_typing', False)
    
    if user_id:
        room = f'user_{user_id}'
        emit('user_typing', {'is_typing': is_typing}, room=room, skip_sid=request.sid)

# ============================================
# Dashboard API
# ============================================

@app.route('/api/dashboard/stats', methods=['GET'])
@login_required
def api_dashboard_stats():
    """Get dashboard statistics"""
    try:
        user_id = session['user_id']
        
        # Get counts
        appointments_count = query_db(
            'SELECT COUNT(*) as count FROM appointments WHERE user_id = ?',
            [user_id], one=True
        )['count']
        
        prescriptions_count = query_db(
            'SELECT COUNT(*) as count FROM prescriptions WHERE user_id = ? AND status = "active"',
            [user_id], one=True
        )['count']
        
        vital_signs_count = query_db(
            'SELECT COUNT(*) as count FROM vital_signs WHERE user_id = ?',
            [user_id], one=True
        )['count']
        
        lab_reports_count = query_db(
            'SELECT COUNT(*) as count FROM lab_reports WHERE user_id = ?',
            [user_id], one=True
        )['count']
        
        # Get health goals count
        goals_count = query_db(
            'SELECT COUNT(*) as count FROM health_goals WHERE user_id = ? AND status = "active"',
            [user_id], one=True
        )
        goals_count = goals_count['count'] if goals_count else 0
        
        return jsonify({
            'success': True,
            'total_appointments': appointments_count,
            'active_prescriptions': prescriptions_count,
            'vital_signs_count': vital_signs_count,
            'lab_reports': lab_reports_count,
            'health_goals': goals_count,
            'health_score': 85  # Placeholder - could calculate based on various factors
        })
    
    except Exception as e:
        logger.error(f"Dashboard stats error: {e}")
        return jsonify({'error': 'Failed to fetch stats'}), 500

# Continue with rest of API endpoints...
# (Appointments, Prescriptions, Vital Signs, Lab Reports, Health Goals, Admin)

if __name__ == '__main__':
    logger.info("Starting HealthAI Modern Backend v3.0")
    logger.info(f"OpenAI Integration: {'Enabled' if OPENAI_ENABLED else 'Disabled (using local AI)'}")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)


# ============================================
# Health Goals API
# ============================================

@app.route('/api/health-goals', methods=['GET'])
@login_required
def api_get_health_goals():
    """Get user's health goals"""
    try:
        user_id = session['user_id']
        
        goals = query_db(
            '''SELECT * FROM health_goals 
               WHERE user_id = ? 
               ORDER BY created_at DESC''',
            [user_id]
        )
        
        return jsonify({
            'success': True,
            'goals': [dict(row) for row in goals]
        })
    
    except Exception as e:
        logger.error(f"Error fetching health goals: {e}")
        return jsonify({'error': 'Failed to fetch health goals'}), 500

@app.route('/api/health-goals', methods=['POST'])
@login_required
def api_create_health_goal():
    """Create a new health goal"""
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        required_fields = ['goal_type', 'title', 'target_value', 'unit', 'target_date']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        goal_id = execute_db(
            '''INSERT INTO health_goals 
               (user_id, goal_type, title, description, target_value, current_value, 
                unit, start_date, target_date, status, priority, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            [
                user_id,
                data['goal_type'],
                data['title'],
                data.get('description', ''),
                data['target_value'],
                data.get('current_value', 0),
                data['unit'],
                datetime.now().strftime('%Y-%m-%d'),
                data['target_date'],
                data.get('status', 'active'),
                data.get('priority', 'medium'),
                datetime.now()
            ]
        )
        
        return jsonify({
            'success': True,
            'message': 'Health goal created successfully',
            'goal_id': goal_id
        }), 201
    
    except Exception as e:
        logger.error(f"Error creating health goal: {e}")
        return jsonify({'error': 'Failed to create health goal'}), 500

@app.route('/api/health-goals/<int:goal_id>', methods=['PUT'])
@login_required
def api_update_health_goal(goal_id):
    """Update a health goal"""
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Verify goal belongs to user
        goal = query_db(
            'SELECT id FROM health_goals WHERE id = ? AND user_id = ?',
            [goal_id, user_id],
            one=True
        )
        
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        # Build update query dynamically
        update_fields = []
        update_values = []
        
        allowed_fields = ['title', 'description', 'current_value', 'target_value', 
                         'status', 'priority', 'target_date']
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f'{field} = ?')
                update_values.append(data[field])
        
        if not update_fields:
            return jsonify({'error': 'No fields to update'}), 400
        
        update_fields.append('updated_at = ?')
        update_values.append(datetime.now())
        update_values.append(goal_id)
        
        execute_db(
            f'UPDATE health_goals SET {", ".join(update_fields)} WHERE id = ?',
            update_values
        )
        
        return jsonify({
            'success': True,
            'message': 'Health goal updated successfully'
        })
    
    except Exception as e:
        logger.error(f"Error updating health goal: {e}")
        return jsonify({'error': 'Failed to update health goal'}), 500

@app.route('/api/health-goals/<int:goal_id>', methods=['DELETE'])
@login_required
def api_delete_health_goal(goal_id):
    """Delete a health goal"""
    try:
        user_id = session['user_id']
        
        # Verify goal belongs to user
        goal = query_db(
            'SELECT id FROM health_goals WHERE id = ? AND user_id = ?',
            [goal_id, user_id],
            one=True
        )
        
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        execute_db('DELETE FROM health_goals WHERE id = ?', [goal_id])
        execute_db('DELETE FROM goal_progress WHERE goal_id = ?', [goal_id])
        
        return jsonify({
            'success': True,
            'message': 'Health goal deleted successfully'
        })
    
    except Exception as e:
        logger.error(f"Error deleting health goal: {e}")
        return jsonify({'error': 'Failed to delete health goal'}), 500

@app.route('/api/health-goals/<int:goal_id>/progress', methods=['POST'])
@login_required
def api_add_goal_progress(goal_id):
    """Add progress entry for a health goal"""
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Verify goal belongs to user
        goal = query_db(
            'SELECT id, target_value FROM health_goals WHERE id = ? AND user_id = ?',
            [goal_id, user_id],
            one=True
        )
        
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        if 'value' not in data:
            return jsonify({'error': 'Value is required'}), 400
        
        # Add progress entry
        progress_id = execute_db(
            '''INSERT INTO goal_progress (goal_id, value, notes, recorded_date)
               VALUES (?, ?, ?, ?)''',
            [
                goal_id,
                data['value'],
                data.get('notes', ''),
                datetime.now()
            ]
        )
        
        # Update current value in goal
        execute_db(
            'UPDATE health_goals SET current_value = ?, updated_at = ? WHERE id = ?',
            [data['value'], datetime.now(), goal_id]
        )
        
        # Check if goal is completed
        if data['value'] >= goal['target_value']:
            execute_db(
                'UPDATE health_goals SET status = ? WHERE id = ?',
                ['completed', goal_id]
            )
        
        return jsonify({
            'success': True,
            'message': 'Progress recorded successfully',
            'progress_id': progress_id
        })
    
    except Exception as e:
        logger.error(f"Error adding goal progress: {e}")
        return jsonify({'error': 'Failed to add progress'}), 500

@app.route('/api/health-goals/<int:goal_id>/progress', methods=['GET'])
@login_required
def api_get_goal_progress(goal_id):
    """Get progress history for a health goal"""
    try:
        user_id = session['user_id']
        
        # Verify goal belongs to user
        goal = query_db(
            'SELECT id FROM health_goals WHERE id = ? AND user_id = ?',
            [goal_id, user_id],
            one=True
        )
        
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        progress = query_db(
            '''SELECT * FROM goal_progress 
               WHERE goal_id = ? 
               ORDER BY recorded_date DESC''',
            [goal_id]
        )
        
        return jsonify({
            'success': True,
            'progress': [dict(row) for row in progress]
        })
    
    except Exception as e:
        logger.error(f"Error fetching goal progress: {e}")
        return jsonify({'error': 'Failed to fetch progress'}), 500

# ============================================
# Admin API
# ============================================

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def api_admin_get_users():
    """Get all users (admin only)"""
    try:
        users = query_db('''
            SELECT id, email, full_name, role, created_at, 
                   (SELECT COUNT(*) FROM appointments WHERE user_id = users.id) as appointment_count,
                   (SELECT COUNT(*) FROM prescriptions WHERE user_id = users.id) as prescription_count
            FROM users
            ORDER BY created_at DESC
        ''')
        
        return jsonify({
            'success': True,
            'users': [dict(row) for row in users]
        })
    
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({'error': 'Failed to fetch users'}), 500

@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def api_admin_get_stats():
    """Get system statistics (admin only)"""
    try:
        stats = {
            'total_users': query_db('SELECT COUNT(*) as count FROM users', one=True)['count'],
            'total_appointments': query_db('SELECT COUNT(*) as count FROM appointments', one=True)['count'],
            'total_prescriptions': query_db('SELECT COUNT(*) as count FROM prescriptions', one=True)['count'],
            'total_chat_messages': query_db('SELECT COUNT(*) as count FROM chat_history', one=True)['count'],
            'active_goals': query_db('SELECT COUNT(*) as count FROM health_goals WHERE status = "active"', one=True)['count'],
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        logger.error(f"Error fetching admin stats: {e}")
        return jsonify({'error': 'Failed to fetch statistics'}), 500

# Add health goals API to enhanced.js API object
# API.healthGoals = {
#     list: () => API.request('/api/health-goals'),
#     create: (data) => API.request('/api/health-goals', { method: 'POST', body: data }),
#     update: (id, data) => API.request(`/api/health-goals/${id}`, { method: 'PUT', body: data }),
#     delete: (id) => API.request(`/api/health-goals/${id}`, { method: 'DELETE' }),
#     addProgress: (id, data) => API.request(`/api/health-goals/${id}/progress`, { method: 'POST', body: data }),
#     getProgress: (id) => API.request(`/api/health-goals/${id}/progress`)
# }
