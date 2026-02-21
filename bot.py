"""
Robo Nexus Birthday Bot - Main Bot Class
Discord bot for managing birthday celebrations in the Robo Nexus server
"""
import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime, time
import asyncio
from typing import Optional

from config import Config
from database import birthday_db
from date_parser import DateParser

logger = logging.getLogger(__name__)

class RoboNexusBirthdayBot(commands.Bot):
    """Main Discord bot class for Robo Nexus Birthday Bot"""
    
    def __init__(self):
        """Initialize the Robo Nexus Birthday Bot"""
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        intents.members = True  # Required to detect member joins!
        
        # Initialize bot with proper settings
        super().__init__(
            command_prefix='!',  # Fallback prefix (we'll use slash commands)
            intents=intents,
            help_command=None,  # We'll create our own help system
            case_insensitive=True
        )
        
        # Initialize components
        self.db_manager = birthday_db
        self.scheduler_started = False
        
        logger.info("Robo Nexus Birthday Bot initialized")
    
    async def setup_hook(self):
        """Called when the bot is starting up"""
        try:
            # Database is already initialized in postgres_db.py
            logger.info("Database connection ready")
            
            # ============================================================================
            # COG LOADING ORDER DOCUMENTATION
            # ============================================================================
            # The cogs are loaded in the order defined below. This sequential order is
            # INTENTIONAL and DEPENDENCY-FREE. Each cog is designed to be independent
            # and does not rely on other cogs being loaded first.
            #
            # Current Load Order (by design):
            #   1. commands          - Basic bot commands
            #   2. admin_commands    - Administrative functions
            #   3. help_commands     - Help system
            #   4. dev_commands      - Developer utilities
            #   5. github_integration - GitHub webhook integration
            #   6. analytics         - Usage analytics
            #   7. auction           - Auction system
            #   8. welcome_system    - User verification and welcome
            #   9. stats_channel     - Statistics display
            #   10. team_system      - Team management
            #
            # Dependency Analysis:
            # - All cogs use shared utilities (async_supabase_wrapper, postgres_db)
            # - No cog imports or depends on another cog's functionality
            # - Module-level imports are safe (no circular dependencies detected)
            # - Order can be changed without breaking functionality
            #
            # TODO: If future cogs develop interdependencies, implement a dependency
            # graph system to automatically determine optimal load order. For now,
            # the simple sequential approach is sufficient and maintainable.
            # ============================================================================
            
            # Define expected cogs for validation
            expected_cogs = [
                'commands',
                'admin_commands', 
                'help_commands',
                'dev_commands',
                'github_integration',
                'analytics',
                'auction',
                'welcome_system',
                'stats_channel',
                'team_system'
            ]
            
            # Load command cogs with validation
            loaded_cogs = []
            failed_cogs = []
            
            for cog_name in expected_cogs:
                try:
                    # Log load attempt with order information
                    load_order = len(loaded_cogs) + 1
                    logger.info(f"Loading cog [{load_order}/{len(expected_cogs)}]: {cog_name}")
                    await self.load_extension(cog_name)
                    
                    # Verify cog loaded successfully
                    # Note: Cog class names may differ from module names
                    # We check if the extension is in the loaded extensions
                    if cog_name in self.extensions:
                        logger.info(f"✅ Successfully loaded cog [{load_order}/{len(expected_cogs)}]: {cog_name}")
                        loaded_cogs.append(cog_name)
                    else:
                        logger.error(f"Cog {cog_name} failed to load - not found in extensions")
                        failed_cogs.append(cog_name)
                        
                except Exception as e:
                    logger.error(f"Error loading cog {cog_name}: {e}")
                    failed_cogs.append(cog_name)
            
            # If any cogs failed to load, raise exception to prevent syncing incomplete commands
            if failed_cogs:
                error_msg = f"Failed to load cogs: {', '.join(failed_cogs)}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            logger.info(f"All {len(loaded_cogs)} command cogs loaded successfully")
            
            # Validate all expected cogs are in the cogs dictionary
            for cog_name in expected_cogs:
                if cog_name not in self.extensions:
                    error_msg = f"Expected cog {cog_name} not found in loaded extensions"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)
            
            # Get all commands from the tree for validation
            all_commands = list(self.tree.get_commands())
            command_names = [cmd.name for cmd in all_commands]
            
            # Add comprehensive logging for diagnostics
            logger.info(f"Commands in tree: {len(all_commands)} total")
            logger.info(f"Unique commands: {len(set(command_names))}")
            
            # Log all command names for debugging
            for cmd in all_commands:
                logger.info(f"  - {cmd.name}")
            
            # Check for duplicate commands in the tree
            if len(command_names) != len(set(command_names)):
                # Find duplicates
                seen = {}
                duplicates = {}
                for name in command_names:
                    if name in seen:
                        if name not in duplicates:
                            duplicates[name] = 2
                        else:
                            duplicates[name] += 1
                    else:
                        seen[name] = 1
                
                logger.error(f"❌ Duplicate commands detected in tree:")
                for cmd, count in sorted(duplicates.items()):
                    logger.error(f"  - {cmd}: appears {count} times")
                
                # CRITICAL FIX: Clear ALL commands and force re-sync
                logger.warning("⚠️ Clearing command tree to remove duplicates...")
                
                # Clear commands for the guild
                if Config.GUILD_ID:
                    guild = discord.Object(id=int(Config.GUILD_ID))
                    self.tree.clear_commands(guild=guild)
                else:
                    self.tree.clear_commands(guild=None)
                
                # Copy commands from cogs back to tree
                logger.info("📋 Re-registering commands from cogs...")
                for cog in self.cogs.values():
                    for command in cog.get_app_commands():
                        self.tree.add_command(command)
                
                # Get commands again after cleanup
                all_commands = list(self.tree.get_commands())
                command_names = [cmd.name for cmd in all_commands]
                logger.info(f"✅ After cleanup: {len(all_commands)} commands ({len(set(command_names))} unique)")
                
                # Verify no duplicates remain
                if len(command_names) != len(set(command_names)):
                    logger.error("❌ Duplicates still exist after cleanup! This should not happen.")
                    # Log which commands are still duplicated
                    seen2 = set()
                    for name in command_names:
                        if name in seen2:
                            logger.error(f"  - Still duplicated: {name}")
                        seen2.add(name)
            else:
                logger.info("✅ Command tree validation passed - no duplicates detected")
            
            # Sync slash commands
            if Config.GUILD_ID:
                # Sync to specific guild for faster updates during development
                guild = discord.Object(id=int(Config.GUILD_ID))
                
                # Check if we should force a clean sync (useful for fixing sync issues)
                import os
                force_clean_sync = os.getenv('FORCE_CLEAN_SYNC', 'false').lower() == 'true'
                
                if force_clean_sync:
                    logger.info("🔄 FORCE_CLEAN_SYNC enabled - clearing and re-syncing all commands...")
                    
                    # Clear existing commands from Discord
                    self.tree.clear_commands(guild=guild)
                    await self.tree.sync(guild=guild)
                    logger.info("✅ Cleared existing commands from Discord")
                    
                    # Re-add commands from cogs
                    logger.info("📋 Re-registering commands from cogs...")
                    for cog in self.cogs.values():
                        for command in cog.get_app_commands():
                            self.tree.add_command(command, guild=guild)
                    
                    # Verify commands in tree
                    all_commands = list(self.tree.get_commands(guild=guild))
                    logger.info(f"📋 Commands in tree after re-registration: {len(all_commands)}")
                
                # Sync commands to Discord
                synced = await self.tree.sync(guild=guild)
                logger.info(f"Synced {len(synced)} commands to guild {Config.GUILD_ID}")
                
                # Log synced command names for verification
                if len(synced) > 0:
                    synced_names = [cmd.name for cmd in synced]
                    logger.info(f"Synced commands: {', '.join(synced_names)}")
                else:
                    logger.error("⚠️ WARNING: Synced 0 commands! Bot may be missing 'applications.commands' scope!")
                    logger.error("⚠️ Solution: Re-invite bot with both 'bot' AND 'applications.commands' scopes")
            else:
                # Sync globally (takes up to 1 hour to propagate)
                synced = await self.tree.sync()
                logger.info(f"Synced {len(synced)} commands globally")
                
                # Log synced command names for verification
                if len(synced) > 0:
                    synced_names = [cmd.name for cmd in synced]
                    logger.info(f"Synced commands: {', '.join(synced_names)}")
                else:
                    logger.error("⚠️ WARNING: Synced 0 commands! Bot may be missing 'applications.commands' scope!")
                    logger.error("⚠️ Solution: Re-invite bot with both 'bot' AND 'applications.commands' scopes")
            
            logger.info("✅ Bot setup completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error during bot setup: {e}")
            raise
    
    async def on_ready(self):
        """Called when the bot is ready and connected to Discord"""
        logger.info(f"🤖 {self.user} is now online!")
        logger.info(f"Bot ID: {self.user.id}")
        logger.info(f"Connected to {len(self.guilds)} guild(s)")
        
        # Log guild information
        for guild in self.guilds:
            logger.info(f"  - {guild.name} (ID: {guild.id}) - {guild.member_count} members")
        
        # Start the birthday scheduler if not already started
        if not self.scheduler_started:
            await self.start_birthday_scheduler()
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="For Robo Nexus :rx:"
        )
        await self.change_presence(activity=activity)
        
        print(f"\n🎉 Robo Nexus Birthday Bot is ready!")
        print(f"📊 Connected to {len(self.guilds)} server(s)")
        print(f"🎂 Monitoring birthdays for Robo Nexus community")
        print(f"⏰ Daily birthday check scheduled for {Config.BIRTHDAY_CHECK_TIME}")
    
    async def start_birthday_scheduler(self):
        """Start the daily birthday check scheduler"""
        try:
            # Parse the configured time
            hour, minute = map(int, Config.BIRTHDAY_CHECK_TIME.split(':'))
            
            # Start the birthday check task
            self.daily_birthday_check.change_interval(time=time(hour=hour, minute=minute))
            self.daily_birthday_check.start()
            
            self.scheduler_started = True
            logger.info(f"Birthday scheduler started - daily check at {Config.BIRTHDAY_CHECK_TIME}")
            
        except Exception as e:
            logger.error(f"Error starting birthday scheduler: {e}")
    
    @tasks.loop(time=time(hour=9, minute=0))  # Default 9:00 AM, will be changed in start_birthday_scheduler
    async def daily_birthday_check(self):
        """Daily task to check for birthdays and send notifications"""
        try:
            logger.info("Running daily birthday check...")
            
            # Get today's birthdays using async method
            from datetime import date
            today_str = date.today().strftime("%m-%d")
            todays_birthdays = await self.db_manager.get_birthdays_today(today_str)
            
            if not todays_birthdays:
                logger.info("No birthdays today")
                return
            
            logger.info(f"Found {len(todays_birthdays)} birthday(s) today!")
            
            # Send birthday messages for each guild
            for guild in self.guilds:
                await self.send_birthday_messages(guild, todays_birthdays)
            
        except Exception as e:
            logger.error(f"Error during daily birthday check: {e}")
    
    async def send_birthday_messages(self, guild: discord.Guild, birthdays: list):
        """
        Send birthday messages to the configured channel and announcements
        
        Args:
            guild: Discord guild object
            birthdays: List of birthday dictionaries
        """
        try:
            # Get the configured birthday channel from database
            birthday_channel_id = await self.db_manager.get_birthday_channel(guild.id)
            birthday_channel = None
            
            if birthday_channel_id:
                birthday_channel = guild.get_channel(birthday_channel_id)
                
                # Verify channel still exists and bot has permissions
                if birthday_channel:
                    permissions = birthday_channel.permissions_for(guild.me)
                    if not permissions.send_messages:
                        logger.error(f"Bot lacks send_messages permission in birthday channel {birthday_channel.name}")
                        return
                else:
                    # FIX: Channel was deleted, log and return
                    logger.warning(f"Birthday channel {birthday_channel_id} no longer exists in guild {guild.name}")
                    return
            
            # If no configured channel or channel not found, log warning
            if not birthday_channel:
                logger.warning(f"No birthday channel configured for guild {guild.name}. Use /set_birthday_channel to configure.")
                return
            
            # Send birthday message for each user
            for birthday_info in birthdays:
                try:
                    user_id = birthday_info['user_id']
                    
                    # Get the user from the guild (use cache first, then fetch)
                    member = guild.get_member(user_id)
                    if not member:
                        try:
                            member = await guild.fetch_member(user_id)
                        except discord.NotFound:
                            logger.warning(f"User {user_id} not found in guild {guild.name}")
                            continue
                        except discord.HTTPException as e:
                            logger.error(f"HTTP error fetching member {user_id}: {e}")
                            continue
                        except Exception as e:
                            # FIX: Catch all exceptions for member fetch
                            logger.error(f"Unexpected error fetching member {user_id}: {e}", exc_info=True)
                            continue
                    
                    if member:
                        # Create birthday message with @everyone mention
                        birthday_message = f"@everyone\n\n🎉🎂 **HAPPY BIRTHDAY {member.mention}!** 🎂🎉\n\nEveryone wish them a fantastic day! 🎈🎁🥳"
                        
                        # Send to configured birthday channel with allowed_mentions to enable @everyone
                        try:
                            await birthday_channel.send(
                                birthday_message,
                                allowed_mentions=discord.AllowedMentions(everyone=True)
                            )
                            logger.info(f"Birthday message sent for {member.display_name} in {guild.name}")
                        except discord.Forbidden:
                            logger.error(f"Bot lacks permission to send messages in {birthday_channel.name}")
                            return
                        except discord.HTTPException as e:
                            logger.error(f"HTTP error sending birthday message: {e}")
                        except Exception as e:
                            # FIX: Catch all exceptions for message send
                            logger.error(f"Unexpected error sending birthday message: {e}", exc_info=True)
                        
                        # Add a small delay between messages to avoid rate limits
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    logger.error(f"Error sending birthday message for user {user_id}: {e}", exc_info=True)
            
        except Exception as e:
            logger.error(f"Error sending birthday messages to guild {guild.name}: {e}", exc_info=True)
    
    @daily_birthday_check.before_loop
    async def before_birthday_check(self):
        """Wait for bot to be ready before starting birthday checks"""
        await self.wait_until_ready()
        logger.info("Bot is ready, birthday scheduler will start")
    
    async def on_command_error(self, ctx, error):
        """Handle command errors with analytics tracking"""
        if isinstance(error, commands.CommandNotFound):
            # Ignore unknown commands
            return
        
        logger.error(f"Command error: {error}")
        
        # Track error in analytics
        analytics_cog = self.get_cog('Analytics')
        if analytics_cog:
            analytics_cog.track_error(error, f"Command: {ctx.command}")
            await analytics_cog.report_error_to_dev(error, f"Command: {ctx.command}")
        
        # Send error message to user
        try:
            await ctx.send("❌ An error occurred while processing your command. The developers have been notified.")
        except:
            pass  # Channel might not be accessible
    
    async def on_application_command_error(self, interaction: discord.Interaction, error):
        """Handle slash command errors with analytics tracking"""
        logger.error(f"Slash command error: {error}")
        
        # Track error in analytics
        analytics_cog = self.get_cog('Analytics')
        if analytics_cog:
            analytics_cog.track_error(error, f"Slash command: {interaction.command}")
            await analytics_cog.report_error_to_dev(error, f"Slash command: {interaction.command}")
        
        # Send error message to user
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "❌ An error occurred while processing your command. The developers have been notified.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "❌ An error occurred while processing your command. The developers have been notified.",
                    ephemeral=True
                )
        except:
            pass
    
    async def on_error(self, event, *args, **kwargs):
        """Handle general bot errors with analytics tracking"""
        logger.error(f"Bot error in event {event}", exc_info=True)
        
        # Track error in analytics
        analytics_cog = self.get_cog('Analytics')
        if analytics_cog:
            import sys
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if exc_value:
                analytics_cog.track_error(exc_value, f"Event: {event}")
                await analytics_cog.report_error_to_dev(exc_value, f"Event: {event}")
    
    async def close(self):
        """Clean shutdown of the bot"""
        logger.info("Shutting down Robo Nexus Birthday Bot...")
        
        # Stop the birthday scheduler
        if hasattr(self, 'daily_birthday_check'):
            self.daily_birthday_check.cancel()
        
        # Close the bot
        await super().close()
        logger.info("Bot shutdown complete")

# Helper function to create and run the bot
async def run_bot():
    """Create and run the Robo Nexus Birthday Bot"""
    bot = RoboNexusBirthdayBot()
    
    try:
        await bot.start(Config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot.close()