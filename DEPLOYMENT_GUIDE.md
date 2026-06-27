# 🚀 Deployment Guide - AI Healthcare Chatbot v2.0

## 📋 Pre-Deployment Checklist

Before deploying to production, ensure you've completed these steps:

### ✅ Code Review
- [ ] Review all code in the Pull Request
- [ ] Test locally on your machine
- [ ] Verify all features work correctly
- [ ] Check responsive design on different devices
- [ ] Review security implementations

### ✅ Configuration
- [ ] Update `SECRET_KEY` in app_enhanced.py
- [ ] Configure production database (PostgreSQL/MySQL)
- [ ] Set up environment variables
- [ ] Configure CORS for your domain
- [ ] Update session settings for HTTPS

### ✅ Testing
- [ ] Test all API endpoints
- [ ] Verify WebSocket connections
- [ ] Test user authentication flow
- [ ] Check all CRUD operations
- [ ] Test on different browsers
- [ ] Test on mobile devices

---

## 🌐 Deployment Options

### Option 1: Heroku (Easiest)

#### Step 1: Prepare for Heroku
```bash
# Create Procfile
echo "web: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 app_enhanced:app" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Update requirements.txt
echo "gunicorn==21.2.0" >> requirements_enhanced.txt
echo "gevent==23.9.1" >> requirements_enhanced.txt
```

#### Step 2: Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-healthcare-app

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Deploy
git push heroku healthcare-v2-enhanced:main

# Initialize database
heroku run python setup_enhanced.py

# Open app
heroku open
```

#### Step 3: Configure Add-ons
```bash
# Add PostgreSQL (recommended for production)
heroku addons:create heroku-postgresql:mini

# Add Redis for session storage (optional)
heroku addons:create heroku-redis:mini
```

---

### Option 2: AWS EC2 (Full Control)

#### Step 1: Launch EC2 Instance
1. Go to AWS Console → EC2
2. Launch new instance:
   - AMI: Ubuntu 22.04 LTS
   - Instance Type: t2.micro (free tier) or t2.small
   - Security Group: Allow ports 22, 80, 443
3. Download key pair (.pem file)

#### Step 2: Connect and Setup
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/jumanalnagesh80-pixel/AI-Healthcare-Chatbot.git
cd AI-Healthcare-Chatbot
git checkout healthcare-v2-enhanced

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_enhanced.txt
pip install gunicorn gevent

# Setup database
python3 setup_enhanced.py
```

#### Step 3: Configure Gunicorn
```bash
# Create gunicorn config
cat > gunicorn_config.py << 'EOF'
bind = "0.0.0.0:8000"
workers = 3
worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
timeout = 120
keepalive = 5
EOF

# Test Gunicorn
gunicorn -c gunicorn_config.py app_enhanced:app
```

#### Step 4: Configure Nginx
```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/healthcare

# Add this configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_buffering off;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/healthcare /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 5: Setup Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/healthcare.service

# Add this content:
[Unit]
Description=AI Healthcare Chatbot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/AI-Healthcare-Chatbot
Environment="PATH=/home/ubuntu/AI-Healthcare-Chatbot/venv/bin"
ExecStart=/home/ubuntu/AI-Healthcare-Chatbot/venv/bin/gunicorn -c gunicorn_config.py app_enhanced:app
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable healthcare
sudo systemctl start healthcare
sudo systemctl status healthcare
```

#### Step 6: SSL Certificate (HTTPS)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

### Option 3: DigitalOcean App Platform (Managed)

#### Step 1: Create App
1. Go to DigitalOcean → Apps
2. Click "Create App"
3. Connect GitHub repository
4. Select `healthcare-v2-enhanced` branch

#### Step 2: Configure App
```yaml
name: healthcare-chatbot
services:
  - name: web
    github:
      repo: jumanalnagesh80-pixel/AI-Healthcare-Chatbot
      branch: healthcare-v2-enhanced
    run_command: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 app_enhanced:app
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xxs
    http_port: 8080
    envs:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        value: ${SECRET_KEY}
```

#### Step 3: Deploy
1. Click "Next" → "Create Resources"
2. Wait for deployment (5-10 minutes)
3. App will be live at: `https://your-app.ondigitalocean.app`

---

### Option 4: Docker Container

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements_enhanced.txt .
RUN pip install --no-cache-dir -r requirements_enhanced.txt
RUN pip install gunicorn gevent

# Copy application
COPY . .

# Initialize database
RUN python setup_enhanced.py

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "-b", "0.0.0.0:5000", "app_enhanced:app"]
```

#### Step 2: Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./healthcare_enhanced.db:/app/healthcare_enhanced.db
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: always
```

#### Step 3: Build and Run
```bash
# Build image
docker build -t healthcare-chatbot .

# Run container
docker run -d -p 5000:5000 --name healthcare healthcare-chatbot

# Or use docker-compose
docker-compose up -d
```

---

## 🔒 Production Security Checklist

### Essential Security Updates

#### 1. Update SECRET_KEY
```python
# In app_enhanced.py, replace:
app.config['SECRET_KEY'] = secrets.token_hex(32)

# With environment variable:
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
```

#### 2. Enable HTTPS
```python
# Update in app_enhanced.py:
app.config['SESSION_COOKIE_SECURE'] = True  # Only send over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Already set
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
```

#### 3. Configure CORS
```python
# Update CORS in app_enhanced.py:
CORS(app, 
     supports_credentials=True,
     origins=['https://your-domain.com'],  # Specify your domain
     methods=['GET', 'POST', 'PUT', 'DELETE'],
     allow_headers=['Content-Type', 'Authorization'])
```

#### 4. Use Production Database
```python
# Replace SQLite with PostgreSQL:
import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Use PostgreSQL
    engine = create_engine(DATABASE_URL)
else:
    # Fallback to SQLite
    DATABASE = 'healthcare_enhanced.db'
```

#### 5. Enable Rate Limiting
```python
# Add Flask-Limiter:
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Apply to endpoints:
@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def api_login():
    # ...
```

---

## 📊 Production Monitoring

### 1. Application Logging
```python
# Add to app_enhanced.py:
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    handler = RotatingFileHandler('healthcare.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info('Healthcare app startup')
```

### 2. Error Tracking (Sentry)
```python
# Install: pip install sentry-sdk[flask]
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### 3. Performance Monitoring
```python
# Add APM monitoring:
from flask import g
import time

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    if diff > 1.0:  # Log slow requests
        app.logger.warning(f'Slow request: {request.path} took {diff:.2f}s')
    return response
```

---

## 🔧 Environment Variables

### Required Variables
```bash
# Create .env file
cat > .env << 'EOF'
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host/db
REDIS_URL=redis://localhost:6379/0
ALLOWED_ORIGINS=https://your-domain.com
EOF
```

### Load Environment Variables
```python
# Add to app_enhanced.py:
from dotenv import load_dotenv
load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

---

## 📈 Database Migration

### From SQLite to PostgreSQL

#### Step 1: Export Data
```bash
# Export SQLite to SQL dump
sqlite3 healthcare_enhanced.db .dump > dump.sql
```

#### Step 2: Modify Dump for PostgreSQL
```bash
# Remove SQLite-specific commands
sed -i 's/AUTOINCREMENT/SERIAL/g' dump.sql
sed -i '/PRAGMA/d' dump.sql
sed -i '/BEGIN TRANSACTION/d' dump.sql
sed -i '/COMMIT/d' dump.sql
```

#### Step 3: Import to PostgreSQL
```bash
# Create database
createdb healthcare

# Import data
psql healthcare < dump.sql
```

---

## 🎯 Performance Optimization

### 1. Enable Caching
```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL')
})

@app.route('/api/dashboard/stats')
@cache.cached(timeout=300)  # Cache for 5 minutes
def dashboard_stats():
    # ...
```

### 2. Database Connection Pooling
```python
from sqlalchemy import create_engine, pool

engine = create_engine(
    DATABASE_URL,
    poolclass=pool.QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)
```

### 3. Compress Responses
```python
from flask_compress import Compress

Compress(app)
```

---

## 🧪 Post-Deployment Testing

### Checklist
- [ ] Test homepage loads
- [ ] Test login/register
- [ ] Test dashboard loads with charts
- [ ] Test AI chat responds
- [ ] Test WebSocket connection
- [ ] Test appointments CRUD
- [ ] Test prescriptions viewing
- [ ] Test vital signs recording
- [ ] Test lab reports display
- [ ] Test on mobile device
- [ ] Test HTTPS certificate
- [ ] Test all API endpoints
- [ ] Check application logs
- [ ] Verify database backups

### Tools
```bash
# Load testing
pip install locust
locust -f locustfile.py --host=https://your-domain.com

# API testing
curl -X POST https://your-domain.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"patient1","password":"password123"}'

# WebSocket testing
wscat -c wss://your-domain.com/socket.io/?EIO=4&transport=websocket
```

---

## 💾 Backup Strategy

### Database Backup
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump healthcare > backup_$DATE.sql
# Upload to S3 or similar
aws s3 cp backup_$DATE.sql s3://your-bucket/backups/
# Keep only last 7 days
find . -name "backup_*.sql" -mtime +7 -delete
```

### Application Backup
```bash
# Backup configuration and database
tar -czf healthcare_backup_$(date +%Y%m%d).tar.gz \
  app_enhanced.py \
  requirements_enhanced.txt \
  healthcare_enhanced.db \
  static/ \
  templates/
```

---

## 📞 Post-Deployment Support

### Monitoring Endpoints
- **Health Check:** `GET /api/health`
- **Status:** `GET /api/status`
- **Metrics:** `GET /api/metrics`

### Log Locations
- Application: `/var/log/healthcare/app.log`
- Nginx: `/var/log/nginx/access.log`
- System: `/var/log/syslog`

### Common Issues
1. **502 Bad Gateway** - Check if Gunicorn is running
2. **WebSocket not connecting** - Verify Nginx WebSocket config
3. **Database connection errors** - Check DATABASE_URL
4. **Static files not loading** - Check Nginx static file serving

---

## 🎉 Congratulations!

Your AI Healthcare Chatbot is now live and ready to help users!

### Next Steps:
1. ✅ Monitor application logs
2. ✅ Set up automated backups
3. ✅ Configure alerts (email/Slack)
4. ✅ Add analytics tracking
5. ✅ Plan regular maintenance
6. ✅ Gather user feedback
7. ✅ Plan feature updates

---

**Your production-ready healthcare application is now serving users!** 🏥💙

For questions or issues, refer to:
- README.md - Main documentation
- SETUP_GUIDE.md - Setup instructions
- PROJECT_COMPLETE.md - Feature reference
