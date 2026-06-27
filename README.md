# 🏥 AI Healthcare Chatbot - Modern Web Application

A comprehensive, real-time healthcare management system built with Flask, JavaScript, and modern web technologies. This project features AI-powered diagnosis, appointment scheduling, prescription management, vital signs tracking, and an intelligent chatbot assistant.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![SQLite](https://img.shields.io/badge/SQLite-3-orange)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow)
![License](https://img.shields.io/badge/License-MIT-red)

---

## ✨ Features

### 🎯 Core Features
- **User Authentication** - Secure login/registration with session management
- **Dashboard** - Comprehensive health overview with statistics and charts
- **AI Chatbot** - Intelligent health assistant powered by AI
- **Real-time Updates** - WebSocket-based live communication
- **Responsive Design** - Beautiful UI that works on all devices

### 🏥 Healthcare Features
1. **Appointments Management**
   - Book, view, and manage appointments
   - Filter by status (Scheduled, Confirmed, Completed, Cancelled)
   - Search functionality
   - Multiple appointment types (General, Follow-up, Emergency, etc.)

2. **Prescriptions Tracking**
   - View active and past prescriptions
   - Medication details (dosage, frequency, duration)
   - Refill reminders
   - Drug interaction warnings

3. **Vital Signs Monitoring**
   - Record vital signs (BP, heart rate, temperature, oxygen saturation)
   - Trend visualization with Chart.js
   - Health metrics analysis
   - Historical data tracking

4. **Lab Reports**
   - View test results
   - Upload and download reports
   - Filter by test type and status
   - AI-powered result analysis

5. **AI Health Assistant**
   - Natural language processing
   - Symptom checker
   - Health advice and tips
   - Medication information
   - 24/7 availability

### 🔒 Security Features
- Password hashing with SHA-256
- Session-based authentication
- CSRF protection
- SQL injection prevention
- Role-based access control (Admin, Doctor, Patient)

### 📊 Analytics & Insights
- Health metrics dashboard
- Statistical analysis
- Trend visualization
- Personalized health recommendations

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
```bash
cd AI-Healthcare-Chatbot-Web
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Initialize the database**
The database will be automatically created on first run, or you can manually initialize:
```bash
python app.py
```

4. **Run the application**
```bash
python app.py
```

5. **Access the application**
Open your browser and navigate to:
```
http://localhost:5000
```

---

## 📁 Project Structure

```
AI-Healthcare-Chatbot-Web/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── healthcare.db                   # SQLite database (auto-generated)
├── README.md                       # This file
│
├── static/                         # Static files
│   ├── css/
│   │   └── style.css              # Main stylesheet with animations
│   ├── js/
│   │   └── main.js                # JavaScript functionality
│   └── img/                       # Images (optional)
│
└── templates/                      # HTML templates
    ├── index.html                 # Landing page
    ├── login.html                 # Login/Register page
    ├── dashboard.html             # Main dashboard
    ├── appointments.html          # Appointments management
    ├── prescriptions.html         # Prescriptions tracking
    ├── vital_signs.html           # Vital signs monitoring
    ├── lab_reports.html           # Lab reports viewer
    └── chat.html                  # AI chatbot interface
```

---

## 🎨 Technologies Used

### Backend
- **Flask** - Python web framework
- **Flask-SocketIO** - Real-time WebSocket communication
- **Flask-CORS** - Cross-Origin Resource Sharing
- **SQLite** - Lightweight database
- **hashlib** - Password encryption

### Frontend
- **HTML5** - Structure and semantics
- **CSS3** - Modern styling with animations and gradients
- **JavaScript (ES6+)** - Interactive functionality
- **Chart.js** - Data visualization
- **WebSocket API** - Real-time chat

### Design
- **Custom CSS** - No frameworks, pure CSS with CSS Variables
- **Responsive Design** - Mobile-first approach
- **Modern UI/UX** - Gradients, shadows, animations
- **Glassmorphism** - Frosted glass effects

---

## 📊 Database Schema

### Tables

1. **users**
   - id (PK)
   - username (unique)
   - password_hash
   - email
   - full_name
   - role (admin, doctor, patient)
   - is_active
   - created_at

2. **patients**
   - id (PK)
   - user_id (FK)
   - name
   - age
   - gender
   - phone
   - email
   - blood_group
   - allergies
   - chronic_conditions
   - created_at

3. **appointments**
   - id (PK)
   - patient_id (FK)
   - doctor_name
   - specialty
   - appointment_date
   - appointment_time
   - symptoms
   - status
   - created_at

4. **prescriptions**
   - id (PK)
   - patient_id (FK)
   - medication_name
   - dosage
   - frequency
   - start_date
   - end_date
   - status
   - notes
   - created_at

5. **vital_signs**
   - id (PK)
   - patient_id (FK)
   - blood_pressure_systolic
   - blood_pressure_diastolic
   - heart_rate
   - temperature
   - oxygen_saturation
   - glucose_level
   - weight
   - bmi
   - recorded_at

6. **lab_reports**
   - id (PK)
   - patient_id (FK)
   - test_name
   - test_date
   - result_value
   - normal_range
   - status
   - notes
   - created_at

7. **chat_history**
   - id (PK)
   - session_id
   - user_id (FK)
   - message
   - sender
   - timestamp

---

## 🔑 Default Credentials

### Admin Account
- **Username:** admin
- **Password:** admin123

### Test Patient Account
- **Username:** patient1
- **Password:** password123

> **Note:** Change these credentials in production!

---

## 🌐 API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration
- `POST /api/logout` - User logout

### Patients
- `GET /api/patients` - Get all patients
- `POST /api/patients` - Create new patient
- `GET /api/patients/<id>` - Get patient details
- `PUT /api/patients/<id>` - Update patient
- `DELETE /api/patients/<id>` - Delete patient

### Appointments
- `GET /api/appointments` - Get all appointments
- `POST /api/appointments` - Create appointment
- `PUT /api/appointments/<id>` - Update appointment
- `DELETE /api/appointments/<id>` - Cancel appointment

### Prescriptions
- `GET /api/prescriptions` - Get all prescriptions
- `POST /api/prescriptions` - Add prescription

### Vital Signs
- `GET /api/vital-signs` - Get vital signs history
- `POST /api/vital-signs` - Record vital signs

### Lab Reports
- `GET /api/lab-reports` - Get all lab reports
- `POST /api/lab-reports` - Add lab report

### Statistics
- `GET /api/statistics` - Get system statistics

### WebSocket Events
- `connect` - Client connection
- `send_message` - Send chat message
- `receive_message` - Receive AI response

---

## 💡 Usage Examples

### Booking an Appointment
```javascript
const appointmentData = {
    patient_id: 1,
    doctor_name: "Dr. Smith",
    specialty: "Cardiology",
    appointment_date: "2026-07-01",
    appointment_time: "10:00 AM",
    symptoms: "Chest pain",
    status: "Scheduled"
};

fetch('/api/appointments', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(appointmentData)
});
```

### Recording Vital Signs
```javascript
const vitalSignsData = {
    patient_id: 1,
    blood_pressure_systolic: 120,
    blood_pressure_diastolic: 80,
    heart_rate: 72,
    temperature: 98.6,
    oxygen_saturation: 98,
    weight: 70.5
};

fetch('/api/vital-signs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(vitalSignsData)
});
```

### Chat with AI Assistant
```javascript
const socket = io();

socket.on('connect', () => {
    console.log('Connected to AI Assistant');
});

socket.emit('send_message', {
    message: 'What should I do for a headache?'
});

socket.on('receive_message', (data) => {
    console.log('AI Response:', data.message);
});
```

---

## 🎯 Key Features Explained

### 1. AI-Powered Diagnosis
The chatbot uses natural language processing to understand symptoms and provide preliminary health advice. It can:
- Analyze symptoms
- Suggest possible conditions
- Recommend when to see a doctor
- Provide general health information

### 2. Real-Time Updates
Using WebSocket technology, the application provides:
- Instant chat responses
- Live notifications
- Real-time data updates
- Synchronized multi-device experience

### 3. Data Visualization
Chart.js integration provides:
- Vital signs trends
- Health score tracking
- Appointment statistics
- Visual health insights

### 4. Responsive Design
The application adapts to:
- Desktop computers
- Tablets
- Mobile phones
- Different screen orientations

---

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file in the root directory:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_PATH=healthcare.db
PORT=5000
```

### Database Configuration
Edit `app.py` to change database settings:
```python
app.config['DATABASE'] = 'healthcare.db'
```

### Security Settings
Update secret key in production:
```python
app.config['SECRET_KEY'] = secrets.token_hex(32)
```

---

## 🧪 Testing

### Manual Testing
1. Test user registration and login
2. Create test appointments
3. Record sample vital signs
4. Add prescriptions
5. Upload lab reports
6. Chat with AI assistant

### Automated Testing (Future Enhancement)
```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/
```

---

## 📈 Future Enhancements

- [ ] Advanced AI diagnosis with machine learning
- [ ] Integration with wearable devices
- [ ] Telemedicine video consultations
- [ ] Prescription refill automation
- [ ] Insurance claim management
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Email/SMS notifications
- [ ] PDF report generation
- [ ] Calendar synchronization
- [ ] Payment gateway integration
- [ ] HIPAA compliance features

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Database not found
```bash
# Solution: Initialize database
python app.py
```

**Issue:** Port 5000 already in use
```bash
# Solution: Use a different port
python app.py --port 5001
```

**Issue:** CSS/JS not loading
```bash
# Solution: Clear browser cache or hard refresh (Ctrl+Shift+R)
```

**Issue:** WebSocket connection failed
```bash
# Solution: Check if Flask-SocketIO is installed
pip install flask-socketio
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Healthcare AI Team** - Initial work

---

## 🙏 Acknowledgments

- Flask documentation and community
- Chart.js for data visualization
- WebSocket protocol for real-time communication
- All healthcare professionals who inspired this project

---

## 📞 Support

For support, email support@healthcareai.com or open an issue in the repository.

---

## ⚠️ Disclaimer

**IMPORTANT:** This application is for educational and demonstration purposes only. It should NOT be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

For medical emergencies, call 911 immediately.

---

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

---

**Made with ❤️ for better healthcare**
