#!/usr/bin/env python3
"""
Quick setup checker for Robo Nexus Bot
Run this to verify everything is configured correctly
"""
import sys
import os

def check_setup():
    """Check if bot is ready to run"""
    print("🔍 Checking Robo Nexus Bot Setup...\n")
    
    issues = []
    warnings = []
    
    # Check Python version
    print("1. Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    else:
        print(f"   ❌ Python {sys.version_info.major}.{sys.version_info.minor} (need 3.8+)")
        issues.append("Python version too old")
    
    # Check required files
    print("\n2. Checking required files...")
    required_files = [
        'main.py',
        'bot.py',
        'config.py',
        'async_supabase_wrapper.py',
        'supabase_api.py',
        'team_system.py',
        'commands.py',
        'requirements.txt'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING!")
            issues.append(f"Missing file: {file}")
    
    # Check environment variables
    print("\n3. Checking environment variables...")
    env_vars = {
        'DISCORD_TOKEN': 'Required - Your Discord bot token',
        'DATABASE_URL': 'Required - PostgreSQL connection string',
        'GUILD_ID': 'Optional - Your Discord server ID',
        'GITHUB_TOKEN': 'Optional - For GitHub integration',
    }
    
    for var, description in env_vars.items():
        if os.getenv(var):
            print(f"   ✅ {var} - Set")
        else:
            if 'Required' in description:
                print(f"   ❌ {var} - NOT SET ({description})")
                issues.append(f"Missing env var: {var}")
            else:
                print(f"   ⚠️  {var} - Not set ({description})")
                warnings.append(f"Optional env var not set: {var}")
    
    # Check dependencies
    print("\n4. Checking dependencies...")
    try:
        import discord
        print(f"   ✅ discord.py {discord.__version__}")
    except ImportError:
        print("   ❌ discord.py - NOT INSTALLED")
        issues.append("discord.py not installed")
    
    try:
        import requests
        print(f"   ✅ requests")
    except ImportError:
        print("   ❌ requests - NOT INSTALLED")
        issues.append("requests not installed")
    
    try:
        import aiohttp
        print(f"   ✅ aiohttp")
    except ImportError:
        print("   ❌ aiohttp - NOT INSTALLED")
        issues.append("aiohttp not installed")
    
    try:
        import psycopg2
        print(f"   ✅ psycopg2")
    except ImportError:
        print("   ❌ psycopg2 - NOT INSTALLED")
        issues.append("psycopg2 not installed")
    
    # Summary
    print("\n" + "="*60)
    if not issues:
        print("✅ ALL CHECKS PASSED!")
        print("="*60)
        print("\n🚀 Ready to start the bot!")
        print("\nRun: python main.py")
        
        if warnings:
            print("\n⚠️  Warnings (optional):")
            for warning in warnings:
                print(f"   - {warning}")
        
        return True
    else:
        print("❌ ISSUES FOUND!")
        print("="*60)
        print("\n🔧 Fix these issues:\n")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        
        print("\n📋 Quick fixes:")
        if any("not installed" in issue.lower() for issue in issues):
            print("\n   Install dependencies:")
            print("   pip install -r requirements.txt")
        
        if any("env var" in issue.lower() for issue in issues):
            print("\n   Set environment variables in Replit Secrets:")
            print("   1. Click the 🔒 icon in Replit")
            print("   2. Add DISCORD_TOKEN and DATABASE_URL")
        
        if any("missing file" in issue.lower() for issue in issues):
            print("\n   Upload missing files from your local repository")
        
        return False

if __name__ == '__main__':
    try:
        success = check_setup()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error running setup check: {e}")
        sys.exit(1)
