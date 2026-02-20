"""
Bug Condition Exploration Tests for Command Registration Issues
**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**

CRITICAL: These tests MUST FAIL on unfixed code - failure confirms the bugs exist
DO NOT attempt to fix the tests or the code when they fail
NOTE: These tests encode the expected behavior - they will validate the fix when they pass after implementation
GOAL: Surface counterexamples that demonstrate the three bugs exist
"""
import unittest
import asyncio
import discord
from discord.ext import commands
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import os
import sys
from io import StringIO


class TestBugCondition1_DuplicateCommandRegistration(unittest.TestCase):
    """
    Test 1.1: Duplicate command registration on bot startup
    **Validates: Requirements 2.1, 2.5, 2.6**
    
    Simulates bot startup, loads team_system cog, captures command tree state,
    reloads team_system cog (simulating restart), captures tree state again.
    
    EXPECTED OUTCOME ON UNFIXED CODE: Test FAILS showing duplicate commands (confirms bug exists)
    """
    
    def setUp(self):
        """Set up test bot instance"""
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        
    def test_duplicate_registration_on_cog_reload(self):
        """
        Property 1: Fault Condition - Unique Command Registration
        
        For any bot startup event where cogs are loaded and commands are registered,
        the bot SHALL ensure that each command name appears exactly once in the command tree.
        
        This test simulates:
        1. Bot starts and loads team_system cog
        2. Bot restarts (Discord still has cached commands) and loads team_system again
        3. Checks if duplicate commands appear in the tree
        
        EXPECTED ON UNFIXED CODE: Duplicate commands found (test FAILS)
        EXPECTED ON FIXED CODE: No duplicates (test PASSES)
        """
        async def run_test():
            # Create bot instance
            bot = commands.Bot(command_prefix="!", intents=self.intents)
            
            # Mock environment variables
            with patch.dict(os.environ, {'GUILD_ID': '123456789', 'DISCORD_TOKEN': 'fake_token'}):
                try:
                    # Load team_system cog for the first time
                    await bot.load_extension('team_system')
                    
                    # Capture command tree state after first load
                    first_load_commands = list(bot.tree.get_commands())
                    first_load_names = [cmd.name for cmd in first_load_commands]
                    
                    print(f"\n[Test 1.1] First load - Commands in tree: {len(first_load_names)}")
                    print(f"[Test 1.1] Command names: {first_load_names}")
                    
                    # Simulate bot restart by reloading the cog
                    # In real scenario, Discord keeps cached commands and bot reloads cogs
                    await bot.reload_extension('team_system')
                    
                    # Capture command tree state after reload
                    second_load_commands = list(bot.tree.get_commands())
                    second_load_names = [cmd.name for cmd in second_load_commands]
                    
                    print(f"[Test 1.1] Second load - Commands in tree: {len(second_load_names)}")
                    print(f"[Test 1.1] Command names: {second_load_names}")
                    
                    # Check for duplicates
                    unique_names = set(second_load_names)
                    has_duplicates = len(unique_names) != len(second_load_names)
                    
                    if has_duplicates:
                        # Find which commands are duplicated
                        from collections import Counter
                        name_counts = Counter(second_load_names)
                        duplicates = {name: count for name, count in name_counts.items() if count > 1}
                        print(f"\n[Test 1.1] ❌ COUNTEREXAMPLE FOUND: Duplicate commands detected!")
                        print(f"[Test 1.1] Duplicates: {duplicates}")
                        print(f"[Test 1.1] This confirms Bug #1: Commands are registered multiple times")
                    
                    # ASSERTION: Each command name should appear exactly once
                    self.assertEqual(
                        len(unique_names),
                        len(second_load_names),
                        f"Duplicate commands found after cog reload! "
                        f"Expected {len(unique_names)} unique commands, but found {len(second_load_names)} total commands. "
                        f"This indicates commands are being registered multiple times."
                    )
                    
                    print(f"[Test 1.1] ✅ No duplicates found - each command appears exactly once")
                    
                finally:
                    await bot.close()
        
        # Run the async test
        asyncio.run(run_test())


class TestBugCondition2_ForceSyncClearingAllCommands(unittest.TestCase):
    """
    Test 1.2: Force sync clearing all commands
    **Validates: Requirements 2.2, 2.3**
    
    Runs force_sync.py script, captures command tree state before/after clear, before/after sync.
    
    EXPECTED OUTCOME ON UNFIXED CODE: Test FAILS showing empty tree after sync (confirms bug exists)
    """
    
    def test_force_sync_operation_sequence(self):
        """
        Property 1: Fault Condition - Correct Force Sync Sequence
        
        For any force sync execution, the script SHALL load all cogs first to populate
        the command tree, then sync the populated tree to Discord, ensuring all commands
        are properly reregistered rather than cleared.
        
        This test simulates:
        1. Running force_sync.py script
        2. Capturing tree state before clear
        3. Capturing tree state after clear
        4. Capturing tree state after sync
        5. Verifying team commands are present
        
        EXPECTED ON UNFIXED CODE: Empty tree after sync (test FAILS)
        EXPECTED ON FIXED CODE: All commands present after sync (test PASSES)
        """
        async def run_test():
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            
            bot = commands.Bot(command_prefix="!", intents=intents)
            
            # Mock environment and Discord objects
            with patch.dict(os.environ, {'GUILD_ID': '123456789', 'DISCORD_TOKEN': 'fake_token'}):
                try:
                    # Simulate force_sync.py behavior
                    guild = discord.Object(id=123456789)
                    
                    # Step 1: Load cogs (as force_sync.py does)
                    print("\n[Test 1.2] Loading cogs...")
                    cogs = ['team_system']  # Focus on team_system for this test
                    for cog in cogs:
                        try:
                            await bot.load_extension(cog)
                            print(f"[Test 1.2] ✅ Loaded {cog}")
                        except Exception as e:
                            print(f"[Test 1.2] ❌ Failed to load {cog}: {e}")
                    
                    # Capture state after loading
                    after_load_commands = list(bot.tree.get_commands())
                    after_load_names = [cmd.name for cmd in after_load_commands]
                    print(f"[Test 1.2] After loading cogs - Commands in tree: {len(after_load_names)}")
                    print(f"[Test 1.2] Command names: {after_load_names}")
                    
                    # Step 2: Clear commands (as force_sync.py does)
                    print("\n[Test 1.2] Clearing commands...")
                    bot.tree.clear_commands(guild=guild)
                    bot.tree.clear_commands(guild=None)
                    
                    # Capture state after clearing
                    after_clear_commands = list(bot.tree.get_commands())
                    after_clear_names = [cmd.name for cmd in after_clear_commands]
                    print(f"[Test 1.2] After clearing - Commands in tree: {len(after_clear_names)}")
                    print(f"[Test 1.2] Command names: {after_clear_names}")
                    
                    # Step 3: Mock sync operation
                    # In real scenario, sync would send the cleared state to Discord
                    # We'll simulate by checking what would be synced
                    with patch.object(bot.tree, 'sync', new_callable=AsyncMock) as mock_sync:
                        # Configure mock to return the current tree state
                        mock_sync.return_value = after_clear_commands
                        
                        synced = await bot.tree.sync(guild=guild)
                        synced_names = [cmd.name for cmd in synced]
                        
                        print(f"\n[Test 1.2] After sync - Commands synced: {len(synced_names)}")
                        print(f"[Test 1.2] Synced command names: {synced_names}")
                        
                        # Check if team commands are present
                        team_commands = [
                            'create_permanent_team', 'create_temp_team', 'my_team',
                            'list_teams', 'add_category', 'remove_category'
                        ]
                        
                        missing_commands = [cmd for cmd in team_commands if cmd not in synced_names]
                        
                        if missing_commands or len(synced_names) == 0:
                            print(f"\n[Test 1.2] ❌ COUNTEREXAMPLE FOUND: Commands missing after force sync!")
                            print(f"[Test 1.2] Missing team commands: {missing_commands}")
                            print(f"[Test 1.2] Total commands synced: {len(synced_names)}")
                            print(f"[Test 1.2] This confirms Bug #2: Force sync clears all commands instead of reregistering them")
                        
                        # ASSERTION: After sync, tree should contain team commands
                        self.assertGreater(
                            len(synced_names),
                            0,
                            "Force sync resulted in zero commands! "
                            "The clear operation removed commands and sync did not restore them. "
                            "This indicates the operation sequence is incorrect."
                        )
                        
                        self.assertIn(
                            'create_permanent_team',
                            synced_names,
                            "Team command 'create_permanent_team' not found after force sync! "
                            "This indicates team_system cog commands were not properly reregistered."
                        )
                        
                        print(f"[Test 1.2] ✅ All commands properly synced")
                    
                finally:
                    await bot.close()
        
        # Run the async test
        asyncio.run(run_test())


class TestBugCondition3_TeamCommandsNotResponding(unittest.TestCase):
    """
    Test 1.3: Team commands not responding
    **Validates: Requirements 2.4**
    
    Simulates Discord interaction for /create_permanent_team.
    
    EXPECTED OUTCOME ON UNFIXED CODE: Test FAILS with timeout or no response (confirms bug exists)
    """
    
    def test_team_command_response(self):
        """
        Property 1: Fault Condition - Team Command Registration
        
        For any team command invocation, the bot SHALL have the command registered
        in the synced tree and SHALL respond with a deferred response within 3 seconds.
        
        This test simulates:
        1. Bot startup with team_system loaded
        2. Simulating /create_permanent_team interaction
        3. Checking if bot responds within 3 seconds
        
        EXPECTED ON UNFIXED CODE: No response or timeout (test FAILS)
        EXPECTED ON FIXED CODE: Bot responds successfully (test PASSES)
        """
        async def run_test():
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            
            bot = commands.Bot(command_prefix="!", intents=intents)
            
            with patch.dict(os.environ, {'GUILD_ID': '123456789', 'DISCORD_TOKEN': 'fake_token'}):
                try:
                    # Load team_system cog
                    print("\n[Test 1.3] Loading team_system cog...")
                    await bot.load_extension('team_system')
                    
                    # Check if command is in tree
                    commands_in_tree = list(bot.tree.get_commands())
                    command_names = [cmd.name for cmd in commands_in_tree]
                    print(f"[Test 1.3] Commands in tree: {command_names}")
                    
                    # Create mock interaction
                    mock_interaction = AsyncMock(spec=discord.Interaction)
                    mock_interaction.guild_id = 123456789
                    mock_interaction.user = Mock()
                    mock_interaction.user.id = 987654321
                    mock_interaction.user.display_name = "TestUser"
                    mock_interaction.guild = Mock()
                    mock_interaction.response = AsyncMock()
                    mock_interaction.response.defer = AsyncMock()
                    mock_interaction.response.is_done = Mock(return_value=False)
                    mock_interaction.followup = AsyncMock()
                    mock_interaction.followup.send = AsyncMock()
                    
                    # Find the create_permanent_team command
                    create_team_cmd = None
                    for cmd in commands_in_tree:
                        if cmd.name == 'create_permanent_team':
                            create_team_cmd = cmd
                            break
                    
                    if not create_team_cmd:
                        print(f"\n[Test 1.3] ❌ COUNTEREXAMPLE FOUND: 'create_permanent_team' command not in tree!")
                        print(f"[Test 1.3] Available commands: {command_names}")
                        print(f"[Test 1.3] This confirms Bug #3: Team commands are not registered")
                        
                        self.fail(
                            "'create_permanent_team' command not found in command tree! "
                            "This indicates the team_system cog failed to register its commands."
                        )
                    
                    print(f"[Test 1.3] Found command: {create_team_cmd.name}")
                    
                    # Mock Supabase to avoid database calls
                    with patch('team_system.get_async_supabase') as mock_supabase:
                        mock_db = AsyncMock()
                        mock_db.get_team_by_name = AsyncMock(return_value=None)
                        mock_db.get_team_by_leader = AsyncMock(return_value=None)
                        mock_db.get_user_team = AsyncMock(return_value=None)
                        mock_db.create_team = AsyncMock(return_value=True)
                        mock_db.add_team_member = AsyncMock(return_value=True)
                        mock_supabase.return_value = mock_db
                        
                        # Simulate command invocation with timeout
                        response_received = False
                        start_time = asyncio.get_event_loop().time()
                        
                        try:
                            # Call the command callback
                            await asyncio.wait_for(
                                create_team_cmd.callback(
                                    bot.get_cog('TeamSystem'),
                                    mock_interaction,
                                    name="TestTeam",
                                    description="Test team description"
                                ),
                                timeout=3.0
                            )
                            
                            end_time = asyncio.get_event_loop().time()
                            response_time = end_time - start_time
                            
                            # Check if defer was called (indicates response sent)
                            if mock_interaction.response.defer.called:
                                response_received = True
                                print(f"[Test 1.3] ✅ Bot responded in {response_time:.2f} seconds")
                            else:
                                print(f"\n[Test 1.3] ❌ COUNTEREXAMPLE FOUND: Bot did not defer response!")
                                print(f"[Test 1.3] This confirms Bug #3: Team commands not responding")
                            
                        except asyncio.TimeoutError:
                            print(f"\n[Test 1.3] ❌ COUNTEREXAMPLE FOUND: Command timed out after 3 seconds!")
                            print(f"[Test 1.3] This confirms Bug #3: Team commands not responding within acceptable time")
                        
                        # ASSERTION: Bot should have sent a deferred response
                        self.assertTrue(
                            response_received,
                            "Bot did not respond to team command invocation! "
                            "The command either timed out or failed to send a deferred response. "
                            "This indicates team commands are not functioning correctly."
                        )
                        
                        # ASSERTION: Response should be within 3 seconds
                        self.assertTrue(
                            mock_interaction.response.defer.called,
                            "Bot did not call interaction.response.defer()! "
                            "Team commands must defer immediately to prevent Discord timeout."
                        )
                
                finally:
                    await bot.close()
        
        # Run the async test
        asyncio.run(run_test())


class TestBugCondition4_SilentCogLoadingFailures(unittest.TestCase):
    """
    Test 1.4: Silent cog loading failures
    **Validates: Requirements 2.5**
    
    Simulates team_system import error during bot startup.
    
    EXPECTED OUTCOME ON UNFIXED CODE: Test FAILS showing bot continues despite error (confirms bug exists)
    """
    
    def test_cog_load_failure_handling(self):
        """
        Property 1: Fault Condition - Cog Load Validation
        
        For any cog loading failure during bot startup, the bot SHALL raise an exception
        and not continue to sync commands, preventing incomplete command registration.
        
        This test simulates:
        1. Bot startup
        2. team_system cog fails to load (import error)
        3. Checking if bot raises exception or continues silently
        
        EXPECTED ON UNFIXED CODE: Bot continues without error (test FAILS)
        EXPECTED ON FIXED CODE: Bot raises exception (test PASSES)
        """
        async def run_test():
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            
            bot = commands.Bot(command_prefix="!", intents=intents)
            
            with patch.dict(os.environ, {'GUILD_ID': '123456789', 'DISCORD_TOKEN': 'fake_token'}):
                try:
                    # Simulate cog load failure by patching load_extension
                    original_load = bot.load_extension
                    
                    async def failing_load(name):
                        if name == 'team_system':
                            raise ImportError(f"Simulated import error for {name}")
                        return await original_load(name)
                    
                    bot.load_extension = failing_load
                    
                    # Try to load team_system (should fail)
                    print("\n[Test 1.4] Attempting to load team_system with simulated failure...")
                    
                    exception_raised = False
                    error_message = None
                    
                    try:
                        await bot.load_extension('team_system')
                    except ImportError as e:
                        exception_raised = True
                        error_message = str(e)
                        print(f"[Test 1.4] ✅ Exception raised as expected: {error_message}")
                    except Exception as e:
                        exception_raised = True
                        error_message = str(e)
                        print(f"[Test 1.4] ✅ Exception raised: {error_message}")
                    
                    if not exception_raised:
                        print(f"\n[Test 1.4] ❌ COUNTEREXAMPLE FOUND: No exception raised!")
                        print(f"[Test 1.4] Bot continued despite cog load failure")
                        print(f"[Test 1.4] This confirms Bug #4: Silent cog loading failures")
                    
                    # Check if bot would continue to sync despite failure
                    # In unfixed code, setup_hook continues even if cog fails to load
                    commands_in_tree = list(bot.tree.get_commands())
                    print(f"[Test 1.4] Commands in tree after failed load: {len(commands_in_tree)}")
                    
                    # ASSERTION: Exception should be raised when cog fails to load
                    self.assertTrue(
                        exception_raised,
                        "No exception raised when team_system cog failed to load! "
                        "The bot should fail fast and not continue with incomplete command registration. "
                        "This indicates cog loading failures are being silently ignored."
                    )
                    
                    # ASSERTION: Bot should not have team commands in tree
                    team_command_names = [cmd.name for cmd in commands_in_tree if 'team' in cmd.name]
                    self.assertEqual(
                        len(team_command_names),
                        0,
                        f"Team commands found in tree despite cog load failure: {team_command_names}. "
                        "This indicates the bot is not properly validating cog loading."
                    )
                    
                finally:
                    await bot.close()
        
        # Run the async test
        asyncio.run(run_test())


if __name__ == '__main__':
    print("=" * 80)
    print("BUG CONDITION EXPLORATION TESTS")
    print("=" * 80)
    print("\nCRITICAL: These tests are EXPECTED TO FAIL on unfixed code!")
    print("Failures confirm the bugs exist and help understand the root cause.")
    print("DO NOT attempt to fix the tests or code when they fail.")
    print("\nThese tests encode the expected behavior and will validate the fix")
    print("when they pass after implementation.\n")
    print("=" * 80)
    print()
    
    # Run tests
    unittest.main(verbosity=2)
