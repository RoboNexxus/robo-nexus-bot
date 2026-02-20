# Replit Setup Checklist

## Required Secrets in Replit

Go to your Replit project → Click the lock icon (🔒 Secrets) → Add these:

### 1. Discord Configuration
```
DISCORD_TOKEN=<your_discord_bot_token>
GUILD_ID=1403310542030114898
```

### 2. Supabase Configuration (REQUIRED!)
```
SUPABASE_URL=https://pyedggezqefeeilxdprj.supabase.co
SUPABASE_SERVICE_KEY=<your_supabase_service_role_key>
```

**Where to find your Supabase Service Key:**
1. Go to https://supabase.com/dashboard/project/pyedggezqefeeilxdprj
2. Click "Settings" (gear icon) in the left sidebar
3. Click "API" 
4. Copy the "service_role" key (NOT the anon key!)
5. Paste it as `SUPABASE_SERVICE_KEY` in Replit Secrets

### 3. Optional (for GitHub integration)
```
GITHUB_TOKEN=<your_github_personal_access_token>
GITHUB_OWNER=RoboNexxus
```

### 4. Optional (for Google Analytics)
```
GA_PROPERTY_ID=<your_property_id>
GOOGLE_CREDENTIALS_JSON=<your_service_account_json>
```

---

## Quick Verification

After adding secrets, restart your Replit and check the logs:

✅ **Success looks like:**
```
✅ Configuration validated successfully
✅ Supabase API initialized with service key
✅ All 10 command cogs loaded successfully
✅ Synced X commands to guild 1403310542030114898
```

❌ **Error looks like:**
```
❌ Configuration error: SUPABASE_SERVICE_KEY environment variable is required!
```

If you see the error, double-check:
1. Secret name is exactly `SUPABASE_SERVICE_KEY` (case-sensitive!)
2. You copied the **service_role** key, not the anon key
3. You restarted the Replit after adding the secret

---

## Database Setup

After secrets are configured, run this in Supabase SQL Editor:

```sql
-- Disable RLS so bot can access database
ALTER TABLE bot_settings DISABLE ROW LEVEL SECURITY;
ALTER TABLE birthdays DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE auctions DISABLE ROW LEVEL SECURITY;
ALTER TABLE bids DISABLE ROW LEVEL SECURITY;
ALTER TABLE teams DISABLE ROW LEVEL SECURITY;
ALTER TABLE team_categories DISABLE ROW LEVEL SECURITY;
ALTER TABLE team_members DISABLE ROW LEVEL SECURITY;
ALTER TABLE competitions DISABLE ROW LEVEL SECURITY;
```

Or just run `fix_rls.sql` from the repo!

---

## Final Checklist

- [ ] `DISCORD_TOKEN` added to Replit Secrets
- [ ] `GUILD_ID` added to Replit Secrets
- [ ] `SUPABASE_URL` added to Replit Secrets
- [ ] `SUPABASE_SERVICE_KEY` added to Replit Secrets (service_role key!)
- [ ] RLS disabled on all tables in Supabase
- [ ] Replit restarted
- [ ] Bot starts without errors
- [ ] Commands work in Discord

---

## Troubleshooting

### "SUPABASE_SERVICE_KEY environment variable is required"
- Make sure the secret name is exactly `SUPABASE_SERVICE_KEY`
- Restart Replit after adding secrets
- Check you're using the service_role key, not anon key

### "Permission denied for table"
- Run `fix_rls.sql` in Supabase SQL Editor
- RLS must be DISABLED for bot to work

### "Commands not appearing in Discord"
- Check `GUILD_ID` is correct
- Wait 1-2 minutes for Discord to sync
- Try `/` in Discord to see if commands appear

### "Team commands not responding"
- Make sure RLS is disabled
- Check `SUPABASE_SERVICE_KEY` is set
- Verify team_system cog loaded (check logs)

---

**You're all set!** 🚀

Once you:
1. Add `SUPABASE_SERVICE_KEY` to Replit Secrets
2. Run `fix_rls.sql` in Supabase
3. Restart your bot

Everything should work perfectly!
