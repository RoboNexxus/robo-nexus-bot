# Google Analytics Setup for Replit

Quick guide to set up Google Analytics stats channel on Replit using Secrets.

## Step 1: Get Your GA4 Property ID

1. Go to [Google Analytics](https://analytics.google.com/)
2. Click **Admin** (gear icon) → **Property Settings**
3. Copy your **Property ID** (example: `123456789`)

## Step 2: Create Google Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select your project
3. Go to **IAM & Admin** → **Service Accounts**
4. Click **Create Service Account**
   - Name: `discord-bot-analytics`
   - Click **Create and Continue**
   - Skip optional steps, click **Done**

## Step 3: Download Service Account Key

1. Click on your new service account
2. Go to **Keys** tab
3. Click **Add Key** → **Create new key**
4. Choose **JSON** format
5. Click **Create** - downloads a JSON file
6. Open the file in a text editor

## Step 4: Grant Analytics Access

1. Go back to [Google Analytics](https://analytics.google.com/)
2. Click **Admin** → **Property Access Management**
3. Click **+** → **Add users**
4. Paste the service account email (from JSON file)
   - Example: `discord-bot-analytics@project-id.iam.gserviceaccount.com`
5. Role: **Viewer**
6. Click **Add**

## Step 5: Add to Replit Secrets

1. In your Replit project, click **Tools** → **Secrets** (or the lock icon 🔒)

2. Add these two secrets:

### Secret 1: GA_PROPERTY_ID
- **Key:** `GA_PROPERTY_ID`
- **Value:** Your property ID (example: `123456789`)

### Secret 2: GOOGLE_CREDENTIALS_JSON
- **Key:** `GOOGLE_CREDENTIALS_JSON`
- **Value:** Copy the ENTIRE contents of your downloaded JSON file
  
  It should look like this:
  ```json
  {
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "abc123...",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
    "client_email": "discord-bot-analytics@project-id.iam.gserviceaccount.com",
    "client_id": "123456789",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
  }
  ```

## Step 6: Install Dependencies

Your bot will automatically install dependencies from `requirements.txt` when it runs. Make sure it includes:

```
google-analytics-data>=0.18.0
```

## Step 7: Restart and Test

1. Click **Stop** then **Run** to restart your bot
2. In Discord, run: `/setup_stats_channel`
3. Check the STATS category for your new channel!

## Expected Result

You should see:
```
📁 STATS
  └─ 📊 Total Views: 1.2K
```

The channel updates every 5 minutes automatically.

## Troubleshooting

### "N/A" showing in channel
- Check that `GA_PROPERTY_ID` is set correctly in Secrets
- Check that `GOOGLE_CREDENTIALS_JSON` contains the full JSON (including curly braces)
- Make sure there are no extra spaces or line breaks

### "Error" showing in channel
- Check bot logs (Console tab in Replit)
- Verify the service account email was added to Google Analytics
- Wait 5-10 minutes for permissions to propagate
- Try `/refresh_stats` command

### Permission errors in logs
- Make sure you added the service account to GA with "Viewer" role
- Double-check the service account email matches exactly

### JSON parsing errors
- Make sure you copied the ENTIRE JSON file contents
- Check for any missing quotes or brackets
- The JSON should start with `{` and end with `}`

## Security Notes

✅ **Safe:** Replit Secrets are encrypted and not visible in your code
✅ **Safe:** Service account only has "Viewer" access (read-only)
✅ **Safe:** Credentials are never committed to Git

❌ **Don't:** Share your service account JSON publicly
❌ **Don't:** Commit credentials to your repository

## Commands

- `/setup_stats_channel` - Create the stats channel
- `/refresh_stats` - Manually update stats now
- `/remove_stats_channel` - Remove the stats channel

## What Gets Tracked

- **Total Views:** Page views from the last 365 days
- Updates every 5 minutes
- Numbers formatted: 1.2K (thousands), 1.5M (millions)

That's it! Your Discord bot will now show live website stats. 🎉
