import os
import logging
from utils.language import get_lang_manager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cmd_handler')

async def command(event, args):
    """
    Command: cmd
    Description: Manage commands (list, install, remove)
    Usage: 
        !cmd list - List all installed commands
        !cmd install - Install command from replied Python file
        !cmd remove <name> - Remove a command
    """
    try:
        logger.info("Command handler started with args: %s", args)
        lang_manager = get_lang_manager()
        
        if not args:
            logger.warning("No arguments provided")
            return {
                "prefix": "cmd",
                "return": lang_manager.get_text("cmd.specify_action")
            }
        
        action = args[0].lower()
        commands_dir = os.getenv('COMMANDS_DIR', 'commands')
        logger.info("Action: %s, Commands dir: %s", action, commands_dir)
        
        if action == "list":
            logger.info("Listing commands from directory: %s", commands_dir)
            try:
                commands = [f for f in os.listdir(commands_dir) if f.endswith('.py') and not f.startswith('_')]
                logger.info("Found commands: %s", commands)
                message = f"{lang_manager.get_text('cmd.installed_commands')}\n\n" + \
                         "\n".join([f"• `{cmd[:-3]}`" for cmd in commands])
                return {
                    "prefix": "cmd",
                    "return": message
                }
            except Exception as e:
                logger.error("Error listing commands: %s", str(e))
                return {
                    "prefix": "cmd",
                    "return": f"Error listing commands: {str(e)}"
                }
        
        elif action == "install":
            logger.info("Install command initiated")
            # Check if the command is a reply to a message
            if not event.message.is_reply:
                logger.warning("No reply message found")
                return {
                    "prefix": "cmd",
                    "return": lang_manager.get_text("cmd.install_no_reply")
                }
            
            try:
                # Get the replied message
                reply_msg = await event.message.get_reply_message()
                logger.info("Got reply message")
                
                # Check if there's a file in the reply
                if not reply_msg.file:
                    logger.warning("No file in reply message")
                    return {
                        "prefix": "cmd",
                        "return": lang_manager.get_text("cmd.install_no_python_file")
                    }
                
                if not reply_msg.file.name.endswith('.py'):
                    logger.warning("File is not a Python file: %s", reply_msg.file.name)
                    return {
                        "prefix": "cmd",
                        "return": lang_manager.get_text("cmd.install_no_python_file")
                    }
                
                # Download the file
                file_path = os.path.join(commands_dir, reply_msg.file.name)
                logger.info("Downloading file to: %s", file_path)
                await reply_msg.download_media(file=file_path)
                logger.info("File downloaded successfully")
                
                # Basic validation of the file content
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        logger.info("Reading file content")
                        if "async def command" not in content:
                            logger.warning("Invalid command format - missing async def command")
                            os.remove(file_path)  # Remove invalid file
                            return {
                                "prefix": "cmd",
                                "return": lang_manager.get_text("cmd.invalid_format")
                            }
                except Exception as e:
                    logger.error("Error reading file: %s", str(e))
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    return {
                        "prefix": "cmd",
                        "return": f"Error reading file: {str(e)}"
                    }
                
                command_name = reply_msg.file.name[:-3]  # Remove .py extension
                logger.info("Command installed successfully: %s", command_name)
                return {
                    "prefix": "cmd",
                    "return": lang_manager.get_text("cmd.install_success", command=command_name)
                }
                
            except Exception as e:
                logger.error("Installation error: %s", str(e))
                if 'file_path' in locals() and os.path.exists(file_path):
                    os.remove(file_path)  # Clean up on error
                return {
                    "prefix": "cmd",
                    "return": lang_manager.get_text("cmd.install_error", error=str(e))
                }
        
        elif action == "remove" and len(args) > 1:
            cmd_name = args[1]
            if not cmd_name.endswith('.py'):
                cmd_name += '.py'
            
            cmd_path = os.path.join(commands_dir, cmd_name)
            logger.info("Attempting to remove command: %s", cmd_path)
            
            if os.path.exists(cmd_path):
                try:
                    os.remove(cmd_path)
                    logger.info("Command removed successfully: %s", cmd_name)
                    return {
                        "prefix": "cmd",
                        "return": lang_manager.get_text("cmd.remove_success", command=cmd_name[:-3])
                    }
                except Exception as e:
                    logger.error("Error removing command: %s", str(e))
                    return {
                        "prefix": "cmd",
                        "return": lang_manager.get_text("cmd.remove_error", error=str(e))
                    }
            else:
                logger.warning("Command not found: %s", cmd_path)
                return {
                    "prefix": "cmd",
                    "return": lang_manager.get_text("cmd.not_found", command=cmd_name[:-3])
                }
        
        logger.warning("Invalid action: %s", action)
        return {
            "prefix": "cmd",
            "return": lang_manager.get_text("cmd.invalid_action")
        }
    except Exception as e:
        logger.error("Unexpected error in cmd command: %s", str(e))
        return {
            "prefix": "cmd",
            "return": f"An unexpected error occurred: {str(e)}"
        }
