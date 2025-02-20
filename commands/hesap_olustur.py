"""
Command: hesap_olustur
Description: Web arayüzü için hesap oluşturur
Usage:
    !hesap_olustur - Web arayüzü için yeni bir hesap oluşturur
"""
import os
import sys
import secrets
import logging
from datetime import datetime
from werkzeug.security import generate_password_hash

# Import from the web package using absolute imports
from web.app import mongo
from web.services.auth import AuthService

logger = logging.getLogger('hesap_olustur')

async def command(event, args):
    """
    Command: hesap_olustur
    Description: Telegram kullanıcıları için yeni bir hesap oluşturur.
    Usage:
        !hesap_olustur - Yeni bir hesap oluşturur.
    """
    try:
        # Get user info
        sender = await event.get_sender()
        telegram_id = str(sender.id)  # Use user ID as username
        username = telegram_id  # Username is the Telegram ID
        
        # Generate temporary password
        temp_password = secrets.token_urlsafe(8)

        # Ensure mongo is initialized
        if mongo is None:
            raise Exception("MongoDB is not initialized.")

        # Check if the 'users' collection exists, if not create it
        if 'users' not in mongo.db.list_collection_names():
            mongo.db.create_collection('users')
            logger.info("'users' collection created in MongoDB.")

        # Initialize auth service
        auth_service = AuthService(mongo.db)

        # Function to create a new user if it doesn't exist
        async def create_user_if_not_exists(telegram_id, username):
            user_data = mongo.db.users.find_one({'telegram_id': telegram_id})
            if user_data is None:
                user_data = {
                    'telegram_id': telegram_id,
                    'username': username,
                    'is_active': True,
                    'created_at': datetime.utcnow()
                }
                mongo.db.users.insert_one(user_data)
                logger.info(f"User created: {telegram_id}")
            else:
                logger.info(f"User already exists: {telegram_id}")
            return user_data

        # Create user if it doesn't exist
        user = await create_user_if_not_exists(telegram_id, username)

        # Set initial password
        if auth_service.set_user_password(telegram_id, temp_password):
            logger.info(f"Created/updated user in MongoDB: {telegram_id}")
        else:
            raise Exception("Failed to set user password")

        # Send credentials to user
        web_url = os.getenv('WEB_URL', 'http://localhost:5000')
        message = (
            "🌟 Web Arayüzü Hesabınız Hazır!\n\n"
            f"🆔 Telegram ID: `{telegram_id}`\n"
            f"🔑 Geçici Şifreniz: `{temp_password}`\n\n"
            "📱 Giriş yapmak için:\n"
            f"1. {web_url} adresine gidin\n"
            "2. Telegram ID'nizi girin\n"
            "3. Geçici şifrenizi kullanın\n\n"
            "⚠️ Güvenliğiniz için lütfen giriş yaptıktan sonra şifrenizi değiştirin!"
        )
        
        return {
            "prefix": "hesap_olustur",
            "return": message
        }

    except Exception as e:
        logger.error(f"Error creating account: {str(e)}")
        return {
            "prefix": "hesap_olustur",
            "return": f"❌ Hesap oluşturulurken bir hata oluştu: {str(e)}"
        }
