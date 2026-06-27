# 🚀 Deployment Guide - AI Healthcare Chatbot

This guide will help you deploy the AI Healthcare Chatbot to various platforms.

---

## 📋 Pre-Deployment Checklist

Before deploying to production, ensure you:

- [ ] Change the SECRET_KEY in `app.py`
- [ ] Update default admin credentials
- [ ] Set up proper SSL/TLS certificates
- [ ] Configure environment variables
- [ ] Set up backup system for database
- [ ] Enable proper logging
- [ ] Configure CORS properly
- [ ] Set debug mode to False
- [ ] Review security settings

---

## 🖥️ Local Development

### Quick Start

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
run.bat
```

**Manual Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Setup database with sample data
python setup.py

# Run the application
python app.py
```

Access at: http://localhost:5000

---

## ☁️ Cloud Deployment Options

### 1. Heroku Deployment

**Step 1: Install Heroku CLI**
```bash
# Mac
brew tap heroku/brew && brew install heroku

# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

**Step 2: Create Heroku App**
```bash
heroku login
heroku create your-healthcare-app
```

**Step 3: Add Procfile**
Create `Procfile` in root directory:
```
web: gunicorn app:app
```

**Step 4: Add gunicorn to requirements.txt**
```bash
echo "gunicorn==20.1.0" >> requirements.txt
```

**Step 5: Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-healthcare-app
git push heroku main
```

**Step 6: Open App**
```bash
heroku open
```

---

### 2. AWS EC2 Deployment

**Step 1: Launch EC2 Instance**
- Choose Ubuntu Server 22.04 LTS
- Instance type: t2.micro (free tier) or larger
- Configure security group (ports 22, 80, 443, 5000)

**Step 2: Connect to EC2**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

**Step 3: Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

**Step 4: Clone Repository**
```bash
git clone https://github.com/yourusername/AI-Healthcare-Chatbot-Web.git
cd AI-Healthcare-Chatbot-Web
```

**Step 5: Setup Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Step 6: Setup Database**
```bash
python setup.py
```

**Step 7: Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/healthcare
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/healthcare /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Step 8: Run with Gunicorn**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Step 9: Setup Systemd Service (Optional)**
Create `/etc/systemd/system/healthcare.service`:
```ini
[Unit]
Description=Healthcare Chatbot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/AI-Healthcare-Chatbot-Web
Environment="PATH=/home/ubuntu/AI-Healthcare-Chatbot-Web/venv/bin"
ExecStart=/home/ubuntu/AI-Healthcare-Chatbot-Web/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable healthcare
sudo systemctl start healthcare
```

---

### 3. DigitalOcean Deployment

**Step 1: Create Droplet**
- Choose Ubuntu 22.04
- Select plan (Basic $6/month recommended)
- Add SSH key

**Step 2: Follow AWS EC2 steps 2-9**
(Same process as EC2)

---

### 4. Google Cloud Platform (GCP)

**Step 1: Create VM Instance**
```bash
gcloud compute instances create healthcare-vm \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --machine-type=e2-micro \
    --zone=us-central1-a
```

**Step 2: SSH into instance**
```bash
gcloud compute ssh healthcare-vm
```

**Step 3: Follow AWS EC2 steps 3-9**

---

### 5. Docker Deployment

**Step 1: Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python setup.py

EXPOSE 5000

CMD ["python", "app.py"]
```

**Step 2: Create docker-compose.yml**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./healthcare.db:/app/healthcare.db
    environment:
      - FLASK_ENV=production
```

**Step 3: Build and Run**
```bash
docker-compose up -d
```

---

### 6. Azure App Service

**Step 1: Install Azure CLI**
```bash
# Mac
brew install azure-cli

# Windows/Linux
# Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
```

**Step 2: Login**
```bash
az login
```

**Step 3: Create App Service**
```bash
az webapp up --name healthcare-app --runtime "PYTHON:3.9"
```

---

## 🔒 Security Configuration

### 1. SSL/TLS Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 2. Environment Variables

Create `.env` file:
```bash
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///healthcare.db
FLASK_ENV=production
```

Update `app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

### 3. Firewall Configuration

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 📊 Monitoring & Logging

### Setup Logging

Update `app.py`:
```python
import logging

logging.basicConfig(
    filename='healthcare.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Monitor with PM2 (Node.js process manager)

```bash
npm install -g pm2
pm2 start app.py --interpreter python3
pm2 startup
pm2 save
```

---

## 🔄 Database Backup

### Automatic Backup Script

Create `backup.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp healthcare.db backups/healthcare_$DATE.db
find backups/ -mtime +7 -delete
```

Setup cron job:
```bash
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

---

## 🧪 Testing in Production

### Health Check Endpoint

Add to `app.py`:
```python
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
```

Test:
```bash
curl https://your-domain.com/health
```

---

## 📈 Performance Optimization

### 1. Enable Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/patients')
@cache.cached(timeout=300)
def api_patients():
    # ...
```

### 2. Database Optimization
```sql
CREATE INDEX idx_patient_id ON appointments(patient_id);
CREATE INDEX idx_user_username ON users(username);
```

### 3. Enable Gzip Compression
```python
from flask_compress import Compress
Compress(app)
```

---

## 🚨 Troubleshooting

### Common Issues

**Database locked:**
```python
# Use WAL mode
conn.execute('PRAGMA journal_mode=WAL')
```

**Port already in use:**
```bash
# Find and kill process
sudo lsof -i :5000
kill -9 <PID>
```

**Permission denied:**
```bash
chmod +x run.sh
sudo chown -R $USER:$USER .
```

---

## 📞 Support

For deployment issues:
- Check logs: `tail -f healthcare.log`
- Monitor resources: `htop`
- Check service status: `systemctl status healthcare`

---

**🎉 Congratulations! Your AI Healthcare Chatbot is now deployed!**
