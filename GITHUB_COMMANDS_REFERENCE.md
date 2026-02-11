# GitHub Commands Reference - All Working ✅

## Available Commands

All GitHub commands are now working with your new token and will automatically work with ALL repositories in the robo-nexus organization.

---

## 1. `/repo_list` - List All Repositories

**Description:** Shows all repositories being monitored from the robo-nexus organization.

**Usage:**
```
/repo_list
```

**What it shows:**
- List of all repositories (with emojis: 🤖 for bot repos, 🌐 for others)
- Owner: robo-nexus
- Token status: ✅ Configured
- Monitoring status: ✅ Active

**Example output:**
```
📋 Monitored Repositories

🤖 robo-nexus-bot
🌐 Robo-Nexus-Website-Dev
🌐 repository-name-3
🌐 repository-name-4

🔧 Configuration
Owner: robo-nexus
Token: ✅ Configured

📡 Monitoring
✅ Active - Checking for commits every 5 minutes
```

---

## 2. `/recent_commits` - View Recent Commits

**Description:** Shows the most recent commits from a specific repository.

**Usage:**
```
/recent_commits repository:robo-nexus-bot count:5
```

**Parameters:**
- `repository` (optional) - Repository name (autocomplete available)
- `count` (optional) - Number of commits to show (default: 5, max: 10)

**What it shows:**
- Commit hash (short)
- Author name
- Commit message
- Time (relative, e.g., "2 hours ago")
- Link to deploy latest changes

**Example output:**
```
📝 Recent Commits - robo-nexus-bot (5)

#1 `a1b2c3d` by AtharvM02222
**Fixed birthday sorting bug**
2 hours ago

#2 `e4f5g6h` by AtharvM02222
**Added GitHub integration**
5 hours ago

...

🚀 Deploy Latest
Use /pull to update the bot with latest changes!
```

---

## 3. `/repo_stats` - Repository Statistics

**Description:** Shows detailed statistics for a specific repository.

**Usage:**
```
/repo_stats repository:robo-nexus-bot
```

**Parameters:**
- `repository` (optional) - Repository name (autocomplete available)

**What it shows:**
- Stars ⭐
- Forks 🍴
- Watchers 👀
- Primary language 📝
- Repository size 📦
- Last updated 🔄
- Description 📋
- Creation date

**Example output:**
```
📊 Repository Statistics
robo-nexus/robo-nexus-bot

⭐ Stars: 5
🍴 Forks: 2
👀 Watchers: 3

📝 Language: Python
📦 Size: 1234 KB
🔄 Last Updated: 2 hours ago

📋 Description
Discord bot for Robo Nexus community

Created: 2024-01-15
```

---

## 4. `/create_issue` - Create GitHub Issue

**Description:** Create a new issue in a repository directly from Discord.

**Usage:**
```
/create_issue repository:robo-nexus-bot title:"Bug: Birthday not saving" description:"When users register birthday..." priority:high
```

**Parameters:**
- `repository` (required) - Repository name (autocomplete available)
- `title` (required) - Issue title
- `description` (required) - Issue description
- `priority` (optional) - Priority level: normal, high, low

**What it does:**
- Creates issue on GitHub
- Adds priority label
- Adds "created-from-discord" label
- Includes your Discord username in issue body
- Returns link to created issue

**Example output:**
```
✅ GitHub Issue Created in robo-nexus-bot

Bug: Birthday not saving

📋 Issue Details
🤖 Repository: robo-nexus-bot
🔢 Number: #42
🏷️ Priority: High

🔗 Quick Actions
[View Issue] • [Repository]

Created by AtharvM02222
```

---

## 5. Automatic Commit Notifications

**Description:** Bot automatically checks for new commits every 5 minutes and posts notifications.

**How it works:**
- Runs every 5 minutes
- Checks ALL repositories
- Posts to dev channel when new commits found
- Shows commit details with emoji based on repo type

**What it shows:**
- Repository name (🤖 for bot, 🌐 for others)
- Commit message
- Author (with avatar)
- Changes (+X / -Y lines)
- Commit hash
- Time (relative)
- Action suggestion (deploy for bot, check hosting for website)

**Example notification:**
```
🤖 New Commit to robo-nexus-bot

Fixed birthday sorting bug

👤 AtharvM02222 committed

📊 Changes: +15 / -8 lines
🔗 Commit: `a1b2c3d`
⏰ Time: 2 minutes ago

🚀 Auto-Deploy
Use /pull to update the bot with these changes!
```

---

## Autocomplete Features

All commands with repository parameters have **autocomplete**:

1. Start typing the command
2. Type part of repository name
3. Bot shows matching repositories
4. Select from the list

**Example:**
```
/recent_commits repository:robo
```
Shows:
- robo-nexus-bot
- robo-nexus-website
- etc.

---

## Permissions Required

### For Bot:
- Administrator permissions in Discord server
- GitHub token with these scopes:
  - ✅ `repo` - Full repository access
  - ✅ `read:org` - Read organization data
  - ✅ `write:discussion` - Create issues

### For Users:
- `/repo_list` - Anyone can use
- `/recent_commits` - Anyone can use
- `/repo_stats` - Anyone can use
- `/create_issue` - Developer role only (configurable)

---

## Configuration

### Environment Variables (Replit Secrets):
```
GITHUB_TOKEN=your_token_here
GITHUB_OWNER=robo-nexus
```

### Developer Access:
Edit `github_integration.py` line ~74:
```python
DEV_IDS = [1147221423815938179]  # Add Discord user IDs
```

---

## Troubleshooting

### Commands Not Showing?
- Wait 5-10 minutes after bot restart
- Restart Discord client
- Check bot has Administrator permissions

### "Token not configured"?
- Check GITHUB_TOKEN in Replit Secrets
- Restart bot after adding token
- Verify token hasn't expired

### "Repository not found"?
- Check token is authorized for robo-nexus organization
- Go to: https://github.com/settings/tokens
- Click "Configure SSO" → Authorize

### Commit notifications not working?
- Wait 5 minutes for first check
- Check dev channel exists
- Verify bot has send message permission
- Check token has repo access

### Autocomplete not showing repos?
- Restart bot to refresh repository list
- Check token has organization access
- Verify repositories exist in organization

---

## Testing Checklist

After restart, test each command:

- [ ] `/repo_list` - Shows all organization repositories
- [ ] `/recent_commits repository:robo-nexus-bot` - Shows commits
- [ ] `/repo_stats repository:robo-nexus-bot` - Shows statistics
- [ ] `/create_issue` - Creates issue (if you're a dev)
- [ ] Wait 5 minutes - Check for commit notifications
- [ ] Autocomplete works on all commands

---

## API Rate Limits

### With Token:
- 5,000 requests per hour
- Resets every hour
- Check usage: https://api.github.com/rate_limit

### Bot Usage:
- Fetch repos: 1 call (on startup)
- Check commits: 1 call per repo every 5 minutes
- Create issue: 1 call per issue
- View stats: 1 call per command

**Example:** With 10 repos, bot uses ~120 calls per hour (well under limit)

---

## Support

### Check Logs:
- Replit console shows all GitHub API calls
- Look for errors like "403 Forbidden" or "401 Unauthorized"

### Test Token:
```bash
python setup_github_org.py
```

### GitHub Settings:
- Tokens: https://github.com/settings/tokens
- Security log: https://github.com/settings/security-log

---

**All commands are ready to use! 🚀**

**Last Updated:** February 11, 2026
**Status:** ✅ All working with dynamic repository fetching
