# 🏥 AI Healthcare Chatbot

A comprehensive, real-time AI-powered healthcare chatbot built with Python and SQLite. This application provides symptom checking, appointment booking, patient management, and general health information through an intuitive web interface.

## 🌟 Features

### 1. **Intelligent Symptom Checking** 🩺
- Natural language symptom analysis
- Severity assessment (Mild, Moderate, High)
- Possible condition suggestions
- Personalized health advice
- Emergency detection and alerts

### 2. **Appointment Management** 📅
- Easy appointment booking with specialists
- View and track appointments
- Multiple medical specialties
- Time slot availability checking
- Appointment history tracking

### 3. **Patient Registration & Management** 👤
- Secure patient registration
- Medical history tracking
- Allergy and chronic condition records
- Quick patient login system

### 4. **Interactive Chatbot** 💬
- Natural language processing
- Context-aware conversations
- Intent recognition
- Multiple conversation flows
- Chat history storage

### 5. **Health Information** 📚
- Medical condition information
- Medication safety tips
- General health advice
- Emergency hotline numbers

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/AI-Healthcare-Chatbot.git
cd AI-Healthcare-Chatbot
```

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

4. **Open your browser:**
The application will automatically open at `http://localhost:8501`

## 📋 Usage Guide

### For New Users

1. **Register as a Patient:**
   - Open the sidebar
   - Click on "New Patient Registration"
   - Fill in your details (name, age, phone, etc.)
   - Click "Register"

2. **Login:**
   - Enter your phone number in the "Patient Login" section
   - Click "Login"

3. **Check Symptoms:**
   - Type your symptoms in the chat (e.g., "I have a headache and fever")
   - Get instant analysis and health advice

4. **Book an Appointment:**
   - Use the "Book Appointment" form in the sidebar
   - Select specialty, date, and time
   - Describe your symptoms
   - Submit the booking

5. **View Appointments:**
   - Click "View My Appointments" in the sidebar
   - See all your scheduled appointments

### Quick Actions

Use the quick action buttons for common tasks:
- 🩺 **Check Symptoms** - Start symptom analysis
- 📅 **Book Appointment** - Schedule a doctor visit
- 📚 **Health Info** - Get health information
- ❓ **Help** - View help and instructions

## 🗄️ Database Schema

The application uses SQLite with the following tables:

### Patients Table
- patient_id (Primary Key)
- name, age, gender, phone
- email, address, blood_group
- allergies, chronic_conditions
- created_at

### Appointments Table
- appointment_id (Primary Key)
- patient_id (Foreign Key)
- patient_name, specialty
- appointment_date, appointment_time
- symptoms, status
- created_at

### Chat History Table
- chat_id (Primary Key)
- session_id, patient_id
- message_type, message
- timestamp

### Symptoms Log Table
- log_id (Primary Key)
- patient_id, symptoms
- severity, possible_conditions
- advice, logged_at

## 🏗️ Project Structure

```
AI-Healthcare-Chatbot/
├── app.py                  # Main Streamlit application
├── chatbot_engine.py       # NLP and chatbot logic
├── database.py             # SQLite database operations
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
└── healthcare_chatbot.db  # SQLite database (auto-created)
```

## 🔧 Configuration

Edit `config.py` to customize:
- Database name
- Medical specialties
- Time slots
- Symptom database
- Emergency keywords
- Application settings

## 💡 Example Conversations

**Symptom Checking:**
```
User: I have a headache and fever
Bot: [Analyzes symptoms, suggests possible conditions, provides advice]
```

**Appointment Booking:**
```
User: I want to book an appointment
Bot: [Guides through booking process with available specialties]
```

**Health Information:**
```
User: Tell me about diabetes
Bot: [Provides detailed information about diabetes]
```

## 📊 Features Breakdown

### Medical Specialties Available
- General Medicine
- Cardiology
- Dermatology
- Pediatrics
- Orthopedics
- Neurology
- ENT (Ear, Nose, Throat)
- Ophthalmology
- Psychiatry
- Gynecology

### Time Slots
- Morning: 9:00 AM - 12:00 PM
- Afternoon: 2:00 PM - 5:00 PM

### Symptom Analysis
The chatbot can analyze common symptoms including:
- Fever, headache, cough
- Chest pain, stomach pain
- Dizziness, fatigue
- Rash, nausea, sore throat
- And many more...

## ⚠️ Important Disclaimer

**This chatbot provides general health information only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.**

- Always seek the advice of your physician or qualified healthcare provider
- In case of emergency, call 911 immediately
- Do not use this chatbot for medical emergencies

## 🛡️ Security & Privacy

- Patient data stored locally in SQLite database
- No external API calls for sensitive data
- Phone number-based authentication
- Chat history maintained securely

## 🔄 Future Enhancements

Potential improvements:
- [ ] AI/ML model integration for better diagnosis
- [ ] Email/SMS notifications
- [ ] Multi-language support
- [ ] Prescription management
- [ ] Lab report integration
- [ ] Doctor dashboard
- [ ] Video consultation scheduling
- [ ] Insurance integration
- [ ] Mobile app version

## 🐛 Troubleshooting

**Issue: Database not found**
- The database is created automatically on first run
- Check write permissions in the project directory

**Issue: Streamlit not running**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (3.8+ required)

**Issue: Module import errors**
- Verify you're in the correct directory
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact: healthcare-chatbot-support@example.com

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Streamlit for the web interface
- SQLite for lightweight database management
- Python for backend processing

## 👨‍💻 Author

Created with ❤️ for improving healthcare accessibility

---

**⚡ Start using the AI Healthcare Chatbot today and take control of your health management!**

```bash
streamlit run app.py
```

**Happy Health Monitoring! 🏥💙**
