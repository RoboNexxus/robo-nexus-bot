# Discord Interaction Timeout Fix

## Problem
Commands were giving "404 Not Found (error code: 10062): Unknown interaction" errors because Discord requires bots to respond within 3 seconds, but commands were doing async work (database calls, permission checks) BEFORE responding.

## Root Cause
Discord interactions expire after 3 seconds if not acknowledged. When commands do database calls or other async operations before calling `interaction.response.defer()` or `interaction.response.send_message()`, the interaction times out.

## Error Pattern
```
discord.errors.NotFound: 404 Not Found (error code: 10062): Unknown interaction
```

This happens when:
1. Command receives interaction from Discord
2. Command does slow async work (database call, API call, etc.)
3. More than 3 seconds pass
4. Command tries to respond → Discord says "Unknown interaction" (it expired)

## The Fix

### Rule: ALWAYS defer immediately at the start of any command that does async work

**BEFORE (Wrong - causes timeout):**
```python
async def my_command(self, interaction: discord.Interaction):
    """My command"""
    # ❌ Doing work before responding
    data = await self.db.get_something()  # This might take >3 seconds
    
    if not data:
        await interaction.response.send_message("Not found")  # TOO LATE - interaction expired
        return
```

**AFTER (Correct - no timeout):**
```python
async def my_command(self, interaction: discord.Interaction):
    """My command"""
    # ✅ Defer immediately to tell Discord "I'm working on it"
    await interaction.response.defer(ephemeral=True)
    
    # Now we have 15 minutes to complete the work
    data = await self.db.get_something()
    
    if not data:
        await interaction.followup.send("Not found")  # Use followup after defer
        return
```

## Files Fixed

### 1. `team_system.py` - `announce_team_creation` command
**Problem:** Did database call `await self.supabase.get_setting()` before deferring

**Fix:**
- Moved `await interaction.response.defer(ephemeral=True)` to the very first line
- Changed all `interaction.response.send_message()` calls to `interaction.followup.send()` (required after defer)

### 2. `admin_commands.py` - `clear_duplicate_commands` command
**Problem:** Did permission check before deferring

**Fix:**
- Moved `await interaction.response.defer(ephemeral=True)` to the very first line
- Changed permission check to use `interaction.followup.send()` instead

### 3. `auction.py` - `set_auction_channel` command
**Problem:** Did admin check with `self.is_admin()` before responding

**Fix:**
- Added `await interaction.response.defer(ephemeral=True)` at the start
- Changed admin check to use `interaction.followup.send()` instead

## Key Concepts

### interaction.response vs interaction.followup

- **`interaction.response`**: First response to Discord (must happen within 3 seconds)
  - `interaction.response.send_message()` - Send immediate response
  - `interaction.response.defer()` - Tell Discord "I'm working on it, give me time"

- **`interaction.followup`**: Additional messages after initial response
  - Used after `defer()` to send the actual response
  - Can be used multiple times
  - Has 15 minutes instead of 3 seconds

### When to use defer()

Use `defer()` when your command:
- Makes database calls
- Makes API requests
- Does complex calculations
- Processes files
- Does anything that might take >1 second

### ephemeral parameter

- `ephemeral=True`: Only the user who ran the command sees the response
- `ephemeral=False`: Everyone in the channel sees the response

## Testing

After these fixes:
1. All commands should respond immediately with "Bot is thinking..." indicator
2. No more "Unknown interaction" errors
3. Commands have 15 minutes to complete instead of 3 seconds

## Verification

Run the bot and test these commands:
- `/announce_team_creation` - Should work without timeout
- `/clear_duplicate_commands` - Should work without timeout  
- `/set_auction_channel` - Should work without timeout

All other commands already had proper defer() placement and should continue working.
