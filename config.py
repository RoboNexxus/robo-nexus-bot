"""
Configuration management for Robo Nexus Birthday Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Bot configuration settings"""
    
    # Discord Configuration
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = os.getenv('GUILD_ID')
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'birthdays.db')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@helium/heliumdb?sslmode=disable')
    
    # Bot Configuration
    BOT_NAME = os.getenv('BOT_NAME', 'Robo Nexus')
    BIRTHDAY_CHECK_TIME = os.getenv('BIRTHDAY_CHECK_TIME', '09:00')
    
    # GitHub Integration Configuration
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # GitHub Personal Access Token
    GITHUB_OWNER = os.getenv('GITHUB_OWNER', 'RoboNexxus')  # GitHub organization or username
    
    # Google Analytics Configuration
    GA_PROPERTY_ID = os.getenv('GA_PROPERTY_ID')  # Google Analytics 4 Property ID
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # Path to service account JSON (optional)
    GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')  # Direct JSON string from Replit Secrets (recommended)
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN environment variable is required")
        
        if not cls.GUILD_ID:
            print("Warning: GUILD_ID not set. Bot will work globally but slash commands may take longer to sync.")
        
        return True