# AI Healthcare Chatbot v2.0 - Setup Guide

## 🚀 Quick Start

This is a complete, production-ready AI Healthcare Chatbot with advanced features, beautiful UI, and real-time capabilities.

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation Steps

#### 1. Install Dependencies

```bash
cd /path/to/AI-Healthcare-Chatbot
pip install -r requirements_enhanced.txt
```

**Required packages:**
- Flask==2.3.3
- Flask-CORS==4.0.0
- Flask-SocketIO==5.3.4
- python-socketio==5.9.0
- python-engineio==4.7.1

#### 2. Set Up Database

The database setup script will create a SQLite database with sample data:

```bash
python3 setup_enhanced.py
```

This creates:
- Database: `healthcare_enhanced.db`
- 6 sample users (1 admin, 3 patients, 2 doctors)
- 90 vital signs records (30 days of data)
- 6 lab reports with abnormal flags
- 5 prescriptions
- 5 appointments
- Sample chat history

#### 3. Run the Application

```bash
python3 app_enhanced.py
```

The server will start at: **http://localhost:5000**

#### 4. Access the Application

Open your browser and navigate to: **http://localhost:5000**

---

## 👤 Demo Login Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Features:** Full access to all features and management

### Patient Accounts
- **Username:** `patient1` | **Password:** `password123`
- **Username:** `patient2` | **Password:** `password123`
- **Username:** `patient3` | **Password:** `password123`

### Doctor Accounts
- **Username:** `doctor1` | **Password:** `password123`
- **Username:** `doctor2` | **Password:** `password123`

---

## 🎯 Features Overview

### 1. **AI Health Chatbot** 🤖
- Natural Language Processing for health queries
- Intent detection (8 types: symptom, medication, appointment, emergency, etc.)
- Sentiment analysis
- Emergency detection with alerts
- Medical knowledge base (symptoms, medications, health tips)
- Real-time WebSocket communication
- Typing indicators
- Chat history with search

### 2. **Dashboard** 📊
- Animated stat cards showing key metrics
- Interactive Chart.js visualizations:
  - Vital signs trends (Heart Rate, Blood Pressure, Oxygen)
  - BMI tracking over time
  - Activity breakdown (doughnut chart)
- Health score with circular progress indicator
- Upcoming appointments preview
- Active prescriptions cards
- Health tips and recommendations
- Floating Action Button (FAB) for quick actions

### 3. **Appointments Management** 📅
- View all appointments with beautiful card layout
- Book new appointments with modal form
- Edit existing appointments
- Cancel appointments
- Search and filter by status/time
- Date badges with visual indicators
- Appointment reminders

### 4. **Prescriptions Viewer** 💊
- Active prescriptions display
- Detailed medication information
- Dosage and frequency tracking
- Refill reminders
- Doctor and prescription details
- Search and filter functionality
- Print prescription capability

### 5. **Vital Signs Tracking** ❤️
- Record multiple vital signs:
  - Heart Rate (bpm)
  - Blood Pressure (Systolic/Diastolic)
  - Temperature (°F)
  - Oxygen Saturation (%)
  - Weight (lbs)
  - BMI (auto-calculated)
- Real-time status indicators (Normal, High, Low)
- Multi-axis Chart.js visualizations
- Historical data table
- Period selector (7, 14, 30 days)
- Weight and BMI trends

### 6. **Lab Reports** 🧪
- View all laboratory test results
- Abnormal flags highlighting
- Detailed test parameters with reference ranges
- Status indicators (Normal, Abnormal, Pending)
- Search and filter by test type/status
- Print and download reports
- Doctor and lab information

### 7. **Beautiful Landing Page** 🏠
- Modern hero section with gradient text
- Feature showcase with icons
- How it works (3-step process)
- User testimonials
- Call-to-action sections
- Responsive design
- Smooth scroll navigation

---

## 🎨 UI/UX Features

### Design System
- **Glassmorphism effects** on cards and modals
- **Gradient buttons** with hover effects
- **Smooth animations:**
  - fadeIn, fadeInUp, slideIn
  - scaleIn, bounce, pulse
  - spin, shimmer, gradient
- **Responsive grid system** (mobile, tablet, desktop)
- **Modern color palette** with CSS variables
- **Beautiful typography** with proper hierarchy
- **Toast notifications** for user feedback
- **Loading spinners** and skeleton screens
- **Modal dialogs** for forms and details

### Accessibility
- Semantic HTML structure
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance
- Responsive touch targets

---

## 🔧 Technical Architecture

### Backend (Flask)
- **File:** `app_enhanced.py` (1,601 lines)
- **Features:**
  - 30+ REST API endpoints
  - WebSocket support via Flask-SocketIO
  - Session management with 24-hour lifetime
  - SHA-256 password hashing
  - SQL injection prevention
  - Activity logging
  - CORS enabled for development

### Database (SQLite)
- **File:** `healthcare_enhanced.db`
- **Tables:**
  1. users - User accounts and authentication
  2. patients - Patient profiles with medical details
  3. doctors - Doctor profiles
  4. appointments - Appointment scheduling
  5. prescriptions - Medication records
  6. vital_signs - Health metrics tracking
  7. lab_reports - Laboratory test results
  8. medical_records - Medical history
  9. activity_logs - User activity tracking

### Frontend
- **CSS:** `static/css/enhanced.css` (1,200+ lines)
- **JavaScript:** `static/js/enhanced.js` (1,400+ lines)
- **HTML Templates:** 8 pages
  - index_enhanced.html - Landing page
  - login_enhanced.html - Login/Register
  - dashboard_enhanced.html - Main dashboard
  - chat_enhanced.html - AI chatbot
  - appointments_enhanced.html - Appointments
  - prescriptions_enhanced.html - Prescriptions
  - vital_signs_enhanced.html - Vital signs
  - lab_reports_enhanced.html - Lab reports

### External Libraries
- **Chart.js 4.4.0** - Data visualization
- **Socket.IO 4.5.4** - Real-time communication
- **Font Awesome 6.4.0** - Icons

---

## 📡 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/check-auth` - Check authentication status

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### Appointments
- `GET /api/appointments` - List appointments
- `POST /api/appointments` - Create appointment
- `PUT /api/appointments/<id>` - Update appointment
- `DELETE /api/appointments/<id>` - Delete appointment

### Prescriptions
- `GET /api/prescriptions` - List prescriptions
- `POST /api/prescriptions` - Create prescription
- `GET /api/prescriptions/<id>` - Get prescription details

### Vital Signs
- `GET /api/vital-signs` - List vital signs
- `POST /api/vital-signs` - Record vital signs
- `DELETE /api/vital-signs/<id>` - Delete vital sign record

### Lab Reports
- `GET /api/lab-reports` - List lab reports
- `POST /api/lab-reports` - Create lab report
- `GET /api/lab-reports/<id>` - Get lab report details

### Chat
- `POST /api/chat` - Send chat message
- `GET /api/chat/history` - Get chat history
- WebSocket: `connect`, `disconnect`, `message`, `typing`

### Activity Logs
- `GET /api/activity-logs` - Get user activity logs

---

## 🔒 Security Features

1. **Password Security**
   - SHA-256 hashing
   - Minimum 6 characters requirement
   - No plain-text storage

2. **Session Management**
   - HTTP-only cookies
   - 24-hour session lifetime
   - Secure session tokens

3. **Authentication**
   - Login required decorators
   - Admin role checking
   - Session validation on all protected routes

4. **SQL Injection Prevention**
   - Parameterized queries
   - Input validation
   - Sanitized database operations

5. **Activity Logging**
   - All user actions logged
   - IP address tracking
   - Timestamp recording

---

## 🧪 Testing the Application

### Manual Testing Checklist

#### 1. Authentication
- [ ] Register new user
- [ ] Login with demo credentials
- [ ] Logout functionality
- [ ] Session persistence

#### 2. Dashboard
- [ ] Stats load correctly
- [ ] Charts render properly
- [ ] Animations work smoothly
- [ ] Quick actions functional

#### 3. AI Chat
- [ ] Send messages
- [ ] Receive AI responses
- [ ] WebSocket connection
- [ ] Typing indicators
- [ ] Chat history

#### 4. Appointments
- [ ] View appointments list
- [ ] Book new appointment
- [ ] Edit appointment
- [ ] Cancel appointment
- [ ] Search and filter

#### 5. Prescriptions
- [ ] View prescriptions
- [ ] View prescription details
- [ ] Search functionality
- [ ] Status filtering

#### 6. Vital Signs
- [ ] View vital signs list
- [ ] Record new vitals
- [ ] View charts
- [ ] Delete records
- [ ] Period selection

#### 7. Lab Reports
- [ ] View lab reports
- [ ] View report details
- [ ] Abnormal flags display
- [ ] Search and filter

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

#### 2. Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements_enhanced.txt --upgrade
```

#### 3. Database Not Found
```bash
# Recreate database
python3 setup_enhanced.py
```

#### 4. Charts Not Displaying
- Check browser console for JavaScript errors
- Ensure Chart.js CDN is accessible
- Clear browser cache

#### 5. WebSocket Connection Failed
- Check if Flask-SocketIO is installed
- Verify server is running
- Check browser console for connection errors

---

## 📈 Performance Optimization

### Recommendations for Production

1. **Use PostgreSQL or MySQL** instead of SQLite
2. **Enable caching** (Redis) for session management
3. **Implement rate limiting** for API endpoints
4. **Use HTTPS** with SSL certificates
5. **Enable Gzip compression** for static files
6. **Minify CSS and JavaScript** files
7. **Use CDN** for static assets
8. **Implement database connection pooling**
9. **Add API authentication tokens** (JWT)
10. **Set up logging** with log rotation

---

## 🚀 Deployment Options

### Option 1: Traditional Hosting
- Deploy on VPS (DigitalOcean, AWS EC2, etc.)
- Use Gunicorn or uWSGI as WSGI server
- Set up Nginx as reverse proxy
- Use systemd for process management

### Option 2: Platform as a Service
- Heroku
- PythonAnywhere
- Google App Engine
- Azure App Service

### Option 3: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements_enhanced.txt .
RUN pip install -r requirements_enhanced.txt
COPY . .
EXPOSE 5000
CMD ["python", "app_enhanced.py"]
```

---

## 📝 License

This project is open-source and available for educational and personal use.

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments in `app_enhanced.py`
3. Check browser console for errors
4. Verify all dependencies are installed

---

## 🎉 Features Highlights

### What Makes This Special

✅ **Complete & Production-Ready** - Not a prototype, fully functional system
✅ **Beautiful Modern UI** - Glassmorphism, gradients, animations
✅ **Real-time Features** - WebSocket chat with typing indicators
✅ **Advanced AI** - NLP, intent detection, sentiment analysis
✅ **Comprehensive** - 8 full pages, 30+ API endpoints
✅ **Well-Architected** - Clean code, proper structure, documented
✅ **Responsive Design** - Works on mobile, tablet, and desktop
✅ **Rich Visualizations** - Chart.js integration with multiple chart types
✅ **Secure** - Password hashing, session management, activity logging
✅ **Sample Data** - 100+ records for immediate testing

---

**Version:** 2.0 Enhanced  
**Last Updated:** 2024  
**Lines of Code:** 10,000+  
**Status:** ✅ Complete and Ready to Use

Enjoy your AI Healthcare Chatbot! 🏥💙
