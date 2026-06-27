# 🏥 AI Healthcare Chatbot - Production Ready

A **comprehensive, enterprise-grade** AI-powered healthcare platform with **advanced real-time features**, built with Python, SQLite, and Streamlit. Features include **AI diagnosis assistant**, **prescription management**, **lab reports**, **vital signs monitoring**, **telemedicine support**, and **emergency services**.

## 🌟 Core Features

### 🔐 **Authentication & Security**
- Secure login with SHA-256 password hashing
- Role-based access control (Admin & Patient)
- Session management and user authentication
- Activity logging and audit trail

### 1. **🤖 AI-Powered Medical Assistant**
- **Advanced pattern recognition** for diseases
- **Critical symptom detection** with emergency alerts
- **Confidence scoring** for diagnoses
- **Specialist referral** recommendations
- **Medical report analysis** with AI insights
- **Follow-up question generation** for better diagnosis

### 2. **💊 Prescription Management System**
- Complete medication tracking
- Dosage and frequency management
- **Refill reminders** and alerts
- Prescription status tracking (Active/Completed/Expired)
- Side effects documentation
- Export prescriptions to CSV/JSON
- Days remaining calculations

### 3. **🔬 Lab Reports & Test Results**
- Upload and store lab reports
- Track test history with trends
- **AI-powered report analysis**
- Normal/Abnormal status indicators
- Visual trends and charts
- Test result comparisons
- Export functionality

### 4. **❤️ Real-Time Vital Signs Monitoring**
- Blood pressure tracking (Systolic/Diastolic)
- Heart rate monitoring (BPM)
- Body temperature tracking
- Oxygen saturation (SpO2)
- Glucose level monitoring
- BMI calculation and tracking
- **Real-time health status** indicators
- **Trend visualization** with charts
- Historical data analysis

### 5. **👨‍⚕️ Doctor Directory & Profiles**
- Browse doctors by specialty
- Doctor profiles with qualifications
- Experience and rating system
- Consultation fee information
- Availability calendar
- Book appointments with specific doctors
- Review and rating system

### 6. **📹 Video Consultation Management**
- Schedule video consultations
- Meeting link generation
- Consultation history
- Duration tracking
- Recording storage (database ready)

### 7. **🚨 Emergency Alert System**
- **One-tap emergency services**
- Emergency contact management
- Location-aware hospital finder
- Medical ID quick access
- Critical symptom recognition
- Emergency hotline directory
- FAST stroke detection guide

### 8. **📊 Advanced Analytics & Insights**
- Real-time health dashboard
- Predictive health analytics
- Trend analysis for all metrics
- System health monitoring
- Activity summary reports
- Export all data types

### 9. **🏥 Complete Patient Management**
- Patient registration and profiles
- Medical history tracking
- Allergy and condition documentation
- Emergency contacts
- Insurance information storage
- Appointment history

### 10. **🎛️ Comprehensive Admin Dashboard**
- Real-time statistics
- Patient management (CRUD)
- Appointment management
- User account management
- Activity logs and audit trail
- System health monitoring
- Data export capabilities

## 🚀 Advanced Real-Time Features

✅ **Auto-refresh** every 30 seconds
✅ **Live countdown timers** for appointments
✅ **Real-time notifications** and alerts
✅ **Instant search** with live results
✅ **Activity tracking** with full audit trail
✅ **Data export** (CSV/JSON) for all modules
✅ **System health** monitoring
✅ **Time-ago formatting** for all timestamps
✅ **Upcoming appointments** widget
✅ **Notification badges** for alerts

## 📂 Project Structure

```
AI-Healthcare-Chatbot/
├── app.py                          # 🏠 Landing page
├── auth.py                         # 🔐 Authentication module
├── database.py                     # 🗄️ Database with 13+ tables
├── chatbot_engine.py               # 🤖 NLP chatbot engine
├── advanced_ai.py                  # 🧠 AI diagnosis assistant
├── utils.py                        # 🔧 Real-time utilities
├── config.py                       # ⚙️ Configuration
├── requirements.txt                # 📦 Dependencies
├── pages/
│   ├── 1_🔐_Login.py              # Login & Registration
│   ├── 2_🎛️_Admin_Dashboard.py    # Admin Panel
│   ├── 3_🏥_Patient_Portal.py     # Patient Interface
│   ├── 4_💊_Prescriptions.py      # Medication Management
│   ├── 5_🔬_Lab_Reports.py        # Test Results
│   ├── 6_❤️_Vital_Signs.py        # Health Monitoring
│   ├── 7_👨‍⚕️_Doctors.py           # Doctor Directory
│   └── 8_🚨_Emergency.py          # Emergency Services
└── README.md                       # 📚 Documentation
```
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

### 6. **Admin Dashboard** 🎛️
- **Complete Patient Management** - View, search, and manage patient records
- **Appointment Management** - Update appointment status, manage bookings
- **User Management** - Create users, activate/deactivate accounts
- **Real-time Statistics** - Dashboard with key metrics and insights
- **Analytics** - Track patients, appointments, and system usage

### 7. **Multi-Page Navigation** 📄
- **Home Page** - Landing page with features overview
- **Login Page** - Secure authentication portal
- **Admin Dashboard** - Complete admin panel with analytics
- **Patient Portal** - Interactive chatbot and patient services

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

## 🔑 Default Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`

### Patient Account
- Create your own account using the registration form on the login page

## 📋 Usage Guide

### For Patients

1. **Register/Login:**
   - Visit the Login page
   - Create a new account or login with existing credentials
   - You'll be redirected to the Patient Portal

2. **Create Patient Profile:**
   - Link your account to a patient profile using your phone number
   - Or create a new patient profile with your medical information

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

### For Administrators

1. **Login as Admin:**
   - Use admin credentials on the Login page
   - You'll be redirected to the Admin Dashboard

2. **Manage Patients:**
   - View all registered patients
   - Search and filter patient records
   - Delete patient records if needed

3. **Manage Appointments:**
   - View all appointments across the system
   - Update appointment status (Scheduled/Completed/Cancelled)
   - Filter by status and date
   - Delete appointments

4. **Manage Users:**
   - Create new user accounts (admin or patient)
   - Activate/deactivate user accounts
   - View user statistics and activity

5. **View Analytics:**
   - Dashboard with real-time statistics
   - Track system usage and patient activity
   - Monitor appointments and health checks

### Quick Actions

Use the quick action buttons for common tasks:
- 🩺 **Check Symptoms** - Start symptom analysis
- 📅 **Book Appointment** - Schedule a doctor visit
- 📚 **Health Info** - Get health information
- ❓ **Help** - View help and instructions

## 🗄️ Database Schema

The application uses SQLite with the following tables:

### Users Table
- user_id (Primary Key)
- username, password_hash, email
- role (admin/patient), full_name
- is_active, created_at, last_login

### Patients Table
- patient_id (Primary Key)
- user_id (Foreign Key to users)
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
├── app.py                      # Home page / Landing page
├── auth.py                     # Authentication module
├── chatbot_engine.py           # NLP and chatbot logic
├── database.py                 # SQLite database operations
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── pages/                      # Multi-page application
│   ├── 1_🔐_Login.py          # Login & Registration page
│   ├── 2_🎛️_Admin_Dashboard.py # Admin dashboard
│   └── 3_🏥_Patient_Portal.py # Patient chatbot interface
├── README.md                   # Documentation
└── healthcare_chatbot.db       # SQLite database (auto-created)
```

## 🔧 Configuration

Edit `config.py` to customize:
- Database name
- Medical specialties
- Time slots
- Symptom database
- Emergency keywords
- Application settings

## 🎨 UI/UX Features

- **Modern Gradient Design** - Beautiful gradient cards and buttons
- **Responsive Layout** - Works on all screen sizes
- **Smooth Animations** - Fade-in effects and hover transitions
- **Intuitive Navigation** - Easy-to-use multi-page interface
- **Real-time Updates** - Live statistics and data refresh
- **Professional Styling** - Clean, medical-themed color scheme

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

- **Password Hashing** - SHA-256 encryption for all passwords
- **Role-Based Access Control** - Separate admin and patient permissions
- **Session Management** - Secure session handling with Streamlit
- **Input Validation** - Protection against malicious inputs
- **SQL Injection Prevention** - Parameterized database queries
- **Patient data stored locally** in SQLite database
- **No external API calls** for sensitive data
- **Chat history maintained** securely with user association

## 🔄 Future Enhancements

Potential improvements:
- [ ] Advanced AI/ML models for better diagnosis (TensorFlow/PyTorch)
- [ ] Email/SMS notifications for appointments
- [ ] Multi-language support (i18n)
- [ ] Video consultation integration
- [ ] Lab report upload and management
- [ ] Prescription tracking system
- [ ] Insurance integration
- [ ] Doctor profiles and ratings
- [ ] Payment gateway integration
- [ ] Mobile app (React Native/Flutter)
- [ ] Export reports to PDF
- [ ] Advanced analytics dashboard
- [ ] API for third-party integrations
- [ ] Two-factor authentication (2FA)
- [ ] HIPAA compliance features
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
