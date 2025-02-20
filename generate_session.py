"""
Telegram UserBot Session String Generator

This script helps generate a session string for Telegram UserBot deployment on Render.com.
It handles API authentication, session generation, and provides a user-friendly interface
with proper error handling and flood wait management.
"""

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError, ApiIdInvalidError, PhoneNumberInvalidError
import traceback
import time
import datetime
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('session_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('SessionGenerator')

class SessionGenerator:
    def __init__(self):
        """Initialize the session generator with default values."""
        self.api_id = None
        self.api_hash = None
        self.session_string = None
        self.output_file = 'session_string.txt'

    @staticmethod
    def format_time(seconds):
        """Format seconds into a human-readable time string."""
        return str(datetime.timedelta(seconds=seconds))

    def display_countdown(self, seconds):
        """Display an interactive countdown timer."""
        start_time = time.time()
        try:
            while seconds > 0:
                remaining = int(seconds - (time.time() - start_time))
                if remaining <= 0:
                    break
                print(f"\rPlease wait: {self.format_time(remaining)} remaining...  ", 
                      end="", flush=True)
                time.sleep(1)
            print("\rCountdown completed! You can proceed now.           ")
        except KeyboardInterrupt:
            print("\nCountdown interrupted by user.")
            raise

    def get_api_credentials(self):
        """
        Get API credentials from user input with validation.
        
        Returns:
            tuple: (api_id, api_hash)
        """
        print("\n=== Telegram API Credentials ===\n")
        print("Please enter your Telegram API credentials.")
        print("You can get these from https://my.telegram.org\n")
        
        while True:
            try:
                api_id = input("Enter your API ID: ").strip()
                if not api_id.isdigit():
                    print("Error: API ID must be a number. Please try again.")
                    continue
                
                api_hash = input("Enter your API Hash: ").strip()
                if not api_hash:
                    print("Error: API Hash cannot be empty.")
                    continue
                
                return int(api_id), api_hash
            except ValueError as e:
                logger.error(f"Invalid input: {str(e)}")
                print("Invalid input. Please try again.")
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                raise

    def create_session(self):
        """
        Create a Telegram session and handle potential errors.
        
        Returns:
            str: Session string on success
        """
        logger.info("Initializing Telegram client...")
        print("\nInitializing connection...")
        print("You'll need to login with your phone number.\n")
        
        while True:
            try:
                with TelegramClient(StringSession(), self.api_id, self.api_hash) as client:
                    return client.session.save()
            except FloodWaitError as e:
                wait_time = e.seconds
                logger.warning(f"FloodWaitError: Need to wait {wait_time} seconds")
                print(f"\n=== FloodWaitError ===")
                print(f"Telegram requires us to wait for {self.format_time(wait_time)}")
                print("This is a security measure to prevent abuse.")
                print("\nOptions:")
                print("1. Wait for the timer (recommended)")
                print("2. Exit and try again later")
                
                choice = input("\nEnter your choice (1 or 2): ").strip()
                if choice == "1":
                    self.display_countdown(wait_time)
                    continue
                else:
                    raise KeyboardInterrupt
            except ApiIdInvalidError:
                logger.error("Invalid API credentials")
                print("\nError: Invalid API credentials. Please check your API ID and Hash.")
                raise
            except PhoneNumberInvalidError:
                logger.error("Invalid phone number format")
                print("\nError: Invalid phone number format. Use international format (e.g., +1234567890)")
                raise
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                raise

    def save_to_file(self):
        """Save the credentials to a file."""
        try:
            with open(self.output_file, 'w') as f:
                f.write(f"API_ID={self.api_id}\n")
                f.write(f"API_HASH={self.api_hash}\n")
                f.write(f"SESSION_STRING={self.session_string}\n")
            logger.info(f"Credentials saved to {self.output_file}")
            print(f"\nCredentials saved to '{self.output_file}'")
            print("Make sure to keep this file secure and delete it after adding the credentials to Render.com")
        except Exception as e:
            logger.error(f"Error saving to file: {str(e)}")
            print(f"\nError saving to file: {str(e)}")

    def run(self):
        """Main execution flow of the session generator."""
        print("\n=== Telegram UserBot Session String Generator ===\n")
        print("This script will help you generate a session string for your Telegram UserBot.")
        print("This string will be used in your Render.com deployment.\n")
        
        try:
            # Get API credentials
            self.api_id, self.api_hash = self.get_api_credentials()
            
            # Create session
            self.session_string = self.create_session()
            
            # Display results
            print("\n=== Your Session String ===\n")
            print(self.session_string)
            print("\n=== Instructions ===")
            print("1. Copy this session string")
            print("2. Add it to your Render.com environment variables as SESSION_STRING")
            print("3. Keep this string secret! Anyone with this string can access your Telegram account!\n")
            
            # Save to file option
            save = input("Would you like to save the session string to a file? (y/n): ").lower()
            if save == 'y':
                self.save_to_file()
        
        except KeyboardInterrupt:
            logger.info("Process interrupted by user")
            print("\n\nProcess interrupted by user.")
        except Exception as e:
            logger.error(f"Error: {str(e)}\n{traceback.format_exc()}")
            print("\n=== Error Occurred ===")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {str(e)}")
            print("\nFull Error Details:")
            print(traceback.format_exc())
            print("\nIf you're having trouble:")
            print("1. Make sure your API ID and API Hash are correct")
            print("2. Check your internet connection")
            print("3. Make sure you're entering a valid phone number in international format (e.g., +1234567890)")
            print("4. If you're getting a FloodWait error, wait for the specified time and try again")
        
        finally:
            print("\nPress Enter to exit...")
            input()

def main():
    """Entry point of the script."""
    generator = SessionGenerator()
    generator.run()

if __name__ == '__main__':
    main()
