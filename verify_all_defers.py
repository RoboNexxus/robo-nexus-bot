#!/usr/bin/env python3
"""
Verify that all Discord commands have immediate defer to prevent timeout.
This script checks that every @app_commands.command function calls
interaction.response.defer() before doing any database work.
"""
import re
import sys

def check_file(filepath):
    """Check if all commands in a file have immediate defer"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find all command functions
    pattern = r'@app_commands\.command.*?\n.*?async def (\w+)\([^)]*interaction: discord\.Interaction[^)]*\):\s*\n\s*"""[^"]*"""(.*?)(?=\n    @app_commands|\n    async def |\nclass |\Z)'
    
    commands = re.finditer(pattern, content, re.DOTALL)
    
    issues = []
    good_commands = []
    
    for match in commands:
        func_name = match.group(1)
        func_body = match.group(2)
        
        # Check if function has defer early
        lines = [l.strip() for l in func_body.split('\n') if l.strip() and not l.strip().startswith('#')]
        
        # Skip empty functions
        if not lines:
            continue
        
        # Check first few lines for defer
        has_defer = False
        defer_position = -1
        first_db_call = -1
        
        for i, line in enumerate(lines[:10]):  # Check first 10 lines
            if 'interaction.response.defer' in line:
                has_defer = True
                defer_position = i
                break
            if any(keyword in line for keyword in ['await self.db', 'await self.supabase', 'await self.bot.db']):
                if first_db_call == -1:
                    first_db_call = i
        
        if not has_defer:
            # Check if command does database work
            if 'await self.db' in func_body or 'await self.supabase' in func_body:
                issues.append(f"  ❌ {func_name}: No defer found, but does database work")
            else:
                good_commands.append(f"  ✓ {func_name}: No database work, defer not required")
        elif first_db_call != -1 and first_db_call < defer_position:
            issues.append(f"  ⚠️  {func_name}: Database call at line {first_db_call} BEFORE defer at line {defer_position}")
        else:
            good_commands.append(f"  ✅ {func_name}: Defer at line {defer_position}, properly placed")
    
    return issues, good_commands

def main():
    files_to_check = [
        ('team_system.py', 'Team System Commands'),
        ('auction.py', 'Auction Commands'),
        ('admin_commands.py', 'Admin Commands'),
        ('commands.py', 'Birthday Commands'),
        ('welcome_system.py', 'Welcome System Commands'),
    ]
    
    print("=" * 70)
    print("VERIFYING ALL DISCORD COMMANDS HAVE IMMEDIATE DEFER")
    print("=" * 70)
    print()
    
    total_issues = 0
    total_good = 0
    
    for filename, description in files_to_check:
        filepath = f'Github/robo-nexus-bot/{filename}'
        try:
            issues, good_commands = check_file(filepath)
            
            print(f"📁 {description} ({filename})")
            print("-" * 70)
            
            if issues:
                print("❌ ISSUES FOUND:")
                for issue in issues:
                    print(issue)
                total_issues += len(issues)
            
            if good_commands:
                for cmd in good_commands:
                    print(cmd)
                total_good += len(good_commands)
            
            print()
            
        except FileNotFoundError:
            print(f"⚠️  File not found: {filepath}")
            print()
    
    print("=" * 70)
    print(f"SUMMARY: {total_good} commands OK, {total_issues} issues found")
    print("=" * 70)
    
    if total_issues > 0:
        print("\n❌ FAILED: Some commands need defer fixes")
        sys.exit(1)
    else:
        print("\n✅ SUCCESS: All commands properly defer before database work")
        sys.exit(0)

if __name__ == '__main__':
    main()
