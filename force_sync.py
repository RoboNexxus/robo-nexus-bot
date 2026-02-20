#!/usr/bin/env python3
"""Force sync all commands to Discord"""
import asyncio
import discord
from discord.ext import commands
import os
import sys

async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event
    async def on_ready():
        print(f"✅ Bot connected as {bot.user}")
        
        try:
            guild_id = os.getenv('GUILD_ID')
            if not guild_id:
                print("❌ GUILD_ID not set in environment")
                await bot.close()
                return
            
            guild = discord.Object(id=int(guild_id))
            
            # Load all cogs FIRST to populate the command tree
            print("📦 Loading cogs...")
            cogs = ['commands', 'admin_commands', 'team_system', 'auction', 'welcome_system']
            failed_cogs = []
            
            for cog in cogs:
                try:
                    await bot.load_extension(cog)
                    print(f"   ✅ Loaded {cog}")
                except Exception as e:
                    print(f"   ❌ Failed to load {cog}: {e}")
                    failed_cogs.append((cog, str(e)))
            
            # Report any cog loading failures
            if failed_cogs:
                print("\n⚠️  Warning: Some cogs failed to load:")
                for cog_name, error in failed_cogs:
                    print(f"   - {cog_name}: {error}")
                print("\nProceeding with available cogs...")
            
            # Validate command tree is populated
            commands_before = list(bot.tree.get_commands(guild=guild))
            print(f"\n📋 Commands in tree before sync: {len(commands_before)}")
            if commands_before:
                print("Commands loaded:")
                for cmd in commands_before:
                    print(f"   - /{cmd.name}")
            else:
                print("⚠️  Warning: No commands found in tree after loading cogs!")
            
            # Now sync to register all commands to Discord
            print("\n🔄 Syncing commands to Discord...")
            synced = await bot.tree.sync(guild=guild)
            
            # Validate sync result
            print(f"\n✅ Successfully synced {len(synced)} commands!")
            
            if len(synced) == 0:
                print("❌ ERROR: No commands were synced! This indicates a problem.")
                if failed_cogs:
                    print("   Possible cause: Critical cogs failed to load")
            else:
                print("\nCommands synced to Discord:")
                for cmd in synced:
                    print(f"   - /{cmd.name}")
                
                # Verify team commands are present
                team_commands = ['create_permanent_team', 'create_temp_team', 'my_team', 'list_teams']
                synced_names = [cmd.name for cmd in synced]
                team_commands_present = [tc for tc in team_commands if tc in synced_names]
                
                if team_commands_present:
                    print(f"\n✅ Team commands verified: {len(team_commands_present)}/{len(team_commands)}")
                    for tc in team_commands_present:
                        print(f"   - /{tc}")
                else:
                    print("\n⚠️  Warning: No team commands found in synced commands!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await bot.close()
    
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ DISCORD_TOKEN not set")
        sys.exit(1)
    
    await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
