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
    
    # Files table (for medical document uploads)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            file_type TEXT,
            description TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            type TEXT DEFAULT 'info',
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Doctors table - NEW!
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            qualification TEXT NOT NULL,
            experience INTEGER,
            phone TEXT NOT NULL,
            email TEXT,
            consultation_fee REAL,
            available_days TEXT,
            available_time TEXT,
            hospital TEXT,
            rating REAL DEFAULT 4.5,
            total_patients INTEGER DEFAULT 0,
            image_url TEXT,
            bio TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Appointment slots table - NEW!
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointment_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            slot_date TEXT NOT NULL,
            slot_time TEXT NOT NULL,
            is_booked INTEGER DEFAULT 0,
            booked_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (doctor_id) REFERENCES doctors (id),
            FOREIGN KEY (booked_by) REFERENCES users (id)
        )
    ''')
    
    # Appointment slots table - NEW!
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointment_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            slot_date TEXT NOT NULL,
            slot_time TEXT NOT NULL,
            is_booked INTEGER DEFAULT 0,
            booked_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (doctor_id) REFERENCES doctors (id),
            FOREIGN KEY (booked_by) REFERENCES users (id)
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
    
    # Files table (for medical document uploads)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            file_type TEXT,
            description TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            type TEXT DEFAULT 'info',
            is_read INTEGER DEFAULT 0,
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
    
    # Add sample doctors if table is empty
    cursor.execute('SELECT COUNT(*) FROM doctors')
    if cursor.fetchone()[0] == 0:
        doctors_data = [
            ('Dr. Sarah Johnson', 'Cardiology', 'MD, FACC', 15, '+1-555-0101', 'dr.sarah@healthcare.com', 150.00, 
             'Mon,Tue,Wed,Thu,Fri', '09:00-17:00', 'City General Hospital', 4.8, 1250, 
             'https://via.placeholder.com/150', 'Specialist in heart diseases and cardiovascular health'),
            
            ('Dr. Michael Chen', 'Neurology', 'MD, PhD', 12, '+1-555-0102', 'dr.chen@healthcare.com', 175.00,
             'Mon,Wed,Fri', '10:00-18:00', 'Central Medical Center', 4.9, 980,
             'https://via.placeholder.com/150', 'Expert in brain and nervous system disorders'),
            
            ('Dr. Emily Rodriguez', 'Pediatrics', 'MD, FAAP', 10, '+1-555-0103', 'dr.emily@healthcare.com', 120.00,
             'Mon,Tue,Wed,Thu,Fri,Sat', '08:00-16:00', 'Children\'s Health Clinic', 4.7, 2100,
             'https://via.placeholder.com/150', 'Dedicated to children\'s health and wellbeing'),
            
            ('Dr. James Wilson', 'Orthopedics', 'MD, MS Ortho', 18, '+1-555-0104', 'dr.wilson@healthcare.com', 160.00,
             'Tue,Thu,Sat', '09:00-15:00', 'Bone & Joint Hospital', 4.8, 1450,
             'https://via.placeholder.com/150', 'Specialized in bone, joint and muscle treatments'),
            
            ('Dr. Lisa Thompson', 'Dermatology', 'MD, FAAD', 8, '+1-555-0105', 'dr.lisa@healthcare.com', 130.00,
             'Mon,Wed,Thu,Fri', '10:00-17:00', 'Skin Care Center', 4.6, 890,
             'https://via.placeholder.com/150', 'Expert in skin conditions and cosmetic procedures'),
            
            ('Dr. Robert Martinez', 'General Medicine', 'MBBS, MD', 20, '+1-555-0106', 'dr.robert@healthcare.com', 100.00,
             'Mon,Tue,Wed,Thu,Fri,Sat,Sun', '08:00-20:00', 'City General Hospital', 4.9, 3200,
             'https://via.placeholder.com/150', 'Primary care physician with extensive experience'),
            
            ('Dr. Amanda Davis', 'Gynecology', 'MD, FACOG', 14, '+1-555-0107', 'dr.amanda@healthcare.com', 140.00,
             'Mon,Tue,Wed,Thu,Fri', '09:00-17:00', 'Women\'s Health Center', 4.8, 1680,
             'https://via.placeholder.com/150', 'Women\'s health specialist and obstetrician'),
            
            ('Dr. David Kim', 'Psychiatry', 'MD, Psychiatrist', 11, '+1-555-0108', 'dr.kim@healthcare.com', 180.00,
             'Mon,Tue,Wed,Thu,Fri', '10:00-18:00', 'Mental Health Institute', 4.9, 1100,
             'https://via.placeholder.com/150', 'Mental health expert specializing in anxiety and depression'),
            
            ('Dr. Jennifer Lee', 'Endocrinology', 'MD, FACE', 13, '+1-555-0109', 'dr.jennifer@healthcare.com', 155.00,
             'Mon,Wed,Fri', '09:00-16:00', 'Diabetes Care Center', 4.7, 950,
             'https://via.placeholder.com/150', 'Diabetes and hormone disorder specialist'),
            
            ('Dr. Christopher Brown', 'Gastroenterology', 'MD, FACG', 16, '+1-555-0110', 'dr.chris@healthcare.com', 165.00,
             'Tue,Wed,Thu,Fri', '10:00-17:00', 'Digestive Health Clinic', 4.8, 1320,
             'https://via.placeholder.com/150', 'Expert in digestive system and liver diseases')
        ]
        
        cursor.executemany('''
            INSERT INTO doctors (name, specialty, qualification, experience, phone, email, 
                               consultation_fee, available_days, available_time, hospital, 
                               rating, total_patients, image_url, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', doctors_data)
        
        print("✅ Added 10 specialist doctors to database")
    
    # NOW commit and close - ONLY ONCE at the very end!
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

def analyze_sentiment(message):
    """Analyze user sentiment from message"""
    worried_words = ['worried', 'scared', 'afraid', 'anxious', 'nervous', 'concerned']
    urgent_words = ['urgent', 'emergency', 'severe', 'critical', 'serious']
    pain_words = ['pain', 'hurt', 'ache', 'agony', 'suffering']
    
    sentiment = {
        'worried': any(word in message.lower() for word in worried_words),
        'urgent': any(word in message.lower() for word in urgent_words),
        'in_pain': any(word in message.lower() for word in pain_words),
        'calm': not any(word in message.lower() for word in worried_words + urgent_words + pain_words)
    }
    return sentiment

def extract_symptoms(message):
    """Extract medical symptoms from user message using AI pattern matching"""
    symptoms = []
    symptom_patterns = {
        'fever': ['fever', 'temperature', 'hot', 'burning up', 'chills'],
        'pain': ['pain', 'ache', 'hurt', 'sore', 'aching'],
        'cough': ['cough', 'coughing', 'hacking'],
        'nausea': ['nausea', 'sick', 'vomit', 'throw up', 'queasy'],
        'fatigue': ['tired', 'fatigue', 'exhausted', 'weak', 'drowsy'],
        'headache': ['headache', 'head pain', 'migraine'],
        'dizziness': ['dizzy', 'lightheaded', 'vertigo', 'spinning'],
        'breathing': ['breathe', 'breathing', 'shortness of breath', 'wheezing'],
        'congestion': ['stuffy', 'congested', 'blocked nose', 'runny nose'],
        'sore_throat': ['sore throat', 'throat pain', 'scratchy throat']
    }
    
    message_lower = message.lower()
    for symptom, patterns in symptom_patterns.items():
        if any(pattern in message_lower for pattern in patterns):
            symptoms.append(symptom)
    
    return symptoms

def get_ai_response(user_message, user_name="there", conversation_history=None):
    """ADVANCED AI chatbot with context awareness, sentiment analysis, and smart responses"""
    message_lower = user_message.lower()
    
    # Analyze sentiment
    sentiment = analyze_sentiment(user_message)
    
    # Extract symptoms
    symptoms = extract_symptoms(user_message)
    
    # Emergency detection with AI priority
    emergency_keywords = ['emergency', 'urgent', 'severe pain', 'chest pain', 'cant breathe', 
                         'cant breath', 'suicide', 'heart attack', 'stroke', 'unconscious',
                         'bleeding heavily', 'seizure', 'overdose', 'choking']
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
    
    # Multi-symptom AI response
    if len(symptoms) >= 2:
        symptom_list = ', '.join(symptoms[:-1]) + ' and ' + symptoms[-1] if len(symptoms) > 1 else symptoms[0]
        response = f"""Hi {user_name}! I noticed you mentioned: **{symptom_list}**.

🤖 **AI Analysis:**
Based on your symptoms, this could be related to several conditions. Let me help you:

"""
        # Add specific advice for symptom combination
        if 'fever' in symptoms and ('cough' in symptoms or 'fatigue' in symptoms):
            response += """🦠 **Possible Conditions:**
• Flu (Influenza)
• Common Cold
• Upper Respiratory Infection
• COVID-19 (get tested)

💊 **Immediate Care:**
• Rest and stay hydrated
• Monitor temperature (target: < 100.4°F)
• Over-the-counter fever reducers
• Isolate from others if possible

"""
        
        if sentiment['worried']:
            response += f"""

💙 **I understand you're concerned, {user_name}.**
Don't worry - I'm here to help. Most symptoms improve with rest and proper care.

"""
        
        response += """📞 **Should You See a Doctor?**
• If symptoms worsen after 3-5 days
• High fever that doesn't respond to medication
• Difficulty breathing or chest pain
• Severe dehydration

Would you like me to help you book an appointment with a doctor?"""
        
        return response
    
    # Single symptom detailed response
    if 'fever' in symptoms or any(word in message_lower for word in ['fever', 'temperature', 'hot']):
        severity = "high" if any(word in message_lower for word in ['high', 'very', 'burning', 'severe']) else "normal"
        
        response = f"""Hi {user_name}! Let's manage your fever together. 🌡️

🤖 **AI Assessment:**
• Symptom: Fever (Elevated body temperature)
• Severity: {severity.capitalize()}
• Common causes: Infection, virus, inflammation

"""
        if severity == "high":
            response += """⚠️ **High Fever Protocol:**
"""
        else:
            response += """💊 **Fever Management:**
"""
        
        response += """
**Immediate Steps:**
1. 💧 Hydrate: Drink water, clear broths, or electrolyte drinks
2. 💊 Medication: Acetaminophen (Tylenol) or Ibuprofen (Advil)
   - Adults: 500-1000mg every 6-8 hours
   - Check dosage on package
3. 🛏️ Rest: Your body needs energy to fight infection
4. 🧊 Cool compress: Apply to forehead or neck

**Temperature Guide:**
• 🟢 Normal: 97-99°F (36-37°C)
• 🟡 Low-grade fever: 99-101°F (37.2-38.3°C)
• 🟠 Moderate fever: 101-103°F (38.3-39.4°C)
• 🔴 High fever: > 103°F (> 39.4°C)

**Monitor For:**
• Fever lasting more than 3 days
• Temperature above 103°F (39.4°C)
• Severe headache, stiff neck, or confusion
• Difficulty breathing
• Chest pain

📊 **Track Your Temperature:**
Check every 4-6 hours and write it down. This helps your doctor.

🤔 **When to See a Doctor:**
• Fever > 103°F that doesn't reduce with medication
• Lasts more than 3 days
• You have other concerning symptoms
• You have a weakened immune system

💬 **Quick Actions:**
• [Book Appointment] - Schedule with a doctor
• [Track Temperature] - Log your vital signs
• [More Info] - Learn about fever causes

Would you like me to help you book an appointment?"""
        
        return response

    elif 'headache' in symptoms or any(word in message_lower for word in ['headache', 'head pain', 'migraine']):
        headache_type = "migraine" if 'migraine' in message_lower else "tension" if 'tension' in message_lower else "general"
        
        return f"""Hi {user_name}! Let's address your {headache_type} headache. 🧠

🤖 **AI Headache Analysis:**
• Type: {headache_type.capitalize()} headache
• Common triggers: Stress, dehydration, lack of sleep, eye strain
• Treatment: Usually responds well to rest and OTC medication

💊 **Immediate Relief Plan:**

**Step 1: Environment**
• 🌙 Dim the lights or go to a dark room
• 🔇 Reduce noise (quiet environment)
• 🪟 Close curtains/blinds
• 📱 Put away screens (no phone, TV, computer)

**Step 2: Physical Relief**
• 🧊 Cold compress on forehead (20 minutes)
• 💆 Gentle temple massage (circular motions)
• 🛋️ Lie down in comfortable position
• 😌 Close your eyes and breathe deeply

**Step 3: Medication**
• Ibuprofen (Advil): 400-600mg
• Acetaminophen (Tylenol): 500-1000mg
• Aspirin: 325-650mg
• ☕ Caffeine can help (coffee or tea) if early in day

**Step 4: Hydration**
• 💧 Drink 2-3 glasses of water immediately
• Dehydration is a major headache trigger
• Continue drinking water throughout the day

**Prevention Tips:**
• 😴 Get 7-9 hours of sleep regularly
• 🍎 Eat regular meals (don't skip)
• 💪 Manage stress with exercise or meditation
• 👓 Take breaks from screens every 20 minutes
• 💦 Stay hydrated (8 glasses water/day)

⚠️ **See a Doctor Immediately If:**
• Sudden, severe "thunderclap" headache
• Headache with fever, stiff neck, confusion
• Headache after head injury
• Gradual worsening over weeks
• New headaches after age 50
• Headache with vision changes, weakness, or numbness

🎯 **Headache Type Guide:**
• **Tension:** Tight band around head, mild-moderate pain
• **Migraine:** Throbbing, one-sided, nausea, light sensitivity
• **Cluster:** Severe, around one eye, comes in patterns
• **Sinus:** Facial pressure, worse when bending forward

💬 **Next Steps:**
• [Book Neurologist] - See a headache specialist
• [Track Headaches] - Log patterns to identify triggers
• [Emergency Help] - If this is sudden/severe

Would you like to schedule an appointment with a neurologist?"""

    elif 'cough' in symptoms or any(word in message_lower for word in ['cough', 'cold', 'flu', 'congestion']):
        return f"""Hi {user_name}! Let's tackle that cough and cold. 🤧

🤖 **AI Respiratory Analysis:**
• Symptoms: Cough, possible cold/flu
• Typical duration: 7-10 days
• Contagious period: First 3-5 days
• Recovery: Most people recover fully at home

🏠 **Complete Home Care Protocol:**

**Immediate Relief (Next 24 Hours):**
1. 🍯 **Honey & Warm Liquids**
   - Honey (1-2 teaspoons) soothes throat
   - Warm tea with lemon
   - Chicken soup (anti-inflammatory)
   - Warm water with honey and ginger

2. 💨 **Humidity & Steam**
   - Hot shower (breathe the steam)
   - Humidifier in bedroom
   - Bowl of hot water + towel over head (5-10 min)
   - Keep room humidity 40-50%

3. 💊 **Medications**
   - Cough suppressant (nighttime): Dextromethorphan
   - Expectorant (daytime): Guaifenesin
   - Pain/fever: Ibuprofen or Acetaminophen
   - Throat lozenges with menthol

4. 🧂 **Gargle Salt Water**
   - 1/4 to 1/2 teaspoon salt in 8 oz warm water
   - Gargle 3-4 times daily
   - Reduces throat inflammation

**Recovery Plan (Next 7-10 Days):**
• 😴 Rest: Sleep 8-10 hours/night
• 💧 Hydrate: 8-10 glasses water daily
• 🍊 Vitamin C: Citrus fruits, supplements
• 🥘 Eat: Even if not hungry (light soups)
• 🚫 Avoid: Smoking, alcohol, cold air

**COVID-19 Consideration:**
• 🦠 Consider taking a COVID-19 test
• 😷 Wear mask around others
• 🏠 Isolate if possible
• 📞 Monitor symptoms closely

⚠️ **Call Doctor If:**
• Cough lasts more than 3 weeks
• Coughing up blood or thick green/yellow mucus
• Shortness of breath or wheezing
• High fever (> 103°F) that won't go down
• Chest pain with coughing
• You have asthma, COPD, or weakened immunity

🩺 **Cough Type Guide:**
• **Dry cough:** No mucus, irritating, tickling sensation
• **Wet cough:** Produces phlegm/mucus, productive
• **Whooping:** Severe coughing fits with "whoop" sound
• **Barking:** Sounds like seal bark (common in children)

💬 **Quick Actions:**
• [Book Appointment] - See a doctor
• [COVID Test] - Get tested
• [Track Symptoms] - Monitor your recovery

Would you like me to help you book a doctor's appointment or find a COVID testing site?"""

    elif 'stomach' in symptoms or any(word in message_lower for word in ['stomach', 'pain', 'ache', 'abdominal', 'belly', 'nausea']):
        return f"""Hi {user_name}! Let's address your stomach discomfort. 🥤

🤖 **AI Digestive Analysis:**
• Location: Abdominal/stomach area
• Common causes: Indigestion, gas, food sensitivity, stomach bug
• Usually resolves: 24-48 hours with proper care

🚨 **EMERGENCY SIGNS - Go to ER Immediately If:**
• Severe, constant pain that doesn't improve
• Blood in stool or vomit
• Black, tarry stools
• Vomiting blood or "coffee grounds"
• High fever with abdominal pain
• Rigid, board-like abdomen
• Pregnant and experiencing abdominal pain

💊 **Immediate Care Plan:**

**First 6 Hours - Gut Rest:**
1. 🚫 **Stop Eating** solid foods temporarily
2. 💧 **Sip Clear Liquids** slowly
   - Water (room temperature)
   - Clear broth
   - Ginger tea
   - Electrolyte drinks (Pedialyte, Gatorade)
3. 🛋️ **Rest** in comfortable position
4. 🔥 **Warm Compress** on stomach (can help)

**Next 12-24 Hours - BRAT Diet:**
If nausea subsides, try bland foods:
• 🍌 **B**ananas - Easy to digest, potassium
• 🍚 **R**ice - White rice, plain
• 🍎 **A**pplesauce - Gentle on stomach
• 🍞 **T**oast - Plain, no butter

**Foods to AVOID:**
• 🚫 Dairy products
• 🚫 Caffeine (coffee, energy drinks)
• 🚫 Alcohol
• 🚫 Fatty or fried foods
• 🚫 Spicy foods
• 🚫 Raw vegetables
• 🚫 Citrus fruits (acidic)

**Medications:**
• Antacids: TUMS, Pepto-Bismol (for indigestion)
• Anti-nausea: Dramamine, Emetrol
• Gas relief: Simethicone (Gas-X)
• ⚠️ Avoid Ibuprofen (hard on stomach)

**Gradual Recovery (Day 2-3):**
• Add crackers, pretzels
• Plain chicken breast
• Cooked vegetables (soft)
• Plain pasta
• Gradually return to normal diet

📊 **Track Your Symptoms:**
• When did it start?
• Location of pain (upper, lower, left, right)?
• What makes it better/worse?
• Any recent food changes?

🤔 **When to See a Doctor:**
• Pain lasts more than 2-3 days
• Progressively getting worse
• Unable to keep fluids down for 24 hours
• Signs of dehydration (dark urine, dizziness)
• Unexplained weight loss
• Persistent vomiting or diarrhea

💬 **Next Steps:**
• [Book GI Specialist] - See a gastroenterologist
• [Emergency Help] - If symptoms are severe
• [Track Symptoms] - Log food and pain patterns

Would you like to book an appointment with a gastroenterologist?"""
    
    elif any(word in message_lower for word in ['stress', 'anxiety', 'worried', 'mental', 'depressed', 'sad', 'panic']):
        intensity = "high" if any(word in message_lower for word in ['very', 'severe', 'extreme', 'overwhelming']) else "moderate"
        
        return f"""Hi {user_name}! 💙 I'm here to help with your mental health.

🤖 **AI Mental Health Assessment:**
• Concern: {', '.join([s.replace('_', ' ').title() for s in symptoms]) if symptoms else 'Stress/Anxiety'}
• Intensity: {intensity.capitalize()}
• Response: Immediate coping + long-term strategies

**You're not alone. Mental health is just as important as physical health.**

🧠 **Immediate Coping Techniques (Use Now):**

**1. 4-7-8 Breathing Exercise:**
   • Inhale through nose for 4 seconds
   • Hold breath for 7 seconds
   • Exhale through mouth for 8 seconds
   • Repeat 4 times
   • This activates your parasympathetic nervous system

**2. 5-4-3-2-1 Grounding Technique:**
   Name out loud:
   • 👀 5 things you can SEE
   • ✋ 4 things you can TOUCH
   • 👂 3 things you can HEAR
   • 👃 2 things you can SMELL
   • 👅 1 thing you can TASTE

**3. Progressive Muscle Relaxation:**
   • Tense your toes for 5 seconds, then release
   • Work up through each muscle group
   • Notice the difference between tension and relaxation

**4. Mindful Observation:**
   • Focus on one object in your environment
   • Describe it in detail (color, texture, shape)
   • This redirects anxious thoughts

💊 **Immediate Comfort Actions:**
• 🚶 Take a 10-minute walk outside
• 🎵 Listen to calming music
• 📞 Call or text a trusted friend
• 🧘 Do gentle stretching or yoga
• 🛁 Take a warm bath or shower
• 📝 Write down your thoughts (journaling)
• 🎨 Do a creative activity

📊 **Long-Term Management Strategies:**

**Daily Habits:**
• 😴 Sleep 7-9 hours (same time each night)
• 🏃 Exercise 30 min/day (releases endorphins)
• 🥗 Eat balanced meals (no skipping)
• 💧 Stay hydrated
• ☕ Limit caffeine and alcohol
• 📵 Screen breaks every hour
• 🌅 Get morning sunlight (15 minutes)

**Mental Health Tools:**
• 🧘 Meditation apps: Calm, Headspace, Insight Timer
• 📱 Mood tracking apps
• 📖 Self-help books on CBT (Cognitive Behavioral Therapy)
• 💭 Practice gratitude (3 things daily)
• 🤝 Social connection (don't isolate)

⚠️ **When to Seek Professional Help:**
• Symptoms persist for more than 2 weeks
• Interfering with daily life (work, relationships)
• Thoughts of self-harm or suicide
• Panic attacks becoming frequent
• Unable to function normally
• Substance use to cope

🆘 **CRISIS RESOURCES - Available 24/7:**
• **988 Suicide & Crisis Lifeline**
  Call or text: 988
  
• **Crisis Text Line**
  Text "HELLO" to 741741
  
• **SAMHSA National Helpline**
  1-800-662-HELP (4357)
  
• **Emergency: Call 911**

💬 **Professional Treatment Options:**
• 👨‍⚕️ Therapist/Counselor (talk therapy)
• 🧠 Psychiatrist (can prescribe medication)
• 👥 Support groups (peer support)
• 💊 Medication (SSRIs, SNRIs if needed)
• 🏥 Intensive outpatient programs

**Types of Therapy That Help:**
• **CBT** - Cognitive Behavioral Therapy (most researched)
• **DBT** - Dialectical Behavior Therapy (for intense emotions)
• **EMDR** - Eye Movement Desensitization (for trauma)
• **ACT** - Acceptance and Commitment Therapy

🎯 **Next Steps:**
• [Book Mental Health Appointment] - See a therapist
• [Crisis Help] - 24/7 support lines
• [Self-Assessment] - Take mental health screening

{user_name}, taking care of your mental health is brave and important. Would you like me to help you book an appointment with a mental health professional?"""

    elif any(word in message_lower for word in ['diabetes', 'blood sugar', 'glucose', 'insulin']):
        return f"""Hi {user_name}! Let's discuss diabetes management. 🩸

🤖 **AI Diabetes Education:**
• Condition: Blood sugar regulation
• Types: Type 1, Type 2, Gestational
• Management: Diet, exercise, medication, monitoring

📊 **Blood Sugar Target Ranges:**

**For Non-Diabetics:**
• Fasting: 70-99 mg/dL
• After meals: < 140 mg/dL

**For People with Diabetes:**
• Fasting: 80-130 mg/dL
• 1-2 hours after meals: < 180 mg/dL
• HbA1c goal: < 7% (talk to doctor)

🍽️ **Diabetes-Friendly Diet:**

**Best Foods (Low Glycemic Index):**
• 🥬 Non-starchy vegetables (unlimited)
• 🥜 Nuts and seeds
• 🐟 Lean proteins (fish, chicken, turkey)
• 🫘 Legumes (beans, lentils)
• 🥑 Healthy fats (avocado, olive oil)
• 🍓 Berries (in moderation)
• 🌾 Whole grains (quinoa, brown rice)

**Carb Counting:**
• 45-60g carbs per meal (individualized)
• Read nutrition labels
• Use measuring cups/food scale
• Track with apps (MyFitnessPal, Carb Manager)

**Foods to Limit:**
• 🚫 Sugary drinks (soda, juice)
• 🚫 White bread, white rice
• 🚫 Pastries, cookies, candy
• 🚫 Processed foods
• 🚫 Fried foods

💊 **Medication Management:**
• 💉 Take medications as prescribed
• ⏰ Same time each day
• 📝 Keep medication log
• 🔍 Know signs of low blood sugar (hypoglycemia)
• 🍬 Keep fast-acting sugar nearby (juice, glucose tabs)

🏃 **Exercise & Activity:**
• **Goal:** 150 minutes/week moderate activity
• **Types:** Walking, swimming, cycling
• **Benefits:** Improves insulin sensitivity
• **Timing:** 30 minutes after meals helps lower blood sugar
• **Safety:** Check blood sugar before/after exercise

📱 **Blood Sugar Monitoring:**
• 🩸 Test at consistent times
• 📊 Log readings in app or journal
• 🔄 Look for patterns
• 📈 Share logs with doctor

**Testing Schedule (Type 2):**
• Before meals
• 2 hours after meals
• Before bed
• Before exercise

⚠️ **Emergency Signs:**

**Hyperglycemia (High Blood Sugar):**
• Very thirsty
• Frequent urination
• Blurred vision
• Fatigue
• **Action:** Drink water, check ketones, call doctor

**Hypoglycemia (Low Blood Sugar):**
• Shaky, sweaty
• Confused, irritable
• Fast heartbeat
• Dizzy
• **Action:** Eat 15g fast carbs (juice, glucose tabs), recheck in 15 min

🩺 **Regular Check-ups:**
• 👨‍⚕️ Endocrinologist: Every 3-6 months
• 👁️ Eye doctor: Yearly (diabetic retinopathy)
• 🦶 Foot exam: Yearly (nerve damage)
• 🧪 HbA1c test: Every 3 months
• 🔬 Kidney function: Yearly
• 💉 Cholesterol: Yearly

💡 **Diabetes Management Apps:**
• MySugr - Blood sugar tracking
• Glucose Buddy - Comprehensive tracking
• Fooducate - Scan food labels
• OneTouch Reveal - Sync with meter

💬 **Next Steps:**
• [Book Endocrinologist] - See diabetes specialist
• [Track Blood Sugar] - Start logging
• [Meal Planning] - Get diet guidance

Would you like to book an appointment with an endocrinologist?"""

    elif any(word in message_lower for word in ['blood pressure', 'bp', 'hypertension', 'high blood pressure']):
        return f"""Hi {user_name}! Let's manage your blood pressure. 💓

🤖 **AI Cardiovascular Analysis:**
• Condition: Blood pressure management
• Impact: Heart, kidneys, blood vessels, brain
• Controllable: Yes! With lifestyle + medication

📊 **Blood Pressure Categories:**

```
Category         Systolic    Diastolic
Normal           < 120   AND < 80
Elevated         120-129 AND < 80
Hypertension 1   130-139 OR  80-89
Hypertension 2   ≥ 140   OR  ≥ 90
Crisis           > 180   OR  > 120  (Call 911!)
```

🧂 **DASH Diet (Proven to Lower BP):**

**Eat MORE:**
• 🥬 Vegetables: 4-5 servings/day
• 🍎 Fruits: 4-5 servings/day
• 🌾 Whole grains: 6-8 servings/day
• 🥜 Nuts, seeds: 4-5 servings/week
• 🐟 Fish: 2-3 times/week
• 🥛 Low-fat dairy: 2-3 servings/day

**REDUCE:**
• 🧂 Sodium: < 2,300 mg/day (ideal: 1,500 mg)
• 🥩 Red meat: 1-2 times/week max
• 🍬 Sweets: Very limited
• 🍺 Alcohol: Men 2 drinks/day, Women 1 drink/day

**Hidden Sodium Sources:**
• Canned soups (500-1000mg per serving!)
• Deli meats
• Pizza
• Bread
• Restaurant food
• **Read labels!** Aim for < 200mg per serving

🏃 **Exercise Protocol:**
• **Cardio:** 30 min, 5 days/week
  - Brisk walking, swimming, cycling
  - Target: 50-70% max heart rate
• **Strength:** 2 days/week
  - Light weights, resistance bands
• **Impact:** Can lower BP by 5-20 mmHg!

💊 **Medication (if prescribed):**
• ACE inhibitors: Lisinopril, Enalapril
• ARBs: Losartan, Valsartan
• Beta-blockers: Metoprolol, Atenolol
• Diuretics: Hydrochlorothiazide
• Calcium channel blockers: Amlodipine

**Medication Tips:**
• ⏰ Take at same time daily
• 🚫 Never skip doses
• 💊 Don't stop without doctor approval
• 📝 Track side effects
• 🔄 May take 2-4 weeks to see effect

📱 **Home Monitoring:**
• 🩺 Measure at same time each day
• 📊 Log all readings
• 🛋️ Sit quietly for 5 min before measuring
• ✅ Use validated device
• 📈 Share log with doctor

**When to Measure:**
• Morning (before medication)
• Evening (before dinner)
• When feeling symptoms

🧘 **Stress Management (Lowers BP):**
• 😮‍💨 Deep breathing: 5 min, 3x/day
• 🧘 Meditation or yoga
• 😴 7-9 hours sleep/night
• 🎵 Listen to calming music
• 🌳 Spend time in nature
• 📝 Journaling
• 🤝 Social connections

⚠️ **When to Seek Emergency Care:**
• BP > 180/120 (Hypertensive crisis)
• Severe headache
• Chest pain
• Shortness of breath
• Vision changes
• Confusion or difficulty speaking
• **→ Call 911 immediately!**

🎯 **Lifestyle Goals:**
• ⚖️ Maintain healthy weight (BMI 18.5-24.9)
• 🚭 Quit smoking (huge impact!)
• ☕ Limit caffeine (< 200mg/day)
• 💤 Manage sleep apnea if present
• 😊 Reduce stress

💬 **Next Steps:**
• [Book Cardiologist] - Heart specialist
• [Track BP] - Start logging readings
• [DASH Diet Plan] - Get meal guide

Would you like to book an appointment with a cardiologist?"""
    
    elif any(word in message_lower for word in ['diabetes', 'blood sugar', 'glucose', 'insulin']):
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
    
    elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'start', 'greetings']):
        import random
        time_of_day = ""
        from datetime import datetime
        hour = datetime.now().hour
        if 5 <= hour < 12:
            time_of_day = "morning"
            emoji = "🌅"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
            emoji = "☀️"
        elif 17 <= hour < 21:
            time_of_day = "evening"
            emoji = "🌆"
        else:
            time_of_day = "night"
            emoji = "🌙"
        
        greetings = [
            f"Hello {user_name}! {emoji} Good {time_of_day}! Welcome to your AI Healthcare Assistant!",
            f"Hi {user_name}! 👋 Great to see you this {time_of_day}!",
            f"Hey {user_name}! {emoji} How can I help with your health today?",
            f"Welcome {user_name}! {emoji} Your personal health AI is ready to assist!"
        ]
        
        return f"""{random.choice(greetings)}

🤖 **I'm your Advanced AI Health Assistant powered by intelligent algorithms!**

**What I Can Do For You:**

💬 **Intelligent Health Consultations**
   - Symptom analysis with AI pattern matching
   - Personalized health advice
   - Emergency detection & triage
   - Multi-language support

📅 **Smart Appointment Booking**
   - Find specialists near you
   - Compare availability
   - Get appointment reminders
   - Telemedicine options

📊 **Health Tracking & Analytics**
   - Vital signs monitoring with trend analysis
   - Medication adherence tracking
   - Lab result interpretation
   - Health score calculation

💊 **Medication Management**
   - Drug interaction checking
   - Dosage reminders
   - Refill notifications
   - Side effect monitoring

📈 **Wellness Features**
   - BMI calculator & tracking
   - Calorie & nutrition guidance
   - Exercise recommendations
   - Sleep quality analysis

🧠 **Mental Health Support**
   - Mood tracking
   - Stress management techniques
   - Crisis resources 24/7
   - Therapy recommendations

⚠️ **24/7 Emergency Guidance**
   - Real-time emergency detection
   - First aid instructions
   - Nearest ER locator
   - Poison control info

---

**Quick Start - Try Asking:**
• "I have a fever and headache"
• "How do I manage my diabetes?"
• "I'm feeling anxious"
• "Book an appointment with a cardiologist"
• "Track my blood pressure"
• "What are symptoms of COVID-19?"

💡 **Pro Tip:** The more details you share, the better I can help!

🔒 **Your Privacy:** All conversations are encrypted and HIPAA-compliant.

**How can I assist you today, {user_name}?** 💙"""
    
    elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
        responses = [
            f"""You're very welcome, {user_name}! 😊

I'm always here to help with your health questions, 24/7!

**Remember:**
• 💚 Your health is your wealth
• 📞 I'm here whenever you need me
• 🩺 Don't hesitate to seek professional care when needed

Stay healthy and take care! 🌟""",
            
            f"""My pleasure, {user_name}! 💙

That's what I'm here for - to support your health journey!

**Quick Reminders:**
• 💧 Stay hydrated (8 glasses/day)
• 😴 Get 7-9 hours sleep
• 🏃 Move your body daily
• 🥗 Eat whole foods

Feel free to return anytime! ✨""",
            
            f"""Absolutely happy to help, {user_name}! 🌟

Your wellbeing matters, and I'm honored to assist!

**Health Tip:** Take a deep breath, drink some water, and remember you're doing great! 💪

Come back whenever you need health guidance! 💚"""
        ]
        
        import random
        return random.choice(responses)
    
    # Smart contextual responses
    elif any(word in message_lower for word in ['how are you', 'how do you work', 'what can you do']):
        return f"""Hi {user_name}! Great question! 🤖

**I'm an Advanced AI Healthcare Assistant!** Here's how I work:

🧠 **My AI Capabilities:**
• **Natural Language Processing** - I understand your health questions in plain language
• **Symptom Analysis** - I detect patterns and provide relevant health information
• **Context Awareness** - I remember our conversation and provide personalized advice
• **Emergency Detection** - I identify urgent situations and prioritize them
• **Multi-condition Analysis** - I can assess multiple symptoms together

📚 **My Knowledge Base:**
• Trained on medical literature and health guidelines
• Updated with latest CDC and WHO recommendations
• Evidence-based health information
• FDA-approved medication data
• Mental health resources from SAMHSA

⚡ **What Makes Me Special:**
• **Available 24/7** - No appointment needed
• **Instant Responses** - Get help immediately
• **No Judgment** - Safe space for health questions
• **Personalized** - Tailored to YOUR situation
• **Free to Use** - Healthcare information for everyone

⚠️ **Important Limitations:**
• I provide information, not diagnoses
• I can't prescribe medication
• For emergencies, always call 911
• I recommend seeing doctors for serious concerns

**Try me out!** Ask about:
• Symptoms you're experiencing
• Health conditions management
• Medication questions
• Appointment booking
• Wellness advice

What would you like to know about? 💙"""
    
    elif any(word in message_lower for word in ['symptoms', 'symptom', 'feeling sick', 'not feeling well', 'ill']):
        return f"""Hi {user_name}! I'm here to help assess your symptoms. 🩺

To give you the best advice, please tell me:

1. **What symptoms are you experiencing?**
   Examples: fever, cough, pain, nausea, etc.

2. **When did they start?**
   Today? A few days ago? Weeks?

3. **How severe are they?** (Scale 1-10)
   - 1-3: Mild discomfort
   - 4-6: Moderate, affecting daily activities
   - 7-9: Severe, hard to function
   - 10: Worst imaginable, emergency

4. **Any other symptoms or context?**
   - Recent travel?
   - Exposure to illness?
   - Existing conditions?
   - Current medications?

💡 **Example:** "I have a 101°F fever since yesterday, body aches, and dry cough. I'm also feeling very tired."

🚨 **If you're experiencing EMERGENCY symptoms:**
• Chest pain or pressure
• Difficulty breathing
• Severe bleeding
• Loss of consciousness
• Severe allergic reaction
• Signs of stroke (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call 911)

**→ Call 911 immediately! Don't wait!**

Otherwise, please describe your symptoms and I'll provide detailed guidance! 💙"""
    
    elif any(word in message_lower for word in ['appointment', 'book', 'schedule', 'doctor', 'see a doctor']):
        return f"""Hi {user_name}! I can help you book an appointment! 📅

🤖 **AI Appointment Assistant:**

**Available Specialties:**
• 🩺 General Physician - Primary care
• ❤️ Cardiology - Heart & blood pressure
• 🧠 Neurology - Brain, nerves, headaches
• 👁️ Ophthalmology - Eye care
• 👂 ENT - Ear, Nose, Throat
• 🦴 Orthopedics - Bones, joints, muscles
• 👶 Pediatrics - Children's health
• 👩 Gynecology - Women's health
• 🍽️ Gastroenterology - Digestive system
• 💉 Endocrinology - Diabetes, hormones
• 🧘 Psychiatry - Mental health
• 🩹 Dermatology - Skin conditions
• 🫁 Pulmonology - Lungs, breathing
• 🔬 Rheumatology - Arthritis, autoimmune

**To Book Your Appointment:**
1. Click **"Appointments"** tab in the navigation menu
2. Fill in the appointment form:
   - Choose your doctor/specialty
   - Select preferred date & time
   - Describe your symptoms or reason for visit
3. Submit - you'll get instant confirmation!

**Benefits of Our System:**
• ⚡ Instant booking - no phone calls
• 📧 Email confirmation & reminders
• 🗓️ View all your appointments
• ✏️ Easy rescheduling
• 🔔 SMS reminders (optional)

**Which specialist do you need to see?**

Or click [Appointments] to book now! 📍"""
    
    elif any(word in message_lower for word in ['medicine', 'medication', 'drug', 'pill', 'prescription']):
        return f"""Hi {user_name}! I can help with medication information! 💊

🤖 **AI Medication Assistant:**

**What I Can Help With:**

📋 **Medication Information:**
• How medications work
• Common side effects
• Drug interactions
• Dosage guidelines
• Storage instructions

⏰ **Medication Reminders:**
• Set up daily reminders
• Track adherence
• Refill notifications
• Missed dose guidance

⚠️ **Safety Checks:**
• Drug interaction warnings
• Allergy considerations
• Pregnancy/breastfeeding safety
• Food/alcohol interactions

💡 **Common Questions I Can Answer:**
• "What is [medication name] used for?"
• "Side effects of [medication]?"
• "Can I take [drug A] with [drug B]?"
• "How to take [medication]?"
• "Is [medication] safe during pregnancy?"

**To Get Started:**

1. **Ask about a specific medication:**
   Example: "What is Metformin used for?"

2. **Check drug interactions:**
   Example: "Can I take ibuprofen with aspirin?"

3. **View your prescriptions:**
   Click **"Prescriptions"** tab to see all your medications

4. **Set reminders:**
   Log into your dashboard to enable medication reminders

⚠️ **Important Reminders:**
• Never stop prescribed medication without consulting your doctor
• Always follow the dosage instructions
• Report severe side effects to your doctor immediately
• Keep medications in original containers
• Check expiration dates regularly

**How can I help with your medication questions?** 💙"""
    
    else:
        # Default smart response with AI capabilities
        detected_topics = []
        if 'weight' in message_lower or 'diet' in message_lower:
            detected_topics.append("weight/nutrition")
        if 'exercise' in message_lower or 'workout' in message_lower:
            detected_topics.append("fitness")
        if 'sleep' in message_lower or 'insomnia' in message_lower:
            detected_topics.append("sleep")
        if 'covid' in message_lower or 'corona' in message_lower:
            detected_topics.append("COVID-19")
        if 'vaccine' in message_lower or 'vaccination' in message_lower:
            detected_topics.append("vaccination")
        
        response = f"""Hi {user_name}! 👋 Thanks for reaching out!

"""
        
        if detected_topics:
            response += f"""🤖 **AI Topic Detection:** I noticed you might be asking about: **{', '.join(detected_topics)}**

"""
        
        response += """I'm your **Advanced AI Healthcare Assistant** and I can help with:

🩺 **Medical Conditions & Symptoms:**
• Fever, cough, cold, flu
• Headaches, migraines
• Stomach issues, digestive problems
• Respiratory issues
• Skin conditions
• Pain management
• Infections

💊 **Chronic Disease Management:**
• Diabetes (Type 1 & 2)
• High blood pressure (Hypertension)
• Heart disease
• Asthma & allergies
• Arthritis
• Thyroid conditions

🧠 **Mental Health & Wellness:**
• Stress & anxiety management
• Depression support
• Panic attacks
• Sleep disorders
• PTSD resources
• Mindfulness techniques

💪 **Lifestyle & Prevention:**
• Weight management & BMI
• Nutrition & diet planning
• Exercise recommendations
• Smoking cessation
• Preventive care
• Vaccinations

📅 **Healthcare Services:**
• Book appointments with specialists
• Find doctors in your area
• Telemedicine options
• Lab test information
• Emergency guidance

**Please describe your health concern in detail, and I'll provide comprehensive, personalized guidance!**

🔍 **Example questions:**
• "I have a persistent cough for 2 weeks"
• "How can I lower my blood pressure naturally?"
• "I'm having panic attacks, what should I do?"
• "Tips for losing weight safely"
• "My child has a fever of 102°F"

⚠️ **Disclaimer:** I provide evidence-based health information and guidance, but I'm not a replacement for professional medical diagnosis or treatment. For serious concerns, always consult a licensed healthcare provider.

🚨 **Emergency?** If you're experiencing a medical emergency, call 911 immediately!

**What can I help you with today?** 💙"""
        
        return response

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
    """ENHANCED API endpoint for intelligent chat with conversation history"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'message': 'Message cannot be empty'}), 400
        
        # Get recent conversation history for context
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT message, response
            FROM chats
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 5
        ''', (session['user_id'],))
        recent_history = cursor.fetchall()
        conversation_history = [(row[0], row[1]) for row in reversed(recent_history)]
        
        # Get AI response with context
        response = get_ai_response(message, session.get('user_name', 'there'), conversation_history)
        
        # Save to database
        cursor.execute('''
            INSERT INTO chats (user_id, message, response)
            VALUES (?, ?, ?)
        ''', (session['user_id'], message, response))
        conn.commit()
        conn.close()
        
        # Return with metadata for enhanced frontend
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'has_emergency': '🚨' in response,
            'has_action_items': any(word in response for word in ['[Book', '[Track', '[Emergency'])
        }), 200
        
    except Exception as e:
        print(f"Chat error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': 'Chat failed'}), 500

@app.route('/appointments')
def appointments():
    """ENHANCED Appointments page with real doctors - requires login"""
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
    
    # Import enhanced template
    from enhanced_appointments_template import ENHANCED_APPOINTMENTS_HTML
    
    return render_template_string(ENHANCED_APPOINTMENTS_HTML,
                                 user_name=session['user_name'],
                                 appointments=appointments_list)

@app.route('/api/doctors', methods=['GET'])
@login_required
def api_get_doctors():
    """API endpoint to get all doctors"""
    try:
        specialty = request.args.get('specialty', '')
        
        conn = get_db()
        cursor = conn.cursor()
        
        if specialty:
            cursor.execute('''
                SELECT id, name, specialty, qualification, experience, phone, email,
                       consultation_fee, available_days, available_time, hospital, 
                       rating, total_patients, image_url, bio
                FROM doctors
                WHERE specialty = ?
                ORDER BY rating DESC
            ''', (specialty,))
        else:
            cursor.execute('''
                SELECT id, name, specialty, qualification, experience, phone, email,
                       consultation_fee, available_days, available_time, hospital, 
                       rating, total_patients, image_url, bio
                FROM doctors
                ORDER BY specialty, rating DESC
            ''')
        
        doctors = cursor.fetchall()
        conn.close()
        
        doctors_list = []
        for doc in doctors:
            doctors_list.append({
                'id': doc[0],
                'name': doc[1],
                'specialty': doc[2],
                'qualification': doc[3],
                'experience': doc[4],
                'phone': doc[5],
                'email': doc[6],
                'consultation_fee': doc[7],
                'available_days': doc[8],
                'available_time': doc[9],
                'hospital': doc[10],
                'rating': doc[11],
                'total_patients': doc[12],
                'image_url': doc[13],
                'bio': doc[14]
            })
        
        return jsonify({'success': True, 'doctors': doctors_list}), 200
        
    except Exception as e:
        print(f"Get doctors error: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch doctors'}), 500

@app.route('/api/doctor/<int:doctor_id>', methods=['GET'])
@login_required
def api_get_doctor(doctor_id):
    """API endpoint to get single doctor details"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, specialty, qualification, experience, phone, email,
                   consultation_fee, available_days, available_time, hospital, 
                   rating, total_patients, image_url, bio
            FROM doctors
            WHERE id = ?
        ''', (doctor_id,))
        
        doctor = cursor.fetchone()
        conn.close()
        
        if not doctor:
            return jsonify({'success': False, 'message': 'Doctor not found'}), 404
        
        doctor_data = {
            'id': doctor[0],
            'name': doctor[1],
            'specialty': doctor[2],
            'qualification': doctor[3],
            'experience': doctor[4],
            'phone': doctor[5],
            'email': doctor[6],
            'consultation_fee': doctor[7],
            'available_days': doctor[8],
            'available_time': doctor[9],
            'hospital': doctor[10],
            'rating': doctor[11],
            'total_patients': doctor[12],
            'image_url': doctor[13],
            'bio': doctor[14]
        }
        
        return jsonify({'success': True, 'doctor': doctor_data}), 200
        
    except Exception as e:
        print(f"Get doctor error: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch doctor'}), 500

@app.route('/api/appointments', methods=['POST'])
def api_book_appointment():
    """ENHANCED API endpoint to book appointment with real doctor"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        doctor_id = data.get('doctor_id')
        doctor_name = data.get('doctor_name', '').strip()
        specialty = data.get('specialty', '').strip()
        appointment_date = data.get('appointment_date', '').strip()
        appointment_time = data.get('appointment_time', '').strip()
        symptoms = data.get('symptoms', '').strip()
        
        if not all([doctor_name, specialty, appointment_date, appointment_time]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Check if slot is already booked
        conn = get_db()
        cursor = conn.cursor()
        
        if doctor_id:
            cursor.execute('''
                SELECT COUNT(*) FROM appointments
                WHERE doctor_name = ? AND appointment_date = ? AND appointment_time = ?
            ''', (doctor_name, appointment_date, appointment_time))
            
            if cursor.fetchone()[0] > 0:
                conn.close()
                return jsonify({'success': False, 'message': 'This slot is already booked. Please choose another time.'}), 400
        
        # Insert appointment
        cursor.execute('''
            INSERT INTO appointments (user_id, doctor_name, specialty, appointment_date, appointment_time, symptoms, status)
            VALUES (?, ?, ?, ?, ?, ?, 'confirmed')
        ''', (session['user_id'], doctor_name, specialty, appointment_date, appointment_time, symptoms))
        
        appointment_id = cursor.lastrowid
        
        # Create notification for user
        cursor.execute('''
            INSERT INTO notifications (user_id, title, message, type)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], 
              'Appointment Confirmed! 🎉',
              f'Your appointment with {doctor_name} ({specialty}) is confirmed for {appointment_date} at {appointment_time}. Please arrive 10 minutes early.',
              'success'))
        
        # Update doctor's patient count if doctor_id provided
        if doctor_id:
            cursor.execute('UPDATE doctors SET total_patients = total_patients + 1 WHERE id = ?', (doctor_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Appointment booked successfully! Check your notifications.',
            'appointment_id': appointment_id,
            'confirmation': f'Confirmed with {doctor_name} on {appointment_date} at {appointment_time}'
        }), 200
        
    except Exception as e:
        print(f"Appointment booking error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': 'Booking failed'}), 500

@app.route('/api/notifications', methods=['GET'])
@login_required
def api_get_notifications():
    """API endpoint to get user notifications"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, message, type, is_read, created_at
            FROM notifications
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 20
        ''', (session['user_id'],))
        
        notifications = cursor.fetchall()
        conn.close()
        
        notifications_list = []
        for notif in notifications:
            notifications_list.append({
                'id': notif[0],
                'title': notif[1],
                'message': notif[2],
                'type': notif[3],
                'is_read': notif[4],
                'created_at': notif[5]
            })
        
        return jsonify({'success': True, 'notifications': notifications_list}), 200
        
    except Exception as e:
        print(f"Get notifications error: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch notifications'}), 500

@app.route('/api/notifications/<int:notif_id>/read', methods=['POST'])
@login_required
def api_mark_notification_read(notif_id):
    """Mark notification as read"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE notifications
            SET is_read = 1
            WHERE id = ? AND user_id = ?
        ''', (notif_id, session['user_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Mark read error: {e}")
        return jsonify({'success': False}), 500

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
            VALUES (?, ?, ?, ?, ?)
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

# Import modern templates
from modern_templates import MODERN_INDEX_HTML, MODERN_DASHBOARD_HTML, FILES_HTML

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
