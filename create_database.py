#!/usr/bin/env python3
"""
Simple script to demonstrate database creation
"""

import sqlite3
import os
from datetime import datetime

def create_database():
    """Create the database and tables"""
    db_path = "backend/finance_advisor.db"
    
    print("🗄️ Creating AI Finance Advisor Database...")
    print(f"📍 Location: {db_path}")
    
    # Create backend directory if it doesn't exist
    os.makedirs("backend", exist_ok=True)
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            is_active BOOLEAN NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create user_sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token_hash TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Create password_reset_tokens table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token_hash TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()
    
    # Check if file was created
    if os.path.exists(db_path):
        file_size = os.path.getsize(db_path)
        print(f"✅ Database created successfully!")
        print(f"📊 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        # Show table structure
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n📋 Created tables ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
        
        conn.close()
        
        return True
    else:
        print("❌ Failed to create database")
        return False

def show_database_info():
    """Show information about the created database"""
    db_path = "backend/finance_advisor.db"
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    print("\n📊 Database Information:")
    print("=" * 40)
    
    # File info
    file_size = os.path.getsize(db_path)
    file_modified = datetime.fromtimestamp(os.path.getmtime(db_path))
    
    print(f"📍 Location: {db_path}")
    print(f"📏 Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"🕒 Last Modified: {file_modified}")
    
    # Database info
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table info
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\n📋 Tables ({len(tables)}):")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   - {table_name}: {count} records")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 AI Finance Advisor - Database Creation Demo")
    print("=" * 50)
    
    success = create_database()
    
    if success:
        show_database_info()
        
        print("\n🎯 What happens when users register:")
        print("   1. User fills out registration form")
        print("   2. Password gets hashed with bcrypt")
        print("   3. User data stored in 'users' table")
        print("   4. JWT token created for authentication")
        print("   5. Token stored in 'user_sessions' table")
        
        print("\n🔍 To view user data:")
        print("   python manage_users.py")
        
        print("\n🧪 To test the full system:")
        print("   ./start_with_auth.sh")
    else:
        print("❌ Database creation failed")
