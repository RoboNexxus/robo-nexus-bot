"""
Quick setup script to configure GitHub organization integration
Run this to verify your GitHub token and organization settings
"""
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def check_github_config():
    """Check GitHub configuration and test token"""
    print("🔍 Checking GitHub Configuration...\n")
    
    # Check environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    github_owner = os.getenv('GITHUB_OWNER', 'robo-nexus')
    
    print(f"📋 Configuration:")
    print(f"   GITHUB_OWNER: {github_owner}")
    print(f"   GITHUB_TOKEN: {'✅ Set' if github_token else '❌ Not set'}")
    
    if not github_token:
        print("\n❌ GITHUB_TOKEN not found!")
        print("\n📝 To fix this:")
        print("   1. Go to Replit Secrets (lock icon)")
        print("   2. Add: GITHUB_TOKEN=your_token_here")
        print("   3. Add: GITHUB_OWNER=robo-nexus")
        print("\n💡 See GITHUB_ORG_SETUP.md for detailed instructions")
        return False
    
    # Test token with GitHub API
    print(f"\n🔐 Testing token with GitHub API...")
    
    try:
        # Test 1: Check user authentication
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ Token valid for user: {user_data['login']}")
        else:
            print(f"   ❌ Token authentication failed: {response.status_code}")
            return False
        
        # Test 2: Check organization access
        print(f"\n🏢 Testing organization access...")
        
        repositories = ['robo-nexus-bot', 'Robo-Nexus-Website-Dev']
        
        for repo in repositories:
            url = f"https://api.github.com/repos/{github_owner}/{repo}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                repo_data = response.json()
                print(f"   ✅ {repo}: Accessible")
                print(f"      - Full name: {repo_data['full_name']}")
                print(f"      - Private: {repo_data['private']}")
                print(f"      - Stars: {repo_data['stargazers_count']}")
            elif response.status_code == 404:
                print(f"   ❌ {repo}: Not found or no access")
                print(f"      - Check if repository exists at: https://github.com/{github_owner}/{repo}")
                print(f"      - Verify token has organization access")
            else:
                print(f"   ❌ {repo}: Error {response.status_code}")
        
        # Test 3: Check rate limit
        print(f"\n📊 Checking API rate limit...")
        response = requests.get('https://api.github.com/rate_limit', headers=headers, timeout=10)
        
        if response.status_code == 200:
            rate_data = response.json()
            core = rate_data['rate']
            print(f"   ✅ Rate limit: {core['remaining']}/{core['limit']} remaining")
            print(f"   ⏰ Resets at: {core['reset']}")
        
        print("\n✅ GitHub configuration is working correctly!")
        print("\n🚀 Next steps:")
        print("   1. Restart your bot to apply changes")
        print("   2. Test with /repo_list command in Discord")
        print("   3. Try /recent_commits to see organization commits")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing GitHub API: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Robo Nexus Bot - GitHub Organization Setup")
    print("=" * 60)
    print()
    
    success = check_github_config()
    
    print()
    print("=" * 60)
    
    if success:
        print("✅ Setup complete! Your bot is ready to use GitHub integration.")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        print("📖 Read GITHUB_ORG_SETUP.md for detailed instructions.")
    
    print("=" * 60)
