"""
Stats Channel System for Robo Nexus Bot
Creates and manages voice channels in STATS category to display website statistics
"""
import discord
from discord import app_commands
from discord.ext import commands, tasks
import logging
import aiohttp
import json
import os
from datetime import datetime, timedelta
from typing import Optional
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

class StatsChannel(commands.Cog):
    """Manages voice channels displaying website statistics"""
    
    def __init__(self, bot):
        self.bot = bot
        self.stats_category_name = "STATS"
        self.website_url = "https://robonexus46.netlify.app"
        
        # Google Analytics Configuration
        self.ga_property_id = os.getenv('GA_PROPERTY_ID')  # Your GA4 Property ID
        
        # Support both file path and direct JSON string from Replit Secrets
        self.ga_credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self.ga_credentials_json = os.getenv('GOOGLE_CREDENTIALS_JSON')  # Direct JSON string
        
        # Store channel IDs per guild
        self.stats_channels = {}
        
        # Cache for stats to avoid excessive API calls
        self.cached_stats = {
            "total_views": "Loading...",
            "last_updated": None
        }
        
        # Start the update task
        self.update_stats_channels.start()
        
        logger.info("Stats Channel system initialized")
    
    def cog_unload(self):
        """Clean up when cog is unloaded"""
        self.update_stats_channels.cancel()
    
    async def get_or_create_stats_category(self, guild: discord.Guild) -> Optional[discord.CategoryChannel]:
        """Get or create the STATS category"""
        try:
            # Look for existing STATS category
            for category in guild.categories:
                if category.name.upper() == self.stats_category_name:
                    return category
            
            # Create new STATS category if it doesn't exist
            category = await guild.create_category(
                name=self.stats_category_name,
                reason="Stats display category for Robo Nexus"
            )
            logger.info(f"Created STATS category in guild {guild.name}")
            return category
            
        except Exception as e:
            logger.error(f"Error getting/creating STATS category: {e}")
            return None
    
    def get_ga_client(self):
        """
        Get Google Analytics client with credentials from Replit Secrets or file
        """
        try:
            # Option 1: Direct JSON string from Replit Secret (RECOMMENDED)
            if self.ga_credentials_json:
                credentials_info = json.loads(self.ga_credentials_json)
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                return BetaAnalyticsDataClient(credentials=credentials)
            
            # Option 2: File path (fallback)
            elif self.ga_credentials_path and os.path.exists(self.ga_credentials_path):
                credentials = service_account.Credentials.from_service_account_file(self.ga_credentials_path)
                return BetaAnalyticsDataClient(credentials=credentials)
            
            else:
                logger.error("No Google Analytics credentials found")
                return None
                
        except Exception as e:
            logger.error(f"Error creating GA client: {e}")
            return None
    
    async def fetch_website_stats(self) -> dict:
        """
        Fetch website statistics from Google Analytics
        """
        try:
            # Check if GA is configured
            if not self.ga_property_id:
                logger.warning("Google Analytics not configured. Set GA_PROPERTY_ID in Replit Secrets")
                return {
                    "total_views": "N/A"
                }
            
            if not self.ga_credentials_json and not self.ga_credentials_path:
                logger.warning("Google Analytics credentials not configured. Set GOOGLE_CREDENTIALS_JSON in Replit Secrets")
                return {
                    "total_views": "N/A"
                }
            
            # Initialize GA client
            client = self.get_ga_client()
            if not client:
                return {
                    "total_views": "Error"
                }
            
            # Get all-time views (last 365 days as approximation)
            total_request = RunReportRequest(
                property=f"properties/{self.ga_property_id}",
                date_ranges=[DateRange(start_date="365daysAgo", end_date="today")],
                metrics=[Metric(name="screenPageViews")],
            )
            total_response = client.run_report(total_request)
            total_views = int(total_response.rows[0].metric_values[0].value) if total_response.rows else 0
            
            # Format numbers for display
            def format_number(num):
                if num >= 1000000:
                    return f"{num/1000000:.1f}M"
                elif num >= 1000:
                    return f"{num/1000:.1f}K"
                else:
                    return str(num)
            
            stats = {
                "total_views": format_number(total_views),
                "total_views_raw": total_views
            }
            
            # Update cache
            self.cached_stats = stats
            self.cached_stats["last_updated"] = datetime.now()
            
            logger.info(f"Fetched website stats: Total views = {stats['total_views']}")
            return stats
            
        except Exception as e:
            logger.error(f"Error fetching website stats from Google Analytics: {e}")
            # Return cached stats if available
            if self.cached_stats.get("last_updated"):
                logger.info("Using cached stats due to error")
                return self.cached_stats
            
            return {
                "total_views": "Error"
            }
    
    async def create_stats_channel(self, guild: discord.Guild, category: discord.CategoryChannel) -> Optional[discord.VoiceChannel]:
        """Create a voice channel to display website stats"""
        try:
            # Fetch current stats
            stats = await self.fetch_website_stats()
            
            # Create channel name with total views
            channel_name = f"📊 Total Views: {stats['total_views']}"
            
            # Create voice channel
            channel = await guild.create_voice_channel(
                name=channel_name,
                category=category,
                reason="Website stats display channel"
            )
            
            # Set permissions so users can't join (display only)
            await channel.set_permissions(
                guild.default_role,
                connect=False,
                view_channel=True
            )
            
            logger.info(f"Created stats channel in guild {guild.name}")
            return channel
            
        except Exception as e:
            logger.error(f"Error creating stats channel: {e}")
            return None
    
    @tasks.loop(minutes=5)  # Update every 5 minutes
    async def update_stats_channels(self):
        """Update all stats channels with current data"""
        try:
            for guild in self.bot.guilds:
                # Get or create STATS category
                category = await self.get_or_create_stats_category(guild)
                if not category:
                    continue
                
                # Find existing stats channel or create new one
                stats_channel = None
                for channel in category.voice_channels:
                    if channel.name.startswith("📊 Total Views:"):
                        stats_channel = channel
                        break
                
                if not stats_channel:
                    stats_channel = await self.create_stats_channel(guild, category)
                    if stats_channel:
                        self.stats_channels[guild.id] = stats_channel.id
                
                # Update channel name with current stats
                if stats_channel:
                    stats = await self.fetch_website_stats()
                    new_name = f"📊 Total Views: {stats['total_views']}"
                    
                    if stats_channel.name != new_name:
                        await stats_channel.edit(name=new_name)
                        logger.info(f"Updated stats channel in {guild.name}: {new_name}")
                        
        except Exception as e:
            logger.error(f"Error updating stats channels: {e}")
    
    @update_stats_channels.before_loop
    async def before_update_stats(self):
        """Wait for bot to be ready"""
        await self.bot.wait_until_ready()
    
    @app_commands.command(name="setup_stats_channel", description="[ADMIN] Set up website stats display channel")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_stats_channel(self, interaction: discord.Interaction):
        """Manually set up the stats channel"""
        await interaction.response.defer(ephemeral=True)
        
        try:
            guild = interaction.guild
            
            # Get or create STATS category
            category = await self.get_or_create_stats_category(guild)
            if not category:
                await interaction.followup.send(
                    "❌ Failed to create STATS category. Check bot permissions.",
                    ephemeral=True
                )
                return
            
            # Check if stats channel already exists
            existing_channel = None
            for channel in category.voice_channels:
                if channel.name.startswith("📊 Total Views:"):
                    existing_channel = channel
                    break
            
            if existing_channel:
                await interaction.followup.send(
                    f"✅ Stats channel already exists: {existing_channel.mention}\n"
                    f"It will update automatically every 5 minutes.",
                    ephemeral=True
                )
                return
            
            # Create new stats channel
            stats_channel = await self.create_stats_channel(guild, category)
            
            if stats_channel:
                self.stats_channels[guild.id] = stats_channel.id
                
                await interaction.followup.send(
                    f"✅ Stats channel created successfully!\n"
                    f"📊 Channel: {stats_channel.mention}\n"
                    f"📁 Category: {category.name}\n"
                    f"🔄 Updates every 5 minutes automatically",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "❌ Failed to create stats channel. Check bot permissions.",
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in setup_stats_channel command: {e}")
            await interaction.followup.send(
                f"❌ Error setting up stats channel: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="remove_stats_channel", description="[ADMIN] Remove website stats display channel")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_stats_channel(self, interaction: discord.Interaction):
        """Remove the stats channel"""
        await interaction.response.defer(ephemeral=True)
        
        try:
            guild = interaction.guild
            
            # Find STATS category
            category = None
            for cat in guild.categories:
                if cat.name.upper() == self.stats_category_name:
                    category = cat
                    break
            
            if not category:
                await interaction.followup.send(
                    "❌ No STATS category found.",
                    ephemeral=True
                )
                return
            
            # Find and delete stats channel
            deleted = False
            for channel in category.voice_channels:
                if channel.name.startswith("📊 Total Views:"):
                    await channel.delete(reason="Stats channel removed by admin")
                    deleted = True
                    
                    # Remove from tracking
                    if guild.id in self.stats_channels:
                        del self.stats_channels[guild.id]
                    
                    break
            
            if deleted:
                await interaction.followup.send(
                    "✅ Stats channel removed successfully!",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "❌ No stats channel found to remove.",
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in remove_stats_channel command: {e}")
            await interaction.followup.send(
                f"❌ Error removing stats channel: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="refresh_stats", description="[ADMIN] Manually refresh website stats")
    @app_commands.checks.has_permissions(administrator=True)
    async def refresh_stats(self, interaction: discord.Interaction):
        """Manually trigger stats update"""
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Trigger the update task
            await self.update_stats_channels()
            
            await interaction.followup.send(
                "✅ Stats channels refreshed successfully!",
                ephemeral=True
            )
            
        except Exception as e:
            logger.error(f"Error in refresh_stats command: {e}")
            await interaction.followup.send(
                f"❌ Error refreshing stats: {str(e)}",
                ephemeral=True
            )


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(StatsChannel(bot))
    logger.info("Stats Channel cog loaded")
