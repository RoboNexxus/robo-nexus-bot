# Complete Team System Commands Reference

## 📋 Table of Contents
- [Admin Commands](#admin-commands) (2 commands)
- [Team Creation Commands](#team-creation-commands) (2 commands)
- [Team Leader Commands](#team-leader-commands) (6 commands)
- [Member Commands](#member-commands) (4 commands)

---

## 🔐 Admin Commands

### `/set_team_channel`
**Who can use:** Administrators only  
**Description:** Set the channel where team announcements will be posted

**Parameters:**
- `channel` (required): The text channel for team announcements

**Example:**
```
/set_team_channel channel:#teams
```

---

### `/announce_team_creation`
**Who can use:** Administrators only  
**Description:** Announce to members that they should create teams for an upcoming event

**Parameters:**
- `event_name` (required): Name of the event/competition
- `categories` (optional): Competition categories (comma-separated: "Robo War, Robo Soccer, Drone")
- `deadline` (optional): Deadline for team creation
- `max_members` (optional): Maximum team size
- `team_type` (optional): Permanent/Temporary/Both
- `additional_info` (optional): Any extra information

**Example:**
```
/announce_team_creation 
  event_name:Robo Nexus Championship 2026
  categories:Robo War, Robo Soccer
  deadline:March 15, 2026
  max_members:10
  team_type:Both Types Allowed
```

---

## 🆕 Team Creation Commands

### `/create_permanent_team`
**Who can use:** Anyone (not already in a team)  
**Description:** Create a permanent team that can compete in multiple categories

**Parameters:**
- `name` (required): Team name (e.g., "2f4u")
- `description` (required): Team description
- `max_members` (optional): Maximum team size (default: 10, range: 2-50)
- `requirements` (optional): Join requirements
- `initial_members` (optional): Comma-separated names to add immediately (e.g., "John, Sarah, Mike")

**Example:**
```
/create_permanent_team 
  name:2f4u
  description:Elite robotics team focused on innovation
  max_members:8
  requirements:Must have robotics experience
  initial_members:John Doe, Sarah Smith
```

**Notes:**
- You become the team leader
- Can add multiple competition categories later
- Initial members can be Discord users or external people

---

### `/create_temp_team`
**Who can use:** Anyone (not already in a team)  
**Description:** Create a temporary team for a specific competition

**Parameters:**
- `name` (required): Team name
- `category` (required): Competition category (choose from dropdown)
- `description` (required): Team description
- `max_members` (optional): Maximum team size (default: 10, range: 2-50)
- `requirements` (optional): Join requirements
- `initial_members` (optional): Comma-separated names to add immediately

**Categories:**
- ⚔️ Robo War
- ⚽ Robo Soccer
- 🚁 Drone
- 💡 Innovation
- 🛤️ Line Follower
- 🏁 Robo Race

**Example:**
```
/create_temp_team 
  name:DroneStars
  category:Drone
  description:Drone racing specialists
  max_members:6
  initial_members:Mike Johnson
```

---

## 👑 Team Leader Commands

### `/add_category`
**Who can use:** Team leaders only (permanent teams only)  
**Description:** Add a competition category to your permanent team

**Parameters:**
- `category` (required): Competition category to add (choose from dropdown)

**Example:**
```
/add_category category:Robo War
```

**Notes:**
- Only works for permanent teams
- Can add multiple categories
- Cannot add duplicate categories

---

### `/remove_category`
**Who can use:** Team leaders only  
**Description:** Remove a competition category from your permanent team

**Parameters:**
- `category` (required): Competition category to remove (choose from dropdown)

**Example:**
```
/remove_category category:Robo Soccer
```

---

### `/convert_to_permanent`
**Who can use:** Team leaders only (temporary teams only)  
**Description:** Convert your temporary team to a permanent team

**Example:**
```
/convert_to_permanent
```

**Notes:**
- Allows your team to compete in multiple categories
- Cannot be reversed
- Use `/add_category` after converting to add more categories

---

### `/recruit_members`
**Who can use:** Team leaders only  
**Description:** Post a recruitment message to find team members

**Parameters:**
- `channel` (optional): Channel to post in (defaults to current channel)

**Example:**
```
/recruit_members channel:#general
```

**What it does:**
- Posts an @here announcement with team details
- Includes a "Join Team" button
- Shows team info, categories, and requirements
- Members can click the button to join

---

### `/add_member`
**Who can use:** Team leaders only  
**Description:** Manually add a member to your team (for Discord users or external people)

**Parameters:**
- `member_name` (required): Name of the person to add
- `user` (optional): Discord user (if they have Discord)

**Examples:**
```
# Add Discord user
/add_member member_name:John user:@JohnDoe

# Add external person (no Discord)
/add_member member_name:Sarah Smith
```

**Notes:**
- Can add Discord members or external people
- Checks if team is full
- Checks if person is already in another team
- Notifies Discord users via DM

---

### `/remove_member`
**Who can use:** Team leaders only  
**Description:** Remove a member from your team

**Parameters:**
- `member_name` (optional): Name of the person to remove
- `user` (optional): Discord user (if they have Discord)

**Examples:**
```
# Remove Discord user
/remove_member user:@JohnDoe

# Remove external person
/remove_member member_name:Sarah Smith
```

**Notes:**
- Must provide either member_name or user
- Cannot remove yourself (use `/disband_team` instead)
- Notifies Discord users via DM

---

## 👥 Member Commands

### `/my_team`
**Who can use:** Anyone in a team  
**Description:** View your team information

**Example:**
```
/my_team
```

**Shows:**
- Team name and type (permanent/temporary)
- Team description
- Competition categories
- Team leader
- Member count and list
- Requirements
- Recruiting status

---

### `/view_team`
**Who can use:** Anyone  
**Description:** View details of any team

**Parameters:**
- `team_name` (required): Name of the team to view

**Example:**
```
/view_team team_name:2f4u
```

---

### `/list_teams`
**Who can use:** Anyone  
**Description:** View all teams in the robotics club

**Parameters:**
- `category` (optional): Filter by competition category
- `team_type` (optional): Filter by team type (Permanent/Temporary)

**Examples:**
```
# List all teams
/list_teams

# List only Robo War teams
/list_teams category:Robo War

# List only permanent teams
/list_teams team_type:Permanent Teams

# List permanent Drone teams
/list_teams category:Drone team_type:Permanent Teams
```

**Shows:**
- Team name and type
- Categories
- Leader
- Member count
- Recruiting status

---

### `/leave_team`
**Who can use:** Team members (not leaders)  
**Description:** Leave your current team

**Example:**
```
/leave_team
```

**Notes:**
- Team leaders cannot use this (use `/disband_team` or `/transfer_leadership` first)
- Notifies the team leader
- You can join another team after leaving

---

## 📊 Team Types Explained

### ♾️ Permanent Teams
- Can compete in multiple categories
- Long-term teams that stay together
- Add/remove categories as needed
- Use `/create_permanent_team` to create

### ⏱️ Temporary Teams
- For a single competition only
- One category per team
- Can be converted to permanent
- Use `/create_temp_team` to create

---

## 🏆 Competition Categories

- ⚔️ **Robo War** - Combat robotics
- ⚽ **Robo Soccer** - Robot soccer competition
- 🚁 **Drone** - Drone racing and challenges
- 💡 **Innovation** - Creative robotics projects
- 🛤️ **Line Follower** - Line following robots
- 🏁 **Robo Race** - Racing competitions

---

## 💡 Quick Start Guide

### For Members:
1. Check available teams: `/list_teams`
2. Create your own team: `/create_permanent_team` or `/create_temp_team`
3. View your team: `/my_team`
4. Leave a team: `/leave_team`

### For Team Leaders:
1. Create team: `/create_permanent_team` or `/create_temp_team`
2. Add categories (permanent only): `/add_category`
3. Recruit members: `/recruit_members`
4. Add members manually: `/add_member`
5. Manage team: `/remove_member`, `/convert_to_permanent`

### For Admins:
1. Set team channel: `/set_team_channel`
2. Announce events: `/announce_team_creation`

---

## 📝 Notes

- You can only be in ONE team at a time
- You can only lead ONE team at a time
- Team names must be unique
- Team size: 2-50 members
- Initial members can be added during team creation
- All optional parameters can be skipped
- Commands show helpful error messages if something goes wrong

---

## 🔢 Total Commands: 14

- **Admin:** 2 commands
- **Team Creation:** 2 commands
- **Team Leader:** 6 commands
- **Member:** 4 commands
