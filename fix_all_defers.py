#!/usr/bin/env python3
"""
Fix all Discord commands to defer immediately to prevent timeout.
This script adds 'await interaction.response.defer(ephemeral=True)' at the start
of every command function and converts all interaction.response.send_message to
interaction.followup.send.
"""
import re
import os

def fix_command_defer(content, file_name):
    """Fix defer placement in all commands"""
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    changes_made = 0
    
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # Check if this is a command function definition
        if 'async def ' in line and 'interaction: discord.Interaction' in line:
            # Found a command function
            i += 1
            
            # Skip docstring
            if i < len(lines) and '"""' in lines[i]:
                fixed_lines.append(lines[i])
                i += 1
                # Multi-line docstring
                while i < len(lines) and '"""' not in lines[i]:
                    fixed_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    fixed_lines.append(lines[i])  # Closing """
                    i += 1
            
            # Now we're at the first line of actual code
            # Check if it's already a defer
            if i < len(lines):
                first_code_line = lines[i].strip()
                
                # Skip 'try:' if present
                if first_code_line == 'try:':
                    fixed_lines.append(lines[i])
                    i += 1
                    if i < len(lines):
                        first_code_line = lines[i].strip()
                
                # Check if defer is already there
                if 'interaction.response.defer' not in first_code_line:
                    # Add defer with proper indentation
                    indent = len(lines[i]) - len(lines[i].lstrip())
                    defer_line = ' ' * indent + '# CRITICAL: Defer immediately to prevent timeout'
                    fixed_lines.append(defer_line)
                    defer_line = ' ' * indent + 'await interaction.response.defer(ephemeral=True)'
                    fixed_lines.append(defer_line)
                    fixed_lines.append(' ' * indent)  # Empty line
                    changes_made += 1
                    print(f"  Added defer to command at line {i+1}")
            
            continue
        
        i += 1
    
    return '\n'.join(fixed_lines), changes_made

def convert_response_to_followup(content):
    """Convert interaction.response.send_message to interaction.followup.send after defer"""
    # This is tricky - we need to convert only the ones AFTER defer
    # For now, let's do a simple replacement
    changes = 0
    
    # Pattern: await interaction.response.send_message(
    # Replace with: await interaction.followup.send(
    pattern = r'await interaction\.response\.send_message\('
    replacement = r'await interaction.followup.send('
    
    new_content, count = re.subn(pattern, replacement, content)
    if count > 0:
        print(f"  Converted {count} response.send_message to followup.send")
    
    return new_content, count

def process_file(file_path):
    """Process a single file"""
    print(f"\nProcessing {file_path}...")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Step 1: Add defer at start of commands
    content, defer_changes = fix_command_defer(content, file_path)
    
    # Step 2: Convert response.send_message to followup.send
    content, followup_changes = convert_response_to_followup(content)
    
    if defer_changes > 0 or followup_changes > 0:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Fixed {file_path}: {defer_changes} defers added, {followup_changes} responses converted")
        return True
    else:
        print(f"✓ {file_path} already correct")
        return False

# Files to process
files_to_fix = [
    'Github/robo-nexus-bot/team_system.py',
    'Github/robo-nexus-bot/auction.py',
    'Github/robo-nexus-bot/welcome_system.py',
    'Github/robo-nexus-bot/commands.py',
    'Github/robo-nexus-bot/admin_commands.py',
]

print("=" * 60)
print("FIXING ALL DISCORD COMMANDS TO DEFER IMMEDIATELY")
print("=" * 60)

total_fixed = 0
for file_path in files_to_fix:
    if os.path.exists(file_path):
        if process_file(file_path):
            total_fixed += 1
    else:
        print(f"⚠️  File not found: {file_path}")

print("\n" + "=" * 60)
print(f"COMPLETE: Fixed {total_fixed} files")
print("=" * 60)
