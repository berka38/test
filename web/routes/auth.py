"""
Authentication routes for the web interface
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..services.auth import AuthService
from ..app import mongo
from loguru import logger

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService(mongo.db)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        try:
            telegram_id = request.form.get('telegram_id')
            password = request.form.get('password')
            
            if not telegram_id or not password:
                flash('Telegram ID ve şifre gerekli.', 'error')
                return redirect(url_for('index'))
                
            user = auth_service.authenticate_user(telegram_id, password)
            if not user:
                flash('Geçersiz kimlik bilgileri.', 'error')
                return redirect(url_for('index'))
                
            login_user(user)
            flash('Başarıyla giriş yapıldı!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash('Bir hata oluştu. Lütfen tekrar deneyin.', 'error')
            return redirect(url_for('index'))
    
    return render_template('index.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    try:
        logout_user()
        flash('Başarıyla çıkış yapıldı.', 'success')
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        flash('Çıkış yaparken bir hata oluştu.', 'error')
    
    return redirect(url_for('index'))

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Handle password change"""
    try:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        
        if not current_password or not new_password:
            flash('Mevcut şifre ve yeni şifre gerekli.', 'error')
            return redirect(url_for('dashboard'))
            
        if not current_user.check_password(current_password):
            flash('Mevcut şifre yanlış.', 'error')
            return redirect(url_for('dashboard'))
            
        auth_service.set_user_password(current_user.telegram_id, new_password)
        flash('Şifre başarıyla güncellendi.', 'success')
        
    except Exception as e:
        logger.error(f"Password change error: {str(e)}")
        flash('Şifre değiştirirken bir hata oluştu.', 'error')
        
    return redirect(url_for('dashboard'))
