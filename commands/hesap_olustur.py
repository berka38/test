"""
Account creation command for the web interface
"""
import os
import secrets
import string
from telethon import events
import jwt
from datetime import datetime, timedelta
import aiohttp

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
            alphabet = string.ascii_letters + string.digits
            temp_password = ''.join(secrets.choice(alphabet) for _ in range(12))

            # Create JWT token
            token = jwt.encode(
                {
                    'telegram_id': telegram_id,
                    'exp': datetime.utcnow() + timedelta(days=1)
                },
                os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here'),
                algorithm="HS256"
            )

            # Send request to web interface API
            api_url = os.environ.get('WEB_API_URL', 'http://localhost:5000')
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{api_url}/api/register",
                    json={
                        'telegram_id': telegram_id,
                        'username': username,
                        'password': temp_password,
                        'token': token
                    }
                ) as response:
                    if response.status == 200:
                        # Send credentials to user
                        message = (
                            "🌟 Web Arayüzü Hesabınız Oluşturuldu!\n\n"
                            f"🔑 Geçici Şifreniz: `{temp_password}`\n\n"
                            "📱 Giriş yapmak için:\n"
                            f"1. {api_url} adresine gidin\n"
                            "2. Telegram ID'nizi girin\n"
                            "3. Geçici şifrenizi kullanın\n\n"
                            "⚠️ Güvenliğiniz için lütfen giriş yaptıktan sonra şifrenizi değiştirin!"
                        )
                    else:
                        error_data = await response.json()
                        message = f"❌ Hesap oluşturma hatası: {error_data.get('message', 'Bilinmeyen hata')}"

            await event.reply(message)

        except Exception as e:
            await event.reply(f"❌ Bir hata oluştu: {str(e)}")

    return hesap_olustur
