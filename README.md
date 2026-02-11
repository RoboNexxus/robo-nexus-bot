# Robo Nexus Bot 🎉

A comprehensive Discord bot for the Robo Nexus robotics community with birthday tracking, member verification, auction system, and GitHub integration.

## 🚀 **DEPLOYED ON REPLIT - 24/7 OPERATION**

This bot runs 24/7 on Replit with PostgreSQL database and automatic uptime monitoring.

## Features

### 🎂 Birthday System
- Birthday registration with flexible date formats (MM-DD, MM/DD, with or without year)
- Automatic daily birthday notifications at 9:00 AM with @everyone mention
- Chronologically sorted upcoming birthdays with countdown indicators
- Birthday lookup and management commands
- Admin-configurable announcement channel

### 👋 Welcome & Verification System
- Multi-stage DM-based verification for new members
- Collects: Name, Class (6-12), Birthday, Email, Phone, Social Links
- Smart class recognition (understands "Class 10", "10th grade", "ten", etc.)
- Automatic class role assignment
- Complete member profile storage and management
- Restricts new members to self-roles channel until verified

### 🏷️ Auction System
- Create auction listings with starting price and buy-now option
- Real-time bidding system with bid tracking
- Auction statistics and history
- View your auctions and bids

### 🔧 GitHub Integration
- Automatic commit monitoring (checks every 5 minutes)
- Create GitHub issues from Discord
- View recent commits and repository statistics
- Supports organization repositories (robo-nexus)

### 🤖 Admin Tools
- Channel configuration for birthdays, welcome, and self-roles
- Member profile management and export
- Manual verification for members
- Verification statistics (excludes bots)
- Data reset and management commands

## Quick Start on Replit

### 1. **Fork/Import Repository**
1. Go to [Replit](https://replit.com)
2. Click "Create Repl" → "Import from GitHub"
3. Paste your repository URL
4. Click "Import from GitHub"

### 2. **Configure Secrets**
Click the **Secrets** tab (🔒 lock icon) and add:

```
DISCORD_TOKEN=your_discord_bot_token_here
GUILD_ID=1403310542030114898
DATABASE_URL=your_postgresql_connection_string
GITHUB_TOKEN=your_github_token_here
GITHUB_OWNER=robo-nexus
```

### 3. **Run Setup**
```bash
python setup_replit.py
```

This will:
- Check PostgreSQL connection
- Create all database tables
- Migrate existing data
- Verify configuration

### 4. **Start Bot**
Click the **Run** button or:
```bash
python main.py
```

### 5. **Configure in Discord**
```
/set_birthday_channel #announcements
/set_welcome_channel #welcome
/set_self_roles_channel #self-roles
```

## Bot Commands

### 👥 User Commands
- `/register_birthday <date>` - Register your birthday
- `/my_birthday` - Check your registered birthday
- `/upcoming_birthdays` - See upcoming birthdays (sorted chronologically)
- `/check_birthday @user` - Look up someone's birthday
- `/remove_birthday` - Remove your birthday
- `/birthday_collect <date>` - Register birthday in self-roles channel

### 🏷️ Auction Commands
- `/create_auction` - Create a new auction listing
- `/bid <auction_id> <amount>` - Place a bid
- `/buy_now <auction_id>` - Buy item at buy-now price
- `/my_auctions` - View your auction listings
- `/auction_stats` - View auction statistics

### 🔧 GitHub Commands
- `/repo_list` - List monitored repositories
- `/recent_commits [repository]` - Show recent commits
- `/repo_stats [repository]` - Show repository statistics
- `/create_issue` - Create a GitHub issue from Discord

### ⚙️ Admin Commands
- `/set_birthday_channel` - Set birthday announcement channel
- `/set_welcome_channel` - Set welcome notifications channel
- `/set_self_roles_channel` - Set verification channel
- `/birthday_config` - View birthday system configuration
- `/welcome_config` - View welcome system configuration
- `/view_profile @user` - View a user's complete profile
- `/update_profile @user` - Update a user's profile
- `/manual_verify @user` - Manually verify a member
- `/export_profiles` - Export all profiles to CSV
- `/verification_stats` - View verification statistics
- `/purge <count>` - Delete messages (1-100)

## 📅 Supported Date Formats

- **MM-DD** (e.g., `12-25` for December 25)
- **MM/DD** (e.g., `12/25` for December 25)
- **MM-DD-YYYY** (e.g., `12-25-1995`)
- **MM/DD/YYYY** (e.g., `12/25/1995`)

## 🎉 How It Works

### Birthday System
1. Admin configures announcement channel with `/set_birthday_channel`
2. Users register birthdays with `/register_birthday` or `/birthday_collect`
3. Bot checks for birthdays daily at 9:00 AM
4. Sends birthday messages to announcements with @everyone mention
5. `/upcoming_birthdays` shows next birthdays with countdown

### Welcome & Verification System
1. New member joins → Restricted to self-roles channel only
2. Bot sends DM requesting name and class (6-12)
3. Collects birthday (required)
4. Collects email (optional)
5. Collects phone (optional)
6. Collects social links (optional)
7. Assigns class role automatically
8. Grants full server access

### Auction System
1. Create auction with starting price and optional buy-now price
2. Members place bids (must be higher than current bid)
3. Use buy-now to instantly purchase
4. Track your auctions and bids
5. View auction statistics

### GitHub Integration
1. Bot monitors organization repositories every 5 minutes
2. Sends commit notifications to dev channel
3. Create issues directly from Discord
4. View repository stats and recent commits

## 🔧 Configuration

### Required Secrets (Replit)

```
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=1403310542030114898
DATABASE_URL=postgresql://postgres:password@helium/heliumdb?sslmode=disable
```

### Optional Secrets (GitHub Integration)

```
GITHUB_TOKEN=your_github_token_here
GITHUB_OWNER=robo-nexus
```

### Discord Bot Setup

1. **Create Discord Application:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create new application named "Robo Nexus Bot"
   - Go to Bot section → Create bot → Copy token
   - Enable "Server Members Intent" and "Message Content Intent"

2. **Invite Bot to Server:**
   - Go to OAuth2 → URL Generator
   - Select: `bot` + `applications.commands`
   - Select: `Administrator` permissions
   - Use generated URL to invite bot

3. **Configure Channels:**
   ```
   /set_birthday_channel #announcements
   /set_welcome_channel #welcome
   /set_self_roles_channel #self-roles
   ```

## 📊 Replit Deployment Benefits

- ✅ **24/7 Operation** - Always On feature keeps bot running
- ✅ **PostgreSQL Database** - Persistent data storage
- ✅ **Auto-restart** - Bot restarts automatically if it crashes
- ✅ **Easy Updates** - Edit code and restart
- ✅ **Built-in Monitoring** - Logs and console output
- ✅ **Web Server** - Keep-alive endpoint for uptime monitoring

## 🛠️ Development

### Project Structure

```
robo-nexus-bot/
├── main.py              # Entry point
├── bot.py               # Main bot class with birthday scheduler
├── config.py            # Configuration management
├── database.py          # Database wrapper (Supabase)
├── postgres_db.py       # PostgreSQL database interface
├── supabase_api.py      # Supabase API client
├── date_parser.py       # Date parsing utilities
├── commands.py          # Birthday commands
├── admin_commands.py    # Admin commands
├── auction.py           # Auction system
├── welcome_system.py    # Welcome & verification system
├── github_integration.py # GitHub integration
├── analytics.py         # Analytics and statistics
├── help_commands.py     # Help system
├── dev_commands.py      # Developer commands
├── keep_alive.py        # Web server for uptime
├── requirements.txt     # Python dependencies
├── replit.nix          # Replit configuration
└── setup_replit.py     # One-command setup script
```

### Adding New Features

1. **New Commands:** Add to appropriate `*_commands.py` file
2. **Database Changes:** Update `postgres_db.py` schema
3. **Configuration:** Add to `config.py` and Replit Secrets
4. **Test:** Run locally in Replit
5. **Deploy:** Restart bot

## 🔍 Troubleshooting

**Bot not responding:**
- Check Replit console for errors
- Verify Secrets are set correctly
- Ensure bot has Administrator permissions
- Check member intents are enabled: `/check_intents`

**Commands not appearing:**
- Wait 5-10 minutes for slash command sync
- Restart bot in Replit
- Check bot is in your server

**Birthday notifications not working:**
- Configure channel: `/set_birthday_channel #announcements`
- Check bot has permissions in announcement channel
- Verify users have registered birthdays
- Test manually: `/test_birthday`

**Verification not working:**
- Check member intents: `/check_intents`
- Configure channels: `/set_welcome_channel` and `/set_self_roles_channel`
- Verify bot can send DMs to members

**GitHub integration not working:**
- Add GITHUB_TOKEN to Replit Secrets
- Run: `python setup_github_org.py` to test
- Check token has organization access
- Verify: `/repo_list`

## 📈 Monitoring

**Replit Console:**
- View real-time logs
- Monitor bot status
- Check for errors
- Track command usage

**Discord:**
- Bot online status
- Command response times
- Daily birthday announcements
- Commit notifications

## 📚 Documentation

- `BOT_DOCUMENTATION.md` - Complete feature documentation
- `SETUP_CHECKLIST.md` - Step-by-step setup guide
- `GITHUB_ORG_SETUP.md` - GitHub integration guide
- `FIXES_APPLIED.md` - Recent bug fixes
- `ALL_FIXES_SUMMARY.md` - Complete changes summary

## 🎯 Features Highlights

- ✅ Chronologically sorted upcoming birthdays with countdown
- ✅ Birthday messages to configured announcements channel with @everyone
- ✅ Verification statistics exclude bots
- ✅ Birthday saves during self-roles verification
- ✅ GitHub organization repository support
- ✅ Multi-stage member verification with DMs
- ✅ Auction system with bidding and buy-now
- ✅ Complete profile management and export

---

**Built for the Robo Nexus Discord community 🤖**

**Deployed on Replit ⚡ | Running 24/7 ☁️ | PostgreSQL Database 💾 | Administrator Permissions 🔐**