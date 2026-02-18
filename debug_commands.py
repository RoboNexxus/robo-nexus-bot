#!/usr/bin/env python3
"""Debug: Print all commands in bot.tree after loading cogs"""
import asyncio
import discord
from discord.ext import commands

async def main():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    print("Loading team_system...")
    await bot.load_extension('team_system')
    
    print(f"\nCommands in tree: {len(list(bot.tree.get_commands()))}")
    
    for cmd in bot.tree.get_commands():
        print(f"  - {cmd.name}")
    
    if len(list(bot.tree.get_commands())) == 0:
        print("\n❌ NO COMMANDS FOUND!")
        print("This means @app_commands.command is not registering to bot.tree")

asyncio.run(main())
