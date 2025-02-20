import os
import sys
import importlib
import traceback
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv
from loguru import logger
from utils.language import get_lang_manager

def main():
    try:
        # Load environment variables
        load_dotenv()

        # Configure logging
        logger.add("bot.log", rotation="1 day", retention="7 days", level="INFO")

        # Initialize language manager
        lang_manager = get_lang_manager()

        class UserBot:
            def __init__(self):
                # Check for required environment variables
                self.api_id = os.getenv('API_ID')
                self.api_hash = os.getenv('API_HASH')
                self.session_string = os.getenv('SESSION_STRING')
                
                if not all([self.api_id, self.api_hash, self.session_string]):
                    raise ValueError(
                        "API_ID, API_HASH, and SESSION_STRING must be set in environment variables\n"
                        "Please set these in your Render.com environment variables or .env file\n"
                        "You can get API credentials from https://my.telegram.org\n"
                        "Generate SESSION_STRING using generate_session.py"
                    )
                    
                self.prefix = os.getenv('COMMAND_PREFIX', '!')
                self.commands_dir = os.getenv('COMMANDS_DIR', 'commands')
                
                # Initialize client with string session
                self.client = TelegramClient(
                    StringSession(self.session_string),
                    self.api_id,
                    self.api_hash
                )
                
                # Command storage
                self.commands = {}
                
                # Load commands
                self.load_commands()
                
                # Register message handler
                self.client.add_event_handler(self.command_handler, events.NewMessage)
            
            def load_commands(self):
                """Load all commands from the commands directory."""
                try:
                    if not os.path.exists(self.commands_dir):
                        os.makedirs(self.commands_dir)
                        
                    # Clear existing commands
                    self.commands = {}
                    
                    # Remove commands_dir from sys.path if it exists
                    if self.commands_dir in sys.path:
                        sys.path.remove(self.commands_dir)
                    
                    # Add commands_dir to sys.path
                    sys.path.insert(0, self.commands_dir)
                    
                    # Load each command
                    for filename in os.listdir(self.commands_dir):
                        if filename.endswith('.py') and not filename.startswith('_'):
                            module_name = filename[:-3]
                            try:
                                # Remove the module if it's already loaded
                                if module_name in sys.modules:
                                    del sys.modules[module_name]
                                
                                # Import the module
                                module = importlib.import_module(module_name)
                                
                                if hasattr(module, 'command'):
                                    self.commands[module_name] = module.command
                                    logger.info(f"Loaded command: {module_name}")
                                else:
                                    logger.warning(f"Module {module_name} has no command function")
                            except Exception as e:
                                logger.error(f"Failed to load command {module_name}: {str(e)}\n{traceback.format_exc()}")
                except Exception as e:
                    logger.error(f"Error in load_commands: {str(e)}\n{traceback.format_exc()}")
            
            async def command_handler(self, event):
                """Handle incoming commands."""
                try:
                    if event.message.text and event.message.text.startswith(self.prefix):
                        command_text = event.message.text[len(self.prefix):]
                        command_name = command_text.split()[0].lower()
                        args = command_text.split()[1:] if len(command_text.split()) > 1 else []
                        
                        logger.info(f"Received command: {command_name} with args: {args}")
                        
                        # Reload commands if using cmd command
                        if command_name == "cmd":
                            self.load_commands()
                            logger.info("Reloaded commands")
                        
                        if command_name in self.commands:
                            try:
                                logger.info(f"Executing command: {command_name}")
                                result = await self.commands[command_name](event, args)
                                
                                # Handle both direct replies and dictionary returns
                                if isinstance(result, dict):
                                    prefix = result.get('prefix', '')
                                    message = result.get('return', 'Command executed successfully')
                                    if prefix:
                                        message = f"[{prefix}] {message}"
                                    await event.reply(message)
                                    logger.info(f"Command {command_name} executed successfully")
                            except Exception as e:
                                error_msg = f"Error executing command {command_name}: {str(e)}\n{traceback.format_exc()}"
                                logger.error(error_msg)
                                await event.reply(f"Error executing command: {str(e)}")
                        else:
                            logger.warning(f"Command not found: {command_name}")
                except Exception as e:
                    logger.error(f"Error in command handler: {str(e)}\n{traceback.format_exc()}")
            
            async def start(self):
                """Start the userbot."""
                logger.info("Starting userbot...")
                await self.client.start()
                logger.info("Userbot is running...")
                await self.client.run_until_disconnected()

        # Create and start the bot
        bot = UserBot()
        bot.client.loop.run_until_complete(bot.start())

    except Exception as e:
        error_msg = f"Error: {str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        print(error_msg)
        logger.error(error_msg)

if __name__ == '__main__':
    main()
