import sqlite3
import json
from datetime import datetime
import os

class Database:
    def __init__(self, db_path="data/chatbot.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT,
                response TEXT,
                entities TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_user_details(self, name=None, email=None, phone=None):
        """Save or update user details"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users LIMIT 1")
        user = cursor.fetchone()
        
        if user:
            # Update existing user
            user_id = user[0]
            if name:
                cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
            if email:
                cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))
            if phone:
                cursor.execute("UPDATE users SET phone = ? WHERE id = ?", (phone, user_id))
        else:
            # Create new user
            cursor.execute(
                "INSERT INTO users (name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone)
            )
            user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return user_id
    
    def save_conversation(self, user_message, bot_response, extracted_entities):
        """Save conversation to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get or create user
        cursor.execute("SELECT id FROM users LIMIT 1")
        user = cursor.fetchone()
        user_id = user[0] if user else self.save_user_details()
        
        # Save conversation
        cursor.execute(
            "INSERT INTO conversations (user_id, message, response, entities) VALUES (?, ?, ?, ?)",
            (user_id, user_message, bot_response, json.dumps(extracted_entities))
        )
        
        conn.commit()
        conn.close()
    
    def get_user_details(self):
        """Retrieve user details"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, email, phone FROM users LIMIT 1")
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'name': user[0],
                'email': user[1],
                'phone': user[2]
            }
        return None
    
    def get_conversation_history(self, limit=10):
        """Get recent conversations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT message, response, created_at FROM conversations ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        conversations = cursor.fetchall()
        conn.close()
        
        return conversations
