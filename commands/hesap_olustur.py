"""
Account creation command for the web interface
"""
import os
import sys
import jwt
from telethon import events
from loguru import logger

# Add parent directory to path so we can import from web package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models.user import User
from web.app import db

async def init(client):
    @client.on(events.NewMessage(pattern=r"!hesap_olustur"))
    async def hesap_olustur(event):
        """Create a web interface account for the user"""
        try:
            # Get user info
            sender = await event.get_sender()
            telegram_id = str(sender.id)
            username = sender.username or f"user_{telegram_id}"
            
            # Generate temporary password
            temp_password = f"temp_{telegram_id}"
            
            # Check if user already exists
            user = User.get_by_telegram_id(telegram_id)
            if user:
                await event.reply("❌ Bu Telegram ID için zaten bir hesap mevcut!")
                return
            
            # Create user in database
            try:
                user = User.create(
                    telegram_id=telegram_id,
                    username=username,
                    password=temp_password
                )
                logger.info(f"Created new user in database: {telegram_id}")
            except Exception as e:
                logger.error(f"Database error creating user {telegram_id}: {str(e)}")
                await event.reply("❌ Hesap oluşturulurken bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
                return
            
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
            
            await event.reply(message)
            logger.info(f"Account creation info sent to user {telegram_id}")

        except Exception as e:
            error_msg = f"❌ Hesap oluşturma hatası: {str(e)}"
            await event.reply(error_msg)
            logger.error(f"Account creation error for {telegram_id}: {str(e)}")

    return hesap_olustur
