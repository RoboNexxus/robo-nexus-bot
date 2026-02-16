# 🤖 ROBO NEXUS TEAM MANAGEMENT - COMPLETE COMMAND LIST

## 📋 FOR ALL MEMBERS (6 commands)

### 1. `/create_team` - Create a new robotics team
**Parameters:**
- `name` - Team name (required, must be unique)
- `category` - Competition category (required)
  - ⚔️ Robo War
  - ⚽ Robo Soccer
  - 🚁 Drone
  - 💡 Innovation
  - 🛤️ Line Follower
  - 🏁 Robo Race
- `description` - Team description (required)
- `max_members` - Max team size, 2-50 (optional, default: 10)
- `duration_days` - Team duration (optional, default: 0)
  - **0 = Permanent team (forever) ♾️**
  - **>0 = Temporary team (expires after X days) ⏱️**
- `requirements` - Join requirements (optional)

**Example:**
```
/create_team name:"Thunder Bots" category:"Robo War" description:"Aggressive combat team" max_members:5 duration_days:30 requirements:"Arduino experience"
```

### 2. `/post_recruitment` - Post recruitment message with join button
**Parameters:**
- `channel` - Where to post (optional, defaults to current channel)

**Example:**
```
/post_recruitment channel:#recruitment
```

### 3. `/my_team` - View YOUR team info
**Parameters:** None

**Example:**
```
/my_team
```

### 4. `/view_team` - View ANY team's details
**Parameters:**
- `team_name` - Name of team to view (required)

**Example:**
```
/view_team team_name:"Thunder Bots"
```

### 5. `/list_teams` - View all teams
**Parameters:**
- `category` - Filter by category (optional)

**Examples:**
```
/list_teams
/list_teams category:"Robo War"
```

### 6. `/leave_team` - Leave your team
**Parameters:** None
**Note:** Leaders must transfer leadership or disband first

**Example:**
```
/leave_team
```

---

## 👑 FOR TEAM LEADERS ONLY (5 commands)

### 7. `/edit_team` - Update team details
**Parameters:** (all optional, update only what you want)
- `description` - New description
- `category` - New category
- `max_members` - New max size (2-50)
- `requirements` - New requirements (leave empty to clear)

**Examples:**
```
/edit_team description:"Updated description" max_members:8
/edit_team category:"Drone" requirements:"Drone flying experience"
/edit_team requirements:""  (clears requirements)
```

### 8. `/kick_member` - Remove a member
**Parameters:**
- `member` - Discord member to kick (required)

**Example:**
```
/kick_member member:@JohnDoe
```

### 9. `/toggle_recruitment` - Open/close recruitment
**Parameters:** None
**Effect:** Toggles between 🟢 Open and 🔴 Closed

**Example:**
```
/toggle_recruitment
```

### 10. `/transfer_leadership` - Give leadership to another member
**Parameters:**
- `new_leader` - Team member to make leader (required)

**Note:** Requires confirmation, you become a regular member

**Example:**
```
/transfer_leadership new_leader:@JaneSmith
```

### 11. `/disband_team` - Delete team permanently
**Parameters:** None
**Note:** Requires confirmation, all members notified, cannot be undone

**Example:**
```
/disband_team
```

---

## 🔐 FOR ADMINISTRATORS ONLY (1 command)

### 12. `/export_teams` - Export all teams to CSV
**Parameters:**
- `category` - Filter by category (optional)

**Output:** CSV file with columns:
- Team Name
- Category
- Leader
- Leader ID
- Description
- Members (semicolon-separated)
- Member Count/Max
- Duration (Permanent or X days)
- Recruiting (Yes/No)
- Requirements
- Created At

**Examples:**
```
/export_teams
/export_teams category:"Robo War"
```

**CSV filename format:**
```
robo_nexus_teams_all_20260216_143022.csv
robo_nexus_teams_Robo_War_20260216_143022.csv
```

---

## 📊 QUICK REFERENCE TABLE

| Command | Who | Required | Optional | Description |
|---------|-----|----------|----------|-------------|
| `/create_team` | Everyone | name, category, description | max_members, duration_days, requirements | Create new team |
| `/post_recruitment` | Leaders | - | channel | Post recruitment |
| `/my_team` | Everyone | - | - | View your team |
| `/view_team` | Everyone | team_name | - | View any team |
| `/list_teams` | Everyone | - | category | View all teams |
| `/leave_team` | Members | - | - | Leave team |
| `/edit_team` | Leaders | - | description, category, max_members, requirements | Update team |
| `/kick_member` | Leaders | member | - | Remove member |
| `/toggle_recruitment` | Leaders | - | - | Open/close |
| `/transfer_leadership` | Leaders | new_leader | - | Transfer control |
| `/disband_team` | Leaders | - | - | Delete team |
| `/export_teams` | Admins | - | category | Export CSV |

**Total: 12 commands**
- 6 for everyone
- 5 for leaders only
- 1 for administrators only

---

## 🎯 COMMON USE CASES

### Creating a Competition Team
```
/create_team name:"Robo Warriors" category:"Robo War" description:"Preparing for inter-school competition" max_members:4 duration_days:45 requirements:"Available for practice on weekends"
```

### Creating a Permanent Club Team
```
/create_team name:"Innovation Squad" category:"Innovation" description:"Long-term R&D projects" max_members:10 duration_days:0
```

### Recruiting Members
```
/post_recruitment channel:#team-recruitment
```

### Viewing Competition Teams
```
/list_teams category:"Robo War"
```

### Checking Another Team
```
/view_team team_name:"Robo Warriors"
```

### Updating Team for Competition
```
/edit_team description:"Competing in State Championship - March 15" max_members:5
```

### Exporting for Competition Registration
```
/export_teams category:"Robo War"
```

---

## ⏰ DURATION FEATURE

### Permanent Teams (duration_days = 0)
- ♾️ Never expires
- Good for: Club core teams, long-term projects
- Example: Innovation team, maintenance team

### Temporary Teams (duration_days > 0)
- ⏱️ Expires after specified days
- Good for: Competition-specific teams, event teams
- Example: 30-day team for upcoming competition

**Note:** Duration is informational - teams don't auto-delete. Admins can track and manage based on creation date + duration.

---

## 📁 CSV EXPORT FORMAT

```csv
Team Name,Category,Leader,Leader ID,Description,Members,Max Members,Duration,Recruiting,Requirements,Created At
Thunder Bots,Robo War,JohnDoe,123456789,Aggressive combat team,"JohnDoe; JaneSmith; BobJones",3/5,30 days,Yes,Arduino experience,2026-02-16 14:30
Innovation Squad,Innovation,AliceWonder,987654321,Long-term R&D projects,"AliceWonder; CharlieBrown",2/10,Permanent,Yes,None,2026-02-15 10:15
```

---

## 🔧 SETUP INSTRUCTIONS

### 1. Add Duration Column (if upgrading)
Run in Supabase SQL Editor:
```sql
-- See add_duration_to_teams.sql
ALTER TABLE teams ADD COLUMN IF NOT EXISTS duration_days INTEGER NOT NULL DEFAULT 0;
CREATE INDEX IF NOT EXISTS idx_teams_duration ON teams(duration_days);
```

### 2. Restart Bot
The team_system cog will load automatically with all 12 commands.

### 3. Test Commands
```
/create_team name:"Test Team" category:"Innovation" description:"Testing" duration_days:7
/my_team
/export_teams
```

---

## 💡 TIPS

1. **Use duration_days for competitions** - Set to competition prep period
2. **Export before competitions** - Get CSV for registration
3. **Filter by category** - Organize teams by competition type
4. **View any team** - Check other teams before joining
5. **Permanent teams** - Use duration_days:0 for club core teams

---

## 🆘 TROUBLESHOOTING

**"Failed to create team"**
- Check if duration_days column exists in database
- Run add_duration_to_teams.sql if needed

**"Export not working"**
- Ensure you have Administrator permissions
- Check bot has permission to send files

**"Can't see duration in team info"**
- Update get_team_embed to display duration
- Restart bot after code changes
