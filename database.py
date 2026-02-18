"""
Supabase Database Interface for Robo Nexus Bot
Uses Supabase REST API instead of direct PostgreSQL connections
"""
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from async_supabase_wrapper import get_async_supabase

logger = logging.getLogger(__name__)

class BirthdayDatabase:
    """Supabase-based birthday database"""
    
    def __init__(self):
        self.db = get_async_supabase()
    
    async def add_birthday(self, user_id: int, birthday: str) -> bool:
        """Add a birthday to the database"""
        try:
            logger.info(f"🎂 [database.py] Adding birthday for user_id: {user_id}, birthday: {birthday}")
            result = await self.db.register_birthday(str(user_id), birthday)
            if result:
                logger.info(f"✅ [database.py] Birthday added successfully for user_id: {user_id}")
            else:
                logger.error(f"❌ [database.py] Failed to add birthday for user_id: {user_id}")
            return result
        except Exception as e:
            logger.error(f"💥 [database.py] Error adding birthday: {e}")
            return False
    
    async def get_birthday(self, user_id: int) -> Optional[str]:
        """Get a user's birthday"""
        try:
            return await self.db.get_birthday(str(user_id))
        except Exception as e:
            logger.error(f"Error getting birthday: {e}")
            return None
    
    async def get_all_birthdays(self) -> List[Dict[str, Any]]:
        """Get all birthdays"""
        try:
            birthdays = await self.db.get_all_birthdays()
            return [
                {
                    'user_id': int(b['user_id']),
                    'birthday': b['birthday'],
                    'registered_at': b.get('registered_at', datetime.now().isoformat())
                }
                for b in birthdays
            ]
        except Exception as e:
            logger.error(f"Error getting all birthdays: {e}")
            return []
    
    async def remove_birthday(self, user_id: int) -> bool:
        """Remove a birthday from the database"""
        try:
            return await self.db.remove_birthday(str(user_id))
        except Exception as e:
            logger.error(f"Error removing birthday: {e}")
            return False
    
    async def get_birthdays_today(self, today_str: str) -> List[Dict[str, Any]]:
        """Get birthdays for today"""
        try:
            return await self.db.get_birthdays_today(today_str)
        except Exception as e:
            logger.error(f"Error getting today's birthdays: {e}")
            return []
    
    async def birthday_exists(self, user_id: int) -> bool:
        """Check if a birthday exists for a user"""
        birthday = await self.get_birthday(user_id)
        return birthday is not None
    
    async def get_birthday_count(self) -> int:
        """Get total number of birthdays"""
        try:
            birthdays = await self.get_all_birthdays()
            return len(birthdays)
        except Exception as e:
            logger.error(f"Error getting birthday count: {e}")
            return 0
    
    async def get_birthday_channel(self, guild_id: int) -> Optional[int]:
        """Get the configured birthday channel for a server"""
        try:
            channel_id = await self.db.get_setting(f'birthday_channel_{guild_id}')
            return int(channel_id) if channel_id else None
        except Exception as e:
            logger.error(f"Error getting birthday channel: {e}")
            return None
    
    async def set_birthday_channel(self, guild_id: int, channel_id: int) -> bool:
        """Set the birthday announcement channel for a server"""
        try:
            return await self.db.set_setting(f'birthday_channel_{guild_id}', str(channel_id))
        except Exception as e:
            logger.error(f"Error setting birthday channel: {e}")
            return False

# Global instances for backward compatibility
birthday_db = BirthdayDatabase()

# Legacy functions for backward compatibility - now async
async def add_birthday(user_id: int, birthday: str) -> bool:
    return await birthday_db.add_birthday(user_id, birthday)

async def get_birthday(user_id: int) -> Optional[str]:
    return await birthday_db.get_birthday(user_id)

async def get_all_birthdays() -> List[Dict[str, Any]]:
    return await birthday_db.get_all_birthdays()

async def remove_birthday(user_id: int) -> bool:
    return await birthday_db.remove_birthday(user_id)

async def birthday_exists(user_id: int) -> bool:
    return await birthday_db.birthday_exists(user_id)

async def get_birthday_count() -> int:
    return await birthday_db.get_birthday_count()

async def get_birthday_channel(guild_id: int) -> Optional[int]:
    return await birthday_db.get_birthday_channel(guild_id)

async def set_birthday_channel(guild_id: int, channel_id: int) -> bool:
    return await birthday_db.set_birthday_channel(guild_id, channel_id)