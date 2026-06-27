"""
Chatbot Engine for AI Healthcare Chatbot
Handles natural language processing, intent recognition, and response generation
"""

import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import config


class HealthcareChatbot:
    """Main chatbot engine with NLP capabilities"""
    
    def __init__(self):
        """Initialize chatbot engine"""
        self.current_context = {}
        self.conversation_state = "initial"
        self.user_data = {}
        
    def process_message(self, message: str, session_context: Dict = None) -> Tuple[str, str]:
        """
        Process user message and generate appropriate response
        Returns: (response_text, intent)
        """
        message = message.lower().strip()
        
        # Update context if provided
        if session_context:
            self.current_context.update(session_context)
        
        # Check for emergency keywords first
        if self._is_emergency(message):
            return self._handle_emergency(), "emergency"
        
        # Detect intent
        intent = self._detect_intent(message)
        
        # Generate response based on intent
        if intent == "greeting":
            return self._handle_greeting(), intent
        elif intent == "symptom_check":
            return self._handle_symptom_check(message), intent
        elif intent == "book_appointment":
            return self._handle_appointment_booking(), intent
        elif intent == "view_appointments":
            return self._handle_view_appointments(), intent
        elif intent == "health_info":
            return self._handle_health_info(message), intent
        elif intent == "registration":
            return self._handle_registration(), intent
        elif intent == "medication_info":
            return self._handle_medication_info(message), intent
        elif intent == "help":
            return self._handle_help(), intent
        elif intent == "thanks":
            return self._handle_thanks(), intent
        else:
            return self._handle_general_query(message), "general"
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        message_lower = message.lower()
        
        # Greeting
        if any(greeting in message_lower for greeting in config.GREETINGS):
            return "greeting"
        
        # Symptom checking
        symptom_keywords = ["symptom", "feeling", "pain", "hurt", "sick", "ache", 
                           "fever", "cough", "headache", "problem", "issue"]
        if any(keyword in message_lower for keyword in symptom_keywords):
            return "symptom_check"
        
        # Appointment booking
        appointment_keywords = ["appointment", "book", "schedule", "reserve", "doctor visit"]
        if any(keyword in message_lower for keyword in appointment_keywords):
            return "book_appointment"
        
        # View appointments
        view_keywords = ["my appointment", "check appointment", "appointment status", "view appointment"]
        if any(keyword in message_lower for keyword in view_keywords):
            return "view_appointments"
        
        # Registration
        registration_keywords = ["register", "sign up", "new patient", "create account"]
        if any(keyword in message_lower for keyword in registration_keywords):
            return "registration"
        
        # Medication info
        medication_keywords = ["medicine", "medication", "drug", "prescription", "dosage"]
        if any(keyword in message_lower for keyword in medication_keywords):
            return "medication_info"
        
        # Health information
        health_keywords = ["what is", "tell me about", "information about", "explain"]
        if any(keyword in message_lower for keyword in health_keywords):
            return "health_info"
        
        # Help
        help_keywords = ["help", "what can you do", "how to", "assist"]
        if any(keyword in message_lower for keyword in help_keywords):
            return "help"
        
        # Thanks
        thanks_keywords = ["thank", "thanks", "appreciate"]
        if any(keyword in message_lower for keyword in thanks_keywords):
            return "thanks"
        
        return "general"
    
    def _is_emergency(self, message: str) -> bool:
        """Check if message contains emergency keywords"""
        return any(keyword in message.lower() for keyword in config.EMERGENCY_KEYWORDS)
    
    def _handle_emergency(self) -> str:
        """Handle emergency situations"""
        return """
🚨 **EMERGENCY DETECTED** 🚨

If you are experiencing a medical emergency:
- **Call 911 immediately** (US)
- Or go to the nearest emergency room
- For chest pain or difficulty breathing, DO NOT WAIT

This chatbot cannot handle emergencies. Please seek immediate medical attention!

**Emergency Hotlines:**
- Emergency: 911
- Poison Control: 1-800-222-1222
- Suicide Prevention: 988
"""
    
    def _handle_greeting(self) -> str:
        """Handle greeting messages"""
        return f"""
👋 Hello! I'm **{config.BOT_NAME}**, your AI Healthcare Assistant.

I can help you with:
✅ Symptom checking and health advice
✅ Booking medical appointments
✅ Viewing your appointments
✅ General health information
✅ Patient registration

How can I assist you today?

💡 **Tip**: Try saying things like:
- "I have a headache and fever"
- "Book an appointment"
- "Tell me about diabetes"
- "I want to register as a new patient"
"""
    
    def _handle_symptom_check(self, message: str) -> str:
        """Analyze symptoms and provide advice"""
        # Extract symptoms from message
        symptoms = self._extract_symptoms(message)
        
        if not symptoms:
            return """
🩺 **Symptom Checker**

Please describe your symptoms in detail. For example:
- "I have a fever and cough"
- "I'm experiencing chest pain and dizziness"
- "I have a headache and nausea"

What symptoms are you experiencing?
"""
        
        # Analyze symptoms
        possible_conditions = self._analyze_symptoms(symptoms)
        severity = self._assess_severity(symptoms)
        advice = self._generate_advice(symptoms, severity)
        
        response = f"""
🩺 **Symptom Analysis**

**Symptoms detected:** {', '.join(symptoms)}
**Severity level:** {severity}

**Possible conditions:**
{possible_conditions}

**Recommended actions:**
{advice}

{config.MEDICAL_DISCLAIMER}

Would you like to book an appointment with a doctor?
"""
        return response
    
    def _extract_symptoms(self, message: str) -> List[str]:
        """Extract symptoms from user message"""
        detected_symptoms = []
        message_lower = message.lower()
        
        # Check against known symptoms
        for symptom in config.SYMPTOM_DATABASE.keys():
            if symptom in message_lower:
                detected_symptoms.append(symptom)
        
        return detected_symptoms
    
    def _analyze_symptoms(self, symptoms: List[str]) -> str:
        """Analyze symptoms and suggest possible conditions"""
        all_conditions = {}
        
        for symptom in symptoms:
            if symptom in config.SYMPTOM_DATABASE:
                conditions = config.SYMPTOM_DATABASE[symptom]
                for condition in conditions:
                    all_conditions[condition] = all_conditions.get(condition, 0) + 1
        
        # Sort conditions by frequency
        sorted_conditions = sorted(all_conditions.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_conditions:
            result = ""
            for condition, count in sorted_conditions[:3]:
                result += f"• {condition}\n"
            return result
        else:
            return "• Requires professional evaluation\n"
    
    def _assess_severity(self, symptoms: List[str]) -> str:
        """Assess severity of symptoms"""
        severe_symptoms = ["chest pain", "difficulty breathing", "severe pain"]
        
        if any(symptom in severe_symptoms for symptom in symptoms):
            return "⚠️ **HIGH** - Requires immediate attention"
        elif len(symptoms) >= 3:
            return "🟡 **MODERATE** - Should see a doctor soon"
        else:
            return "🟢 **MILD** - Monitor symptoms"
    
    def _generate_advice(self, symptoms: List[str], severity: str) -> str:
        """Generate health advice based on symptoms"""
        if "HIGH" in severity:
            return """
1. ⚠️ Seek immediate medical attention
2. Go to emergency room or call 911
3. Do not drive yourself if possible
"""
        elif "MODERATE" in severity:
            return """
1. Schedule an appointment with your doctor within 24-48 hours
2. Monitor symptoms closely
3. Rest and stay hydrated
4. Avoid strenuous activities
5. Keep track of any changes in symptoms
"""
        else:
            return """
1. Rest and stay hydrated
2. Take over-the-counter medications if needed
3. Monitor symptoms for 2-3 days
4. If symptoms worsen, consult a doctor
5. Maintain a healthy diet and get adequate sleep
"""
    
    def _handle_appointment_booking(self) -> str:
        """Handle appointment booking requests"""
        return """
📅 **Book an Appointment**

I'll help you schedule an appointment with a doctor.

To proceed, please provide:
1. Your phone number (for identification)
2. Preferred medical specialty
3. Preferred date and time

Or use the **Appointment Booking** section in the sidebar to book directly!

Available specialties:
""" + "\n".join([f"• {specialty}" for specialty in config.MEDICAL_SPECIALTIES])
    
    def _handle_view_appointments(self) -> str:
        """Handle view appointments requests"""
        return """
📋 **View Your Appointments**

To view your appointments, please:
1. Enter your phone number in the sidebar
2. Click on "View My Appointments"

You'll be able to see all your scheduled appointments with details including:
- Date and time
- Medical specialty
- Symptoms
- Status
"""
    
    def _handle_health_info(self, message: str) -> str:
        """Provide general health information"""
        message_lower = message.lower()
        
        # Simple health information database
        health_topics = {
            "diabetes": """
📚 **Diabetes Information**

**What is Diabetes?**
Diabetes is a chronic condition that affects how your body processes blood sugar (glucose).

**Types:**
• Type 1: Body doesn't produce insulin
• Type 2: Body doesn't use insulin properly
• Gestational: Occurs during pregnancy

**Symptoms:**
• Increased thirst and urination
• Extreme fatigue
• Blurred vision
• Slow healing wounds

**Management:**
• Regular blood sugar monitoring
• Healthy diet and exercise
• Medication as prescribed
• Regular doctor visits
""",
            "hypertension": """
📚 **Hypertension (High Blood Pressure) Information**

**What is Hypertension?**
A condition where blood pressure in arteries is persistently elevated.

**Risk Factors:**
• Age, family history
• Obesity, physical inactivity
• High salt intake
• Stress, smoking

**Symptoms:**
• Often no symptoms (silent killer)
• Severe cases: headaches, dizziness

**Prevention:**
• Maintain healthy weight
• Regular exercise
• Reduce sodium intake
• Limit alcohol
• Manage stress
""",
            "asthma": """
📚 **Asthma Information**

**What is Asthma?**
A chronic respiratory condition causing inflammation and narrowing of airways.

**Symptoms:**
• Wheezing
• Shortness of breath
• Chest tightness
• Coughing

**Triggers:**
• Allergens (pollen, dust)
• Exercise
• Cold air
• Respiratory infections

**Management:**
• Use prescribed inhalers
• Avoid triggers
• Regular monitoring
• Emergency action plan
"""
        }
        
        # Check if question is about a known topic
        for topic, info in health_topics.items():
            if topic in message_lower:
                return info
        
        # General response
        return """
📚 **Health Information**

I can provide information about various health topics including:
• Diabetes
• Hypertension (High Blood Pressure)
• Asthma
• Heart Disease
• Mental Health
• Nutrition and Diet

Please ask about a specific health condition, and I'll provide detailed information.

Example: "Tell me about diabetes"
"""
    
    def _handle_registration(self) -> str:
        """Handle patient registration"""
        return """
📝 **New Patient Registration**

Welcome! To register as a new patient, please use the **Patient Registration** form in the sidebar.

You'll need to provide:
- Full Name
- Age
- Gender
- Phone Number (for identification)
- Email Address (optional)
- Address (optional)
- Blood Group (optional)
- Known Allergies (optional)
- Chronic Conditions (optional)

Once registered, you'll be able to:
✅ Book appointments
✅ Track your medical history
✅ Access symptom checking
✅ View appointment records
"""
    
    def _handle_medication_info(self, message: str) -> str:
        """Provide medication information"""
        return """
💊 **Medication Information**

**Important:** I cannot prescribe medications or provide specific dosage information. 
Please consult with your healthcare provider or pharmacist.

**General Medication Safety Tips:**
1. Always take medications as prescribed
2. Don't share medications with others
3. Store medications properly
4. Check expiration dates
5. Be aware of potential drug interactions
6. Never stop medications abruptly without consulting your doctor

**For specific medication information:**
- Consult your pharmacist
- Read the medication guide
- Use resources like FDA.gov or drugs.com
- Talk to your healthcare provider

Would you like to book an appointment to discuss your medications with a doctor?
"""
    
    def _handle_help(self) -> str:
        """Provide help information"""
        return """
❓ **How I Can Help You**

I'm your AI Healthcare Assistant! Here's what I can do:

**1. 🩺 Symptom Checking**
   - Describe your symptoms
   - Get possible diagnoses
   - Receive health advice

**2. 📅 Appointment Management**
   - Book appointments with specialists
   - View your scheduled appointments
   - Check available time slots

**3. 📝 Patient Registration**
   - Register as a new patient
   - Update your health profile
   - Maintain medical records

**4. 📚 Health Information**
   - Learn about medical conditions
   - Get medication safety tips
   - Access health resources

**5. 🚨 Emergency Guidance**
   - Recognize emergency situations
   - Provide emergency hotline numbers

**How to Use:**
Just type your question or concern naturally, like:
- "I have a headache"
- "Book an appointment for cardiology"
- "Tell me about diabetes"

**Need more help?** Just ask me anything!
"""
    
    def _handle_thanks(self) -> str:
        """Handle thank you messages"""
        return """
😊 You're welcome! I'm glad I could help.

Is there anything else you'd like assistance with?
- Check more symptoms
- Book an appointment
- Get health information

Feel free to ask anytime!
"""
    
    def _handle_general_query(self, message: str) -> str:
        """Handle general queries that don't match specific intents"""
        return """
I understand you have a question, but I'm not quite sure how to help with that specific query.

I specialize in:
🩺 Symptom checking and health advice
📅 Booking and managing appointments
📚 General health information
📝 Patient registration

Could you please rephrase your question or let me know which of these areas you need help with?

For example, you could say:
- "I'm feeling sick with a fever"
- "I want to book an appointment"
- "Tell me about high blood pressure"
"""


# Create chatbot instance
chatbot = HealthcareChatbot()
