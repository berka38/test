"""
Command: hesap_olustur
Description: Web arayüzü için hesap oluşturur
Usage:
    !hesap_olustur - Web arayüzü için yeni bir hesap oluşturur
"""
import os
import sqlite3
import hashlib
import secrets
import logging

logger = logging.getLogger('hesap_olustur')

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

async def command(event, args):
    try:
        # Get user info
        sender = await event.get_sender()
        telegram_id = str(sender.id)
        username = sender.username or f"user_{telegram_id}"
        
        # Generate temporary password
        temp_password = secrets.token_urlsafe(8)
        hashed_password = hash_password(temp_password)
        
        # Connect to SQLite database
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'web.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Create users table if not exists
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Check if user exists
            cursor.execute('SELECT telegram_id FROM users WHERE telegram_id = ?', (telegram_id,))
            if cursor.fetchone():
                return {
                    "prefix": "hesap_olustur",
                    "return": "❌ Bu Telegram ID için zaten bir hesap mevcut!"
                }
            
            # Insert new user
            cursor.execute(
                'INSERT INTO users (telegram_id, username, password) VALUES (?, ?, ?)',
                (telegram_id, username, hashed_password)
            )
            conn.commit()
            logger.info(f"Created new user in database: {telegram_id}")
            
        except Exception as e:
            logger.error(f"Database error creating user {telegram_id}: {str(e)}")
            return {
                "prefix": "hesap_olustur",
                "return": "❌ Hesap oluşturulurken bir hata oluştu. Lütfen daha sonra tekrar deneyin."
            }
        finally:
            conn.close()
        
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
