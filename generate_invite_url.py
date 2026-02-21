"""
Generate the correct Discord bot invite URL with all required permissions
"""
from config import Config
import discord

def generate_invite_url():
    """Generate bot invite URL with correct permissions"""
    
    # Get bot's client ID from the token (first part before the dot)
    # Or you can manually set it here
    print("=" * 60)
    print("DISCORD BOT INVITE URL GENERATOR")
    print("=" * 60)
    
    client_id = input("\nEnter your bot's Client ID (from Discord Developer Portal): ").strip()
    
    if not client_id:
        print("❌ Client ID is required!")
        return
    
    # Required permissions for the bot
    permissions = discord.Permissions()
    permissions.send_messages = True
    permissions.read_messages = True
    permissions.read_message_history = True
    permissions.manage_messages = True
    permissions.embed_links = True
    permissions.attach_files = True
    permissions.mention_everyone = True
    permissions.add_reactions = True
    permissions.manage_roles = True
    permissions.manage_channels = True
    permissions.view_channel = True
    permissions.manage_guild = True
    permissions.create_instant_invite = True
    
    # Generate the invite URL
    # CRITICAL: Must include both 'bot' and 'applications.commands' scopes
    invite_url = (
        f"https://discord.com/api/oauth2/authorize?"
        f"client_id={client_id}&"
        f"permissions={permissions.value}&"
        f"scope=bot%20applications.commands"  # BOTH scopes are required!
    )
    
    print("\n" + "=" * 60)
    print("✅ INVITE URL GENERATED")
    print("=" * 60)
    print("\n🔗 Use this URL to invite your bot:")
    print(f"\n{invite_url}\n")
    print("=" * 60)
    print("\n⚠️ IMPORTANT:")
    print("1. This URL includes BOTH 'bot' and 'applications.commands' scopes")
    print("2. Without 'applications.commands', slash commands won't work!")
    print("3. If your bot is already in the server, you need to:")
    print("   a. Kick the bot from the server")
    print("   b. Use this new URL to re-invite it")
    print("   c. Run 'python force_sync_commands.py' after re-inviting")
    print("\n4. After re-inviting, wait 1-2 minutes for commands to appear")
    print("=" * 60)
    
    # Also show the permissions value
    print(f"\n📊 Permissions value: {permissions.value}")
    print(f"🔑 Client ID: {client_id}")
    print("\n")

if __name__ == "__main__":
    generate_invite_url()
