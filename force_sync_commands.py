"""
Force sync all commands to Discord
This script will clear and re-sync all commands to fix the "0 commands synced" issue
"""
import discord
from discord.ext import commands
import asyncio
import logging
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def force_sync():
    """Force sync all commands to Discord"""
    
    # Set up intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.guild_messages = True
    intents.members = True
    
    # Create bot instance
    bot = commands.Bot(
        command_prefix='!',
        intents=intents,
        help_command=None
    )
    
    @bot.event
    async def on_ready():
        """When bot is ready, sync commands"""
        try:
            logger.info(f"Logged in as {bot.user}")
            logger.info(f"Bot ID: {bot.user.id}")
            
            # Load all cogs
            cogs = [
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
            
            logger.info("Loading cogs...")
            for cog in cogs:
                try:
                    await bot.load_extension(cog)
                    logger.info(f"✅ Loaded: {cog}")
                except Exception as e:
                    logger.error(f"❌ Failed to load {cog}: {e}")
            
            # Get all commands
            all_commands = bot.tree.get_commands()
            logger.info(f"\n📋 Found {len(all_commands)} commands in tree:")
            for cmd in all_commands:
                logger.info(f"  - {cmd.name}")
            
            if Config.GUILD_ID:
                guild = discord.Object(id=int(Config.GUILD_ID))
                
                # STEP 1: Clear existing commands
                logger.info(f"\n🗑️ Clearing existing commands from guild {Config.GUILD_ID}...")
                bot.tree.clear_commands(guild=guild)
                await bot.tree.sync(guild=guild)
                logger.info("✅ Cleared existing commands")
                
                # STEP 2: Copy commands from cogs
                logger.info("\n📋 Copying commands from cogs to tree...")
                for cog in bot.cogs.values():
                    for command in cog.get_app_commands():
                        bot.tree.add_command(command, guild=guild)
                        logger.info(f"  + Added: {command.name}")
                
                # STEP 3: Sync new commands
                logger.info(f"\n🔄 Syncing commands to guild {Config.GUILD_ID}...")
                synced = await bot.tree.sync(guild=guild)
                logger.info(f"\n✅ Successfully synced {len(synced)} commands!")
                
                logger.info("\n📋 Synced commands:")
                for cmd in synced:
                    logger.info(f"  ✓ {cmd.name}")
                
            else:
                # Global sync
                logger.info("\n🗑️ Clearing existing global commands...")
                bot.tree.clear_commands(guild=None)
                await bot.tree.sync()
                
                logger.info("\n📋 Copying commands from cogs to tree...")
                for cog in bot.cogs.values():
                    for command in cog.get_app_commands():
                        bot.tree.add_command(command)
                        logger.info(f"  + Added: {command.name}")
                
                logger.info("\n🔄 Syncing commands globally...")
                synced = await bot.tree.sync()
                logger.info(f"\n✅ Successfully synced {len(synced)} commands globally!")
                
                logger.info("\n📋 Synced commands:")
                for cmd in synced:
                    logger.info(f"  ✓ {cmd.name}")
            
            logger.info("\n🎉 Command sync complete! Commands should appear in Discord within 1-2 minutes.")
            logger.info("💡 If commands still don't appear, check:")
            logger.info("   1. Bot has 'applications.commands' scope in Discord Developer Portal")
            logger.info("   2. Bot has been re-invited with the correct permissions")
            logger.info("   3. GUILD_ID is correct in your .env file")
            
        except Exception as e:
            logger.error(f"❌ Error during sync: {e}", exc_info=True)
        finally:
            await bot.close()
    
    # Start the bot
    try:
        await bot.start(Config.DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(force_sync())
