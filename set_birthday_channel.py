"""
Quick script to set the birthday announcement channel
Run this once to configure the birthday channel to announcements
"""
from database import set_birthday_channel

# Your server ID
GUILD_ID = 1403310542030114898

# Announcements channel ID
ANNOUNCEMENTS_CHANNEL_ID = 1403347140390031493

# Set the birthday channel
success = set_birthday_channel(GUILD_ID, ANNOUNCEMENTS_CHANNEL_ID)

if success:
    print(f"✅ Birthday channel set to announcements (ID: {ANNOUNCEMENTS_CHANNEL_ID})")
    print("Birthday messages will now be sent to the announcements channel with @everyone")
else:
    print("❌ Failed to set birthday channel")
