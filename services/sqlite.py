import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_hash TEXT NOT NULL,
            is_premium BOOLEAN NOT NULL DEFAULT 0,
            email TEXT NOT NULL UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Resumes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Resumes (
            resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            resume_filename TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')

    # Create Skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            skill_text TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')

    conn.commit()
    conn.close()

create_database()
print("Database and tables created successfully.")