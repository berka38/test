"""
Command routes for the web interface
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from loguru import logger
from ..app import mongo
from ..models.command import Command

command_bp = Blueprint('command', __name__)

@command_bp.route('/list', methods=['GET'])
@login_required
def list_commands():
    """List all available commands"""
    try:
        commands = mongo.db.commands.find()
        return jsonify([Command(cmd).to_dict() for cmd in commands])
    except Exception as e:
        logger.error(f"Error listing commands: {str(e)}")
        return jsonify({'error': str(e)}), 500

@command_bp.route('/create', methods=['POST'])
@login_required
def create_command():
    """Create a new command"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        name = data.get('name')
        description = data.get('description')
        code = data.get('code')
        
        if not all([name, description, code]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Check if command already exists
        if mongo.db.commands.find_one({'name': name}):
            return jsonify({'error': 'Command already exists'}), 409
            
        # Create command
        command_data = {
            'name': name,
            'description': description,
            'code': code,
            'created_by': current_user.telegram_id,
            'is_active': True
        }
        
        result = mongo.db.commands.insert_one(command_data)
        if result.inserted_id:
            return jsonify({'message': 'Command created successfully'}), 201
        else:
            return jsonify({'error': 'Failed to create command'}), 500
            
    except Exception as e:
        logger.error(f"Error creating command: {str(e)}")
        return jsonify({'error': str(e)}), 500

@command_bp.route('/update/<name>', methods=['PUT'])
@login_required
def update_command(name):
    """Update an existing command"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Check if command exists
        command = mongo.db.commands.find_one({'name': name})
        if not command:
            return jsonify({'error': 'Command not found'}), 404
            
        # Update fields
        update_data = {}
        if 'description' in data:
            update_data['description'] = data['description']
        if 'code' in data:
            update_data['code'] = data['code']
        if 'is_active' in data:
            update_data['is_active'] = data['is_active']
            
        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400
            
        result = mongo.db.commands.update_one(
            {'name': name},
            {'$set': update_data}
        )
        
        if result.modified_count:
            return jsonify({'message': 'Command updated successfully'})
        else:
            return jsonify({'error': 'Failed to update command'}), 500
            
    except Exception as e:
        logger.error(f"Error updating command: {str(e)}")
        return jsonify({'error': str(e)}), 500

@command_bp.route('/delete/<name>', methods=['DELETE'])
@login_required
def delete_command(name):
    """Delete a command"""
    try:
        result = mongo.db.commands.delete_one({'name': name})
        if result.deleted_count:
            return jsonify({'message': 'Command deleted successfully'})
        else:
            return jsonify({'error': 'Command not found'}), 404
    except Exception as e:
        logger.error(f"Error deleting command: {str(e)}")
        return jsonify({'error': str(e)}), 500
