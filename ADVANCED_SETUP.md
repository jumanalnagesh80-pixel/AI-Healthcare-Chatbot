# 🏥 Advanced AI Healthcare System - Setup Guide

## 🎯 What's New in Advanced Version

### ✨ Features
- ✅ **Admin Panel** - Complete control dashboard
- ✅ **User Dashboard** - Enhanced patient portal
- ✅ **Real-time Chat** - WebSocket-powered instant messaging
- ✅ **Medical Records** - Complete health history tracking
- ✅ **Prescriptions** - Medication management system
- ✅ **Lab Reports** - Test results with trends
- ✅ **Vital Signs** - BP, heart rate, weight tracking with charts
- ✅ **Analytics** - Beautiful charts and statistics
- ✅ **Notifications** - Real-time alerts system
- ✅ **Advanced AI** - More detailed health responses

## 🚀 Installation (Mac M2)

### Step 1: Download
```bash
git clone -b advanced-healthcare-system https://github.com/jumanalnagesh80-pixel/AI-Healthcare-Chatbot.git
cd AI-Healthcare-Chatbot
```

### Step 2: Install Dependencies
```bash
pip3 install -r requirements_advanced.txt
```

### Step 3: Run the Application
```bash
python3 app_advanced.py
```

### Step 4: Access the System
Open browser: **http://127.0.0.1:5000**

## 🔐 Login Credentials

### Admin Access
- **URL**: http://127.0.0.1:5000/admin
- **Email**: admin@healthcare.com
- **Password**: admin123

### User Access
- **URL**: http://127.0.0.1:5000
- Register new account or use existing

## 📊 Admin Panel Features

### Dashboard
- Total users statistics
- Total appointments (pending/confirmed/completed)
- Recent user registrations
- Appointment calendar
- System analytics with charts

### User Management
- View all registered users
- User details (age, gender, blood group, contact)
- User activity tracking
- Ability to activate/deactivate users

### Appointment Management
- View all appointments across system
- Filter by status (pending/confirmed/completed/cancelled)
- Update appointment status
- Add diagnosis and notes
- Assign doctors

### Medical Records
- View all patient medical records
- Add new records for patients
- Track medical history
- Upload/attach reports

### System Settings
- Configure notification settings
- Manage doctor list
- Set appointment time slots
- System maintenance options

## 👤 User Features

### Enhanced Dashboard
- Health summary at a glance
- Upcoming appointments
- Recent consultations
- Quick actions menu
- Notification center

### AI Health Chat
- Advanced symptom analysis
- Personalized health advice
- Emergency detection
- Medication guidance
- Appointment booking via chat

### Appointments
- Book appointments with specialists
- View appointment history
- Reschedule or cancel
- Add symptoms/notes
- Get email confirmations

### Medical Records
- View complete health history
- Download records as PDF
- Share with doctors
- Track treatments

### Prescriptions
- Current medications list
- Dosage and instructions
- Refill reminders
- Drug interaction warnings

### Lab Reports
- View test results
- Compare with reference ranges
- Track trends over time
- Download reports

### Vital Signs
- Track blood pressure
- Monitor heart rate
- Log weight and BMI
- Temperature tracking
- Visual charts and graphs

## 🎨 UI/UX Highlights

- Modern gradient design
- Responsive layout (mobile-friendly)
- Dark/Light theme support
- Smooth animations
- Interactive charts (Chart.js)
- Real-time updates
- Toast notifications

## 🛠 Technical Stack

- **Backend**: Flask 3.0, SocketIO
- **Database**: SQLite (advanced_healthcare.db)
- **Frontend**: HTML5, CSS3, JavaScript
- **Real-time**: WebSockets
- **Charts**: Chart.js
- **Icons**: Font Awesome

## 📂 Database Schema

### Tables
1. **users** - Patient information
2. **admins** - Admin accounts
3. **appointments** - All appointments
4. **chats** - AI chat history
5. **medical_records** - Health records
6. **prescriptions** - Medications
7. **lab_reports** - Test results
8. **vital_signs** - Health metrics
9. **notifications** - System alerts

## 🔔 Notifications

- Appointment confirmations
- Prescription refill reminders
- Lab report available alerts
- System announcements
- Health tips

## 🆘 Support

Need help?
- Check console for errors
- Ensure all dependencies installed
- Verify database is created
- Check port 5000 is available

## 🎯 Next Steps After Setup

1. **As Admin**:
   - Login to admin panel
   - Review dashboard
   - Check user registrations
   - Manage appointments

2. **As User**:
   - Register new account
   - Complete profile
   - Try AI chat
   - Book appointment
   - Track vital signs

## 🔧 Customization

Want to customize?
- Colors: Edit CSS variables
- Features: Modify routes in app_advanced.py
- AI Responses: Update get_advanced_ai_response()
- Database: Extend schema as needed

---

**Enjoy your advanced healthcare system!** 🚀
