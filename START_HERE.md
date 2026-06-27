# 🏥 AI Healthcare Chatbot - Quick Start Guide

## 📋 Project Overview

This is a **complete, production-ready AI Healthcare Chatbot** built with Python, Flask, and SQLite. It features:

- 🎨 **Modern, Beautiful UI** - Complete redesign with medical-themed interface
- 🤖 **AI-Powered Chat** - Real-time chat with medical knowledge base & OpenAI integration
- 📊 **Health Goals Tracking** - Set and monitor health objectives
- 📅 **Appointments** - Schedule and manage medical appointments
- 💊 **Prescriptions** - Track medications and dosages
- 👨‍⚕️ **Admin Panel** - User management and system analytics
- ✅ **Complete Tests** - Unit and integration tests included

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements_modern.txt

# Install test dependencies (optional)
pip install pytest pytest-flask pytest-cov
```

### Step 2: Initialize Database

```bash
# Run database setup
python setup_enhanced.py

# Add health goals table
python add_health_goals_table.py
```

### Step 3: Start the Application

```bash
# Linux/Mac
python app_modern.py

# Or use the run script
bash run.sh

# Windows
python app_modern.py
# Or
run.bat
```

**That's it!** Open your browser to: **http://localhost:5000**

---

## 🎯 Key Features

### 1. **AI Chat with Medical Knowledge** 🤖
- Real-time WebSocket chat
- Symptom analysis and advice
- Medication information
- Emergency detection
- Health tips
- OpenAI GPT integration (optional)

### 2. **Health Goals Tracking** 📈
- Weight loss goals
- Exercise tracking
- Nutrition plans
- Sleep monitoring
- Progress visualization
- Achievement tracking

### 3. **Appointment Management** 📅
- Schedule appointments
- View upcoming visits
- Status tracking
- Reminders

### 4. **Admin Dashboard** 👨‍💼
- User management
- System statistics
- Analytics charts
- Activity monitoring

### 5. **Modern UI** 🎨
- Beautiful medical-themed design
- Responsive layout
- Smooth animations
- Custom logo
- Professional color scheme

---

## 📁 Project Structure

```
AI-Healthcare-Chatbot/
├── app_modern.py              # Main Flask application
├── ai_medical_knowledge.py    # AI engine with medical knowledge
├── database.py                # Database models
├── requirements_modern.txt    # Python dependencies
├── healthcare.db              # SQLite database (created on first run)
│
├── static/
│   ├── css/
│   │   └── modern.css        # Modern UI styles
│   ├── js/
│   │   └── enhanced.js       # Frontend API client
│   └── images/
│       ├── logo.svg          # Custom logo
│       └── favicon.svg       # Favicon
│
├── templates/
│   ├── index_modern.html     # Landing page
│   ├── login_modern.html     # Login/Register
│   ├── chat_modern.html      # AI Chat interface
│   ├── health_goals_modern.html  # Health goals
│   └── admin_modern.html     # Admin panel
│
└── tests/                     # Test suite
    ├── conftest.py           # Test fixtures
    ├── test_auth.py          # Authentication tests
    ├── test_chat.py          # Chat & AI tests
    ├── test_api.py           # API endpoint tests
    └── test_admin.py         # Admin panel tests
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html

# Use the test script
bash run_tests.sh
```

---

## 🔧 Configuration

### OpenAI Integration (Optional)

To use OpenAI GPT for enhanced AI responses:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Or add to .env file
echo "OPENAI_API_KEY=your-api-key" > .env
```

**Note:** The app works perfectly without OpenAI - it has a comprehensive built-in medical knowledge base!

### Database

The app uses SQLite by default. Database file: `healthcare.db`

To reset the database:
```bash
rm healthcare.db
python setup_enhanced.py
python add_health_goals_table.py
```

---

## 👥 Default Users

### Regular User (Patient)
- **Email:** test@example.com
- **Password:** password123

### Admin User
- **Email:** admin@example.com
- **Password:** admin123

*(Create these after first run or register new users)*

---

## 📊 Features Breakdown

### AI Medical Knowledge Base

The AI includes:
- **10+ Symptoms** with severity levels, conditions, advice, red flags
- **12+ Medications** with uses, dosages, side effects, warnings
- **50+ Health Tips** across nutrition, exercise, sleep, mental health
- **First Aid Guidelines** for common emergencies
- **Care Guidelines** (when to call 911, ER, doctor)
- **Intent Detection** for smart responses
- **Context Awareness** for conversation flow

### Health Goals Types

- 🏃 Weight Loss
- 💪 Exercise
- 🥗 Nutrition
- 😴 Sleep
- 💧 Hydration
- 🧘 Meditation
- ✏️ Custom Goals

### Admin Features

- View all users
- System statistics dashboard
- Analytics charts (Chart.js)
- User activity monitoring
- Role-based access control

---

## 🌐 URLs & Routes

| Page | URL | Description |
|------|-----|-------------|
| Landing | `/` | Home page |
| Login/Register | `/login` | Authentication |
| Dashboard | `/dashboard` | User dashboard |
| AI Chat | `/chat` | Chat interface |
| Health Goals | `/health-goals` | Goals tracking |
| Appointments | `/appointments` | Manage appointments |
| Prescriptions | `/prescriptions` | View prescriptions |
| Admin Panel | `/admin` | Admin dashboard (admin only) |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send chat message |
| GET | `/api/chat/history` | Get chat history |
| GET | `/api/health-goals` | List health goals |
| POST | `/api/health-goals` | Create goal |
| PUT | `/api/health-goals/<id>` | Update goal |
| DELETE | `/api/health-goals/<id>` | Delete goal |
| POST | `/api/health-goals/<id>/progress` | Add progress |
| GET | `/api/admin/users` | Get all users (admin) |
| GET | `/api/admin/stats` | Get system stats (admin) |

---

## 🛠️ Technologies Used

### Backend
- **Flask** - Web framework
- **Flask-SocketIO** - Real-time WebSocket
- **SQLAlchemy** - Database ORM
- **SQLite** - Database
- **OpenAI** - AI integration (optional)
- **Werkzeug** - Password hashing

### Frontend
- **Vanilla JavaScript** - No framework overhead
- **Socket.IO Client** - WebSocket client
- **Chart.js** - Analytics charts
- **Custom CSS** - Modern UI framework
- **Google Fonts** - Inter & Poppins

### Testing
- **pytest** - Test framework
- **pytest-flask** - Flask testing
- **pytest-cov** - Coverage reporting

---

## 🐛 Troubleshooting

### Issue: Port 5000 already in use
```bash
# Change port in app_modern.py (line ~last line)
socketio.run(app, debug=True, port=5001)
```

### Issue: Database errors
```bash
# Reset database
rm healthcare.db
python setup_enhanced.py
python add_health_goals_table.py
```

### Issue: Module not found
```bash
# Reinstall dependencies
pip install -r requirements_modern.txt
```

### Issue: WebSocket not connecting
- Check browser console for errors
- Ensure Socket.IO versions match
- Try different browser

---

## 📝 Development Tips

### Adding New Features

1. **Add database model** in `database.py`
2. **Create API endpoint** in `app_modern.py`
3. **Add frontend UI** in `templates/`
4. **Update JavaScript** in `static/js/enhanced.js`
5. **Write tests** in `tests/`

### Testing Workflow

```bash
# 1. Write test
vi tests/test_new_feature.py

# 2. Run test
pytest tests/test_new_feature.py -v

# 3. Fix code
vi app_modern.py

# 4. Rerun test
pytest tests/test_new_feature.py -v
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in `app_modern.py`
- [ ] Use production WSGI server (gunicorn, uWSGI)
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set secure `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Set up backup for database
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Set up monitoring

### Deploy to Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app_modern:app" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Deploy to AWS/DigitalOcean

```bash
# Use gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_modern:app
```

---

## 📞 Support & Contact

For questions or issues:
1. Check this documentation
2. Review code comments
3. Check test files for examples
4. Review Flask documentation

---

## 🎓 Learning Resources

- **Flask:** https://flask.palletsprojects.com/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **Socket.IO:** https://socket.io/docs/
- **OpenAI API:** https://platform.openai.com/docs/

---

## ✅ Project Checklist

- ✅ Modern UI redesign
- ✅ Custom logo and branding
- ✅ AI chat with WebSocket
- ✅ OpenAI integration
- ✅ Medical knowledge base
- ✅ Health goals tracking
- ✅ Admin panel
- ✅ Complete test suite
- ✅ Documentation

**Status: 100% Complete & Ready to Use!** 🎉

---

## 📄 License

This project is open source and available for educational and commercial use.

---

**Happy Coding! 🚀**

*Built with ❤️ using Python, Flask, and SQLite*
