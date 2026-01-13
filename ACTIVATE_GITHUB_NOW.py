#!/usr/bin/env python3
"""
ACTIVATE GITHUB PAGES - JETZT SOFORT
User: "nie nur ankündigen, durchführen"

Activates GitHub Pages for docs/index.html (Dashboard)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from EXTERNAL_ACTIONS import ExternalActionsAPI

def activate_github_pages():
    """Enable GitHub Pages immediately"""
    
    api = ExternalActionsAPI()
    
    if not api.credentials["github_token"]:
        print("❌ GITHUB_TOKEN not set")
        return False
    
    print("\n" + "="*80)
    print("ACTIVATING GITHUB PAGES - JETZT SOFORT")
    print("="*80 + "\n")
    
    # GitHub Pages API endpoint
    url = f"https://api.github.com/repos/{api.credentials['github_repo']}/pages"
    headers = {
        "Authorization": f"token {api.credentials['github_token']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if already enabled
    import requests
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            pages_info = response.json()
            print(f"✅ GitHub Pages already active!")
            print(f"   URL: {pages_info['html_url']}")
            print(f"   Source: {pages_info['source']['branch']} / {pages_info['source']['path']}")
            return True
            
        elif response.status_code == 404:
            print("📄 GitHub Pages not yet enabled. Enabling now...")
            
            # Enable GitHub Pages (source: main branch, /docs folder)
            data = {
                "source": {
                    "branch": "main",
                    "path": "/docs"
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                pages_info = response.json()
                print(f"✅ GitHub Pages ACTIVATED!")
                print(f"   URL: {pages_info['html_url']}")
                print(f"   Building... (may take 1-2 minutes)")
                
                # Update pages settings (enable HTTPS)
                requests.put(url, headers=headers, json={"https_enforced": True})
                
                return True
            else:
                print(f"❌ Failed to enable Pages: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def enable_github_features():
    """Enable Issues, Discussions, Projects"""
    
    api = ExternalActionsAPI()
    
    if not api.credentials["github_token"]:
        print("❌ GITHUB_TOKEN not set")
        return False
    
    print("\n" + "="*80)
    print("ENABLING GITHUB FEATURES")
    print("="*80 + "\n")
    
    # Repository settings API
    url = f"https://api.github.com/repos/{api.credentials['github_repo']}"
    headers = {
        "Authorization": f"token {api.credentials['github_token']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Enable features
    data = {
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }
    
    import requests
    
    try:
        response = requests.patch(url, headers=headers, json=data)
        
        if response.status_code == 200:
            print("✅ GitHub Issues: ENABLED")
            print("✅ GitHub Projects: ENABLED")
            print("✅ GitHub Wiki: ENABLED")
            
            # Note: Discussions must be enabled via web UI or GraphQL
            print("⚠️  GitHub Discussions: Enable manually at:")
            print(f"   https://github.com/{api.credentials['github_repo']}/settings")
            print("   → Features → Discussions → Set up discussions")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 EXECUTING IMMEDIATELY - NO ANNOUNCEMENTS\n")
    
    # Execute now
    activate_github_pages()
    enable_github_features()
    
    print("\n" + "="*80)
    print("✅ ACTIONS EXECUTED")
    print("="*80)
    print("\nNext: Run CREATE_ISSUES_NOW.py to populate issues")
