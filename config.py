"""
Configuration file for AI Healthcare Chatbot
"""

# Database configuration
DATABASE_NAME = "healthcare_chatbot.db"

# Application settings
APP_TITLE = "AI Healthcare Chatbot"
APP_ICON = "🏥"

# Chatbot settings
BOT_NAME = "HealthBot"
MAX_CHAT_HISTORY = 100

# Medical specialties
MEDICAL_SPECIALTIES = [
    "General Medicine",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Orthopedics",
    "Neurology",
    "ENT (Ear, Nose, Throat)",
    "Ophthalmology",
    "Psychiatry",
    "Gynecology"
]

# Time slots for appointments
TIME_SLOTS = [
    "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
    "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"
]

# Common symptoms and their possible conditions
SYMPTOM_DATABASE = {
    "fever": ["Common Cold", "Flu", "Infection", "COVID-19"],
    "headache": ["Migraine", "Tension Headache", "Sinusitis", "Dehydration"],
    "cough": ["Common Cold", "Bronchitis", "Asthma", "Allergies"],
    "chest pain": ["Angina", "Heart Attack", "Gastric Issue", "Muscle Strain"],
    "stomach pain": ["Gastritis", "Ulcer", "Food Poisoning", "Appendicitis"],
    "dizziness": ["Low Blood Pressure", "Dehydration", "Vertigo", "Anemia"],
    "fatigue": ["Anemia", "Thyroid Issues", "Depression", "Sleep Disorder"],
    "rash": ["Allergic Reaction", "Eczema", "Fungal Infection", "Heat Rash"],
    "nausea": ["Food Poisoning", "Pregnancy", "Migraine", "Gastritis"],
    "sore throat": ["Strep Throat", "Tonsillitis", "Common Cold", "Allergies"]
}

# Emergency keywords
EMERGENCY_KEYWORDS = [
    "emergency", "urgent", "severe pain", "chest pain", 
    "difficulty breathing", "unconscious", "bleeding heavily",
    "heart attack", "stroke", "seizure"
]

# Greeting responses
GREETINGS = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"]

# Disclaimer
MEDICAL_DISCLAIMER = """
⚠️ **Medical Disclaimer**: This chatbot provides general health information only. 
It is NOT a substitute for professional medical advice, diagnosis, or treatment. 
Always seek the advice of your physician or qualified healthcare provider with any questions 
you may have regarding a medical condition. In case of emergency, call 911 immediately.
"""
