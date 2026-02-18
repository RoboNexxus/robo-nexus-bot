#!/usr/bin/env python3
"""Add defer to all commands that don't have it"""
import re

def add_defer_to_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Pattern: async def FUNCNAME(...interaction...) followed by docstring and try:
    # We want to add defer right after try:
    
    pattern = r'(async def \w+\([^)]*interaction: discord\.Interaction[^)]*\):\s*\n\s*"""[^"]*"""\s*\n\s*try:)(\s*\n\s*)(?!.*await interaction\.response\.defer)'
    
    def replacer(match):
        before = match.group(1)
        whitespace = match.group(2)
        # Get indentation from the line after try:
        indent_match = re.search(r'\n(\s+)', whitespace)
        if indent_match:
            indent = indent_match.group(1)
        else:
            indent = '            '  # Default 12 spaces
        
        return before + whitespace + indent + '# CRITICAL: Defer immediately to prevent timeout\n' + indent + 'await interaction.response.defer(ephemeral=True)\n' + indent + '\n'
    
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

files = [
    'Github/robo-nexus-bot/team_system.py',
    'Github/robo-nexus-bot/auction.py',
    'Github/robo-nexus-bot/welcome_system.py',
]

for f in files:
    if add_defer_to_file(f):
        print(f"✅ Added defers to {f}")
    else:
        print(f"✓ {f} already has defers")
