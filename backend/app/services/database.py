import sqlite3
import os
from datetime import datetime
from typing import Optional, List
from contextlib import contextmanager
from loguru import logger

from ..models.auth import UserCreate, UserInDB, User, UserUpdate
from ..utils.auth_utils import get_password_hash, verify_password


class DatabaseService:
    def __init__(self, db_path: str = "finance_advisor.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database and create tables"""
        with self.get_connection() as conn:
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
            
            # Create user_sessions table for token management
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
            logger.info("Database initialized successfully")

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()

    def create_user(self, user_create: UserCreate) -> Optional[User]:
        """Create a new user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if user already exists
                cursor.execute("SELECT id FROM users WHERE email = ?", (user_create.email,))
                if cursor.fetchone():
                    logger.warning(f"User with email {user_create.email} already exists")
                    return None
                
                # Hash password and create user
                hashed_password = get_password_hash(user_create.password)
                now = datetime.utcnow()
                
                cursor.execute("""
                    INSERT INTO users (email, full_name, hashed_password, role, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user_create.email,
                    user_create.full_name,
                    hashed_password,
                    user_create.role.value,
                    now,
                    now
                ))
                
                user_id = cursor.lastrowid
                conn.commit()
                
                # Return the created user
                return self.get_user_by_id(user_id)
                
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return None

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, email, full_name, hashed_password, role, is_active, created_at, updated_at
                    FROM users WHERE email = ?
                """, (email,))
                
                row = cursor.fetchone()
                if row:
                    return UserInDB(
                        id=row['id'],
                        email=row['email'],
                        full_name=row['full_name'],
                        hashed_password=row['hashed_password'],
                        role=row['role'],
                        is_active=bool(row['is_active']),
                        created_at=datetime.fromisoformat(row['created_at']),
                        updated_at=datetime.fromisoformat(row['updated_at'])
                    )
                return None
                
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID (without password)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, email, full_name, role, is_active, created_at, updated_at
                    FROM users WHERE id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                if row:
                    return User(
                        id=row['id'],
                        email=row['email'],
                        full_name=row['full_name'],
                        role=row['role'],
                        is_active=bool(row['is_active']),
                        created_at=datetime.fromisoformat(row['created_at']),
                        updated_at=datetime.fromisoformat(row['updated_at'])
                    )
                return None
                
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """Authenticate user with email and password"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Build update query dynamically
                update_fields = []
                update_values = []
                
                if user_update.full_name is not None:
                    update_fields.append("full_name = ?")
                    update_values.append(user_update.full_name)
                
                if user_update.email is not None:
                    update_fields.append("email = ?")
                    update_values.append(user_update.email)
                
                if not update_fields:
                    return self.get_user_by_id(user_id)
                
                update_fields.append("updated_at = ?")
                update_values.append(datetime.utcnow())
                update_values.append(user_id)
                
                query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
                cursor.execute(query, update_values)
                conn.commit()
                
                return self.get_user_by_id(user_id)
                
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return None

    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get current user
                cursor.execute("SELECT hashed_password FROM users WHERE id = ?", (user_id,))
                row = cursor.fetchone()
                if not row:
                    return False
                
                # Verify current password
                if not verify_password(current_password, row['hashed_password']):
                    return False
                
                # Update password
                new_hashed_password = get_password_hash(new_password)
                cursor.execute("""
                    UPDATE users SET hashed_password = ?, updated_at = ? WHERE id = ?
                """, (new_hashed_password, datetime.utcnow(), user_id))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error changing password: {str(e)}")
            return False

    def create_password_reset_token(self, user_id: int, token_hash: str, expires_at: datetime) -> bool:
        """Create a password reset token"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Invalidate any existing tokens for this user
                cursor.execute("""
                    UPDATE password_reset_tokens SET used = 1 
                    WHERE user_id = ? AND used = 0
                """, (user_id,))
                
                # Create new token
                cursor.execute("""
                    INSERT INTO password_reset_tokens (user_id, token_hash, expires_at)
                    VALUES (?, ?, ?)
                """, (user_id, token_hash, expires_at))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error creating password reset token: {str(e)}")
            return False

    def verify_password_reset_token(self, token_hash: str) -> Optional[int]:
        """Verify password reset token and return user_id if valid"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT user_id FROM password_reset_tokens 
                    WHERE token_hash = ? AND used = 0 AND expires_at > ?
                """, (token_hash, datetime.utcnow()))
                
                row = cursor.fetchone()
                return row['user_id'] if row else None
                
        except Exception as e:
            logger.error(f"Error verifying password reset token: {str(e)}")
            return None

    def mark_password_reset_token_used(self, token_hash: str) -> bool:
        """Mark password reset token as used"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE password_reset_tokens SET used = 1 
                    WHERE token_hash = ?
                """, (token_hash,))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error marking password reset token as used: {str(e)}")
            return False

    def get_all_users(self) -> List[User]:
        """Get all users (for admin)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, email, full_name, role, is_active, created_at, updated_at
                    FROM users ORDER BY created_at DESC
                """)
                
                users = []
                for row in cursor.fetchall():
                    users.append(User(
                        id=row['id'],
                        email=row['email'],
                        full_name=row['full_name'],
                        role=row['role'],
                        is_active=bool(row['is_active']),
                        created_at=datetime.fromisoformat(row['created_at']),
                        updated_at=datetime.fromisoformat(row['updated_at'])
                    ))
                
                return users
                
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            return []


# Global database instance
db_service = DatabaseService()
