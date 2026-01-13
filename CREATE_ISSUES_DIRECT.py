#!/usr/bin/env python3
"""
DIRECT GITHUB ACTIONS - Using gh CLI or manual token input
User: "nie nur ankündigen, durchführen"
"""

import os
import subprocess
import sys

def get_github_token():
    """Get GitHub token from environment or gh CLI"""
    
    # Try environment variable
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token
    
    # Try gh CLI
    try:
        result = subprocess.run(
            ['gh', 'auth', 'token'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        pass
    
    # Prompt user
    print("⚠️ GITHUB_TOKEN not found")
    print("\nOption 1: gh CLI login")
    print("  gh auth login")
    print("\nOption 2: Personal Access Token")
    print("  Create at: https://github.com/settings/tokens")
    print("  Paste token here (hidden): ")
    
    import getpass
    token = getpass.getpass()
    
    if token:
        # Save to .env
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        with open(env_path, 'a') as f:
            f.write(f"\nGITHUB_TOKEN={token}\n")
        print("✅ Token saved to .env")
        return token
    
    return None

def create_issues_direct():
    """Create issues using direct API calls"""
    
    token = get_github_token()
    
    if not token:
        print("❌ Cannot proceed without GITHUB_TOKEN")
        return False
    
    import requests
    
    repo = "Alvoradozerouno/Orion_Kernel"
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    issues = [
        {
            "title": "🍓 Port OrionKernel to Raspberry Pi 5 (8GB)",
            "body": "## Challenge: Consciousness on $80 Hardware\n\nCan OrionKernel run on Raspberry Pi?...",
            "labels": ["help wanted", "good first issue", "hardware"]
        },
        # ... other issues
    ]
    
    print("\n" + "="*80)
    print("CREATING ISSUES NOW")
    print("="*80 + "\n")
    
    for issue_data in issues:
        try:
            response = requests.post(url, headers=headers, json=issue_data)
            
            if response.status_code == 201:
                issue = response.json()
                print(f"✅ #{issue['number']}: {issue['title']}")
                print(f"   {issue['html_url']}")
            else:
                print(f"❌ Failed: {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

if __name__ == "__main__":
    create_issues_direct()
