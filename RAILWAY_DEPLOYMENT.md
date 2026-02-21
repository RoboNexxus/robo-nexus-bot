# Railway Deployment Guide

## 🚀 Quick Setup

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Create Railway Project
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `robo-nexus-bot` repository

### Step 3: Add Environment Variables
In Railway dashboard, go to Variables tab and add:

**Required:**
```
DISCORD_TOKEN=your_discord_bot_token_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
```

**Optional:**
```
GUILD_ID=1403310542030114898
GITHUB_TOKEN=your_github_token
GITHUB_OWNER=RoboNexxus
GA_PROPERTY_ID=your_ga_property_id
GA_CREDENTIALS=your_ga_credentials_json
```

### Step 4: Deploy
Railway will automatically:
1. Detect Python project
2. Install dependencies from `requirements.txt`
3. Run `python3 main.py`

### Step 5: Verify
1. Check logs in Railway dashboard
2. Look for "✅ Successfully loaded cog [10/10]: team_system"
3. Check Discord - bot should be online
4. Test a command

## 📋 Files for Railway

Railway uses these files (already created):
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Tells Railway how to run the bot
- ✅ `railway.json` - Railway configuration
- ✅ `runtime.txt` - Python version
- ✅ `main.py` - Entry point

## 🔧 Troubleshooting

### Bot doesn't start
**Check logs in Railway dashboard for:**
- Missing environment variables
- Import errors
- Database connection issues

### Commands don't appear
- Wait 1-2 minutes for Discord to sync
- Make sure `GUILD_ID` is set for faster sync
- Check bot has proper permissions in Discord

### Database errors
- Verify `SUPABASE_URL` is correct
- Verify `SUPABASE_SERVICE_KEY` is correct
- Check Supabase dashboard for connection issues

## ✅ Expected Logs

You should see:
```
🤖 Starting Robo Nexus Birthday Bot...
Database connection ready
Loading cog [1/10]: commands
✅ Successfully loaded cog [1/10]: commands
...
✅ Successfully loaded cog [10/10]: team_system
All 10 command cogs loaded successfully
Commands in tree: 59 total
Unique commands: 59
✅ Command tree validation passed - no duplicates detected
Synced 59 commands to guild 1403310542030114898
```

## 💰 Cost

Railway offers:
- **$5 free credit per month** (enough for a Discord bot)
- **500 hours free execution time**
- Your bot will use ~$3-4/month

## 🎉 Success!

Once deployed, your bot will:
- ✅ Run 24/7
- ✅ Auto-restart on crashes
- ✅ Have all 59 commands available
- ✅ All team commands working
- ✅ No blocking issues

---

**Need help?** Check Railway logs or Discord bot logs for errors.
