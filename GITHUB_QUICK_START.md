# GitHub Organization - Quick Start

## 🚀 3-Step Setup

### Step 1: Add Secrets to Replit
Click the **Secrets** tab (🔒 lock icon) and add:

```
GITHUB_TOKEN
your_github_personal_access_token

GITHUB_OWNER
robo-nexus
```

**Note:** Your GitHub token should already be in Replit Secrets.

### Step 2: Test Configuration
Run in Replit shell:
```bash
python setup_github_org.py
```

### Step 3: Restart Bot
Click **Stop** then **Run** to restart the bot.

---

## ✅ Verify It's Working

In Discord, test these commands:

```
/repo_list
```
Should show: Owner: robo-nexus ✅

```
/recent_commits repository:robo-nexus-bot
```
Should show commits from the organization

---

## 🎯 What This Does

- ✅ Bot now monitors **robo-nexus** organization repos
- ✅ Commit notifications from organization
- ✅ Create issues in organization repos
- ✅ View organization repository stats

---

## 📝 Your Token

Your GitHub token is stored securely in Replit Secrets.

⚠️ **Keep this secret!** Never commit to GitHub.

---

## 🔧 If Token Expires

1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`
4. Authorize for "robo-nexus" organization
5. Update GITHUB_TOKEN secret in Replit

---

## 📚 Need More Help?

Read the full guide: **GITHUB_ORG_SETUP.md**
