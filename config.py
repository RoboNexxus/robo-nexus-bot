"""
Configuration management for Robo Nexus Birthday Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
# In Replit, environment variables are already loaded from Secrets
load_dotenv(override=False)  # Don't override existing environment variables

class Config:
    """Bot configuration settings"""
    
    # Debug: Print available environment variables (for troubleshooting)
    # Remove this after confirming it works
    print("🔍 Checking environment variables...")
    print(f"DISCORD_TOKEN present: {bool(os.getenv('DISCORD_TOKEN'))}")
    print(f"SUPABASE_URL present: {bool(os.getenv('SUPABASE_URL'))}")
    print(f"SUPABASE_SERVICE_KEY present: {bool(os.getenv('SUPABASE_SERVICE_KEY'))}")
    
    # Discord Configuration
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = os.getenv('GUILD_ID')
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'birthdays.db')
    # SECURITY FIX: Removed default database URL with hardcoded credentials
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://pyedggezqefeeilxdprj.supabase.co')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
    
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
        
        # SECURITY FIX: Validate Discord token format
        if cls.DISCORD_TOKEN and not cls.DISCORD_TOKEN.startswith(('MT', 'mT')):
            raise ValueError("DISCORD_TOKEN appears to be invalid (should start with MT)")
        
        # Validate GUILD_ID format
        if cls.GUILD_ID:
            try:
                int(cls.GUILD_ID)
            except ValueError:
                raise ValueError("GUILD_ID must be a valid integer")
        else:
            print("Warning: GUILD_ID not set. Bot will work globally but slash commands may take longer to sync.")
        
        # Validate BIRTHDAY_CHECK_TIME format (HH:MM)
        if cls.BIRTHDAY_CHECK_TIME:
            try:
                hour, minute = map(int, cls.BIRTHDAY_CHECK_TIME.split(':'))
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    raise ValueError("BIRTHDAY_CHECK_TIME must be in HH:MM format (00:00 to 23:59)")
            except (ValueError, AttributeError):
                raise ValueError("BIRTHDAY_CHECK_TIME must be in HH:MM format (e.g., '09:00')")
        
        # Validate DATABASE_URL if using PostgreSQL
        if cls.DATABASE_URL and not cls.DATABASE_URL.startswith('postgresql://'):
            print("Warning: DATABASE_URL should start with 'postgresql://'")
        
        # Validate Supabase configuration
        if not cls.SUPABASE_SERVICE_KEY:
            raise ValueError("SUPABASE_SERVICE_KEY environment variable is required! Please set it in your Replit Secrets.")
        
        if not cls.SUPABASE_URL:
            print("Warning: SUPABASE_URL not set, using default")
        
        # Test Supabase connection
        try:
            import requests
            response = requests.get(f"{cls.SUPABASE_URL}/rest/v1/", headers={"apikey": cls.SUPABASE_SERVICE_KEY}, timeout=5)
            if response.status_code not in [200, 401, 404]:  # 401/404 are ok, means API is reachable
                print(f"Warning: Supabase connection test returned status {response.status_code}")
        except Exception as e:
            print(f"Warning: Could not verify Supabase connection: {e}")
        
        return True