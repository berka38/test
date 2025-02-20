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
from werkzeug.security import generate_password_hash
from datetime import datetime

# Add parent directory to path so we can import from web package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.app import mongo

logger = logging.getLogger('hesap_olustur')

async def command(event, args):
    try:
        # Get user info
        sender = await event.get_sender()
        telegram_id = str(sender.id)
        username = sender.username or f"user_{telegram_id}"
        
        # Generate temporary password
        temp_password = secrets.token_urlsafe(8)
        hashed_password = generate_password_hash(temp_password)
        
        try:
            # Check if user exists
            existing_user = mongo.db.users.find_one({"telegram_id": telegram_id})
            if existing_user:
                return {
                    "prefix": "hesap_olustur",
                    "return": "❌ Bu Telegram ID için zaten bir hesap mevcut!"
                }
            
            # Create user document
            user_data = {
                "telegram_id": telegram_id,
                "username": username,
                "password": hashed_password,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "last_login": None
            }
            
            # Insert into MongoDB
            result = mongo.db.users.insert_one(user_data)
            if not result.inserted_id:
                raise Exception("Failed to create user in database")
                
            logger.info(f"Created new user in MongoDB: {telegram_id}")
            
        except Exception as e:
            logger.error(f"Database error creating user {telegram_id}: {str(e)}")
            return {
                "prefix": "hesap_olustur",
                "return": "❌ Hesap oluşturulurken bir hata oluştu. Lütfen daha sonra tekrar deneyin."
            }
        
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
        error_msg = f"❌ Hesap oluşturma hatası: {str(e)}"
        logger.error(error_msg)
        return {
            "prefix": "hesap_olustur",
            "return": error_msg
        }
