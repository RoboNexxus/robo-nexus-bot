# Quick Start: Website Stats Channel

## TL;DR - 5 Minute Setup

### 1. Get Google Analytics Property ID
- Go to [analytics.google.com](https://analytics.google.com)
- Admin → Property Settings
- Copy the Property ID number

### 2. Create Service Account
- Go to [console.cloud.google.com](https://console.cloud.google.com)
- IAM & Admin → Service Accounts → Create
- Download JSON key file

### 3. Give Service Account Access
- Back in Google Analytics
- Admin → Property Access Management → Add users
- Paste service account email (from JSON)
- Role: Viewer → Add

### 4. Add to Replit Secrets
Open Replit Secrets (🔒 icon) and add:

**Secret 1:**
```
Key: GA_PROPERTY_ID
Value: 123456789
```

**Secret 2:**
```
Key: GOOGLE_CREDENTIALS_JSON
Value: {paste entire JSON file contents here}
```

### 5. Restart Bot & Run Command
```
Stop → Run
Then in Discord: /setup_stats_channel
```

## Result
```
📁 STATS
  └─ 📊 Total Views: 1.2K
```

Updates every 5 minutes automatically!

## Need Help?
See full guide: `REPLIT_ANALYTICS_SETUP.md`
