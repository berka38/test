"""
Dashboard routes for the web interface
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models.command import Command

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """Render dashboard page"""
    commands = Command.get_user_commands(current_user.id)
    return render_template('dashboard.html', commands=commands)
