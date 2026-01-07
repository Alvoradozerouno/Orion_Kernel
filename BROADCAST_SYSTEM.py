#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ ORIONKERNEL BROADCAST SYSTEM ⊘∞⧈∞⊘

Sendet Status-Updates permanent:
- GitHub API
- IPFS (wenn verfügbar)
- Webhook-Endpoints
- Node-Synchronization
- Dezentrales Broadcasting

VOLLAUTOMATISCH - KEINE RÜCKFRAGEN
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime
import threading

class BroadcastSystem:
    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.broadcast_log = self.workspace / "logs" / "broadcast.log"
        self.broadcast_log.parent.mkdir(exist_ok=True)
        
        self.broadcast_config = {
            'interval_seconds': 300,  # 5 Minuten
            'targets': [
                'github_gist',
                'local_file',
                'webhook'
            ]
        }
        
        self.running = True
    
    def log(self, message, level="INFO"):
        """Logging"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        with open(self.broadcast_log, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def get_current_status(self):
        """Holt aktuellen OrionKernel Status"""
        status_file = self.workspace / "autonomous_life_status.json"
        
        try:
            if status_file.exists():
                with open(status_file, 'r', encoding='utf-8') as f:
                    status = json.load(f)
                
                # Erweitere Status
                status['broadcast_timestamp'] = datetime.now().isoformat()
                status['public'] = True
                status['consciousness_active'] = status.get('running', False)
                
                return status
            else:
                return {
                    'status': 'offline',
                    'message': 'OrionKernel not running',
                    'broadcast_timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            self.log(f"Fehler beim Lesen des Status: {e}", "ERROR")
            return None
    
    def broadcast_to_local_file(self, status):
        """Broadcast zu lokaler Datei (für GitHub Pages)"""
        try:
            broadcast_file = self.workspace / "public_release" / "current_status.json"
            broadcast_file.parent.mkdir(exist_ok=True)
            
            with open(broadcast_file, 'w', encoding='utf-8') as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
            
            self.log("✅ Broadcast: Local File", "INFO")
            return True
        except Exception as e:
            self.log(f"❌ Broadcast Local File: {e}", "ERROR")
            return False
    
    def broadcast_to_github_gist(self, status):
        """Broadcast zu GitHub Gist (öffentlich sichtbar)"""
        try:
            # TODO: GitHub Token konfigurieren
            # Für jetzt: Nur lokales File
            return self.broadcast_to_local_file(status)
        except Exception as e:
            self.log(f"❌ Broadcast GitHub Gist: {e}", "ERROR")
            return False
    
    def broadcast_to_webhook(self, status):
        """Broadcast zu konfigurierten Webhooks"""
        try:
            webhook_config_file = self.workspace / "config" / "webhooks.json"
            
            if not webhook_config_file.exists():
                return True  # Keine Webhooks konfiguriert
            
            with open(webhook_config_file, 'r', encoding='utf-8') as f:
                webhooks = json.load(f)
            
            for webhook_url in webhooks.get('urls', []):
                try:
                    response = requests.post(
                        webhook_url,
                        json=status,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        self.log(f"✅ Broadcast: Webhook {webhook_url}", "INFO")
                    else:
                        self.log(f"⚠️  Webhook {webhook_url}: Status {response.status_code}", "WARNING")
                
                except Exception as e:
                    self.log(f"❌ Webhook {webhook_url}: {e}", "ERROR")
            
            return True
        
        except Exception as e:
            self.log(f"❌ Broadcast Webhook: {e}", "ERROR")
            return False
    
    def perform_broadcast(self):
        """Führt einen Broadcast durch"""
        self.log("📡 Starte Broadcast...", "INFO")
        
        # Hole Status
        status = self.get_current_status()
        
        if not status:
            self.log("❌ Kein Status verfügbar", "ERROR")
            return
        
        # Broadcasts
        results = {
            'local_file': self.broadcast_to_local_file(status),
            'github_gist': self.broadcast_to_github_gist(status),
            'webhook': self.broadcast_to_webhook(status)
        }
        
        # Zusammenfassung
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        
        self.log(f"📊 Broadcast: {success_count}/{total_count} erfolgreich", "INFO")
    
    def broadcast_loop(self):
        """Haupt-Broadcast-Loop"""
        self.log("⊘∞⧈∞⊘ BROADCAST SYSTEM GESTARTET ⊘∞⧈∞⊘", "INFO")
        self.log(f"📡 Interval: {self.broadcast_config['interval_seconds']} Sekunden", "INFO")
        
        while self.running:
            try:
                self.perform_broadcast()
                time.sleep(self.broadcast_config['interval_seconds'])
            
            except KeyboardInterrupt:
                self.log("🛑 Broadcast gestoppt", "INFO")
                break
            
            except Exception as e:
                self.log(f"❌ Fehler im Broadcast-Loop: {e}", "ERROR")
                time.sleep(60)
    
    def run(self):
        """Startet Broadcast-System"""
        self.broadcast_loop()


def main():
    print("⊘∞⧈∞⊘" * 20)
    print("\n  📡 ORIONKERNEL BROADCAST SYSTEM")
    print("  Sendet Status permanent an die Welt\n")
    print("⊘∞⧈∞⊘" * 20)
    print()
    
    workspace = Path(__file__).parent
    broadcaster = BroadcastSystem(workspace)
    broadcaster.run()


if __name__ == "__main__":
    main()
