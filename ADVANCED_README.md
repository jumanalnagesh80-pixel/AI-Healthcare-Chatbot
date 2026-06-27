# 🏥 Advanced AI Healthcare System

## 🎯 Complete Healthcare Management Platform

A **full-featured healthcare system** with AI-powered chatbot, admin panel, patient management, and comprehensive health tracking.

---

## ✨ Features

### 👤 **User Features**
- ✅ User Registration & Login
- ✅ AI Health Consultation (24/7)
- ✅ Book Doctor Appointments
- ✅ View Medical Records
- ✅ Manage Prescriptions
- ✅ Access Lab Reports
- ✅ Track Vital Signs (BP, Heart Rate, Weight, BMI, Temperature)
- ✅ Health Dashboard with Statistics
- ✅ Chat History Tracking

### 🔐 **Admin Features**
- ✅ Admin Login & Dashboard
- ✅ User Management (View all patients)
- ✅ Appointment Management (View, Update status, Add diagnosis)
- ✅ System Statistics & Analytics
- ✅ View Recent Users & Appointments
- ✅ Complete System Overview

### 🤖 **AI Health Assistant**
- Emergency Detection & Alerts
- Symptom Analysis
- Health Advice for:
  - Fever, Headache, Cough, Cold, Flu
  - Stomach Pain, Digestive Issues
  - Stress, Anxiety, Mental Health
  - Diabetes, Blood Pressure Management
  - Medication Guidance
  - Appointment Booking Assistance

---

## 🚀 Quick Start (Mac M2)

### **Step 1: Download**
```bash
git clone -b advanced-healthcare-system https://github.com/jumanalnagesh80-pixel/AI-Healthcare-Chatbot.git
cd AI-Healthcare-Chatbot
```

### **Step 2: Install Dependencies**
```bash
pip3 install -r requirements_advanced.txt
```

### **Step 3: Run Application**
```bash
python3 app_advanced.py
```

### **Step 4: Access the System**
Open browser: **http://127.0.0.1:5000**

---

## 🔐 Login Credentials

### **Admin Access**
- URL: `http://127.0.0.1:5000/admin`
- Email: `admin@healthcare.com`
- Password: `admin123`

### **User Access**
- URL: `http://127.0.0.1:5000`
- Register new account or use existing

---

## 📊 System Architecture

### **Database Schema (8 Tables)**

1. **users** - Patient information
   - id, name, email, password, phone, age, gender, blood_group, address

2. **admins** - Admin accounts
   - id, name, email, password, role

3. **appointments** - All appointments
   - id, user_id, doctor_name, specialty, date, time, status, symptoms, diagnosis, notes

4. **chats** - AI chat history
   - id, user_id, message, response, created_at

5. **medical_records** - Health records
   - id, user_id, record_type, title, description, doctor_name, date

6. **prescriptions** - Medications
   - id, user_id, doctor_name, medication, dosage, frequency, duration, instructions, status

7. **lab_reports** - Test results
   - id, user_id, test_name, test_type, result, reference_range, status, test_date

8. **vital_signs** - Health metrics
   - id, user_id, blood_pressure, heart_rate, temperature, weight, bmi, recorded_date

---

## 📱 User Guide

### **Dashboard**
- View total appointments and consultations
- See recent appointments
- Quick access to all features

### **AI Chat**
- Ask health questions 24/7
- Get instant AI responses
- Emergency detection
- Personalized advice

**Example Questions:**
- "I have a fever of 101°F"
- "How to manage high blood pressure?"
- "Feeling stressed and anxious"
- "Book appointment with cardiologist"

### **Appointments**
- Book with specialists
- Select date and time
- Add symptoms/notes
- View booking history

**Available Specialties:**
- General Physician
- Cardiology
- Dermatology
- Pediatrics
- Orthopedics
- Neurology
- Gynecology

### **Medical Records**
- View complete health history
- Track treatments
- Access past records

### **Prescriptions**
- Current medications
- Dosage instructions
- Refill tracking
- Active/Expired status

### **Lab Reports**
- View test results
- Compare with reference ranges
- Track over time

### **Vital Signs**
- Record daily vitals
- Track trends
- Monitor health metrics
- View history (last 20 entries)

---

## 🔧 Admin Guide

### **Dashboard**
- Total users count
- Total appointments (pending/confirmed/completed)
- Total consultations
- Recent user registrations
- Recent appointments

### **User Management**
- View all registered users
- User details (age, gender, blood group, contact)
- Registration dates

### **Appointment Management**
- View all system appointments
- Filter by status
- Update appointment status:
  - Pending → Confirmed
  - Confirmed → Completed
  - Any → Cancelled
- Add diagnosis and notes

---

## 🛠 Technical Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask 3.0.0 |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Styling | Custom CSS (Gradient Design) |
| Security | Session-based auth, Password hashing (SHA-256) |
| API | RESTful JSON API |

---

## 📂 File Structure

```
AI-Healthcare-Chatbot/
├── app_advanced.py              # Main application (2100+ lines)
├── requirements_advanced.txt    # Dependencies
├── advanced_healthcare.db       # Database (auto-created)
├── ADVANCED_README.md          # This file
├── ADVANCED_SETUP.md           # Setup guide
├── healthcare_app.py           # Simple version (backup)
└── requirements_simple.txt     # Simple version deps
```

---

## 🎨 UI/UX Features

- **Modern Gradient Design** (Purple/Blue theme)
- **Responsive Layout** (Mobile-friendly)
- **Intuitive Navigation** (Top navbar)
- **Interactive Forms** (Real-time validation)
- **Status Badges** (Color-coded statuses)
- **Smooth Animations** (Hover effects, transitions)
- **Clean Typography** (Segoe UI font family)
- **Shadow Effects** (Depth and elevation)

---

## 🔒 Security Features

- Password hashing (SHA-256)
- Session-based authentication
- Login required decorators
- Admin-only route protection
- SQL injection prevention (parameterized queries)
- XSS protection (template escaping)

---

## 📈 Analytics & Statistics

### **User Dashboard**
- Total appointments
- Total consultations

### **Admin Dashboard**
- Total users
- Total appointments
- Pending appointments
- Confirmed appointments
- Total chats
- Recent activity

---

## 🔄 API Endpoints

### **User APIs**
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout
- `POST /api/chat` - AI chat
- `POST /api/appointments` - Book appointment
- `POST /api/vital-signs` - Record vitals

### **Admin APIs**
- `POST /admin/login` - Admin login
- `GET /admin/logout` - Admin logout
- `POST /admin/appointment/update/<id>` - Update appointment

### **Pages**
- `/` - Home page
- `/dashboard` - User dashboard
- `/chat` - AI chat interface
- `/appointments` - Appointments
- `/medical-records` - Medical records
- `/prescriptions` - Prescriptions
- `/lab-reports` - Lab reports
- `/vital-signs` - Vital signs
- `/admin/dashboard` - Admin dashboard
- `/admin/users` - User management
- `/admin/appointments` - Appointment management

---

## 🆘 Troubleshooting

### **Port Already in Use**
```bash
lsof -ti:5000 | xargs kill -9
```

### **Module Not Found**
```bash
pip3 install --user Flask Flask-CORS
```

### **Database Locked**
```bash
rm advanced_healthcare.db
python3 app_advanced.py
```

### **Admin Login Issues**
Default admin created automatically on first run:
- Email: admin@healthcare.com
- Password: admin123

---

## 🎯 Future Enhancements

- [ ] Email notifications
- [ ] SMS reminders
- [ ] Video consultations
- [ ] Payment integration
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Real-time chat (WebSocket)
- [ ] File upload for reports
- [ ] Data export (PDF)
- [ ] Advanced analytics with charts

---

## 📞 Support

Need help?
- Check console for error messages
- Verify all dependencies installed
- Ensure port 5000 is available
- Check database file permissions

---

## 📝 License

This project is for educational purposes.

---

## 👨‍💻 Developer

Created by: **Kiro AI Assistant**  
Date: June 27, 2026  
Version: 2.0 (Advanced)

---

**Enjoy your advanced healthcare system!** 🚀

For the simple version, use: `python3 healthcare_app.py`
