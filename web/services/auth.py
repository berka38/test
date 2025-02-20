"""
Authentication service for the web interface
"""
from loguru import logger
from werkzeug.security import generate_password_hash
from datetime import datetime
from ..models.user import User

class AuthService:
    """Service class that handles user authentication"""
    
    def __init__(self, mongo_db):
        """
        Initialize auth service
        
        Args:
            mongo_db: MongoDB database instance
        """
        self.db = mongo_db

    def get_or_create_user(self, telegram_id, username=None):
        """
        Get existing user or create new one
        
        Args:
            telegram_id (str): Telegram user ID
            username (str, optional): Username
            
        Returns:
            User: User instance
        """
        user_data = self.db.users.find_one({"telegram_id": str(telegram_id)})
        if not user_data:
            logger.info(f"Creating new user with telegram_id: {telegram_id}")
            user_data = {
                "telegram_id": str(telegram_id),
                "username": username or f"user_{telegram_id}",
                "is_active": True,
                "created_at": datetime.utcnow(),
                "last_login": None
            }
            self.db.users.insert_one(user_data)
            user_data = self.db.users.find_one({"telegram_id": str(telegram_id)})
        return User(user_data)

    def authenticate_user(self, telegram_id, password):
        """
        Authenticate user with telegram ID and password
        
        Args:
            telegram_id (str): Telegram user ID
            password (str): Password
            
        Returns:
            User: User instance if authenticated, None otherwise
        """
        user_data = self.db.users.find_one({"telegram_id": str(telegram_id)})
        if user_data:
            user = User(user_data)
            if user.check_password(password):
                self.db.users.update_one(
                    {"telegram_id": str(telegram_id)},
                    {"$set": {"last_login": datetime.utcnow()}}
                )
                return user
        return None

    def set_user_password(self, telegram_id, password):
        """
        Set user password
        
        Args:
            telegram_id (str): Telegram user ID
            password (str): New password
            
        Returns:
            bool: True if successful, False otherwise
        """
        result = self.db.users.update_one(
            {"telegram_id": str(telegram_id)},
            {"$set": {"password": generate_password_hash(password)}}
        )
        return result.modified_count > 0
