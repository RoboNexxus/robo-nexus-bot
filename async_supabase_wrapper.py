"""
Async wrapper for SupabaseAPI to prevent blocking the Discord event loop.
This wrapper runs all synchronous database calls in a thread pool.
"""
import asyncio
import logging
from typing import List, Dict, Optional, Any
from supabase_api import get_supabase_api

logger = logging.getLogger(__name__)

class AsyncSupabaseWrapper:
    """Async wrapper that runs synchronous Supabase calls in a thread pool"""
    
    def __init__(self):
        self._sync_api = get_supabase_api()
        logger.info("Async Supabase wrapper initialized")
    
    # Settings methods
    async def get_setting(self, key: str) -> Optional[str]:
        return await asyncio.to_thread(self._sync_api.get_setting, key)
    
    async def set_setting(self, key: str, value: str) -> bool:
        return await asyncio.to_thread(self._sync_api.set_setting, key, value)
    
    # Auction methods
    async def get_all_auctions(self, status: str = 'active') -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_all_auctions, status)
    
    async def get_auction(self, auction_id: int) -> Optional[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_auction, auction_id)
    
    async def create_auction(self, auction_data: Dict[str, Any]) -> int:
        return await asyncio.to_thread(self._sync_api.create_auction, auction_data)
    
    async def place_bid(self, auction_id: int, bidder_id: str, bidder_name: str, amount: float) -> bool:
        return await asyncio.to_thread(self._sync_api.place_bid, auction_id, bidder_id, bidder_name, amount)
    
    async def get_auction_bids(self, auction_id: int) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_auction_bids, auction_id)
    
    # User profile methods
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_user_profile, user_id)
    
    async def create_user_profile(self, profile_data: Dict[str, Any]) -> bool:
        return await asyncio.to_thread(self._sync_api.create_user_profile, profile_data)
    
    async def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> bool:
        return await asyncio.to_thread(self._sync_api.update_user_profile, user_id, updates)
    
    # Birthday methods
    async def register_birthday(self, user_id: str, birthday: str) -> bool:
        return await asyncio.to_thread(self._sync_api.register_birthday, user_id, birthday)
    
    async def get_birthday(self, user_id: str) -> Optional[str]:
        return await asyncio.to_thread(self._sync_api.get_birthday, user_id)
    
    async def get_birthdays_today(self, today_str: str) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_birthdays_today, today_str)
    
    async def get_all_birthdays(self) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_all_birthdays)
    
    async def remove_birthday(self, user_id: str) -> bool:
        return await asyncio.to_thread(self._sync_api.remove_birthday, user_id)
    
    
    
    
    async def count_user_profiles(self) -> int:
        return await asyncio.to_thread(self._sync_api.count_user_profiles)
    
    async def get_all_user_profiles(self) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_all_user_profiles)
    
    # Team Management methods
    async def create_team(self, team_data: Dict[str, Any]) -> bool:
        return await asyncio.to_thread(self._sync_api.create_team, team_data)
    
    async def add_team_category(self, guild_id: str, team_name: str, category: str) -> bool:
        return await asyncio.to_thread(self._sync_api.add_team_category, guild_id, team_name, category)
    
    async def remove_team_category(self, guild_id: str, team_name: str, category: str) -> bool:
        return await asyncio.to_thread(self._sync_api.remove_team_category, guild_id, team_name, category)
    
    async def get_team_categories(self, guild_id: str, team_name: str) -> List[str]:
        return await asyncio.to_thread(self._sync_api.get_team_categories, guild_id, team_name)
    
    async def get_team_by_name(self, guild_id: str, team_name: str) -> Optional[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_team_by_name, guild_id, team_name)
    
    async def get_team_by_leader(self, guild_id: str, leader_id: str) -> Optional[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_team_by_leader, guild_id, leader_id)
    
    async def get_all_teams(self, guild_id: str) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_all_teams, guild_id)
    
    async def update_team(self, guild_id: str, team_name: str, updates: Dict[str, Any]) -> bool:
        return await asyncio.to_thread(self._sync_api.update_team, guild_id, team_name, updates)
    
    async def delete_team(self, guild_id: str, team_name: str) -> bool:
        return await asyncio.to_thread(self._sync_api.delete_team, guild_id, team_name)
    
    async def add_team_member(self, member_data: Dict[str, Any]) -> bool:
        return await asyncio.to_thread(self._sync_api.add_team_member, member_data)
    
    async def remove_team_member(self, guild_id: str, team_name: str, user_id: str) -> bool:
        return await asyncio.to_thread(self._sync_api.remove_team_member, guild_id, team_name, user_id)
    
    async def get_team_members(self, guild_id: str, team_name: str) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_team_members, guild_id, team_name)
    
    async def get_user_team(self, guild_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_user_team, guild_id, user_id)
    
    # Competition Management methods
    async def create_competition(self, comp_data: Dict[str, Any]) -> bool:
        return await asyncio.to_thread(self._sync_api.create_competition, comp_data)
    
    async def get_all_competitions(self, guild_id: str) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_api.get_all_competitions, guild_id)


# Global instance
_async_supabase = None

def get_async_supabase():
    """Get the global async Supabase wrapper instance"""
    global _async_supabase
    if _async_supabase is None:
        _async_supabase = AsyncSupabaseWrapper()
    return _async_supabase
