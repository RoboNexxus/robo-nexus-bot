# Team Management System Setup

## Overview
The Team Management System allows Robo Nexus members to create teams for robotics competitions, recruit members, and manage their teams efficiently.

## Competition Categories
- ⚔️ **Robo War** - Combat robotics
- ⚽ **Robo Soccer** - Soccer playing robots
- 🚁 **Drone** - Drone competitions
- 💡 **Innovation** - Innovative robotics projects
- 🛤️ **Line Follower** - Line following robots
- 🏁 **Robo Race** - Racing robots

## Database Setup

### Step 1: Run SQL Script
1. Go to your Supabase Dashboard
2. Navigate to SQL Editor
3. Open the file `setup_teams_tables.sql`
4. Copy and paste the entire SQL script
5. Click "Run" to create the tables

This will create two tables:
- `teams` - Stores team information
- `team_members` - Stores team membership data

### Step 2: Verify Tables
After running the script, verify the tables were created:
```sql
SELECT * FROM teams;
SELECT * FROM team_members;
```

## Bot Commands

### For All Members

#### `/create_team`
Create a new robotics team for competitions.
- **name**: Team name (must be unique)
- **category**: Competition category (Robo War, Robo Soccer, etc.)
- **description**: Brief description of your team
- **max_members**: Maximum team size (2-50, default: 10)
- **requirements**: Optional skills/requirements for joining

**Example:**
```
/create_team name:"Thunder Bots" category:"Robo War" description:"Aggressive combat robot team" max_members:5 requirements:"Experience with Arduino"
```

#### `/post_recruitment`
Post a recruitment message with a "Join Team" button.
- **channel**: Optional - where to post (defaults to current channel)

Members can click the button to instantly join your team!

#### `/my_team`
View your current team information including:
- Team category and description
- Team leader
- All team members
- Recruitment status
- Requirements

#### `/list_teams`
View all teams in the robotics club.
- **category**: Optional filter by competition category

#### `/leave_team`
Leave your current team (leaders must disband or transfer leadership first).

### For Team Leaders Only

#### `/kick_member`
Remove a member from your team.
- **member**: The Discord member to kick

#### `/toggle_recruitment`
Open or close recruitment for your team.

#### `/disband_team`
Permanently disband your team (requires confirmation).
- All members will be notified
- Cannot be undone

## Features

### Smart Team Management
- ✅ One team per person (must leave to join another)
- ✅ One leadership per person
- ✅ Automatic team capacity management
- ✅ Auto-close recruitment when team is full
- ✅ Leader notifications when members join/leave

### Competition Categories
- 🏆 Teams are organized by competition type
- 🔍 Filter teams by category
- 📊 Easy for organizers to see who's competing in what

### Persistent Data
- 💾 All data stored in Supabase
- 🔄 Survives bot restarts
- 📈 Scalable for large clubs

### Interactive Recruitment
- 🎯 One-click join with buttons
- 📢 @here mentions for visibility
- 🎨 Beautiful embeds with team info
- ✉️ DM notifications to leaders

## Use Cases

### Competition Registration
When a competition is announced:
1. Core team creates teams for each category
2. Posts recruitment messages
3. Members join with one click
4. Organizers can see all teams with `/list_teams`

### Existing Teams Recruiting
If a team of 3 needs one more member:
1. Leader uses `/post_recruitment`
2. Posts in recruitment channel
3. Interested members click "Join Team"
4. Team automatically closes when full

### Team Organization
- View all Robo War teams: `/list_teams category:"Robo War"`
- Check your team status: `/my_team`
- Manage team roster: `/kick_member` or `/toggle_recruitment`

## Database Schema

### teams table
```sql
- id: BIGSERIAL PRIMARY KEY
- guild_id: TEXT (Discord server ID)
- name: TEXT (team name)
- leader_id: TEXT (Discord user ID)
- description: TEXT
- category: TEXT (competition category)
- max_members: INTEGER
- requirements: TEXT (optional)
- recruiting: BOOLEAN
- recruitment_message_id: TEXT (optional)
- recruitment_channel_id: TEXT (optional)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### team_members table
```sql
- id: BIGSERIAL PRIMARY KEY
- guild_id: TEXT
- team_name: TEXT (references teams)
- user_id: TEXT (Discord user ID)
- user_name: TEXT (Discord display name)
- joined_at: TIMESTAMP
```

## Troubleshooting

### "Failed to create team"
- Check Supabase connection
- Verify tables exist
- Check service role key in `supabase_api.py`

### "Team not found"
- Team may have been disbanded
- Check spelling of team name
- Use `/list_teams` to see all teams

### Button not working
- Bot may have restarted (buttons are persistent but need bot online)
- Try posting a new recruitment message

## Admin Notes

### Viewing All Teams
```sql
SELECT 
    t.name,
    t.category,
    t.leader_id,
    COUNT(tm.user_id) as member_count,
    t.max_members,
    t.recruiting
FROM teams t
LEFT JOIN team_members tm ON t.guild_id = tm.guild_id AND t.name = tm.team_name
GROUP BY t.id
ORDER BY t.created_at DESC;
```

### Finding Teams by Category
```sql
SELECT name, leader_id, description
FROM teams
WHERE category = 'Robo War'
AND recruiting = true;
```

### Member Participation
```sql
SELECT user_name, team_name, joined_at
FROM team_members
WHERE guild_id = 'YOUR_GUILD_ID'
ORDER BY joined_at DESC;
```

## Future Enhancements
- Team achievements/stats
- Competition results tracking
- Team photos/logos
- Private team channels
- Team roles assignment
