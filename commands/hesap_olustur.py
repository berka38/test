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
from utils.language import get_lang_manager
from werkzeug.security import generate_password_hash

# Add parent directory to path so we can import from web package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..app import mongo
from ..services.auth import AuthService

logger = logging.getLogger('hesap_olustur')

async def command(event, args):
    try:
        lang_manager = get_lang_manager()
        
        # Get user info
        sender = await event.get_sender()
        telegram_id = str(sender.id)  # Use user ID as username
        username = telegram_id  # Username is the Telegram ID
        
        # Generate temporary password
        temp_password = secrets.token_urlsafe(8)
        
        # Initialize auth service
        auth_service = AuthService(mongo.db)
        
        # Check if user exists
        user = auth_service.get_or_create_user(telegram_id, username)
        if user:
            # Set initial password
            if auth_service.set_user_password(telegram_id, temp_password):
                logger.info(f"Created/updated user in MongoDB: {telegram_id}")
            else:
                raise Exception("Failed to set user password")
        else:
            raise Exception("Failed to create user")
        
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
            "return": lang_manager.get_text("hesap_olustur.error", error=str(e))
        }
