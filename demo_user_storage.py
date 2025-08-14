#!/usr/bin/env python3
"""
Demo script to show how user data gets stored in the database
"""

import sqlite3
import os
from datetime import datetime
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_demo_user():
    """Create a demo user to show storage"""
    db_path = "backend/finance_advisor.db"
    
    if not os.path.exists(db_path):
        print("❌ Database not found! Run create_database.py first.")
        return
    
    print("👤 Creating Demo User...")
    print("=" * 40)
    
    # Demo user data
    demo_user = {
        "email": "demo@example.com",
        "full_name": "Demo User",
        "password": "demo123456",
        "role": "user"
    }
    
    # Hash the password
    hashed_password = hash_password(demo_user["password"])
    
    print(f"📧 Email: {demo_user['email']}")
    print(f"👤 Name: {demo_user['full_name']}")
    print(f"🔑 Password: {demo_user['password']} (will be hashed)")
    print(f"🔐 Hashed Password: {hashed_password[:50]}...")
    print(f"👨‍💼 Role: {demo_user['role']}")
    
    # Insert into database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO users (email, full_name, hashed_password, role, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            demo_user["email"],
            demo_user["full_name"],
            hashed_password,
            demo_user["role"],
            datetime.utcnow(),
            datetime.utcnow()
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        print(f"\n✅ Demo user created successfully!")
        print(f"🆔 User ID: {user_id}")
        
        # Show the stored data
        cursor.execute("""
            SELECT id, email, full_name, hashed_password, role, is_active, created_at, updated_at
            FROM users WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        
        print(f"\n📊 Stored User Data:")
        print("=" * 40)
        print(f"ID: {user[0]}")
        print(f"Email: {user[1]}")
        print(f"Full Name: {user[2]}")
        print(f"Hashed Password: {user[3][:50]}...")
        print(f"Role: {user[4]}")
        print(f"Active: {'Yes' if user[5] else 'No'}")
        print(f"Created: {user[6]}")
        print(f"Updated: {user[7]}")
        
    except sqlite3.IntegrityError:
        print("⚠️  Demo user already exists!")
    except Exception as e:
        print(f"❌ Error creating demo user: {str(e)}")
    finally:
        conn.close()

def show_all_users():
    """Show all users in the database"""
    db_path = "backend/finance_advisor.db"
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, email, full_name, role, is_active, created_at, updated_at
            FROM users ORDER BY created_at DESC
        """)
        
        users = cursor.fetchall()
        
        if not users:
            print("📭 No users found in the database.")
            return
        
        print(f"\n👥 All Users in Database ({len(users)}):")
        print("=" * 80)
        
        for user in users:
            print(f"🆔 ID: {user['id']}")
            print(f"📧 Email: {user['email']}")
            print(f"👤 Name: {user['full_name']}")
            print(f"👨‍💼 Role: {user['role']}")
            print(f"✅ Active: {'Yes' if user['is_active'] else 'No'}")
            print(f"📅 Created: {user['created_at']}")
            print(f"🔄 Updated: {user['updated_at']}")
            print("-" * 40)
    
    except Exception as e:
        print(f"❌ Error viewing users: {str(e)}")
    finally:
        conn.close()

def show_database_structure():
    """Show the database structure"""
    db_path = "backend/finance_advisor.db"
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n🗄️ Database Structure:")
    print("=" * 40)
    
    # Show tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\n📋 Table: {table_name}")
        
        # Show table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            print(f"   - {col_name}: {col_type} {'(PK)' if pk else ''} {'(NOT NULL)' if not_null else ''}")
        
        # Show record count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   📊 Records: {count}")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 AI Finance Advisor - User Storage Demo")
    print("=" * 50)
    
    # Show database structure first
    show_database_structure()
    
    # Create demo user
    create_demo_user()
    
    # Show all users
    show_all_users()
    
    print("\n🎯 Key Points:")
    print("   1. User data is stored in SQLite database")
    print("   2. Passwords are hashed with bcrypt")
    print("   3. Each user gets a unique ID")
    print("   4. Timestamps track creation and updates")
    print("   5. Database file: backend/finance_advisor.db")
    
    print("\n🔍 To view users anytime:")
    print("   python manage_users.py")
