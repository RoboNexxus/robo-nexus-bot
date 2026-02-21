"""
Diagnose why commands aren't appearing in Discord
This script checks all possible issues and provides solutions
"""
import discord
from discord.ext import commands
import asyncio
import logging
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def diagnose():
    """Run comprehensive diagnostics"""
    
    print("\n" + "=" * 70)
    print("🔍 DISCORD BOT COMMAND DIAGNOSTICS")
    print("=" * 70)
    
    # Check 1: Environment variables
    print("\n📋 CHECK 1: Environment Variables")
    print("-" * 70)
    
    if Config.DISCORD_TOKEN:
        print("✅ DISCORD_TOKEN is set")
    else:
        print("❌ DISCORD_TOKEN is missing!")
        return
    
    if Config.GUILD_ID:
        print(f"✅ GUILD_ID is set: {Config.GUILD_ID}")
    else:
        print("⚠️ GUILD_ID is not set (commands will sync globally - takes 1 hour)")
    
    # Check 2: Bot connection
    print("\n📋 CHECK 2: Bot Connection")
    print("-" * 70)
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.guild_messages = True
    intents.members = True
    
    bot = commands.Bot(
        command_prefix='!',
        intents=intents,
        help_command=None
    )
    
    @bot.event
    async def on_ready():
        try:
            print(f"✅ Bot connected: {bot.user.name} (ID: {bot.user.id})")
            print(f"✅ Connected to {len(bot.guilds)} guild(s)")
            
            for guild in bot.guilds:
                print(f"   - {guild.name} (ID: {guild.id})")
            
            # Check 3: Bot permissions in guild
            print("\n📋 CHECK 3: Bot Permissions")
            print("-" * 70)
            
            if Config.GUILD_ID:
                guild = bot.get_guild(int(Config.GUILD_ID))
                if guild:
                    bot_member = guild.get_member(bot.user.id)
                    if bot_member:
                        perms = bot_member.guild_permissions
                        
                        required_perms = {
                            'send_messages': perms.send_messages,
                            'read_messages': perms.read_messages,
                            'manage_messages': perms.manage_messages,
                            'embed_links': perms.embed_links,
                            'manage_roles': perms.manage_roles,
                            'manage_channels': perms.manage_channels,
                        }
                        
                        all_good = True
                        for perm_name, has_perm in required_perms.items():
                            status = "✅" if has_perm else "❌"
                            print(f"{status} {perm_name}: {has_perm}")
                            if not has_perm:
                                all_good = False
                        
                        if not all_good:
                            print("\n⚠️ Bot is missing some permissions!")
                    else:
                        print("❌ Bot is not a member of the guild!")
                else:
                    print(f"❌ Guild {Config.GUILD_ID} not found!")
            
            # Check 4: Load cogs
            print("\n📋 CHECK 4: Loading Cogs")
            print("-" * 70)
            
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
            
            loaded_count = 0
            for cog in cogs:
                try:
                    await bot.load_extension(cog)
                    print(f"✅ {cog}")
                    loaded_count += 1
                except Exception as e:
                    print(f"❌ {cog}: {e}")
            
            print(f"\n📊 Loaded {loaded_count}/{len(cogs)} cogs")
            
            # Check 5: Commands in tree
            print("\n📋 CHECK 5: Commands in Tree")
            print("-" * 70)
            
            all_commands = list(bot.tree.get_commands())
            print(f"✅ Found {len(all_commands)} commands in tree")
            
            if len(all_commands) == 0:
                print("❌ No commands found! This is the problem!")
                print("\n💡 SOLUTION:")
                print("   Commands are not being added to the tree.")
                print("   This usually means cogs aren't registering commands properly.")
            else:
                # Show command breakdown by cog
                command_by_cog = {}
                for cmd in all_commands:
                    # Try to find which cog owns this command
                    cog_name = "Unknown"
                    for cog in bot.cogs.values():
                        if cmd in cog.get_app_commands():
                            cog_name = cog.__class__.__name__
                            break
                    
                    if cog_name not in command_by_cog:
                        command_by_cog[cog_name] = []
                    command_by_cog[cog_name].append(cmd.name)
                
                for cog_name, cmds in sorted(command_by_cog.items()):
                    print(f"\n   {cog_name}: {len(cmds)} commands")
                    for cmd_name in sorted(cmds):
                        print(f"      - {cmd_name}")
            
            # Check 6: Check if commands are synced
            print("\n📋 CHECK 6: Synced Commands")
            print("-" * 70)
            
            if Config.GUILD_ID:
                guild = discord.Object(id=int(Config.GUILD_ID))
                try:
                    # Fetch currently synced commands
                    synced_commands = await bot.tree.fetch_commands(guild=guild)
                    print(f"✅ Currently synced: {len(synced_commands)} commands")
                    
                    if len(synced_commands) == 0:
                        print("\n❌ NO COMMANDS ARE SYNCED TO DISCORD!")
                        print("\n💡 SOLUTION:")
                        print("   Run: python force_sync_commands.py")
                    else:
                        print("\n📋 Synced commands:")
                        for cmd in synced_commands:
                            print(f"   - {cmd.name}")
                    
                    # Compare tree vs synced
                    tree_names = set(cmd.name for cmd in all_commands)
                    synced_names = set(cmd.name for cmd in synced_commands)
                    
                    missing = tree_names - synced_names
                    extra = synced_names - tree_names
                    
                    if missing:
                        print(f"\n⚠️ Commands in tree but NOT synced: {len(missing)}")
                        for cmd in sorted(missing):
                            print(f"   - {cmd}")
                    
                    if extra:
                        print(f"\n⚠️ Commands synced but NOT in tree: {len(extra)}")
                        for cmd in sorted(extra):
                            print(f"   - {cmd}")
                    
                except Exception as e:
                    print(f"❌ Error fetching synced commands: {e}")
            
            # Check 7: Bot application info
            print("\n📋 CHECK 7: Bot Application Info")
            print("-" * 70)
            
            try:
                app_info = await bot.application_info()
                print(f"✅ Bot Name: {app_info.name}")
                print(f"✅ Bot ID: {app_info.id}")
                print(f"✅ Owner: {app_info.owner}")
                
                # Check if bot has the right flags
                if hasattr(app_info, 'flags'):
                    print(f"✅ Flags: {app_info.flags}")
                
            except Exception as e:
                print(f"❌ Error getting app info: {e}")
            
            # Final recommendations
            print("\n" + "=" * 70)
            print("📋 DIAGNOSIS SUMMARY")
            print("=" * 70)
            
            if len(all_commands) == 0:
                print("\n❌ PROBLEM: No commands in tree")
                print("\n💡 SOLUTIONS:")
                print("   1. Check that cogs are loading correctly")
                print("   2. Check that commands are decorated with @app_commands.command()")
                print("   3. Restart the bot")
            elif len(all_commands) > 0:
                try:
                    if Config.GUILD_ID:
                        guild = discord.Object(id=int(Config.GUILD_ID))
                        synced_commands = await bot.tree.fetch_commands(guild=guild)
                    else:
                        synced_commands = await bot.tree.fetch_commands()
                    
                    if len(synced_commands) == 0:
                        print("\n❌ PROBLEM: Commands in tree but not synced to Discord")
                        print("\n💡 SOLUTIONS:")
                        print("   1. Run: python force_sync_commands.py")
                        print("   2. Check bot has 'applications.commands' scope")
                        print("   3. Re-invite bot with correct URL (run generate_invite_url.py)")
                    elif len(synced_commands) < len(all_commands):
                        print(f"\n⚠️ PROBLEM: Only {len(synced_commands)}/{len(all_commands)} commands synced")
                        print("\n💡 SOLUTIONS:")
                        print("   1. Run: python force_sync_commands.py")
                        print("   2. Wait 1-2 minutes for Discord to update")
                    else:
                        print("\n✅ ALL CHECKS PASSED!")
                        print(f"\n✅ {len(all_commands)} commands in tree")
                        print(f"✅ {len(synced_commands)} commands synced to Discord")
                        print("\n💡 If you still can't see commands in Discord:")
                        print("   1. Wait 1-2 minutes for Discord to update")
                        print("   2. Try restarting Discord client")
                        print("   3. Check bot has 'applications.commands' scope")
                        print("   4. Re-invite bot with: python generate_invite_url.py")
                except Exception as e:
                    print(f"\n❌ Error checking synced commands: {e}")
            
            print("\n" + "=" * 70)
            
        except Exception as e:
            logger.error(f"Error during diagnostics: {e}", exc_info=True)
        finally:
            await bot.close()
    
    try:
        await bot.start(Config.DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        if not bot.is_closed():
            await bot.close()

if __name__ == "__main__":
    asyncio.run(diagnose())
