#!/usr/bin/env python3
"""
Create GitHub repository and push Kwork AI Bot code
"""

import subprocess
import sys
import json
import urllib.request

# Get GitHub token
github_token = None

try:
    with open('/root/.openclaw/secret/github.env', 'r') as f:
        for line in f:
            if line.startswith('GITHUB_TOKEN='):
                github_token = line.split('=', 1)[1].strip()
                break
except:
    print("❌ GITHUB_TOKEN not found")
    print("Create token at: https://github.com/settings/tokens")
    sys.exit(1)

print("🔑 GitHub token found")
print(f"Token: {github_token[:10]}...")

# Repository details
repo_name = "kwork-ai-bot"
owner = "Egorov3008"

# Create repository
api_url = "https://api.github.com/user/repos"

payload = {
    "name": repo_name,
    "private": False,
    "description": "Telegram bot for monitoring Kwork freelance orders with AI-generated responses",
    "homepage": "https://github.com/Egorov3008/kwork-ai-bot",
    "auto_init": True
}

data = json.dumps(payload).encode('utf-8')

req = urllib.request.Request(api_url, data=data)
req.add_header('Authorization', f'token {github_token}')
req.add_header('Content-Type', 'application/json')

print(f"\n📦 Creating repository {repo_name}...")

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print(f"✅ Repository created!")
        print(f"   Name: {result['name']}")
        print(f"   URL: {result['html_url']}")
        print(f"   Private: {result['private']}")
except urllib.error.HTTPError as e:
    if e.code == 422:
        print("⚠️ Repository already exists")
    else:
        print(f"❌ Error creating repo: {e}")
        sys.exit(1)

# Add remote and push
print(f"\n🔄 Adding remote origin...")
subprocess.run(
    f"git remote add origin https://{github_token}@github.com/{owner}/{repo_name}.git",
    shell=True,
    cwd="/root/.openclaw/workspace/kwork-ai-bot"
)

print(f"📤 Pushing to GitHub...")
subprocess.run(f"git branch -M main", shell=True, cwd="/root/.openclaw/workspace/kwork-ai-bot")
subprocess.run(f"git push -u origin main", shell=True, cwd="/root/.openclaw/workspace/kwork-ai-bot")

print("\n" + "="*70)
print("✅ SUCCESS!")
print("="*70)
print(f"Repository: https://github.com/{owner}/{repo_name}")
print("="*70)
