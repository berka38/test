# Telegram UserBot

A modular Telegram UserBot with multilingual support and dynamic command loading.

## Features

- Multi-language support (English, Turkish, Spanish)
- Dynamic command loading system
- Secure command installation
- 24/7 uptime on Render.com
- Modular architecture

## Deployment to Render.com

### Step 1: Generate Session String

1. Clone this repository
2. Create a `.env` file with your Telegram API credentials:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   ```
3. Run the session string generator:
   ```bash
   python generate_session.py
   ```
4. Follow the prompts to log in with your phone number
5. Save the generated session string

### Step 2: Deploy to Render.com

1. Fork this repository to your GitHub account
2. Go to [Render.com](https://render.com) and create a new account if you don't have one
3. Click "New +" and select "Web Service"
4. Connect your GitHub account and select the forked repository
5. Configure the service:
   - Name: `telegram-userbot` (or your preferred name)
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`

6. Add Environment Variables:
   - `API_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API Hash
   - `SESSION_STRING`: The session string you generated
   - `COMMAND_PREFIX`: `!` (or your preferred prefix)
   - `COMMANDS_DIR`: `commands`

7. Click "Create Web Service"

Your UserBot will now run 24/7 on Render.com!

## Adding New Commands

1. Create a new Python file in the `commands` directory
2. Follow the command template:
   ```python
   async def command(event, args):
       """
       Command: your_command_name
       Description: What your command does
       Usage: 
           !your_command [args] - Usage description
       """
       # Your code here
       return {
           "prefix": "your_command_name",
           "return": "Response message"
       }
   ```
3. The command will be automatically loaded

## Security Notes

- Keep your session string private
- Never share your API credentials
- Regularly check your active sessions in Telegram
- Be careful when installing third-party commands

## Support

For more information about command development, check the `docs/command_development_guide.md` file.
