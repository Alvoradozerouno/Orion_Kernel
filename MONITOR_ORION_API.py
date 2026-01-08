#!/usr/bin/env python3
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
                    f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
                
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
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        time.sleep(interval)

if __name__ == "__main__":
    import sys
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    
    try:
        monitor_api(interval)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring gestoppt")
