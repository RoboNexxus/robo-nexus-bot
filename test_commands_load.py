#!/usr/bin/env python3
"""
Test script to verify commands are loading correctly
Run this to see what's actually happening
"""
import discord
from discord.ext import commands
import asyncio
import sys

async def test_command_loading():
    """Test if commands load properly"""
    print("=" * 60)
    print("TESTING COMMAND LOADING")
    print("=" * 60)
    
    # Create a minimal bot
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    print("\n1. Loading team_system cog...")
    try:
        await bot.load_extension('team_system')
        print("   ✅ team_system loaded")
    except Exception as e:
        print(f"   ❌ Failed to load team_system: {e}")
        return False
    
    print("\n2. Checking registered commands...")
    team_commands = [cmd for cmd in bot.tree.get_commands() if 'team' in cmd.name.lower()]
    
    if not team_commands:
        print("   ❌ NO TEAM COMMANDS FOUND!")
        print(f"   Total commands in tree: {len(list(bot.tree.get_commands()))}")
        
        # List all commands
        all_commands = list(bot.tree.get_commands())
        if all_commands:
            print(f"\n   Found {len(all_commands)} commands:")
            for cmd in all_commands[:10]:
                print(f"     - {cmd.name}")
        else:
            print("   ❌ NO COMMANDS AT ALL IN TREE!")
        
        return False
    
    print(f"   ✅ Found {len(team_commands)} team commands:")
    for cmd in team_commands:
        print(f"     - {cmd.name}")
    
    print("\n3. Checking if commands have defer...")
    # This would require inspecting the actual command code
    print("   (Manual check required - see verify_all_defers.py)")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        result = asyncio.run(test_command_loading())
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
