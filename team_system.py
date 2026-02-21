"""
Team Management System for Robo Nexus Bot
Supports permanent teams (multi-category) and temporary teams (single competition)
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging
from datetime import datetime
from typing import Optional, List
from async_supabase_wrapper import get_async_supabase

logger = logging.getLogger(__name__)

# Competition categories
COMPETITION_CATEGORIES = [
    "Robo War",
    "Robo Soccer",
    "Drone",
    "Innovation",
    "Line Follower",
    "Robo Race"
]

class TeamSystem(commands.Cog):
    """Manages permanent and temporary teams for Robo Nexus robotics club"""
    
    def __init__(self, bot):
        self.bot = bot
        self.supabase = get_async_supabase()
        
        logger.info("Team System initialized with Async Supabase")
    
    async def get_team_embed(self, team_name: str, team_data: dict, guild: discord.Guild) -> discord.Embed:
        """Create an embed for team display"""
        # Get team members and categories
        members = await self.supabase.get_team_members(str(guild.id), team_name)
        categories = await self.supabase.get_team_categories(str(guild.id), team_name)
        
        is_permanent = team_data.get('is_permanent', False)
        
        embed = discord.Embed(
            title=f"{'♾️' if is_permanent else '⏱️'} {team_name}",
            description=team_data.get('description', 'No description provided'),
            color=discord.Color.blue() if is_permanent else discord.Color.green(),
            timestamp=datetime.now()
        )
        
        # Team Type
        team_type = "♾️ Permanent Team" if is_permanent else "⏱️ Temporary Team"
        embed.add_field(name="📋 Type", value=team_type, inline=True)
        
        # Competition Categories
        category_emojis = {
            "Robo War": "⚔️",
            "Robo Soccer": "⚽",
            "Drone": "🚁",
            "Innovation": "💡",
            "Line Follower": "🛤️",
            "Robo Race": "🏁"
        }
        
        if categories:
            cat_list = [f"{category_emojis.get(cat, '🔧')} {cat}" for cat in categories]
            embed.add_field(
                name="🏆 Categories" if len(categories) > 1 else "🏆 Category",
                value="\n".join(cat_list),
                inline=True
            )
        else:
            embed.add_field(name="🏆 Categories", value="None set", inline=True)
        
        # Team Leader
        leader = guild.get_member(int(team_data['leader_id']))
        leader_name = leader.mention if leader else "Unknown"
        embed.add_field(name="👑 Leader", value=leader_name, inline=True)
        
        # Member Count
        member_count = len(members)
        max_members = team_data.get('max_members', 10)
        embed.add_field(
            name="👥 Members", 
            value=f"{member_count}/{max_members}", 
            inline=True
        )
        
        # Status
        status = "🟢 Recruiting" if team_data.get('recruiting', True) else "🔴 Closed"
        embed.add_field(name="📊 Status", value=status, inline=True)
        
        # Team Members List
        if members:
            members_list = []
            for member_data in members[:10]:
                member = guild.get_member(int(member_data['user_id']))
                if member:
                    members_list.append(f"• {member.mention}")
                else:
                    members_list.append(f"• {member_data['user_name']}")
            
            if members_list:
                embed.add_field(
                    name="🔧 Team Members",
                    value="\n".join(members_list),
                    inline=False
                )
        
        # Requirements
        if team_data.get('requirements'):
            embed.add_field(
                name="📋 Requirements",
                value=team_data['requirements'],
                inline=False
            )
        
        # Footer
        created_date = datetime.fromisoformat(team_data['created_at'].replace('Z', '+00:00')).strftime("%B %d, %Y")
        embed.set_footer(text=f"Team created on {created_date}")
        
        return embed
    
    @app_commands.command(name="create_permanent_team", description="Create a permanent team (can compete in multiple categories)")
    @app_commands.describe(
        name="Team name (e.g., '2f4u')",
        description="Team description",
        max_members="Maximum team size (default: 10)",
        requirements="Join requirements (optional)",
        initial_members="Comma-separated names to add immediately (e.g., 'John, Sarah, Mike')"
    )
    async def create_permanent_team(
        self,
        interaction: discord.Interaction,
        name: str,
        description: str,
        max_members: Optional[int] = 10,
        requirements: Optional[str] = None,
        initial_members: Optional[str] = None
    ):
        """Create a permanent team"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            # Validate team name (prevent SQL injection and special characters)
            if not name or len(name) > 50:
                await interaction.followup.send(
                    "❌ Team name must be between 1 and 50 characters!",
                    ephemeral=True
                )
                return
            
            # Only allow alphanumeric, spaces, hyphens, and underscores
            import re
            if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
                await interaction.followup.send(
                    "❌ Team name can only contain letters, numbers, spaces, hyphens, and underscores!",
                    ephemeral=True
                )
                return
            
            guild_id = str(interaction.guild_id)
            
            # Check if team name already exists
            existing_team = await self.supabase.get_team_by_name(guild_id, name)
            if existing_team:
                await interaction.followup.send(
                    f"❌ A team named **{name}** already exists!",
                    ephemeral=True
                )
                return
            
            # Check if user already leads a team
            leader_team = await self.supabase.get_team_by_leader(guild_id, str(interaction.user.id))
            if leader_team:
                await interaction.followup.send(
                    f"❌ You already lead **{leader_team['name']}**! You can only lead one team at a time.",
                    ephemeral=True
                )
                return
            
            # Check if user is already in a team
            user_team = await self.supabase.get_user_team(guild_id, str(interaction.user.id))
            if user_team:
                await interaction.followup.send(
                    f"❌ You are already in **{user_team['name']}**! Leave your current team first.",
                    ephemeral=True
                )
                return
            
            # Validate max_members
            if max_members < 2 or max_members > 50:
                await interaction.followup.send(
                    "❌ Team size must be between 2 and 50!",
                    ephemeral=True
                )
                return
            
            # Parse initial members
            member_names = []
            if initial_members:
                member_names = [name.strip() for name in initial_members.split(',') if name.strip()]
                
                # Check if total members (including leader) exceeds max
                if len(member_names) + 1 > max_members:
                    await interaction.followup.send(
                        f"❌ Too many initial members! You have {len(member_names)} + you = {len(member_names) + 1}, but max is {max_members}.\n"
                        f"Either reduce initial members or increase max_members.",
                        ephemeral=True
                    )
                    return
            
            # Create team
            team_data = {
                'guild_id': guild_id,
                'name': name,
                'leader_id': str(interaction.user.id),
                'description': description,
                'is_permanent': True,
                'max_members': max_members,
                'requirements': requirements,
                'recruiting': True
            }
            
            if not await self.supabase.create_team(team_data):
                await interaction.followup.send(
                    "❌ Failed to create team. Please try again.",
                    ephemeral=True
                )
                return
            
            # Add leader as first member
            leader_data = {
                'guild_id': guild_id,
                'team_name': name,
                'user_id': str(interaction.user.id),
                'user_name': interaction.user.display_name
            }
            await self.supabase.add_team_member(leader_data)
            
            # Add initial members
            added_members = []
            if member_names:
                for member_name in member_names:
                    member_id = f"external_{member_name.lower().replace(' ', '_')}"
                    member_data = {
                        'guild_id': guild_id,
                        'team_name': name,
                        'user_id': member_id,
                        'user_name': member_name
                    }
                    if await self.supabase.add_team_member(member_data):
                        added_members.append(member_name)
            
            response_msg = (
                f"✅ Permanent team **{name}** created!\n"
                f"♾️ This team can compete in multiple categories\n"
                f"👑 You are the team leader\n"
                f"👥 Team capacity: {len(added_members) + 1}/{max_members} members\n"
            )
            
            if added_members:
                response_msg += f"\n✅ Added members: {', '.join(added_members)}\n"
            
            response_msg += (
                f"\nUse `/add_category` to add competition categories!\n"
                f"Use `/recruit_members` to ask for more members!"
            )
            
            await interaction.followup.send(response_msg, ephemeral=True)
            
            logger.info(f"Permanent team '{name}' created by {interaction.user} with {len(added_members)} initial members")
            
        except Exception as e:
            logger.error(f"Error creating permanent team: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(name="create_temp_team", description="Create a temporary team for a specific competition")
    @app_commands.describe(
        name="Team name",
        category="Competition category",
        description="Team description",
        max_members="Maximum team size (default: 10)",
        requirements="Join requirements (optional)",
        initial_members="Comma-separated names to add immediately (e.g., 'John, Sarah, Mike')"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name="⚔️ Robo War", value="Robo War"),
        app_commands.Choice(name="⚽ Robo Soccer", value="Robo Soccer"),
        app_commands.Choice(name="🚁 Drone", value="Drone"),
        app_commands.Choice(name="💡 Innovation", value="Innovation"),
        app_commands.Choice(name="🛤️ Line Follower", value="Line Follower"),
        app_commands.Choice(name="🏁 Robo Race", value="Robo Race"),
    ])
    async def create_temp_team(
        self,
        interaction: discord.Interaction,
        name: str,
        category: app_commands.Choice[str],
        description: str,
        max_members: Optional[int] = 10,
        requirements: Optional[str] = None,
        initial_members: Optional[str] = None
    ):
        """Create a temporary team for a specific competition"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            
            # Check if team name already exists
            existing_team = await self.supabase.get_team_by_name(guild_id, name)
            if existing_team:
                await interaction.followup.send(
                    f"❌ A team named **{name}** already exists!",
                    ephemeral=True
                )
                return
            
            # Check if user already leads a team
            leader_team = await self.supabase.get_team_by_leader(guild_id, str(interaction.user.id))
            if leader_team:
                await interaction.followup.send(
                    f"❌ You already lead **{leader_team['name']}**! You can only lead one team at a time.",
                    ephemeral=True
                )
                return
            
            # Check if user is already in a team
            user_team = await self.supabase.get_user_team(guild_id, str(interaction.user.id))
            if user_team:
                await interaction.followup.send(
                    f"❌ You are already in **{user_team['name']}**! Leave your current team first.",
                    ephemeral=True
                )
                return
            
            # Validate max_members
            if max_members < 2 or max_members > 50:
                await interaction.followup.send(
                    "❌ Team size must be between 2 and 50!",
                    ephemeral=True
                )
                return
            
            # Parse initial members
            member_names = []
            if initial_members:
                member_names = [name.strip() for name in initial_members.split(',') if name.strip()]
                
                # Check if total members (including leader) exceeds max
                if len(member_names) + 1 > max_members:
                    await interaction.followup.send(
                        f"❌ Too many initial members! You have {len(member_names)} + you = {len(member_names) + 1}, but max is {max_members}.\n"
                        f"Either reduce initial members or increase max_members.",
                        ephemeral=True
                    )
                    return
            
            # Create team
            team_data = {
                'guild_id': guild_id,
                'name': name,
                'leader_id': str(interaction.user.id),
                'description': description,
                'is_permanent': False,
                'max_members': max_members,
                'requirements': requirements,
                'recruiting': True
            }
            
            if not await self.supabase.create_team(team_data):
                await interaction.followup.send(
                    "❌ Failed to create team. Please try again.",
                    ephemeral=True
                )
                return
            
            # Add category
            await self.supabase.add_team_category(guild_id, name, category.value)
            
            # Add leader as first member
            leader_data = {
                'guild_id': guild_id,
                'team_name': name,
                'user_id': str(interaction.user.id),
                'user_name': interaction.user.display_name
            }
            await self.supabase.add_team_member(leader_data)
            
            # Add initial members
            added_members = []
            if member_names:
                for member_name in member_names:
                    member_id = f"external_{member_name.lower().replace(' ', '_')}"
                    member_data = {
                        'guild_id': guild_id,
                        'team_name': name,
                        'user_id': member_id,
                        'user_name': member_name
                    }
                    if await self.supabase.add_team_member(member_data):
                        added_members.append(member_name)
            
            category_emojis = {
                "Robo War": "⚔️",
                "Robo Soccer": "⚽",
                "Drone": "🚁",
                "Innovation": "💡",
                "Line Follower": "🛤️",
                "Robo Race": "🏁"
            }
            emoji = category_emojis.get(category.value, "🔧")
            
            response_msg = (
                f"✅ Temporary team **{name}** created!\n"
                f"⏱️ For this competition only\n"
                f"🏆 Category: {emoji} {category.value}\n"
                f"👑 You are the team leader\n"
                f"👥 Team capacity: {len(added_members) + 1}/{max_members} members\n"
            )
            
            if added_members:
                response_msg += f"\n✅ Added members: {', '.join(added_members)}\n"
            
            response_msg += f"\nUse `/recruit_members` to ask for more members!"
            
            await interaction.followup.send(response_msg, ephemeral=True)
            
            logger.info(f"Temporary team '{name}' ({category.value}) created by {interaction.user} with {len(added_members)} initial members")
            
        except Exception as e:
            logger.error(f"Error creating temporary team: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="add_category", description="[LEADER] Add a competition category to your permanent team")
    @app_commands.describe(category="Competition category to add")
    @app_commands.choices(category=[
        app_commands.Choice(name="⚔️ Robo War", value="Robo War"),
        app_commands.Choice(name="⚽ Robo Soccer", value="Robo Soccer"),
        app_commands.Choice(name="🚁 Drone", value="Drone"),
        app_commands.Choice(name="💡 Innovation", value="Innovation"),
        app_commands.Choice(name="🛤️ Line Follower", value="Line Follower"),
        app_commands.Choice(name="🏁 Robo Race", value="Robo Race"),
    ])
    async def add_category(self, interaction: discord.Interaction, category: app_commands.Choice[str]):
        """Add a category to permanent team (leader only)"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            
            # Get leader's team
            leader_team = await self.supabase.get_team_by_leader(guild_id, str(interaction.user.id))
            
            if not leader_team:
                await interaction.followup.send(
                    "❌ You don't lead any team!",
                    ephemeral=True
                )
                return
            
            # Check if team is permanent
            if not leader_team.get('is_permanent', False):
                await interaction.followup.send(
                    "❌ Only permanent teams can have multiple categories!\n"
                    "Temporary teams are for single competitions.",
                    ephemeral=True
                )
                return
            
            # Check if category already added
            categories = await self.supabase.get_team_categories(guild_id, leader_team['name'])
            if category.value in categories:
                await interaction.followup.send(
                    f"❌ Your team already competes in **{category.value}**!",
                    ephemeral=True
                )
                return
            
            # Add category
            if await self.supabase.add_team_category(guild_id, leader_team['name'], category.value):
                category_emojis = {
                    "Robo War": "⚔️",
                    "Robo Soccer": "⚽",
                    "Drone": "🚁",
                    "Innovation": "💡",
                    "Line Follower": "🛤️",
                    "Robo Race": "🏁"
                }
                emoji = category_emojis.get(category.value, "🔧")
                
                await interaction.followup.send(
                    f"✅ Added {emoji} **{category.value}** to **{leader_team['name']}**!",
                    ephemeral=True
                )
                
                logger.info(f"Category '{category.value}' added to team '{leader_team['name']}'")
            else:
                await interaction.followup.send(
                    "❌ Failed to add category. Please try again.",
                    ephemeral=True
                )
            
        except Exception as e:
            logger.error(f"Error adding category: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="remove_category", description="[LEADER] Remove a competition category from your permanent team")
    @app_commands.describe(category="Competition category to remove")
    @app_commands.choices(category=[
        app_commands.Choice(name="⚔️ Robo War", value="Robo War"),
        app_commands.Choice(name="⚽ Robo Soccer", value="Robo Soccer"),
        app_commands.Choice(name="🚁 Drone", value="Drone"),
        app_commands.Choice(name="💡 Innovation", value="Innovation"),
        app_commands.Choice(name="🛤️ Line Follower", value="Line Follower"),
        app_commands.Choice(name="🏁 Robo Race", value="Robo Race"),
    ])
    async def remove_category(self, interaction: discord.Interaction, category: app_commands.Choice[str]):
        """Remove a category from permanent team (leader only)"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            
            # Get leader's team
            leader_team = await self.supabase.get_team_by_leader(guild_id, str(interaction.user.id))
            
            if not leader_team:
                await interaction.followup.send(
                    "❌ You don't lead any team!",
                    ephemeral=True
                )
                return
            
            # Check if category exists
            categories = await self.supabase.get_team_categories(guild_id, leader_team['name'])
            if category.value not in categories:
                await interaction.followup.send(
                    f"❌ Your team doesn't compete in **{category.value}**!",
                    ephemeral=True
                )
                return
            
            # Remove category
            if await self.supabase.remove_team_category(guild_id, leader_team['name'], category.value):
                await interaction.followup.send(
                    f"✅ Removed **{category.value}** from **{leader_team['name']}**!",
                    ephemeral=True
                )
                
                logger.info(f"Category '{category.value}' removed from team '{leader_team['name']}'")
            else:
                await interaction.followup.send(
                    "❌ Failed to remove category. Please try again.",
                    ephemeral=True
                )
            
        except Exception as e:
            logger.error(f"Error removing category: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(name="convert_to_permanent", description="[LEADER] Convert your temporary team to permanent")
    async def convert_to_permanent(self, interaction: discord.Interaction):
        """Convert temporary team to permanent (leader only)"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            
            # Get leader's team
            leader_team = await self.supabase.get_team_by_leader(guild_id, str(interaction.user.id))
            
            if not leader_team:
                await interaction.followup.send(
                    "❌ You don't lead any team!",
                    ephemeral=True
                )
                return
            
            # Check if already permanent
            if leader_team.get('is_permanent', False):
                await interaction.followup.send(
                    "❌ Your team is already permanent!",
                    ephemeral=True
                )
                return
            
            # Convert to permanent
            if await self.supabase.update_team(guild_id, leader_team['name'], {'is_permanent': True}):
                await interaction.followup.send(
                    f"✅ **{leader_team['name']}** is now a permanent team!\n"
                    f"♾️ Your team can now compete in multiple categories\n"
                    f"Use `/add_category` to add more competition categories!",
                    ephemeral=True
                )
                
                logger.info(f"Team '{leader_team['name']}' converted to permanent by {interaction.user}")
            else:
                await interaction.followup.send(
                    "❌ Failed to convert team. Please try again.",
                    ephemeral=True
                )
            
        except Exception as e:
            logger.error(f"Error converting team: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="my_team", description="View your team information")
    async def my_team(self, interaction: discord.Interaction):
        """View your team information"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            
            user_team = await self.supabase.get_user_team(guild_id, str(interaction.user.id))
            
            if not user_team:
                await interaction.followup.send(
                    "❌ You are not part of any team yet!\n"
                    "Use `/list_teams` to see available teams or create your own!",
                    ephemeral=True
                )
                return
            
            embed = await self.get_team_embed(user_team['name'], user_team, interaction.guild)
            
            if user_team['leader_id'] == str(interaction.user.id):
                embed.set_author(name="Your Team (You are the leader)", icon_url=interaction.user.display_avatar.url)
            else:
                embed.set_author(name="Your Team", icon_url=interaction.user.display_avatar.url)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error showing team: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="view_team", description="View details of any team")
    @app_commands.describe(team_name="Name of the team to view")
    async def view_team(self, interaction: discord.Interaction, team_name: str):
        """View any team's information"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            
            team_data = await self.supabase.get_team_by_name(guild_id, team_name)
            
            if not team_data:
                await interaction.followup.send(
                    f"❌ Team **{team_name}** not found!\n"
                    "Use `/list_teams` to see all available teams.",
                    ephemeral=True
                )
                return
            
            embed = await self.get_team_embed(team_name, team_data, interaction.guild)
            
            user_team = await self.supabase.get_user_team(guild_id, str(interaction.user.id))
            if user_team and user_team['name'] == team_name:
                if team_data['leader_id'] == str(interaction.user.id):
                    embed.set_author(name="Your Team (You are the leader)", icon_url=interaction.user.display_avatar.url)
                else:
                    embed.set_author(name="Your Team", icon_url=interaction.user.display_avatar.url)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error viewing team: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="list_teams", description="View all teams in the robotics club")
    @app_commands.describe(
        category="Filter by competition category (optional)",
        team_type="Filter by team type (optional)"
    )
    @app_commands.choices(
        category=[
            app_commands.Choice(name="⚔️ Robo War", value="Robo War"),
            app_commands.Choice(name="⚽ Robo Soccer", value="Robo Soccer"),
            app_commands.Choice(name="🚁 Drone", value="Drone"),
            app_commands.Choice(name="💡 Innovation", value="Innovation"),
            app_commands.Choice(name="🛤️ Line Follower", value="Line Follower"),
            app_commands.Choice(name="🏁 Robo Race", value="Robo Race"),
        ],
        team_type=[
            app_commands.Choice(name="♾️ Permanent Teams", value="permanent"),
            app_commands.Choice(name="⏱️ Temporary Teams", value="temporary"),
        ]
    )
    async def list_teams(
        self, 
        interaction: discord.Interaction, 
        category: Optional[app_commands.Choice[str]] = None,
        team_type: Optional[app_commands.Choice[str]] = None
    ):
        """List all teams"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            
            teams = await self.supabase.get_all_teams(guild_id)
            
            if not teams:
                await interaction.followup.send(
                    "❌ No teams have been created yet!\n"
                    "Use `/create_permanent_team` or `/create_temp_team` to create the first team!",
                    ephemeral=True
                )
                return
            
            # Filter by team type
            if team_type:
                is_perm = team_type.value == "permanent"
                teams = [t for t in teams if t.get('is_permanent', False) == is_perm]
            
            # Filter by category
            if category:
                filtered_teams = []
                for team in teams:
                    categories = await self.supabase.get_team_categories(guild_id, team['name'])
                    if category.value in categories:
                        filtered_teams.append(team)
                teams = filtered_teams
            
            if not teams:
                await interaction.followup.send(
                    f"❌ No teams found with the selected filters!",
                    ephemeral=True
                )
                return
            
            # Create embed
            title_parts = ["🤖 Robo Nexus Teams"]
            if team_type:
                title_parts.append(f"({'♾️ Permanent' if team_type.value == 'permanent' else '⏱️ Temporary'})")
            if category:
                title_parts.append(f"- {category.value}")
            
            embed = discord.Embed(
                title=" ".join(title_parts),
                description="All robotics teams in the club",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            
            category_emojis = {
                "Robo War": "⚔️",
                "Robo Soccer": "⚽",
                "Drone": "🚁",
                "Innovation": "💡",
                "Line Follower": "🛤️",
                "Robo Race": "🏁"
            }
            
            for team in teams[:25]:  # Discord limit
                leader = interaction.guild.get_member(int(team['leader_id']))
                leader_name = leader.display_name if leader else "Unknown"
                
                members = await self.supabase.get_team_members(guild_id, team['name'])
                member_count = len(members)
                max_members = team['max_members']
                status = "🟢 Recruiting" if team.get('recruiting', True) else "🔴 Closed"
                
                team_categories = await self.supabase.get_team_categories(guild_id, team['name'])
                cat_list = [f"{category_emojis.get(cat, '🔧')} {cat}" for cat in team_categories]
                categories_str = ", ".join(cat_list) if cat_list else "None"
                
                team_type_icon = "♾️" if team.get('is_permanent', False) else "⏱️"
                
                field_value = (
                    f"**Type:** {team_type_icon} {'Permanent' if team.get('is_permanent', False) else 'Temporary'}\n"
                    f"**Categories:** {categories_str}\n"
                    f"**Leader:** {leader_name}\n"
                    f"**Members:** {member_count}/{max_members}\n"
                    f"**Status:** {status}"
                )
                
                embed.add_field(
                    name=f"{team_type_icon} {team['name']}",
                    value=field_value,
                    inline=False
                )
            
            embed.set_footer(text=f"Total Teams: {len(teams)}")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error listing teams: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="leave_team", description="Leave your current team")
    async def leave_team(self, interaction: discord.Interaction):
        """Leave current team"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            
            user_team = await self.supabase.get_user_team(guild_id, str(interaction.user.id))
            
            if not user_team:
                await interaction.followup.send(
                    "❌ You are not part of any team!",
                    ephemeral=True
                )
                return
            
            if user_team['leader_id'] == str(interaction.user.id):
                await interaction.followup.send(
                    "❌ You are the team leader! Use `/disband_team` to disband or `/transfer_leadership` to transfer first.",
                    ephemeral=True
                )
                return
            
            if await self.supabase.remove_team_member(guild_id, user_team['name'], str(interaction.user.id)):
                await interaction.followup.send(
                    f"✅ You have left **{user_team['name']}**!",
                    ephemeral=True
                )
                
                leader = interaction.guild.get_member(int(user_team['leader_id']))
                if leader:
                    try:
                        await leader.send(
                            f"📢 **{interaction.user.display_name}** has left your team **{user_team['name']}**."
                        )
                    except:
                        pass
                
                logger.info(f"{interaction.user} left team '{user_team['name']}'")
            else:
                await interaction.followup.send(
                    "❌ Failed to leave team. Please try again.",
                    ephemeral=True
                )
            
        except Exception as e:
            logger.error(f"Error leaving team: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="recruit_members", description="[LEADER] Ask for members to join your team")
    @app_commands.describe(channel="Channel to post recruitment message (optional)")
    async def recruit_members(
        self,
        interaction: discord.Interaction,
        channel: Optional[discord.TextChannel] = None
    ):
        """Post a recruitment message for a team"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            
            team_data = await self.supabase.get_team_by_leader(guild_id, str(interaction.user.id))
            
            if not team_data:
                await interaction.followup.send(
                    "❌ You don't lead any team!",
                    ephemeral=True
                )
                return
            
            members = await self.supabase.get_team_members(guild_id, team_data['name'])
            if len(members) >= team_data['max_members']:
                await interaction.followup.send(
                    "❌ Your team is already full!",
                    ephemeral=True
                )
                return
            
            target_channel = channel or interaction.channel
            
            embed = await self.get_team_embed(team_data['name'], team_data, interaction.guild)
            embed.color = discord.Color.green()
            embed.title = f"{'♾️' if team_data.get('is_permanent', False) else '⏱️'} {team_data['name']} is Recruiting!"
            
            view = JoinTeamView(self, team_data['name'], guild_id)
            
            recruitment_msg = await target_channel.send(
                content="@here **New Team Recruitment!**",
                embed=embed,
                view=view
            )
            
            await interaction.followup.send(
                f"✅ Recruitment message posted in {target_channel.mention}!",
                ephemeral=True
            )
            
            logger.info(f"Recruitment posted for team '{team_data['name']}' by {interaction.user}")
            
        except Exception as e:
            logger.error(f"Error posting recruitment: {e}")
            try:
                await interaction.followup.send(
                    f"❌ Error: {str(e)}",
                    ephemeral=True
                )
            except:
                await interaction.followup.send(
                    f"❌ Error: {str(e)}",
                    ephemeral=True
                )
    @app_commands.command(name="add_member", description="[LEADER] Manually add a member to your team (for non-Discord members)")
    @app_commands.describe(
        member_name="Name of the person to add (e.g., 'John Doe')",
        user="Discord user (optional, if they have Discord)"
    )
    async def add_member(
        self,
        interaction: discord.Interaction,
        member_name: str,
        user: Optional[discord.Member] = None
    ):
        """Manually add a member to team (leader only)"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)

            # Get leader's team
            leader_team = await self.supabase.get_team_by_leader(guild_id, str(interaction.user.id))

            if not leader_team:
                await interaction.followup.send(
                    "❌ You don't lead any team!",
                    ephemeral=True
                )
                return

            # Check if team is full
            members = await self.supabase.get_team_members(guild_id, leader_team['name'])
            if len(members) >= leader_team['max_members']:
                await interaction.followup.send(
                    f"❌ Your team is full ({leader_team['max_members']} members)!\n"
                    f"Use `/edit_team` to increase max_members first.",
                    ephemeral=True
                )
                return

            # If Discord user provided, use their ID and name
            if user:
                user_id = str(user.id)
                display_name = user.display_name

                # Check if user is already in a team
                existing_team = await self.supabase.get_user_team(guild_id, user_id)
                if existing_team:
                    await interaction.followup.send(
                        f"❌ {user.mention} is already in team **{existing_team['name']}**!",
                        ephemeral=True
                    )
                    return
            else:
                # Non-Discord member - use name as ID (prefixed with "external_")
                user_id = f"external_{member_name.lower().replace(' ', '_')}"
                display_name = member_name

                # Check if this name is already in the team
                for member in members:
                    if member['user_name'].lower() == member_name.lower():
                        await interaction.followup.send(
                            f"❌ **{member_name}** is already in your team!",
                            ephemeral=True
                        )
                        return

            # Add member
            member_data = {
                'guild_id': guild_id,
                'team_name': leader_team['name'],
                'user_id': user_id,
                'user_name': display_name
            }

            if await self.supabase.add_team_member(member_data):
                if user:
                    await interaction.followup.send(
                        f"✅ Added {user.mention} to **{leader_team['name']}**!",
                        ephemeral=True
                    )

                    # Notify the user
                    try:
                        await user.send(
                            f"🎉 You've been added to team **{leader_team['name']}** by {interaction.user.display_name}!\n"
                            f"Use `/my_team` to view your team information."
                        )
                    except:
                        pass
                else:
                    await interaction.followup.send(
                        f"✅ Added **{member_name}** (non-Discord member) to **{leader_team['name']}**!",
                        ephemeral=True
                    )

                logger.info(f"{display_name} added to team '{leader_team['name']}' by {interaction.user}")
            else:
                await interaction.followup.send(
                    "❌ Failed to add member. Please try again.",
                    ephemeral=True
                )

        except Exception as e:
            logger.error(f"Error adding member: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(name="remove_member", description="[LEADER] Remove a member from your team")
    @app_commands.describe(
        member_name="Name of the person to remove",
        user="Discord user (optional, if they have Discord)"
    )
    async def remove_member(
        self,
        interaction: discord.Interaction,
        member_name: Optional[str] = None,
        user: Optional[discord.Member] = None
    ):
        """Remove a member from team (leader only)"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)

            # Get leader's team
            leader_team = await self.supabase.get_team_by_leader(guild_id, str(interaction.user.id))

            if not leader_team:
                await interaction.followup.send(
                    "❌ You don't lead any team!",
                    ephemeral=True
                )
                return

            # Need either member_name or user
            if not member_name and not user:
                await interaction.followup.send(
                    "❌ Please provide either a member name or Discord user!",
                    ephemeral=True
                )
                return

            # Get team members
            members = await self.supabase.get_team_members(guild_id, leader_team['name'])

            # Find the member to remove
            member_to_remove = None

            if user:
                # Remove by Discord user
                for member in members:
                    if member['user_id'] == str(user.id):
                        member_to_remove = member
                        break

                if not member_to_remove:
                    await interaction.followup.send(
                        f"❌ {user.mention} is not in your team!",
                        ephemeral=True
                    )
                    return

                # Can't remove yourself
                if user.id == interaction.user.id:
                    await interaction.followup.send(
                        "❌ You can't remove yourself! Use `/disband_team` to disband the team.",
                        ephemeral=True
                    )
                    return
            else:
                # Remove by name (for non-Discord members)
                for member in members:
                    if member['user_name'].lower() == member_name.lower():
                        member_to_remove = member
                        break

                if not member_to_remove:
                    await interaction.followup.send(
                        f"❌ **{member_name}** is not in your team!",
                        ephemeral=True
                    )
                    return

            # Remove member
            if await self.supabase.remove_team_member(guild_id, leader_team['name'], member_to_remove['user_id']):
                await interaction.followup.send(
                    f"✅ Removed **{member_to_remove['user_name']}** from **{leader_team['name']}**!",
                    ephemeral=True
                )

                # Notify if Discord user
                if user:
                    try:
                        await user.send(
                            f"📢 You have been removed from team **{leader_team['name']}** by the team leader."
                        )
                    except:
                        pass

                logger.info(f"{member_to_remove['user_name']} removed from team '{leader_team['name']}' by {interaction.user}")
            else:
                await interaction.followup.send(
                    "❌ Failed to remove member. Please try again.",
                    ephemeral=True
                )

        except Exception as e:
            logger.error(f"Error removing member: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
    @app_commands.command(name="set_team_channel", description="[ADMIN] Set the channel for team announcements")
    @app_commands.describe(channel="The channel where team announcements will be sent")
    @app_commands.default_permissions(administrator=True)
    async def set_team_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Set the team announcement channel (Admin only)"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            key = f'team_channel_{guild_id}'
            channel_id = str(channel.id)

            logger.info(f"Attempting to set team channel: guild_id={guild_id}, key={key}, channel_id={channel_id}")

            # Save to database
            result = await self.supabase.set_setting(key, channel_id)
            
            logger.info(f"Database set_setting result: {result}")
            
            if result:
                # Verify it was saved by reading it back
                saved_value = await self.supabase.get_setting(key)
                logger.info(f"Verification read: saved_value={saved_value}")
                
                if saved_value == channel_id:
                    embed = discord.Embed(
                        title="✅ Team Channel Set",
                        description=f"Team announcements will now be sent to {channel.mention}",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Channel ID", value=channel_id, inline=False)
                    embed.add_field(name="Verification", value="✅ Confirmed in database", inline=False)
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    logger.info(f"Team channel set to {channel.name} by {interaction.user}")
                else:
                    embed = discord.Embed(
                        title="⚠️ Partial Success",
                        description=f"Channel was saved but verification failed.",
                        color=discord.Color.orange()
                    )
                    embed.add_field(name="Expected", value=channel_id, inline=True)
                    embed.add_field(name="Got", value=str(saved_value), inline=True)
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    logger.warning(f"Team channel verification mismatch: expected={channel_id}, got={saved_value}")
            else:
                embed = discord.Embed(
                    title="❌ Failed to Set Team Channel",
                    description="Database operation returned False. Check bot logs for details.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                logger.error(f"Failed to set team channel: set_setting returned False")
        except Exception as e:
            logger.error(f"Error setting team channel: {e}", exc_info=True)
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(name="announce_team_creation", description="[ADMIN] Announce team creation for an event")
    @app_commands.describe(
        event_name="Name of the event/competition",
        categories="Competition categories (comma-separated, optional)",
        deadline="Deadline for team creation (optional)",
        max_members="Maximum team size (optional)",
        team_type="Permanent or Temporary teams (optional)",
        additional_info="Any additional information (optional)"
    )
    @app_commands.choices(team_type=[
        app_commands.Choice(name="♾️ Permanent Teams", value="permanent"),
        app_commands.Choice(name="⏱️ Temporary Teams", value="temporary"),
        app_commands.Choice(name="Both Types Allowed", value="both"),
    ])
    @app_commands.default_permissions(administrator=True)
    async def announce_team_creation(
        self,
        interaction: discord.Interaction,
        event_name: str,
        categories: Optional[str] = None,
        deadline: Optional[str] = None,
        max_members: Optional[int] = None,
        team_type: Optional[app_commands.Choice[str]] = None,
        additional_info: Optional[str] = None
    ):
        """Announce team creation for an event (Admin only)"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)

            # Get team channel
            team_channel_id = await self.supabase.get_setting(f'team_channel_{guild_id}')

            if not team_channel_id:
                await interaction.followup.send(
                    "❌ Team channel not configured! Use `/set_team_channel` first.",
                    ephemeral=True
                )
                return

            team_channel = interaction.guild.get_channel(int(team_channel_id))

            if not team_channel:
                await interaction.followup.send(
                    "❌ Team channel not found! Please reconfigure using `/set_team_channel`.",
                    ephemeral=True
                )
                return

            # Create announcement embed
            embed = discord.Embed(
                title=f"🤖 Team Creation Announcement",
                description=f"**{event_name}**\n\nIt's time to form your teams for the upcoming event!",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )

            # Add categories if provided
            if categories:
                category_list = [cat.strip() for cat in categories.split(',')]
                category_emojis = {
                    "Robo War": "⚔️",
                    "Robo Soccer": "⚽",
                    "Drone": "🚁",
                    "Innovation": "💡",
                    "Line Follower": "🛤️",
                    "Robo Race": "🏁"
                }

                formatted_cats = []
                for cat in category_list:
                    emoji = category_emojis.get(cat, "🔧")
                    formatted_cats.append(f"{emoji} {cat}")

                embed.add_field(
                    name="🏆 Competition Categories",
                    value="\n".join(formatted_cats),
                    inline=False
                )

            # Add team type info
            if team_type:
                type_info = {
                    "permanent": "♾️ **Permanent Teams Only**\nCreate teams that can compete in multiple categories",
                    "temporary": "⏱️ **Temporary Teams Only**\nCreate teams for this specific competition",
                    "both": "♾️⏱️ **Both Types Allowed**\nChoose permanent or temporary based on your needs"
                }
                embed.add_field(
                    name="📋 Team Type",
                    value=type_info.get(team_type.value, "Any type allowed"),
                    inline=False
                )

            # Add max members if provided
            if max_members:
                embed.add_field(
                    name="👥 Maximum Team Size",
                    value=f"{max_members} members per team",
                    inline=True
                )

            # Add deadline if provided
            if deadline:
                embed.add_field(
                    name="⏰ Deadline",
                    value=deadline,
                    inline=True
                )

            # Add additional info if provided
            if additional_info:
                embed.add_field(
                    name="📝 Additional Information",
                    value=additional_info,
                    inline=False
                )

            # Add instructions
            instructions = (
                "**How to Create Your Team:**\n"
                "• Use `/create_permanent_team` for permanent teams\n"
                "• Use `/create_temp_team` for temporary teams\n"
                "• Use `/list_teams` to see all existing teams\n"
                "• Use `/recruit_members` to find teammates\n"
                "• Use `/my_team` to view your team info"
            )
            embed.add_field(
                name="💡 Commands",
                value=instructions,
                inline=False
            )

            embed.set_footer(text=f"Announced by {interaction.user.display_name}")

            # Send announcement
            announcement_msg = await team_channel.send(
                content="@everyone **🚨 TEAM CREATION ANNOUNCEMENT 🚨**",
                embed=embed
            )

            await interaction.followup.send(
                f"✅ Team creation announcement posted in {team_channel.mention}!",
                ephemeral=True
            )

            logger.info(f"Team creation announced for '{event_name}' by {interaction.user}")

        except Exception as e:
            logger.error(f"Error announcing team creation: {e}")
            try:
                await interaction.followup.send(
                    f"❌ Error: {str(e)}",
                    ephemeral=True
                )
            except:
                await interaction.followup.send(
                    f"❌ Error: {str(e)}",
                    ephemeral=True
                )




class JoinTeamView(discord.ui.View):
    """View with button to join a team"""
    
    def __init__(self, cog: TeamSystem, team_name: str, guild_id: str):
        super().__init__(timeout=None)
        self.cog = cog
        self.team_name = team_name
        self.guild_id = guild_id
    
    @discord.ui.button(label="Join Team", style=discord.ButtonStyle.green, emoji="✋")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle join team button click"""
        try:
            # CRITICAL: Defer immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            team_data = await self.cog.supabase.get_team_by_name(self.guild_id, self.team_name)
            
            if not team_data:
                await interaction.followup.send(
                    "❌ This team no longer exists!",
                    ephemeral=True
                )
                return
            
            user_team = await self.cog.supabase.get_user_team(self.guild_id, str(interaction.user.id))
            if user_team:
                await interaction.followup.send(
                    f"❌ You are already in **{user_team['name']}**!\n"
                    f"Use `/leave_team` first if you want to switch teams.",
                    ephemeral=True
                )
                return
            
            if not team_data.get('recruiting', True):
                await interaction.followup.send(
                    "❌ This team is not currently recruiting!",
                    ephemeral=True
                )
                return
            
            members = await self.cog.supabase.get_team_members(self.guild_id, self.team_name)
            if len(members) >= team_data['max_members']:
                await interaction.followup.send(
                    "❌ This team is full!",
                    ephemeral=True
                )
                return
            
            member_data = {
                'guild_id': self.guild_id,
                'team_name': self.team_name,
                'user_id': str(interaction.user.id),
                'user_name': interaction.user.display_name
            }
            
            if await self.cog.supabase.add_team_member(member_data):
                await interaction.followup.send(
                    f"✅ Welcome to **{self.team_name}**!\n"
                    f"Use `/my_team` to view your team information.",
                    ephemeral=True
                )
                
                leader = interaction.guild.get_member(int(team_data['leader_id']))
                if leader:
                    try:
                        await leader.send(
                            f"🎉 **{interaction.user.display_name}** has joined your team **{self.team_name}**!"
                        )
                    except:
                        pass
                
                logger.info(f"{interaction.user} joined team '{self.team_name}'")
            else:
                await interaction.followup.send(
                    "❌ Failed to join team. Please try again.",
                    ephemeral=True
                )
            
        except Exception as e:
            logger.error(f"Error joining team: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="debug_team_channel", description="[ADMIN] Debug team channel configuration")
    @app_commands.default_permissions(administrator=True)
    async def debug_team_channel(self, interaction: discord.Interaction):
        """Debug command to check team channel configuration"""
        try:
            await interaction.response.defer(ephemeral=True)
            
            guild_id = str(interaction.guild_id)
            key = f'team_channel_{guild_id}'
            
            # Try to get the setting
            team_channel_id = await self.supabase.get_setting(key)
            
            embed = discord.Embed(
                title="🔍 Team Channel Debug Info",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="Guild ID",
                value=guild_id,
                inline=False
            )
            
            embed.add_field(
                name="Setting Key",
                value=f"`{key}`",
                inline=False
            )
            
            if team_channel_id:
                embed.add_field(
                    name="Stored Channel ID",
                    value=team_channel_id,
                    inline=False
                )
                
                # Try to get the channel
                channel = interaction.guild.get_channel(int(team_channel_id))
                if channel:
                    embed.add_field(
                        name="Channel Found",
                        value=f"✅ {channel.mention}",
                        inline=False
                    )
                    embed.color = discord.Color.green()
                else:
                    embed.add_field(
                        name="Channel Found",
                        value="❌ Channel not found (may have been deleted)",
                        inline=False
                    )
                    embed.color = discord.Color.red()
            else:
                embed.add_field(
                    name="Stored Channel ID",
                    value="❌ Not set in database",
                    inline=False
                )
                embed.color = discord.Color.red()
                embed.add_field(
                    name="Solution",
                    value="Use `/set_team_channel` to configure",
                    inline=False
                )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error in debug_team_channel: {e}")
            await interaction.followup.send(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(TeamSystem(bot))
    logger.info("Team System cog loaded")

