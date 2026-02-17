# Replit Setup Guide (Recovery Mode)

## Quick Start Commands

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Go to Replit Secrets (🔒 icon) and add:
```
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=1403310542030114898
DATABASE_URL=your_postgresql_url
GITHUB_TOKEN=your_github_token (optional)
GITHUB_OWNER=robo-nexus (optional)
```

### 3. Start the Bot
```bash
python main.py
```

Or use the start script:
```bash
bash start.sh
```

## If You See Errors

### "Module not found" Error
```bash
pip install discord.py requests aiohttp psycopg2-binary
```

### "Permission denied" Error
Don't use `./requirements.txt` - that's not executable
Use: `pip install -r requirements.txt`

### "Database connection failed"
Check your DATABASE_URL in Secrets is correct

### "Bot token invalid"
Check your DISCORD_TOKEN in Secrets

## Verify Setup

After starting, you should see:
```
🤖 RoboNexusBot#1234 is now online!
Bot ID: 123456789
Connected to 1 guild(s)
✅ Synced X commands to guild 1403310542030114898
```

## Common Replit Commands

```bash
# Check Python version
python --version

# List installed packages
pip list

# Check if bot file exists
ls -la main.py

# View bot logs
python main.py

# Stop bot (Ctrl+C)
```

## Troubleshooting

### Bot starts but commands don't appear
1. Wait 2-3 minutes for Discord to sync
2. Restart Discord app
3. Use `/clear_duplicate_commands` if duplicates appear

### Bot crashes immediately
1. Check Secrets are set correctly
2. Check database connection
3. Look at error message in console

### "Application not responding"
This should be fixed with the async wrapper. If it still happens:
1. Check database connection is stable
2. Verify all files were uploaded correctly
3. Check console for errors

## Files You Need

Essential files (must be present):
- ✅ main.py
- ✅ bot.py
- ✅ config.py
- ✅ async_supabase_wrapper.py
- ✅ supabase_api.py
- ✅ team_system.py
- ✅ commands.py
- ✅ admin_commands.py
- ✅ auction.py
- ✅ welcome_system.py
- ✅ requirements.txt

Optional files:
- github_integration.py (if using GitHub features)
- analytics.py (if using analytics)
- stats_channel.py (if using stats)

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Set Secrets in Replit
3. Run: `python main.py`
4. Configure in Discord: `/set_birthday_channel`, `/set_welcome_channel`
5. Test: `/create_permanent_team`, `/list_teams`

## Need Help?

Check the main README.md for full documentation.
