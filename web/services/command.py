"""
Command service for the web interface
"""
from ..models.command import Command
from loguru import logger

class CommandService:
    """Service class for handling command operations"""
    
    def __init__(self, db):
        """
        Initialize command service
        
        Args:
            db: MongoDB database instance
        """
        self.db = db

    def create_command(self, name, author_id, description=None, category=None, code=None):
        """
        Create a new command
        
        Args:
            name (str): Command name
            author_id (str): Author's user ID
            description (str, optional): Command description
            category (str, optional): Command category
            code (str, optional): Command code
            
        Returns:
            Command: New command instance
        """
        try:
            command = Command.create(
                self.db,
                name=name,
                author_id=author_id,
                description=description,
                category=category,
                code=code
            )
            logger.info(f"Created new command: {name} by user {author_id}")
            return command
        except Exception as e:
            logger.error(f"Error creating command: {str(e)}")
            raise

    def get_user_commands(self, user_id):
        """
        Get all commands for a user
        
        Args:
            user_id (str): User ID
            
        Returns:
            list: List of Command instances
        """
        try:
            commands = Command.get_user_commands(self.db, user_id)
            logger.debug(f"Retrieved {len(commands)} commands for user {user_id}")
            return commands
        except Exception as e:
            logger.error(f"Error getting user commands: {str(e)}")
            raise

    def toggle_command(self, command_id):
        """
        Toggle command active status
        
        Args:
            command_id (str): Command ID
            
        Returns:
            bool: New active state
        """
        try:
            command = Command.get_by_id(self.db, command_id)
            if not command:
                logger.warning(f"Command not found: {command_id}")
                return None
                
            new_state = command.toggle_active(self.db)
            logger.info(f"Toggled command {command_id} to {new_state}")
            return new_state
        except Exception as e:
            logger.error(f"Error toggling command: {str(e)}")
            raise

    def update_command(self, command_id, **updates):
        """
        Update command attributes
        
        Args:
            command_id (str): Command ID
            **updates: Attributes to update
            
        Returns:
            Command: Updated command instance
        """
        try:
            command = Command.get_by_id(self.db, command_id)
            if not command:
                logger.warning(f"Command not found: {command_id}")
                return None
                
            command.update(self.db, **updates)
            logger.info(f"Updated command {command_id}")
            return command
        except Exception as e:
            logger.error(f"Error updating command: {str(e)}")
            raise
