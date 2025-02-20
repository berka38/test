"""
Command model for the web interface
"""
from datetime import datetime

class Command:
    """Command model that represents a bot command"""
    
    def __init__(self, command_data):
        """Initialize command from MongoDB document"""
        self.command_data = command_data
        
    @property
    def name(self):
        return self.command_data.get('name')
        
    @property
    def description(self):
        return self.command_data.get('description')
        
    @property
    def code(self):
        return self.command_data.get('code')
        
    @property
    def created_by(self):
        return self.command_data.get('created_by')
        
    @property
    def is_active(self):
        return self.command_data.get('is_active', True)
        
    @property
    def created_at(self):
        return self.command_data.get('created_at')
        
    def to_dict(self):
        """Convert command to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'created_by': self.created_by,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
