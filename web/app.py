"""
Flask application for the web interface
"""
from flask import Flask, jsonify, render_template
from flask_login import LoginManager
from flask_pymongo import PyMongo
from loguru import logger
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from the correct path
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Initialize MongoDB
mongo = PyMongo()

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
    
    # Explicitly set MongoDB URI from environment
    mongodb_uri = os.getenv('MONGO_URI')
    if not mongodb_uri:
        raise ValueError("MONGO_URI environment variable is not set!")
    
    app.config['MONGO_URI'] = mongodb_uri
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Connecting to MongoDB at: {mongodb_uri}")
    
    # Initialize MongoDB with app
    try:
        mongo.init_app(app)
        # Test the connection
        mongo.db.command('ping')
        logger.info("Successfully connected to MongoDB!")
        
        # Check if the 'users' collection exists, if not create it
        if 'users' not in mongo.db.list_collection_names():
            mongo.db.create_collection('users')
            logger.info("'users' collection created in MongoDB.")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise
    
    # Log the available collections to verify access
    try:
        collections = mongo.db.list_collection_names()
        logger.info(f"Available collections in MongoDB: {collections}")
    except Exception as e:
        logger.error(f"Error accessing collections: {str(e)}")
    
    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Import models after mongo is initialized
    from .models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by telegram_id for Flask-Login"""
        user_data = mongo.db.users.find_one({'telegram_id': str(user_id)})
        return User(user_data) if user_data else None
        
    @login_manager.unauthorized_handler
    def unauthorized():
        """Handle unauthorized access attempts"""
        return jsonify({'error': 'Unauthorized access'}), 401
    
    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.command import command_bp
    from .routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(command_bp, url_prefix='/api/command')
    app.register_blueprint(dashboard_bp)
    
    # Create default admin user if doesn't exist
    admin_id = os.getenv('DEFAULT_ADMIN_ID')
    if admin_id:
        from .services.auth import AuthService
        auth_service = AuthService(mongo.db)
        auth_service.get_or_create_user(admin_id, username="admin")
        logger.info(f"Default admin user created/verified with ID: {admin_id}")
    
    @app.route('/')
    def index():
        """Render index page"""
        return render_template('index.html')
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Not found'}), 404
        
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app
