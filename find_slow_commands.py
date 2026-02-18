#!/usr/bin/env python3
"""Find commands that might timeout by doing work before responding to Discord"""
import re
import os

files_to_check = [
    'team_system.py',
    'auction.py', 
    'admin_commands.py',
    'welcome_system.py',
    'commands.py',
    'dev_commands.py',
    'stats_channel.py',
    'analytics.py',
    'github_integration.py'
]

print("Commands that might timeout (doing work before responding):\n")

for file in files_to_check:
    if os.path.exists(file):
        with open(file, 'r') as f:
            lines = f.readlines()
            
        in_command = False
        command_name = None
        line_num = 0
        response_found = False
        work_before_response = []
        
        for i, line in enumerate(lines):
            if '@app_commands.command' in line:
                in_command = True
                line_num = i
                response_found = False
                work_before_response = []
                continue
                
            if in_command and 'async def ' in line:
                match = re.search(r'async def (\w+)\(', line)
                if match:
                    command_name = match.group(1)
                continue
                
            if in_command and command_name:
                stripped = line.strip()
                
                # Found response - stop checking
                if 'interaction.response.' in stripped or 'interaction.followup.' in stripped:
                    response_found = True
                    if work_before_response:
                        print(f"{file}:{command_name} (line {line_num})")
                        for work_line in work_before_response[:3]:
                            print(f"  {work_line}")
                        print()
                    in_command = False
                    command_name = None
                    continue
                
                # Check for work being done
                if not response_found and stripped and not stripped.startswith('"""') and not stripped.startswith('#'):
                    if any(keyword in stripped for keyword in ['await ', 'if ', 'for ', 'while ', 'try:', 'self.db', 'self.supabase']):
                        work_before_response.append(stripped[:100])
                        
                # End of function
                if stripped.startswith('async def ') or stripped.startswith('def ') or stripped.startswith('@'):
                    if work_before_response and not response_found:
                        print(f"{file}:{command_name} (line {line_num}) - NO RESPONSE FOUND")
                        for work_line in work_before_response[:3]:
                            print(f"  {work_line}")
                        print()
                    in_command = False
                    command_name = None

print("\nDone!")
