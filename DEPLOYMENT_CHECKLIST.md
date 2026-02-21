# Deployment Checklist for Replit

## ✅ Pre-Deployment Checklist

### 1. Files Present
- [x] `main.py` - Entry point
- [x] `bot.py` - Bot logic
- [x] `requirements.txt` - Python dependencies
- [x] `.replit` - Replit configuration
- [x] `replit.nix` - System dependencies
- [x] `pyproject.toml` - Project metadata
- [x] `start.sh` - Startup script

### 2. Environment Variables (Set in Replit Secrets)
Required:
- [ ] `DISCORD_TOKEN` - Your Discord bot token
- [ ] `SUPABASE_URL` - Your Supabase project URL
- [ ] `SUPABASE_SERVICE_KEY` - Your Supabase service key

Optional:
- [ ] `GUILD_ID` - Your Discord server ID (for faster command sync)
- [ ] `GITHUB_TOKEN` - GitHub personal access token
- [ ] `GITHUB_OWNER` - GitHub organization name
- [ ] `GA_PROPERTY_ID` - Google Analytics property ID
- [ ] `GA_CREDENTIALS` - Google Analytics credentials JSON

### 3. Code Quality
- [x] All Python files have correct syntax
- [x] No import errors
- [x] All 10 cogs load successfully
- [x] All 59 commands registered

### 4. Dependencies
All dependencies in `requirements.txt`:
- [x] discord.py>=2.3.0
- [x] python-dotenv>=1.0.0
- [x] flask>=2.3.0
- [x] requests>=2.31.0
- [x] psutil>=5.9.0
- [x] psycopg2-binary>=2.9.0
- [x] aiohttp>=3.9.0
- [x] google-analytics-data>=0.18.0

## 🚀 Deployment Steps

### Step 1: Set Environment Variables
1. Go to Replit Secrets (lock icon in left sidebar)
2. Add all required environment variables
3. Make sure `DISCORD_TOKEN`, `SUPABASE_URL`, and `SUPABASE_SERVICE_KEY` are set

### Step 2: Test Locally First
1. Click "Run" button in Replit
2. Check console for errors
3. Verify all 10 cogs load
4. Test a command in Discord

### Step 3: Deploy
1. Click "Deploy" button
2. Wait for build to complete
3. Check deployment logs for errors

### Step 4: Verify Deployment
1. Check bot is online in Discord
2. Test a few commands
3. Check logs for any errors

## 🐛 Troubleshooting

### Build Fails
- **Check**: Are all environment variables set in Replit Secrets?
- **Check**: Is `replit.nix` present?
- **Check**: Is `start.sh` executable? (`chmod +x start.sh`)
- **Check**: Are there any Python syntax errors?

### Bot Doesn't Start
- **Check**: Is `DISCORD_TOKEN` set correctly?
- **Check**: Is the token valid (not expired)?
- **Check**: Does the bot have proper permissions in Discord?

### Commands Don't Appear
- **Check**: Is `GUILD_ID` set (for faster sync)?
- **Check**: Wait a few minutes for Discord to sync
- **Check**: Try using `/clear_duplicate_commands` if you see duplicates

### Database Errors
- **Check**: Is `SUPABASE_URL` correct?
- **Check**: Is `SUPABASE_SERVICE_KEY` correct?
- **Check**: Does the service key have proper permissions?

## 📝 Post-Deployment

### Verify Everything Works
- [ ] Bot is online in Discord
- [ ] All 59 commands visible
- [ ] Team commands work (create_permanent_team, etc.)
- [ ] Birthday commands work
- [ ] Stats channels update
- [ ] GitHub integration works (if configured)

### Monitor
- Check Replit logs regularly
- Monitor Discord for any error messages
- Check database for any issues

## 🎉 Success!

If all checks pass, your bot is successfully deployed and running!

---

**Last Updated**: February 21, 2026
**Bot Version**: 1.0.0
**Python Version**: 3.11
