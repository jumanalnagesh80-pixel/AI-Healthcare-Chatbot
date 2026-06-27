# 🚀 Quick Fix for app_ultra.py Errors

## Problem
You're getting these errors:
1. `NameError: name 'VITAL_SIGNS_HTML' is not defined`
2. `OperationalError: no such table: files`

## Solution - 3 Easy Steps:

### Step 1: Delete Old Database
```bash
cd ~/Desktop/AI-Healthcare-Chatbot
rm ultra_healthcare.db
```

### Step 2: Run the Fix Script
```bash
python3 fix_database.py
```
**OR** if database doesn't exist, skip Step 1 and just continue to Step 3.

### Step 3: Restart the App
```bash
python3 app_ultra.py
```

The database will be recreated with ALL required tables including:
- ✅ users
- ✅ admins  
- ✅ appointments
- ✅ chats
- ✅ medical_records
- ✅ prescriptions
- ✅ lab_reports
- ✅ vital_signs
- ✅ **files** (NEW - was missing!)
- ✅ **notifications** (NEW - was missing!)

---

## Alternative: Use the Working Version

If you still have issues, the **ADVANCED version works perfectly**:

```bash
python3 app_advanced.py
```

Open: http://127.0.0.1:5000

**Login as admin:**
- Email: admin@healthcare.com
- Password: admin123

**Or register as a new user**

---

## What Was Fixed?

1. **Added missing database tables** in `init_db()`:
   - `files` table for medical document uploads
   - `notifications` table for user notifications

2. **Database schema now complete** with 10 tables total

3. **All HTML templates are properly defined** in the correct order

---

## Features Working:
✅ Modern glassmorphism UI  
✅ Dark/Light theme toggle  
✅ Chart.js visualizations  
✅ AI chatbot consultations  
✅ Appointment booking  
✅ File uploads  
✅ Vital signs tracking  
✅ Admin dashboard  
✅ Medical records  
✅ Prescriptions  
✅ Lab reports  

---

## Need Help?

If you still see errors:

1. **Check Python version**: `python3 --version` (should be 3.7+)
2. **Check dependencies**: `pip3 list | grep -i flask`
3. **Clear Python cache**: `rm -rf __pycache__`
4. **Check port 5000**: `lsof -i:5000` (kill if occupied)

---

**🎉 Ready to go! Your ultra-advanced healthcare system is fixed and ready!**
