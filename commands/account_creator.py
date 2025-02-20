"""
Command: account_creator
Description: Creates a new user account via Telegram
Usage:
    !account_creator <username> <password>
Help:
    Creates a new user account with the given username and password.
    The password is hashed before being stored in the database.
    Returns a success message if the account is created successfully.
    Returns an error message if the account cannot be created.
"""
import logging
import secrets
import os
import sys
from werkzeug.security import generate_password_hash

# Add parent directory to path so we can import from web package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..app import mongo
from ..services.auth import AuthService

logger = logging.getLogger('account_creator')

async def command(event, args):
    try:
        if len(args) < 2:
            return {
                "prefix": "account_creator",
                "return": "❌ Kullanıcı adı ve şifre gereklidir."
            }
        username = args[0]
        password = args[1]
        
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Create user in MongoDB
        user_data = {
            "username": username,
            "password": hashed_password,
            "is_active": True
        }
        
        result = mongo.db.users.insert_one(user_data)
        if result.inserted_id:
            logger.info(f"Kullanıcı oluşturuldu: {username}")
            return {
                "prefix": "account_creator",
                "return": "✅ Kullanıcı başarıyla oluşturuldu!"
            }
        else:
            return {
                "prefix": "account_creator",
                "return": "❌ Kullanıcı oluşturulamadı."
            }
    except Exception as e:
        logger.error(f"Error creating account: {str(e)}")
        return {
            "prefix": "account_creator",
            "return": "❌ Hata oluştu. Lütfen tekrar deneyin."
        }
