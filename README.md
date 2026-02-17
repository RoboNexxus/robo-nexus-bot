# Robo Nexus Bot 🤖

A comprehensive Discord bot for the Robo Nexus robotics community with team management, birthday tracking, auctions, and GitHub integration.

## 🚀 Quick Start (Replit)

1. **Import to Replit** → Add Secrets (DISCORD_TOKEN, DATABASE_URL, GITHUB_TOKEN)
2. **Run:** `python main.py`
3. **Configure:** `/set_birthday_channel`, `/set_welcome_channel`, `/set_self_roles_channel`

## ✨ Features

### 🤝 Team Management System
- **Permanent Teams**: Compete in multiple categories
- **Temporary Teams**: Single competition teams
- Create, join, manage teams with `/create_permanent_team`, `/create_temp_team`
- Recruit members, add categories, view team info
- Admin announcements for team creation events

### 🎂 Birthday System
- Register birthdays with flexible formats (MM-DD, MM/DD, with/without year)
- Automatic daily announcements at 9:00 AM with @everyone
- Upcoming birthdays with countdown indicators

### 👋 Welcome & Verification
- Multi-stage DM verification for new members
- Collects: Name, Class (6-12), Birthday, Email, Phone, Social Links
- Automatic class role assignment
- Profile management and export

### 🏷️ Auction System
- Create listings with starting/buy-now prices
- Real-time bidding with bid tracking
- View auctions and statistics

### 🔧 GitHub Integration
- Automatic commit monitoring (every 5 minutes)
- Create issues from Discord
- View commits and repository stats
- Organization repository support

## 📋 Commands

### Team Commands
```
/create_permanent_team - Create multi-category team
/create_temp_team - Create single competition team
/add_category - Add competition category (leader)
/remove_category - Remove category (leader)
/convert_to_permanent - Convert temp to permanent
/my_team - View your team info
/view_team - View any team
/list_teams - List all teams (filter by category/type)
/leave_team - Leave current team
/recruit_members - Post recruitment message
/add_member - Manually add member (leader)
/remove_member - Remove member (leader)
/set_team_channel - Set announcement channel (admin)
/announce_team_creation - Announce team event (admin)
```

### Birthday Commands
```
/register_birthday <date> - Register birthday
/my_birthday - Check your birthday
/upcoming_birthdays - See upcoming birthdays
/check_birthday @user - Look up birthday
/remove_birthday - Remove birthday
```

### Auction Commands
```
/create_auction - Create listing
/bid <id> <amount> - Place bid
/buy_now <id> - Instant purchase
/my_auctions - View your auctions
/auction_stats - View statistics
```

### GitHub Commands
```
/repo_list - List repositories
/recent_commits [repo] - Show commits
/repo_stats [repo] - Repository stats
/create_issue - Create GitHub issue
```

### Admin Commands
```
/set_birthday_channel - Configure birthday channel
/set_welcome_channel - Configure welcome channel
/set_self_roles_channel - Configure verification channel
/view_profile @user - View member profile
/manual_verify @user - Manually verify member
/export_profiles - Export profiles to CSV
/verification_stats - View stats
/purge <count> - Delete messages
/clear_duplicate_commands - Fix duplicate slash commands
```

## 🔧 Configuration

### Required Secrets (Replit)
```
DISCORD_TOKEN=your_bot_token
GUILD_ID=1403310542030114898
DATABASE_URL=postgresql://connection_string
GITHUB_TOKEN=your_github_token (optional)
GITHUB_OWNER=robo-nexus (optional)
```

### Discord Bot Setup
1. Create bot at [Discord Developer Portal](https://discord.com/developers/applications)
2. Enable "Server Members Intent" and "Message Content Intent"
3. Invite with Administrator permissions
4. Configure channels with `/set_*` commands

## 📊 Database Schema

### Teams Table
- guild_id, name, leader_id, description
- is_permanent, max_members, requirements
- recruiting, created_at

### Team Members Table
- guild_id, team_name, user_id, user_name
- joined_at

### Team Categories Table
- guild_id, team_name, category
- created_at

### Other Tables
- user_profiles, birthdays, auctions, bids
- bot_settings, competitions

## 🛠️ Project Structure

```
robo-nexus-bot/
├── main.py                    # Entry point
├── bot.py                     # Main bot with scheduler
├── config.py                  # Configuration
├── supabase_api.py           # Sync database API
├── async_supabase_wrapper.py # Async wrapper (fixes blocking)
├── team_system.py            # Team management
├── commands.py               # Birthday commands
├── auction.py                # Auction system
├── welcome_system.py         # Verification system
├── github_integration.py     # GitHub integration
├── admin_commands.py         # Admin commands
├── help_commands.py          # Help system
├── keep_alive.py             # Uptime monitoring
└── requirements.txt          # Dependencies
```

## 🐛 Recent Fixes

### Application Not Responding (Fixed)
**Problem:** Team commands caused "application not responding" errors due to blocking database calls.

**Solution:** Created `async_supabase_wrapper.py` that wraps synchronous database calls with `asyncio.to_thread()` to prevent event loop blocking.

**Files Updated:**
- ✅ team_system.py, auction.py, commands.py
- ✅ admin_commands.py, welcome_system.py, database.py

All database calls now use `await` and run in thread pool without blocking Discord.

### Duplicate Slash Commands (Fixed)
**Problem:** Commands appeared 2-3 times in Discord's command menu due to improper syncing.

**Solution:** 
- Removed `tree.copy_global_to()` that was duplicating commands
- Clear both global and guild commands before syncing
- Sync only to guild (not both global and guild)

**Manual Fix:** Use `/clear_duplicate_commands` if duplicates still appear after restart.

### Dangerous Commands Removed (Security)
**Removed to prevent accidental data loss:**
- ❌ `/reset_birthdays` - Would delete ALL birthdays
- ❌ `/reset_auctions` - Would delete ALL auctions
- ❌ `/reset_all_except_auctions` - Would delete multiple tables
- ❌ `delete_all_*()` database functions

**Safe commands kept:**
- ✅ `/remove_birthday` - User removes their own birthday
- ✅ `/purge <count>` - Delete chat messages (not database)
- ✅ Individual record deletions

To reset data, use Supabase dashboard with proper SQL queries and backups.

## 🔍 Troubleshooting

**Bot not responding:**
- Check Replit console for errors
- Verify Secrets are configured
- Ensure Administrator permissions
- Check member intents: `/check_intents`

**Commands not appearing:**
- Wait 5-10 minutes for sync
- Restart bot
- Verify bot is in server

**Team commands slow:**
- Should be fixed with async wrapper
- Check database connection
- Monitor Replit logs

**Birthday notifications not working:**
- Configure: `/set_birthday_channel`
- Check bot permissions
- Test: `/test_birthday`

**GitHub integration issues:**
- Add GITHUB_TOKEN to Secrets
- Verify token has org access
- Check: `/repo_list`

## 📈 Monitoring

- **Replit Console**: Real-time logs and errors
- **Discord**: Bot status and command responses
- **Database**: PostgreSQL connection status
- **Uptime**: Keep-alive web server

## 🎯 Competition Categories

- ⚔️ Robo War
- ⚽ Robo Soccer
- 🚁 Drone
- 💡 Innovation
- 🛤️ Line Follower
- 🏁 Robo Race

## 📅 Supported Date Formats

- MM-DD (e.g., 12-25)
- MM/DD (e.g., 12/25)
- MM-DD-YYYY (e.g., 12-25-1995)
- MM/DD/YYYY (e.g., 12/25/1995)

## 🚀 Deployment

**Replit Benefits:**
- ✅ 24/7 operation with Always On
- ✅ PostgreSQL database
- ✅ Auto-restart on crashes
- ✅ Easy code updates
- ✅ Built-in monitoring
- ✅ Web server for uptime

## 📚 Development

**Adding Features:**
1. Add commands to appropriate `*_commands.py` file
2. Update database schema in `postgres_db.py`
3. Add configuration to `config.py`
4. Test in Replit
5. Restart bot

**Database Changes:**
- Use Supabase dashboard or SQL migrations
- Update `supabase_api.py` methods
- Async wrapper handles threading automatically

---

**Built for Robo Nexus Discord Community 🤖**

**Deployed on Replit ⚡ | 24/7 Uptime ☁️ | PostgreSQL 💾 | Async Database 🚀**
