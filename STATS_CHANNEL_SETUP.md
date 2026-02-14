# Website Stats Channel Setup Guide

## Overview
The Stats Channel system creates a voice channel in a "STATS" category that displays your club's website statistics in real-time.

## Features
- ✅ Automatically creates a "STATS" category if it doesn't exist
- ✅ Creates a voice channel showing website status (Online/Offline)
- ✅ Updates every 5 minutes automatically
- ✅ Display-only channel (users can't join)
- ✅ Admin commands to manage the stats channel

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Bot Permissions Required
Make sure your bot has these permissions:
- Manage Channels
- View Channels
- Connect (for voice channels)

### 3. Run the Bot
The stats channel system will automatically start when the bot runs.

## Commands

### `/setup_stats_channel` (Admin Only)
Manually creates the stats channel in the STATS category.

**Usage:**
```
/setup_stats_channel
```

**What it does:**
- Creates "STATS" category if it doesn't exist
- Creates a voice channel named "🌐 Website: [Status]"
- Sets up automatic updates every 5 minutes

### `/remove_stats_channel` (Admin Only)
Removes the stats channel.

**Usage:**
```
/remove_stats_channel
```

### `/refresh_stats` (Admin Only)
Manually triggers an immediate stats update.

**Usage:**
```
/refresh_stats
```

## Customization

### Adding More Stats Channels
You can easily add more stats channels by modifying `stats_channel.py`. Here are some ideas:

1. **Member Count Channel**
```python
channel_name = f"👥 Members: {guild.member_count}"
```

2. **Bot Uptime Channel**
```python
uptime = datetime.now() - self.bot.start_time
channel_name = f"⏱️ Uptime: {uptime.days}d"
```

3. **GitHub Stars Channel** (if you have GitHub integration)
```python
channel_name = f"⭐ GitHub Stars: {stars_count}"
```

### Integrating Real Website Analytics

To display actual website statistics, you'll need to integrate with an analytics service:

#### Option 1: Google Analytics API
```python
async def fetch_website_stats(self):
    # Use Google Analytics API
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    # ... implement GA4 API calls
```

#### Option 2: Netlify Analytics API
```python
async def fetch_website_stats(self):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {NETLIFY_TOKEN}"}
        async with session.get(
            f"https://api.netlify.com/api/v1/sites/{SITE_ID}/analytics",
            headers=headers
        ) as response:
            data = await response.json()
            return {
                "total_visitors": data.get("visitors", "N/A"),
                "page_views": data.get("pageviews", "N/A")
            }
```

#### Option 3: Custom Analytics Endpoint
If your website has a custom analytics endpoint:
```python
async def fetch_website_stats(self):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://your-website.com/api/stats") as response:
            data = await response.json()
            return data
```

### Changing Update Frequency
Edit the `@tasks.loop` decorator in `stats_channel.py`:

```python
@tasks.loop(minutes=5)  # Change to desired interval
async def update_stats_channels(self):
    ...
```

Options:
- `minutes=1` - Update every minute
- `minutes=10` - Update every 10 minutes
- `hours=1` - Update every hour

## Troubleshooting

### Stats channel not appearing
1. Check bot has "Manage Channels" permission
2. Run `/setup_stats_channel` manually
3. Check bot logs for errors

### Stats not updating
1. Check bot is online
2. Verify the update task is running (check logs)
3. Try `/refresh_stats` to manually trigger update

### Permission errors
Make sure the bot role has these permissions:
- Manage Channels
- View Channels
- Connect

## Example Output

The voice channel will appear like this:
```
📁 STATS
  └─ 🌐 Website: Online ✅
```

When you add more stats channels:
```
📁 STATS
  ├─ 🌐 Website: Online ✅
  ├─ 👥 Members: 150
  ├─ ⭐ GitHub Stars: 42
  └─ 📊 Monthly Visitors: 1.2K
```

## Notes

- Voice channels are used because they can be updated more frequently than text channels
- The channels are set to "display only" - users can see them but can't join
- Stats update automatically every 5 minutes to avoid rate limits
- The current implementation shows website online/offline status as a starting point

## Next Steps

1. Run `/setup_stats_channel` in your Discord server
2. Customize the stats you want to display
3. Integrate with your actual analytics service
4. Add more stat channels as needed!
