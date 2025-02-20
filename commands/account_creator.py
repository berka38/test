"""
Command: account_creator
Description: Creates a new user account via Telegram
Usage:
    !account_creator <username> <password>
"""
import logging
from werkzeug.security import generate_password_hash
from web.app import mongo

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
