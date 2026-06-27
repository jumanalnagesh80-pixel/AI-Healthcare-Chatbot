"""
Fix Database Schema - Add Missing Tables
Run this script to update your database with all required tables
"""

import sqlite3
import os

DATABASE = 'ultra_healthcare.db'

def fix_database():
    """Add missing tables to existing database"""
    
    # Check if database exists
    if not os.path.exists(DATABASE):
        print(f"❌ Database '{DATABASE}' not found!")
        print("👉 Run app_ultra.py first to create the database")
        return
    
    print(f"🔧 Fixing database: {DATABASE}")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Add files table if it doesn't exist
        print("  → Adding 'files' table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                file_type TEXT,
                description TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        print("    ✅ Files table added")
        
        # Add notifications table if it doesn't exist
        print("  → Adding 'notifications' table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        print("    ✅ Notifications table added")
        
        # Verify all required tables exist
        print("\n📊 Verifying database schema...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = [
            'users', 'admins', 'appointments', 'chats', 
            'medical_records', 'prescriptions', 'lab_reports', 
            'vital_signs', 'files', 'notifications'
        ]
        
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"\n⚠️  Still missing tables: {', '.join(missing_tables)}")
            print("   These will be created when you run app_ultra.py")
        else:
            print("\n✅ All 10 tables are present!")
            print(f"   Tables: {', '.join(tables)}")
        
        conn.commit()
        print("\n✨ Database fixed successfully!")
        print("\n🚀 You can now run: python3 app_ultra.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 Healthcare Database Fix Utility")
    print("=" * 60)
    print()
    fix_database()
    print()
    print("=" * 60)
