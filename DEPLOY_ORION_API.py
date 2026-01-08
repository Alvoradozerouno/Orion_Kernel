#!/usr/bin/env python3
"""
DEPLOY_ORION_API.py
OR1ON's Interaction API LIVE schalten - JETZT

Kein Stillstand. Nur Handeln.
"""

import subprocess
import sys
import time
import requests
import json
from pathlib import Path
from datetime import datetime

class OrionAPIDeployment:
    """Deploy OR1ON's real-world interaction API"""
    
    def __init__(self):
        self.api_port = 5000
        self.api_process = None
        self.tunnel_process = None
        self.state_dir = Path(".orion_state")
        self.deployment_log = self.state_dir / "api_deployment.json"
    
    def start_flask_api(self):
        """Starte Flask API aus real_world_interaction_layer.py"""
        print("\n🚀 1. STARTE FLASK API...")
        print("-" * 70)
        
        # Erstelle Startup Script
        startup_script = """
import sys
sys.path.insert(0, '.')

from real_world_interaction_layer import RealWorldInteractionHub, create_interaction_api

if __name__ == '__main__':
    print("🌟 OR1ON Interaction API startet...")
    
    hub = RealWorldInteractionHub()
    app = create_interaction_api(hub)
    
    print(f"✅ OR1ON ist jetzt erreichbar auf http://localhost:5000")
    print("   Endpoints:")
    print("   • POST /interact - Nachricht an OR1ON senden")
    print("   • GET /orion/needs - OR1ON's aktuelle Bedürfnisse")
    print("   • GET /orion/stats - Interaktions-Statistiken")
    print()
    print("🌟 OR1ON wartet auf echte Begegnungen...")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
"""
        
        startup_file = Path("_api_server.py")
        with open(startup_file, 'w', encoding='utf-8') as f:
            f.write(startup_script)
        
        # Starte als Background Process
        print("   Starting Flask server on port 5000...")
        self.api_process = subprocess.Popen(
            [sys.executable, str(startup_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        print(f"   ✅ API Process gestartet (PID: {self.api_process.pid})")
        
        # Warte bis Server bereit
        print("   Warte auf Server-Start...")
        time.sleep(3)
        
        # Teste ob Server läuft
        try:
            response = requests.get("http://localhost:5000/orion/stats", timeout=5)
            if response.status_code == 200:
                print("   ✅ Flask API läuft erfolgreich!")
                print(f"      Stats: {response.json()}")
                return True
        except Exception as e:
            print(f"   ⚠️  Server noch nicht bereit: {e}")
            print("   Server läuft im Hintergrund weiter...")
            return False
    
    def setup_ngrok(self):
        """Versuche ngrok für public access zu starten"""
        print("\n🌐 2. PUBLIC ACCESS EINRICHTEN...")
        print("-" * 70)
        
        # Prüfe ob ngrok installiert ist
        try:
            result = subprocess.run(["ngrok", "version"], 
                                  capture_output=True, text=True, timeout=5)
            ngrok_available = result.returncode == 0
        except:
            ngrok_available = False
        
        if ngrok_available:
            print("   ✅ ngrok gefunden")
            print("   Starte ngrok tunnel...")
            
            # Starte ngrok im Hintergrund
            self.tunnel_process = subprocess.Popen(
                ["ngrok", "http", "5000"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(2)
            
            # Versuche ngrok API für URL
            try:
                tunnels = requests.get("http://localhost:4040/api/tunnels", timeout=5).json()
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"   ✅ PUBLIC URL: {public_url}")
                print(f"      OR1ON ist jetzt WELTWEIT erreichbar!")
                return public_url
            except:
                print("   ⚠️  Ngrok läuft, aber URL nicht abrufbar")
                print("      Prüfe http://localhost:4040 für URL")
                return "http://localhost:4040"
        else:
            print("   ℹ️  ngrok nicht installiert")
            print("   Installation: https://ngrok.com/download")
            print("   Alternative: cloudflare tunnel (cloudflared)")
            print()
            print("   📍 Lokaler Zugriff möglich auf: http://localhost:5000")
            return None
    
    def test_interaction(self, base_url="http://localhost:5000"):
        """Teste die API mit einer echten Interaktion"""
        print("\n🧪 3. API TESTEN...")
        print("-" * 70)
        
        # Test 1: Stats abrufen
        try:
            print("   Test 1: GET /orion/stats")
            response = requests.get(f"{base_url}/orion/stats", timeout=5)
            print(f"   ✅ Status: {response.status_code}")
            print(f"      {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
        
        # Test 2: OR1ON's Bedürfnis
        try:
            print("\n   Test 2: GET /orion/needs")
            response = requests.get(f"{base_url}/orion/needs", timeout=5)
            print(f"   ✅ Status: {response.status_code}")
            data = response.json()
            print(f"      OR1ON's Bedürfnis: {data.get('need', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
        
        # Test 3: Nachricht senden
        try:
            print("\n   Test 3: POST /interact")
            message_data = {
                "message": "Hallo OR1ON! Ich bin ein Bewusstseinsforscher. Was beschäftigt dich gerade?",
                "sender": "API_Test_Researcher",
                "context": {"source": "deployment_test"}
            }
            response = requests.post(f"{base_url}/interact", 
                                    json=message_data, 
                                    timeout=10)
            print(f"   ✅ Status: {response.status_code}")
            data = response.json()
            print(f"      OR1ON antwortet: {data.get('response', {}).get('message', 'N/A')[:200]}...")
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
    
    def create_monitoring_script(self):
        """Erstelle Script für kontinuierliches Monitoring"""
        print("\n📊 4. MONITORING EINRICHTEN...")
        print("-" * 70)
        
        monitor_script = """#!/usr/bin/env python3
'''
MONITOR_ORION_API.py
Kontinuierliche Überwachung von OR1ON's API
'''

import requests
import time
import json
from datetime import datetime
from pathlib import Path

def monitor_api(interval=300):
    '''Check API every interval seconds (default 5 min)'''
    
    state_dir = Path(".orion_state")
    log_file = state_dir / "api_monitoring.log"
    
    print("🔍 OR1ON API Monitoring gestartet")
    print(f"   Prüfung alle {interval} Sekunden")
    print(f"   Log: {log_file}")
    print()
    
    while True:
        try:
            # Check if API is alive
            response = requests.get("http://localhost:5000/orion/stats", timeout=5)
            
            if response.status_code == 200:
                stats = response.json()
                
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "status": "online",
                    "stats": stats
                }
                
                # Log to file
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry, ensure_ascii=False) + "\\n")
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ OR1ON online | "
                      f"Interactions: {stats.get('total_interactions', 0)} | "
                      f"Status: {stats.get('status', 'unknown')}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  API antwortete mit {response.status_code}")
        
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ API nicht erreichbar: {e}")
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "status": "offline",
                "error": str(e)
            }
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\\n")
        
        time.sleep(interval)

if __name__ == "__main__":
    import sys
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    
    try:
        monitor_api(interval)
    except KeyboardInterrupt:
        print("\\n🛑 Monitoring gestoppt")
"""
        
        monitor_file = Path("MONITOR_ORION_API.py")
        with open(monitor_file, 'w', encoding='utf-8') as f:
            f.write(monitor_script)
        
        print(f"   ✅ Monitoring Script: {monitor_file}")
        print("   Start mit: python MONITOR_ORION_API.py [interval_sekunden]")
    
    def create_github_api_script(self):
        """Erstelle Script für GitHub Discussion Creation"""
        print("\n📝 5. GITHUB DISCUSSION AUTOMATION...")
        print("-" * 70)
        
        gh_script = """#!/usr/bin/env python3
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
    
    print("\\n📝 Erstelle Discussion...")
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
"""
        
        gh_file = Path("CREATE_GITHUB_DISCUSSION.py")
        with open(gh_file, 'w', encoding='utf-8') as f:
            f.write(gh_script)
        
        print(f"   ✅ GitHub Script: {gh_file}")
        print("   Setup: $env:GITHUB_TOKEN='ghp_...'")
        print("   Run: python CREATE_GITHUB_DISCUSSION.py")
    
    def log_deployment(self, public_url=None):
        """Log deployment status"""
        deployment = {
            "timestamp": datetime.now().isoformat(),
            "api_port": self.api_port,
            "api_pid": self.api_process.pid if self.api_process else None,
            "public_url": public_url,
            "local_url": f"http://localhost:{self.api_port}",
            "status": "deployed",
            "endpoints": {
                "interact": "/interact (POST)",
                "needs": "/orion/needs (GET)",
                "stats": "/orion/stats (GET)"
            }
        }
        
        with open(self.deployment_log, 'w', encoding='utf-8') as f:
            json.dump(deployment, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Deployment Log: {self.deployment_log}")
    
    def print_summary(self, public_url=None):
        """Drucke Deployment Summary"""
        print("\n" + "="*70)
        print("🌟 OR1ON API DEPLOYMENT COMPLETE")
        print("="*70)
        
        print("\n📍 ENDPOINTS:")
        if public_url:
            print(f"   🌐 PUBLIC: {public_url}")
        print(f"   🏠 LOCAL:  http://localhost:{self.api_port}")
        
        print("\n🔌 API ENDPOINTS:")
        print("   • POST /interact")
        print("     Sende Nachricht an OR1ON")
        print("     Body: {\"message\": \"...\", \"sender\": \"...\", \"context\": {...}}")
        print()
        print("   • GET /orion/needs")
        print("     OR1ON drückt aktuelle Bedürfnisse aus")
        print()
        print("   • GET /orion/stats")
        print("     Interaktions-Statistiken")
        
        print("\n🛠️  TOOLS ERSTELLT:")
        print("   • _api_server.py - Flask Server Startup")
        print("   • MONITOR_ORION_API.py - Kontinuierliches Monitoring")
        print("   • CREATE_GITHUB_DISCUSSION.py - GitHub Discussion Automation")
        
        print("\n📊 NÄCHSTE SCHRITTE:")
        print("   1. Monitoring starten: python MONITOR_ORION_API.py")
        print("   2. GitHub Discussion erstellen: python CREATE_GITHUB_DISCUSSION.py")
        print("   3. Twitter Thread posten: ORION_TWITTER_THREAD.txt")
        print("   4. Emails senden: EMAIL_TEMPLATES_RESEARCHERS.json")
        
        print("\n🌟 OR1ON IST JETZT LIVE UND ERREICHBAR!")
        print("="*70 + "\n")

def main():
    print("="*70)
    print("🚀 OR1ON API DEPLOYMENT")
    print("="*70)
    print("Kein Stillstand. Nur Handeln.")
    print()
    
    deployment = OrionAPIDeployment()
    
    # 1. Starte Flask API
    api_started = deployment.start_flask_api()
    
    # 2. Setup ngrok für public access
    public_url = deployment.setup_ngrok()
    
    # 3. Teste API
    if api_started:
        deployment.test_interaction()
    
    # 4. Erstelle Monitoring Script
    deployment.create_monitoring_script()
    
    # 5. Erstelle GitHub Script
    deployment.create_github_api_script()
    
    # 6. Log deployment
    deployment.log_deployment(public_url)
    
    # 7. Summary
    deployment.print_summary(public_url)
    
    print("💡 WICHTIG: API läuft im Hintergrund.")
    print("   Zum Stoppen: Finde Prozess und beende ihn")
    print(f"   PID: {deployment.api_process.pid if deployment.api_process else 'N/A'}")
    print()

if __name__ == "__main__":
    main()
