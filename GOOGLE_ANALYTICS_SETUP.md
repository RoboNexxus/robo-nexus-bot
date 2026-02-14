# Google Analytics Setup Guide

This guide will help you connect your bot to Google Analytics to display website views in Discord.

## Step 1: Get Your GA4 Property ID

1. Go to [Google Analytics](https://analytics.google.com/)
2. Select your website property
3. Click on **Admin** (gear icon at bottom left)
4. Under **Property**, click on **Property Settings**
5. Copy your **Property ID** (looks like: `123456789`)

## Step 2: Create a Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create a new one)
3. Go to **IAM & Admin** > **Service Accounts**
4. Click **Create Service Account**
5. Give it a name like "Discord Bot Analytics"
6. Click **Create and Continue**
7. Skip the optional steps and click **Done**

## Step 3: Create Service Account Key

1. Click on the service account you just created
2. Go to the **Keys** tab
3. Click **Add Key** > **Create new key**
4. Choose **JSON** format
5. Click **Create** - a JSON file will download
6. Save this file securely (e.g., `google-credentials.json`)

## Step 4: Grant Access to Google Analytics

1. Go back to [Google Analytics](https://analytics.google.com/)
2. Click **Admin** (gear icon)
3. Under **Property**, click **Property Access Management**
4. Click the **+** button (top right)
5. Click **Add users**
6. Paste the service account email (from the JSON file, looks like: `discord-bot-analytics@project-id.iam.gserviceaccount.com`)
7. Select role: **Viewer**
8. Click **Add**

## Step 5: Configure Your Bot

### Option A: Using Environment Variables (Recommended for Replit/Cloud)

Add these to your `.env` file or Replit Secrets:

```env
GA_PROPERTY_ID=123456789
GOOGLE_APPLICATION_CREDENTIALS=/path/to/google-credentials.json
```

### Option B: Using Replit Secrets (for Replit deployment)

1. In Replit, go to **Tools** > **Secrets**
2. Add these secrets:
   - Key: `GA_PROPERTY_ID`, Value: `123456789` (your property ID)
   - Key: `GOOGLE_APPLICATION_CREDENTIALS`, Value: `/home/runner/${REPL_SLUG}/google-credentials.json`
3. Upload your `google-credentials.json` file to your Replit project root

## Step 6: Install Dependencies

```bash
pip install google-analytics-data
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Step 7: Test the Setup

1. Restart your bot
2. Run `/setup_stats_channel` in your Discord server
3. Check if the channel shows your total views

## Troubleshooting

### "Google Analytics not configured" error
- Make sure `GA_PROPERTY_ID` is set in your environment variables
- Make sure `GOOGLE_APPLICATION_CREDENTIALS` points to the correct JSON file path

### "Permission denied" error
- Make sure you added the service account email to Google Analytics with Viewer access
- Wait a few minutes for permissions to propagate

### "File not found" error
- Check that the path in `GOOGLE_APPLICATION_CREDENTIALS` is correct
- Make sure the JSON file exists at that location
- For Replit, the file should be in your project root

### Views showing "Error" or "N/A"
- Check bot logs for detailed error messages
- Verify your Property ID is correct
- Make sure the service account has access to the property

## What the Bot Shows

The bot will display:
- **📊 Total Views: X** - Total page views from the last 365 days

The channel updates automatically every 5 minutes.

## Example Output

```
📁 STATS
  └─ 📊 Total Views: 1.2K
```

## Notes

- The bot fetches views from the last 365 days (as an approximation of "total views")
- Numbers are formatted: 1.2K for thousands, 1.5M for millions
- Stats are cached to avoid excessive API calls
- Updates happen every 5 minutes automatically
- The voice channel is display-only (users can't join)

## Security Tips

- Never commit your `google-credentials.json` file to Git
- Add it to `.gitignore`
- Keep your service account key secure
- Only grant "Viewer" access (not Editor or Admin)
