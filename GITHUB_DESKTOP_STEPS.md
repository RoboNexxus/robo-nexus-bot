# GitHub Desktop - Push Steps

## Step 1: Open GitHub Desktop

Open GitHub Desktop and select your `robo-nexus-bot` repository

## Step 2: Check Changed Files

You should see 5 changed files in the left sidebar:
- ✅ bot.py
- ✅ admin_commands.py
- ✅ team_system.py
- ✅ auction.py
- ✅ welcome_system.py

## Step 3: Review Changes (Optional)

Click on each file to see what changed:
- Green lines = added code
- Red lines = removed code

## Step 4: Write Commit Message

In the bottom left, write:

**Summary (required):**
```
Fix: Stop deleting commands + add defer to prevent timeouts
```

**Description (optional):**
```
- bot.py: Removed clear_commands() that was deleting all commands
- admin_commands.py: Fixed clear_duplicate_commands
- team_system.py: Added defer to 14 commands
- auction.py: Added defer to 8 commands
- welcome_system.py: Added defer to 1 command

Fixes:
- Commands showing 0 available
- Team commands timing out
- Application did not respond errors
```

## Step 5: Commit

Click the blue "Commit to main" button at the bottom

## Step 6: Push

Click "Push origin" button at the top (or press Ctrl+P / Cmd+P)

## Step 7: Go to Replit

1. Open your Replit project
2. Click "Stop" to stop the bot
3. Wait for it to pull changes (or manually pull)
4. Click "Run" to start the bot

## Step 8: Check Logs

Look for this line in Replit logs:
```
✅ Synced X commands to guild
```

X should be 40+ (not 0!)

## Step 9: Test in Discord

1. Open Discord
2. Type `/` in any channel
3. You should see ALL commands
4. Try `/my_team` - should work without timeout
5. Try `/create_permanent_team` - should work without timeout

## Done!

If commands appear and work, problem solved! 🎉

If not, tell me:
- How many commands synced? (from Replit logs)
- What error appears?
