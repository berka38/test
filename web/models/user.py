"""
User model for the web interface using MongoDB
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pymongo import MongoClient
import os

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('MONGO_DB_NAME', 'userbot')

class User(UserMixin):
    """User model that handles user authentication and management"""
    
    def __init__(self, user_data):
        self.user_data = user_data
        
    @property
    def id(self):
        """Return telegram_id as the user identifier for Flask-Login"""
        return self.telegram_id
        
    @property
    def telegram_id(self):
        return self.user_data.get('telegram_id')
        
    @property
    def username(self):
        return self.user_data.get('username')
        
    @property
    def is_active(self):
        return self.user_data.get('is_active', True)
        
    @property
    def created_at(self):
        return self.user_data.get('created_at')
        
    @property
    def last_login(self):
        return self.user_data.get('last_login')
    
    def check_password(self, password):
        """Check if password matches"""
        stored_password = self.user_data.get('password')
        if not stored_password:
            return False
        return check_password_hash(stored_password, password)
        
    def update_last_login(self):
        """Update last login timestamp"""
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        users = db.users
        
        users.update_one(
            {'telegram_id': self.telegram_id},
            {'$set': {'last_login': datetime.utcnow()}}
        )
        client.close()

    @staticmethod
    def get_by_telegram_id(telegram_id):
        """Get user by Telegram ID"""
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        users = db.users
        
        user_data = users.find_one({'telegram_id': str(telegram_id)})
        client.close()
        
        if user_data:
            return User(user_data)
        return None

    def set_password(self, password):
        """Set new password"""
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        users = db.users
        
        users.update_one(
            {'telegram_id': self.telegram_id},
            {'$set': {'password': generate_password_hash(password)}}
        )
        client.close()
        
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'telegram_id': self.telegram_id,
            'username': self.username,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    @staticmethod
    def create(telegram_id, username=None, password=None):
        """
        Create a new user
        
        Args:
            telegram_id (str): Telegram user ID
            username (str, optional): Username
            password (str, optional): Password
            
        Returns:
            User: New user instance
        """
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        users = db.users
        
        user_data = {
            'telegram_id': str(telegram_id),
            'username': username or f"user_{telegram_id}",
            'password': generate_password_hash(password) if password else None,
            'is_active': True,
            'created_at': datetime.utcnow()
        }
        
        users.insert_one(user_data)
        client.close()
        
        return User(user_data)
