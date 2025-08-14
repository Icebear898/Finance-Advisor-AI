#!/usr/bin/env python3
"""
User Management Script for AI Finance Advisor
This script helps you view and manage user data in the database
"""

import sqlite3
import os
import sys
from datetime import datetime

def connect_db():
    """Connect to the database"""
    db_path = "backend/finance_advisor.db"
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        print(f"   Expected location: {db_path}")
        print("   Start the backend server first to create the database.")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {str(e)}")
        return None

def view_all_users():
    """View all users in the database"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, email, full_name, role, is_active, created_at, updated_at
            FROM users ORDER BY created_at DESC
        """)
        
        users = cursor.fetchall()
        
        if not users:
            print("📭 No users found in the database.")
            print("   Register a user through the application first.")
            return
        
        print(f"👥 Found {len(users)} user(s) in the database:")
        print("=" * 80)
        
        for user in users:
            print(f"ID: {user['id']}")
            print(f"Email: {user['email']}")
            print(f"Name: {user['full_name']}")
            print(f"Role: {user['role']}")
            print(f"Active: {'✅ Yes' if user['is_active'] else '❌ No'}")
            print(f"Created: {user['created_at']}")
            print(f"Updated: {user['updated_at']}")
            print("-" * 40)
    
    except Exception as e:
        print(f"❌ Error viewing users: {str(e)}")
    finally:
        conn.close()

def main():
    """Main function"""
    print("👤 AI Finance Advisor - User Management")
    print("=" * 50)
    view_all_users()

if __name__ == "__main__":
    main()
