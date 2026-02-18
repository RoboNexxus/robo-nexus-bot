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
            
            # Load all cogs
            print("📦 Loading cogs...")
            cogs = ['commands', 'admin_commands', 'team_system', 'auction', 'welcome_system']
            for cog in cogs:
                try:
                    await bot.load_extension(cog)
                    print(f"   ✅ Loaded {cog}")
                except Exception as e:
                    print(f"   ❌ Failed to load {cog}: {e}")
            
            # Clear and sync
            print("\n🔄 Clearing old commands...")
            bot.tree.clear_commands(guild=guild)
            bot.tree.clear_commands(guild=None)
            
            print("🔄 Syncing commands...")
            synced = await bot.tree.sync(guild=guild)
            
            print(f"\n✅ Successfully synced {len(synced)} commands!")
            print("\nCommands synced:")
            for cmd in synced:
                print(f"   - /{cmd.name}")
            
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
