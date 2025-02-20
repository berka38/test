"""
Run script for the web interface
"""
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, project_root)

try:
    from loguru import logger
    from web.app import create_app
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Failed to import required modules: {e}")
    print("Make sure all required packages are installed:")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

def main():
    try:
        # Configure logging to both file and console
        logger.remove()  # Remove default handler
        logger.add(
            "web.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="DEBUG",
            rotation="1 day",
            retention="7 days",
        )
        logger.add(sys.stderr, level="INFO")  # Add console output
        
        # Load environment variables
        load_dotenv()
        
        # Create and run app
        app = create_app()
        
        # Run the app
        port = int(os.getenv('PORT', 5000))
        logger.info(f"Starting web interface on port {port}")
        app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        input("Press Enter to exit...")  # Keep console window open
        sys.exit(1)

if __name__ == '__main__':
    main()
