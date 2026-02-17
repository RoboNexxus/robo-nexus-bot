# Team System Admin Commands

## Setup Commands

### `/set_team_channel`
**Description:** Set the channel where team announcements will be posted

**Parameters:**
- `channel` (required): The text channel for team announcements

**Example:**
```
/set_team_channel channel:#teams
```

**Your Channel ID:** `1463500991298015356`

---

## Announcement Commands

### `/announce_team_creation`
**Description:** Announce to members that they should create teams for an upcoming event

**Parameters:**
- `event_name` (required): Name of the event/competition
- `categories` (optional): Competition categories (comma-separated)
  - Example: "Robo War, Robo Soccer, Drone"
- `deadline` (optional): Deadline for team creation
  - Example: "March 15, 2026" or "Next Friday"
- `max_members` (optional): Maximum team size
  - Example: 10
- `team_type` (optional): Type of teams allowed
  - Choices: "Permanent Teams", "Temporary Teams", "Both Types Allowed"
- `additional_info` (optional): Any extra information

**Example Usage:**

**Minimal:**
```
/announce_team_creation event_name:Robo Nexus Championship 2026
```

**Full Example:**
```
/announce_team_creation 
  event_name:Robo Nexus Championship 2026
  categories:Robo War, Robo Soccer, Drone
  deadline:March 15, 2026
  max_members:10
  team_type:Both Types Allowed
  additional_info:Registration opens next week. Early bird teams get bonus points!
```

**What it does:**
- Posts an @everyone announcement in the configured team channel
- Shows event name and details
- Lists competition categories (if provided)
- Shows team type requirements (permanent/temporary/both)
- Displays max team size (if provided)
- Shows deadline (if provided)
- Includes instructions on how to create teams
- All parameters except event_name are optional (skippable)

---

## Available Competition Categories

When specifying categories, use these exact names (comma-separated):
- Robo War ⚔️
- Robo Soccer ⚽
- Drone 🚁
- Innovation 💡
- Line Follower 🛤️
- Robo Race 🏁

---

## Team Types Explained

### ♾️ Permanent Teams
- Can compete in multiple categories
- Long-term teams that stay together
- Use `/create_permanent_team` to create

### ⏱️ Temporary Teams
- For a single competition only
- Disbanded after the event
- Use `/create_temp_team` to create

### Both Types Allowed
- Members can choose either type
- Flexible for different team preferences

---

## Quick Setup Guide

1. **Set the team channel:**
   ```
   /set_team_channel channel:#teams
   ```

2. **Announce team creation:**
   ```
   /announce_team_creation event_name:Your Event Name
   ```

3. **Members create teams using:**
   - `/create_permanent_team` or `/create_temp_team`

4. **Monitor teams:**
   - `/list_teams` to see all teams
   - Check the team channel for recruitment posts

---

## Notes

- All admin commands require Administrator permissions
- The announcement will ping @everyone in the team channel
- Members will see clear instructions on how to create teams
- All parameters except `event_name` are optional and can be skipped
