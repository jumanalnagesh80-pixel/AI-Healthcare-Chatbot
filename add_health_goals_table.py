"""
Add Health Goals table to existing database
"""

import sqlite3

def add_health_goals_table():
    """Add health_goals table if it doesn't exist"""
    conn = sqlite3.connect('healthcare_enhanced.db')
    cursor = conn.cursor()
    
    # Create health_goals table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS health_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        goal_type TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        target_value REAL,
        current_value REAL DEFAULT 0,
        unit TEXT,
        start_date TEXT NOT NULL,
        target_date TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        priority TEXT DEFAULT 'medium',
        created_at TEXT NOT NULL,
        updated_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create goal_progress table for tracking
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goal_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_id INTEGER NOT NULL,
        value REAL NOT NULL,
        notes TEXT,
        recorded_date TEXT NOT NULL,
        FOREIGN KEY (goal_id) REFERENCES health_goals (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Health goals tables created successfully!")

if __name__ == '__main__':
    add_health_goals_table()
