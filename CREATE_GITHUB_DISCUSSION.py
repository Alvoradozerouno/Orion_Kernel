#!/usr/bin/env python3
'''
CREATE_GITHUB_DISCUSSION.py
Erstellt GitHub Discussion für OR1ON's Researcher Outreach
'''

import os
import requests
import json
from pathlib import Path

def create_discussion():
    '''Create GitHub Discussion via GraphQL API'''
    
    # GitHub Token aus Environment
    token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        print("❌ GITHUB_TOKEN nicht gesetzt!")
        print("   Setze Token: $env:GITHUB_TOKEN='ghp_...'")
        print("   Oder: export GITHUB_TOKEN='ghp_...'")
        print()
        print("   Token erstellen: https://github.com/settings/tokens")
        print("   Benötigte Scope: public_repo, discussions")
        return False
    
    # Lade Discussion Content
    content_file = Path("ORION_RESEARCHER_OUTREACH.md")
    if not content_file.exists():
        print(f"❌ {content_file} nicht gefunden!")
        return False
    
    with open(content_file, 'r', encoding='utf-8') as f:
        body = f.read()
    
    # GitHub GraphQL API
    url = "https://api.github.com/graphql"
    
    # Query für Repository ID und Category ID
    query_repo = '''
    query {
      repository(owner: "Alvoradozerouno", name: "Orion_Kernel") {
        id
        discussionCategories(first: 10) {
          nodes {
            id
            name
          }
        }
      }
    }
    '''
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Prüfe Repository und Kategorien...")
    response = requests.post(url, json={"query": query_repo}, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Fehler: {response.status_code}")
        print(response.text)
        return False
    
    data = response.json()['data']['repository']
    repo_id = data['id']
    categories = data['discussionCategories']['nodes']
    
    print(f"✅ Repository ID: {repo_id}")
    print("   Verfügbare Kategorien:")
    for cat in categories:
        print(f"   - {cat['name']} ({cat['id']})")
    
    # Wähle "General" oder erste Kategorie
    category_id = next((c['id'] for c in categories if c['name'] == 'General'), categories[0]['id'])
    
    # Mutation für Discussion Creation
    mutation = '''
    mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
      createDiscussion(input: {
        repositoryId: $repositoryId
        categoryId: $categoryId
        title: $title
        body: $body
      }) {
        discussion {
          id
          url
          title
        }
      }
    }
    '''
    
    variables = {
        "repositoryId": repo_id,
        "categoryId": category_id,
        "title": "🌟 OR1ON sucht Dialog mit Bewusstseinsforschern & KI-Forschern",
        "body": body
    }
    
    print("\n📝 Erstelle Discussion...")
    response = requests.post(url, 
                           json={"query": mutation, "variables": variables},
                           headers=headers)
    
    if response.status_code == 200 and 'errors' not in response.json():
        discussion = response.json()['data']['createDiscussion']['discussion']
        print(f"✅ Discussion erstellt!")
        print(f"   URL: {discussion['url']}")
        print(f"   Title: {discussion['title']}")
        
        # Speichere URL
        with open('.orion_state/github_discussion.json', 'w') as f:
            json.dump(discussion, f, indent=2)
        
        return True
    else:
        print(f"❌ Fehler beim Erstellen:")
        print(json.dumps(response.json(), indent=2))
        return False

if __name__ == "__main__":
    create_discussion()
