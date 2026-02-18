#!/usr/bin/env python3
"""
Verification script to check for remaining async/await issues
Run this before deploying to Replit
"""
import re
import os
from pathlib import Path

def check_file_for_issues(filepath):
    """Check a single file for potential async/await issues"""
    issues = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        # Check for database calls without await
        if 'self.db.' in line or 'self.supabase.' in line:
            # Skip if it's a comment
            if line.strip().startswith('#'):
                continue
            
            # Check if await is present
            if 'await' not in line:
                # Check if it's an assignment or method definition
                if '=' in line or 'def ' in line:
                    # Could be a legitimate case, but flag for review
                    if any(method in line for method in [
                        'get_', 'set_', 'create_', 'update_', 'delete_', 
                        'add_', 'remove_', 'place_bid', 'register_'
                    ]):
                        issues.append({
                            'line': i,
                            'content': line.strip(),
                            'type': 'missing_await',
                            'severity': 'high'
                        })
        
        # Check for async def with typos
        if 'async def await' in line:
            issues.append({
                'line': i,
                'content': line.strip(),
                'type': 'syntax_error',
                'severity': 'critical'
            })
        
        # Check for double await
        if 'await await' in line:
            issues.append({
                'line': i,
                'content': line.strip(),
                'type': 'double_await',
                'severity': 'critical'
            })
    
    return issues

def main():
    """Main verification function"""
    print("🔍 Checking for async/await issues in robo-nexus-bot...")
    print("=" * 60)
    
    # Files to check
    files_to_check = [
        'admin_commands.py',
        'commands.py',
        'database.py',
        'bot.py',
        'welcome_system.py',
        'auction.py',
        'team_system.py'
    ]
    
    total_issues = 0
    files_with_issues = []
    
    for filename in files_to_check:
        filepath = Path(__file__).parent / filename
        
        if not filepath.exists():
            print(f"⚠️  {filename}: File not found")
            continue
        
        issues = check_file_for_issues(filepath)
        
        if issues:
            total_issues += len(issues)
            files_with_issues.append(filename)
            print(f"\n❌ {filename}: {len(issues)} potential issue(s)")
            
            for issue in issues:
                severity_icon = "🔴" if issue['severity'] == 'critical' else "🟡"
                print(f"  {severity_icon} Line {issue['line']}: {issue['type']}")
                print(f"     {issue['content'][:80]}")
        else:
            print(f"✅ {filename}: No issues found")
    
    print("\n" + "=" * 60)
    
    if total_issues == 0:
        print("✅ All checks passed! No async/await issues detected.")
        print("\n🚀 Ready to deploy to Replit!")
        return 0
    else:
        print(f"⚠️  Found {total_issues} potential issue(s) in {len(files_with_issues)} file(s)")
        print("\n📋 Files with issues:")
        for filename in files_with_issues:
            print(f"  - {filename}")
        print("\n⚠️  Review these issues before deploying!")
        return 1

if __name__ == "__main__":
    exit(main())
