# 🤖 NEW ROBO NEXUS TEAM SYSTEM

## 🎯 CONCEPT

### Two Types of Teams:

**1. ♾️ PERMANENT TEAMS**
- Stay together forever (like "2f4u")
- Can compete in MULTIPLE categories
- Example: Your team competes in both Robo War AND Robo Soccer
- Fully editable (description, members, categories)

**2. ⏱️ TEMPORARY TEAMS**
- For specific competitions only
- SINGLE category
- Disbanded after competition ends

## 📊 DATABASE SCHEMA

### Tables:
1. **teams** - Team info (name, leader, is_permanent, etc.)
2. **team_categories** - Categories per team (many-to-many)
3. **team_members** - Team membership
4. **competitions** - Admin competition announcements

### Key Fields:
- `is_permanent` (BOOLEAN) - True = permanent, False = temporary
- Teams can have multiple categories (stored in team_categories table)

## 🎮 COMMANDS

### FOR EVERYONE:

**`/create_permanent_team`** - Create a permanent team
- `name` - Team name (e.g., "2f4u")
- `description` - Team description
- `max_members` - Team size (optional, default: 10)
- `requirements` - Join requirements (optional)
- Can add multiple categories later with `/add_category`

**`/create_temp_team`** - Create a temporary team for one competition
- `name` - Team name
- `category` - Single competition category
- `description` - Team description
- `max_members` - Team size (optional, default: 10)
- `requirements` - Join requirements (optional)

**`/my_team`** - View your team

**`/view_team`** - View any team
- `team_name` - Team to view

**`/list_teams`** - View all teams
- `category` - Filter by category (optional)
- `team_type` - Filter by permanent/temporary (optional)

**`/leave_team`** - Leave your team

### FOR TEAM LEADERS:

**`/add_category`** - Add category to permanent team
- `category` - Category to add
- Only works for permanent teams
- Example: Add "Robo Soccer" to your team that already has "Robo War"

**`/remove_category`** - Remove category from permanent team
- `category` - Category to remove

**`/edit_team`** - Update team details
- `description`, `max_members`, `requirements` (all optional)

**`/kick_member`** - Remove a member
- `member` - Member to kick

**`/toggle_recruitment`** - Open/close recruitment

**`/transfer_leadership`** - Transfer leadership
- `new_leader` - New team leader

**`/disband_team`** - Delete team

**`/post_recruitment`** - Post recruitment message
- `channel` - Where to post (optional)

### FOR ADMINISTRATORS:

**`/announce_competition`** - Announce a new competition
- `name` - Competition name
- `categories` - Categories (comma-separated)
- `description` - Competition details
- `start_date` - Competition date (optional)
- `channel` - Where to announce (optional)
- Posts message asking: "Use permanent team or create temp team?"

**`/export_teams`** - Export teams to CSV
- `category` - Filter by category (optional)
- `team_type` - Filter by permanent/temporary (optional)

## 💡 USE CASES

### Scenario 1: Permanent Team "2f4u"
```
1. Leader creates: /create_permanent_team name:"2f4u" description:"Best team ever" max_members:4

2. Add categories:
   /add_category category:"Robo Soccer"
   /add_category category:"Robo War"

3. Now "2f4u" can compete in both categories!

4. For next competition, just use existing team
```

### Scenario 2: Competition Announcement
```
1. Admin announces:
   /announce_competition name:"State Championship" categories:"Robo War, Robo Soccer, Drone" description:"March 15-17" start_date:2026-03-15

2. Message posted:
   "🏆 State Championship Announced!
   Categories: Robo War, Robo Soccer, Drone
   Date: March 15-17
   
   Choose your approach:
   🔹 Use your permanent team (if you have one)
   🔹 Create a temporary team for this competition
   
   Permanent teams: Use /add_category to add competition categories
   New teams: Use /create_temp_team for single competition"

3. Members decide:
   - "2f4u" (permanent) adds "Drone" category
   - New members create temp teams
```

### Scenario 3: Temporary Team for One Competition
```
1. Create temp team:
   /create_temp_team name:"Quick Bots" category:"Drone" description:"For State Championship only" max_members:3

2. Recruit members:
   /post_recruitment

3. After competition, disband:
   /disband_team
```

## 📁 CSV EXPORT FORMAT

```csv
Team Name,Type,Categories,Leader,Members,Max,Recruiting,Requirements,Created
2f4u,Permanent,"Robo War; Robo Soccer",JohnDoe,"John; Jane; Bob; Alice",4/4,No,None,2026-01-15
Quick Bots,Temporary,Drone,CharlieBrown,"Charlie; Dave; Eve",3/3,No,None,2026-02-10
```

## 🔧 SETUP INSTRUCTIONS

### 1. Run SQL Script
In Supabase SQL Editor, run `update_teams_schema.sql`:
```sql
-- Creates 4 tables:
-- - teams (with is_permanent field)
-- - team_categories (many-to-many)
-- - team_members
-- - competitions
```

### 2. Update Supabase API
The new methods are already added:
- `add_team_category()`
- `remove_team_category()`
- `get_team_categories()`
- `create_competition()`

### 3. Restart Bot
All commands will be available.

## 🎨 VISUAL DIFFERENCES

**Permanent Team Embed:**
```
♾️ 2f4u
📋 Type: ♾️ Permanent Team
🏆 Categories:
   ⚔️ Robo War
   ⚽ Robo Soccer
👑 Leader: @JohnDoe
👥 Members: 4/4
📊 Status: 🔴 Closed
```

**Temporary Team Embed:**
```
⏱️ Quick Bots
📋 Type: ⏱️ Temporary Team
🏆 Category: 🚁 Drone
👑 Leader: @CharlieBrown
👥 Members: 3/3
📊 Status: 🟢 Recruiting
```

## ✅ ADVANTAGES

1. **Permanent teams** - Like real robotics teams that stay together
2. **Multi-category** - One team, multiple competitions
3. **Flexibility** - Add/remove categories as needed
4. **Temporary teams** - For one-off competitions
5. **Admin control** - Announce competitions, guide team formation
6. **Export** - Get CSV for competition registration

## 🔄 MIGRATION FROM OLD SYSTEM

If you already have teams with the old schema:

```sql
-- Add is_permanent column
ALTER TABLE teams ADD COLUMN IF NOT EXISTS is_permanent BOOLEAN DEFAULT FALSE;

-- Migrate old category field to team_categories table
INSERT INTO team_categories (guild_id, team_name, category)
SELECT guild_id, name, category FROM teams WHERE category IS NOT NULL;

-- Remove old category column
ALTER TABLE teams DROP COLUMN IF EXISTS category;
ALTER TABLE teams DROP COLUMN IF EXISTS duration_days;
```

## 📝 NOTES

- Permanent teams are FULLY EDITABLE (not frozen)
- Leaders can add/remove categories anytime
- Temporary teams have single category (can't add more)
- Both types can recruit, kick members, etc.
- Export shows team type and all categories

This system matches real robotics club workflows!
