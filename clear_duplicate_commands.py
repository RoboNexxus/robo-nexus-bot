"""
Clear Duplicate Commands from Discord

This script will clear all commands from Discord and force a fresh sync.
Run this if you see duplicate commands in Discord.

Usage:
1. Make sure your bot is running
2. In Discord, use the /clear_duplicate_commands command
   OR
3. Stop the bot, run this script, then restart the bot
"""

import asyncio
import os
import discord
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def clear_commands():
    """Clear all commands from Discord"""
    
    # Load config
    from config import Config
    
    # Create bot instance
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    bot = commands.Bot(command_prefix='/', intents=intents)
    
    @bot.event
    async def on_ready():
        logger.info(f"Logged in as {bot.user}")
        
        try:
            # Clear guild commands
            if Config.GUILD_ID:
                guild = discord.Object(id=int(Config.GUILD_ID))
                logger.info(f"Clearing commands for guild {Config.GUILD_ID}...")
                
                # Get current commands
                current_commands = await bot.tree.fetch_commands(guild=guild)
                logger.info(f"Found {len(current_commands)} commands in guild")
                
                for cmd in current_commands:
                    logger.info(f"  - {cmd.name}")
                
                # Clear all commands
                bot.tree.clear_commands(guild=guild)
                synced = await bot.tree.sync(guild=guild)
                logger.info(f"✅ Cleared {len(current_commands)} commands from guild")
                logger.info(f"   Synced {len(synced)} commands (should be 0)")
            else:
                # Clear global commands
                logger.info("Clearing global commands...")
                current_commands = await bot.tree.fetch_commands()
                logger.info(f"Found {len(current_commands)} global commands")
                
                for cmd in current_commands:
                    logger.info(f"  - {cmd.name}")
                
                bot.tree.clear_commands(guild=None)
                synced = await bot.tree.sync()
                logger.info(f"✅ Cleared {len(current_commands)} global commands")
                logger.info(f"   Synced {len(synced)} commands (should be 0)")
            
            logger.info("\n" + "="*60)
            logger.info("✅ COMMANDS CLEARED SUCCESSFULLY")
            logger.info("="*60)
            logger.info("\nNext steps:")
            logger.info("1. Restart your bot")
            logger.info("2. The bot will re-register all commands fresh")
            logger.info("3. Wait a few seconds for Discord to update")
            logger.info("4. Check Discord - duplicates should be gone!")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"❌ Error clearing commands: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await bot.close()
    
    # Run bot
    try:
        await bot.start(Config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == '__main__':
    print("="*60)
    print("DISCORD COMMAND CLEANER")
    print("="*60)
    print("\nThis will clear ALL commands from Discord.")
    print("After running this, restart your bot to re-register commands.")
    print("\nPress Ctrl+C to cancel, or wait 3 seconds to continue...")
    print("="*60)
    
    try:
        import time
        time.sleep(3)
        asyncio.run(clear_commands())
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
