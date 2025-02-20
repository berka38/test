import os
import importlib
import inspect
import logging
from utils.language import get_lang_manager

logger = logging.getLogger('help')

def parse_docstring(doc):
    """Parse command docstring to extract name, description and usage."""
    if not doc:
        return None, None, None
    
    lines = [line.strip() for line in doc.split('\n') if line.strip()]
    name = ""
    description = ""
    usage = []
    
    for line in lines:
        if line.startswith('Command:'):
            name = line.replace('Command:', '').strip()
        elif line.startswith('Description:'):
            description = line.replace('Description:', '').strip()
        elif line.startswith('Usage:'):
            continue
        elif line.startswith('!'):
            usage.append(line.strip())
    
    return name, description, '\n'.join(usage) if usage else None

def is_builtin_command(module_name):
    """Check if a command is built-in or externally loaded."""
    builtin_commands = {'help', 'cmd', 'ping', 'echo', 'sysinfo', 'lang'}
    return module_name in builtin_commands

async def command(event, args):
    """
    Command: help
    Description: Shows list of available commands and their usage
    Usage: 
        !help - Lists all available commands
        !help <command> - Shows detailed help for specific command
    """
    lang_manager = get_lang_manager()
    commands_dir = os.getenv('COMMANDS_DIR', 'commands')
    prefix = os.getenv('COMMAND_PREFIX', '!')
    
    if not args:
        # List all commands
        commands = []
        for filename in os.listdir(commands_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_name = filename[:-3]
                logger.info(f"Checking command: {module_name}")  # Log command check
                try:
                    if is_builtin_command(module_name):
                        # Use translations for built-in commands
                        cmd_name = lang_manager.get_text(f"commands.{module_name}.name")
                        cmd_desc = lang_manager.get_text(f"commands.{module_name}.description")
                        commands.append(f"• `{prefix}{cmd_name}` - {cmd_desc}")
                    else:
                        # Use docstring for external commands
                        module = importlib.import_module(module_name)
                        if module and hasattr(module, 'command'):
                            doc = inspect.getdoc(module.command)
                            name, desc, _ = parse_docstring(doc)
                            if name and desc:
                                commands.append(f"• `{prefix}{name}` - {desc}")
                            else:
                                commands.append(f"• `{prefix}{module_name}` - No description available")
                            logger.info(f"Loaded command: {module_name}")
                        else:
                            logger.warning(f"Module {module_name} has no command function")
                except Exception as e:
                    logger.error(f"Failed to load command {module_name}: {str(e)}")
        
        help_text = lang_manager.get_text("help.title") + "\n\n"
        help_text += '\n'.join(sorted(commands))
        help_text += f"\n\n{lang_manager.get_text('help.usage_note', prefix=prefix)}"
        
        return {
            "prefix": "help",
            "return": help_text
        }
    else:
        # Show detailed help for specific command
        command_name = args[0].lower()
        try:
            if is_builtin_command(command_name):
                # Use translations for built-in commands
                cmd_desc = lang_manager.get_text(f"commands.{command_name}.description")
                cmd_usage = lang_manager.get_text(f"commands.{command_name}.usage")
                help_text = lang_manager.get_text("help.detail_title", command=command_name) + "\n\n"
                help_text += f"**Description:** {cmd_desc}\n"
                help_text += f"**Usage:** {cmd_usage}"
            else:
                # Use docstring for external commands
                module = importlib.import_module(command_name)
                if module and hasattr(module, 'command'):
                    doc = inspect.getdoc(module.command)
                    name, desc, usage = parse_docstring(doc)
                    if desc:
                        help_text = f"**{command_name.upper()} Command**\n\n"
                        help_text += f"**Description:** {desc}\n"
                        if usage:
                            help_text += f"**Usage:**\n{usage}"
                        else:
                            help_text += f"**Usage:** {prefix}{command_name}"
                    else:
                        help_text = lang_manager.get_text("help.not_found", command=command_name)
                else:
                    help_text = lang_manager.get_text("help.not_found", command=command_name)
            
            return {
                "prefix": "help",
                "return": help_text
            }
        except Exception as e:
            logger.error(f"Failed to load command {command_name}: {str(e)}")
            return {
                "prefix": "help",
                "return": lang_manager.get_text("help.not_found", command=command_name)
            }
