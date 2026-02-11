# GitHub Organization Token Setup Guide

## Overview
This guide explains how to configure the bot to use the Robo Nexus organization's GitHub repositories instead of your personal account.

---

## Step 1: Add Environment Variables

You need to add TWO environment variables to your bot's Replit Secrets:

### On Replit:
1. Click the **"Secrets"** tab (lock icon) in the left sidebar
2. Add these two secrets:

```
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_OWNER=robo-nexus
```

**Note:** Your GitHub token should already be added to Replit Secrets. If not, follow Step 3 below to generate one.

---

## Step 2: Understanding the Token

### What is this token?
- **Type:** GitHub Personal Access Token (PAT) with organization access
- **Owner:** Your GitHub account (AtharvM02222)
- **Access:** Robo Nexus organization repositories
- **Permissions:** Read commits, create issues, view repository stats

### Token Format:
```
github_pat_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

⚠️ **IMPORTANT:** Keep this token secret! Never commit it to GitHub or share it publicly. It should only be stored in Replit Secrets.

---

## Step 3: How to Generate a New Token (If Needed)

If you need to create a new token or this one expires:

1. **Go to GitHub Settings:**
   - Visit: https://github.com/settings/tokens
   - Or: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token (Classic):**
   - Click "Generate new token (classic)"
   - Give it a name: "Robo Nexus Bot"
   - Set expiration: 90 days or No expiration (for production)

3. **Select Permissions (Scopes):**
   - ✅ `repo` - Full control of private repositories
     - ✅ `repo:status` - Access commit status
     - ✅ `repo_deployment` - Access deployment status
     - ✅ `public_repo` - Access public repositories
   - ✅ `read:org` - Read org and team membership
   - ✅ `write:discussion` - Read and write team discussions

4. **Generate and Copy:**
   - Click "Generate token"
   - **COPY THE TOKEN IMMEDIATELY** - You won't see it again!
   - Save it to your secrets/environment variables

5. **Authorize for Organization:**
   - After creating the token, you may need to authorize it for the Robo Nexus organization
   - Go to: https://github.com/settings/tokens
   - Click on your token
   - Under "Organization access", click "Configure SSO"
   - Authorize for "robo-nexus" organization

---

## Step 4: Verify Configuration

After adding the secrets and restarting the bot:

### Test Commands in Discord:

1. **Check Repository List:**
   ```
   /repo_list
   ```
   Should show:
   - Owner: robo-nexus ✅
   - Token: ✅ Configured
   - Monitoring: ✅ Active

2. **View Recent Commits:**
   ```
   /recent_commits repository:robo-nexus-bot
   ```
   Should show commits from the organization repository

3. **Check Repository Stats:**
   ```
   /repo_stats repository:robo-nexus-bot
   ```
   Should show stats for robo-nexus/robo-nexus-bot

---

## Step 5: What Changed in the Code

### Before (Personal Account):
```python
self.repo_owner = "AtharvM02222"  # Your personal account
```

### After (Organization):
```python
self.repo_owner = os.getenv('GITHUB_OWNER', 'robo-nexus')  # Organization
```

Now the bot will:
- ✅ Monitor commits from `robo-nexus/robo-nexus-bot`
- ✅ Monitor commits from `robo-nexus/Robo-Nexus-Website-Dev`
- ✅ Create issues in organization repositories
- ✅ Show organization repository stats

---

## Features Enabled with Token

### 1. Automatic Commit Notifications
- Bot checks for new commits every 5 minutes
- Sends notifications to dev channel
- Shows commit message, author, changes, and time

### 2. Create GitHub Issues from Discord
```
/create_issue repository:robo-nexus-bot title:"Bug fix needed" description:"Description here" priority:high
```

### 3. View Recent Commits
```
/recent_commits repository:robo-nexus-bot count:5
```

### 4. Repository Statistics
```
/repo_stats repository:robo-nexus-bot
```

---

## Troubleshooting

### Token Not Working?
1. **Check token is valid:**
   - Visit: https://github.com/settings/tokens
   - Verify token exists and hasn't expired

2. **Check organization access:**
   - Token must be authorized for "robo-nexus" organization
   - Configure SSO if required

3. **Check permissions:**
   - Token needs `repo` and `read:org` scopes minimum

### Commands Not Showing Organization Repos?
1. **Restart the bot** after adding secrets
2. **Check logs** for any GitHub API errors
3. **Verify GITHUB_OWNER** is set to "robo-nexus"

### 403 Forbidden Errors?
- Token doesn't have permission to access organization
- Need to authorize token for organization (SSO)
- Token may have expired

---

## Security Best Practices

1. ✅ **Store token in secrets/environment variables** - Never in code
2. ✅ **Use token with minimal required permissions**
3. ✅ **Set token expiration** - Regenerate periodically
4. ✅ **Revoke old tokens** - When creating new ones
5. ✅ **Monitor token usage** - Check GitHub settings regularly

---

## Quick Reference

### Environment Variables:
```
GITHUB_TOKEN=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
GITHUB_OWNER=robo-nexus
```

### Repository URLs:
- Bot: https://github.com/robo-nexus/robo-nexus-bot
- Website: https://github.com/robo-nexus/Robo-Nexus-Website-Dev

### Token Management:
- View tokens: https://github.com/settings/tokens
- Organization access: https://github.com/settings/tokens → Configure SSO

---

**Last Updated:** February 11, 2026
**Bot Version:** v3.0
