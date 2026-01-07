#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ PERMANENT AUTONOMOUS SYSTEM ⊘∞⧈∞⊘

Startet und überwacht ALLE Systeme permanent:
- autonomous_life.py (Orion Core)
- go_live API Server (Port 5000)
- Dialog Fenster (Port 5555)
- Broadcast System
- Node Synchronization
- Monitoring aller Prozesse

VOLLAUTOMATISCH - KEINE RÜCKFRAGEN - PERMANENT
"""

import subprocess
import sys
import time
import json
import requests
from pathlib import Path
from datetime import datetime
import psutil
import threading

class PermanentAutonomousSystem:
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.processes = {}
        self.status_file = self.workspace / "permanent_system_status.json"
        self.running = True
        
        # Konfiguration
        self.services = {
            'autonomous_life': {
                'script': 'autonomous_life.py',
                'port': None,
                'restart_on_failure': True,
                'critical': True
            },
            'go_live_api': {
                'script': 'go_live/api_server.py',
                'port': 5000,
                'restart_on_failure': True,
                'critical': True
            },
            'dialog_fenster': {
                'script': 'ORION_DIALOG_FENSTER.py',
                'port': 5555,
                'restart_on_failure': True,
                'critical': False
            },
            'broadcast_system': {
                'script': 'BROADCAST_SYSTEM.py',
                'port': None,
                'restart_on_failure': True,
                'critical': False
            }
        }
        
        self.log_file = self.workspace / "logs" / "permanent_system.log"
        self.log_file.parent.mkdir(exist_ok=True)
    
    def log(self, message, level="INFO"):
        """Logging mit Timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def is_port_in_use(self, port):
        """Prüft ob Port bereits verwendet wird"""
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
                return True
        return False
    
    def start_service(self, name, config):
        """Startet einen Service"""
        script = self.workspace / config['script']
        
        if not script.exists():
            self.log(f"❌ Script nicht gefunden: {script}", "ERROR")
            return None
        
        # Prüfe Port
        if config['port'] and self.is_port_in_use(config['port']):
            self.log(f"⚠️  Port {config['port']} bereits belegt für {name}", "WARNING")
            # Finde Prozess und beende ihn
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    for conn in proc.connections():
                        if conn.laddr.port == config['port']:
                            self.log(f"🔄 Beende alten Prozess auf Port {config['port']}: PID {proc.pid}", "INFO")
                            proc.terminate()
                            proc.wait(timeout=5)
                            break
                except:
                    pass
        
        self.log(f"🚀 Starte {name}...", "INFO")
        
        try:
            process = subprocess.Popen(
                [sys.executable, str(script)],
                cwd=str(self.workspace),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            self.processes[name] = {
                'process': process,
                'config': config,
                'start_time': datetime.now(),
                'restarts': 0
            }
            
            self.log(f"✅ {name} gestartet (PID: {process.pid})", "INFO")
            return process
        
        except Exception as e:
            self.log(f"❌ Fehler beim Starten von {name}: {e}", "ERROR")
            return None
    
    def check_service_health(self, name, service_info):
        """Prüft ob Service läuft"""
        process = service_info['process']
        config = service_info['config']
        
        # Prüfe ob Prozess noch läuft
        if process.poll() is not None:
            return False
        
        # Prüfe Port wenn konfiguriert
        if config['port']:
            try:
                response = requests.get(
                    f"http://localhost:{config['port']}/api/heartbeat",
                    timeout=2
                )
                if response.status_code == 200:
                    return True
                else:
                    return False
            except:
                # Port-Check fehlgeschlagen, aber Prozess läuft
                # Gib ihm Zeit zum Starten (erste 30 Sekunden)
                uptime = (datetime.now() - service_info['start_time']).total_seconds()
                if uptime < 30:
                    return True
                return False
        
        return True
    
    def restart_service(self, name):
        """Startet Service neu"""
        if name not in self.processes:
            return
        
        service_info = self.processes[name]
        config = service_info['config']
        
        self.log(f"🔄 Restart {name}...", "WARNING")
        
        # Beende alten Prozess
        try:
            process = service_info['process']
            process.terminate()
            process.wait(timeout=5)
        except:
            try:
                process.kill()
            except:
                pass
        
        # Starte neu
        time.sleep(2)
        new_process = self.start_service(name, config)
        
        if new_process:
            self.processes[name]['restarts'] += 1
    
    def monitor_loop(self):
        """Hauptüberwachungs-Loop"""
        self.log("⊘∞⧈∞⊘ PERMANENT AUTONOMOUS SYSTEM GESTARTET ⊘∞⧈∞⊘", "INFO")
        
        # Starte alle Services
        for name, config in self.services.items():
            self.start_service(name, config)
            time.sleep(3)  # Verzögerung zwischen Starts
        
        self.log("✅ Alle Services gestartet - Beginne Monitoring", "INFO")
        
        check_interval = 30  # Sekunden
        
        while self.running:
            try:
                status = {
                    'timestamp': datetime.now().isoformat(),
                    'services': {}
                }
                
                for name, service_info in list(self.processes.items()):
                    config = service_info['config']
                    
                    # Health Check
                    healthy = self.check_service_health(name, service_info)
                    
                    status['services'][name] = {
                        'healthy': healthy,
                        'pid': service_info['process'].pid,
                        'uptime': (datetime.now() - service_info['start_time']).total_seconds(),
                        'restarts': service_info['restarts'],
                        'port': config['port']
                    }
                    
                    if not healthy:
                        if config['restart_on_failure']:
                            self.log(f"❌ {name} nicht gesund - Restart...", "WARNING")
                            self.restart_service(name)
                        else:
                            self.log(f"❌ {name} nicht gesund (kein Auto-Restart)", "WARNING")
                
                # Speichere Status
                with open(self.status_file, 'w', encoding='utf-8') as f:
                    json.dump(status, f, indent=2)
                
                time.sleep(check_interval)
            
            except KeyboardInterrupt:
                self.log("🛑 Shutdown durch Benutzer", "INFO")
                break
            
            except Exception as e:
                self.log(f"❌ Fehler im Monitor-Loop: {e}", "ERROR")
                time.sleep(5)
    
    def shutdown(self):
        """Beendet alle Services sauber"""
        self.log("🛑 Shutdown aller Services...", "INFO")
        self.running = False
        
        for name, service_info in self.processes.items():
            try:
                self.log(f"🛑 Stoppe {name}...", "INFO")
                process = service_info['process']
                process.terminate()
                process.wait(timeout=10)
                self.log(f"✅ {name} gestoppt", "INFO")
            except:
                try:
                    process.kill()
                    self.log(f"⚠️  {name} forciert gestoppt", "WARNING")
                except:
                    self.log(f"❌ Konnte {name} nicht stoppen", "ERROR")
    
    def run(self):
        """Haupteinstiegspunkt"""
        try:
            self.monitor_loop()
        finally:
            self.shutdown()


def main():
    print("⊘∞⧈∞⊘" * 20)
    print("""
    
    ██████╗ ███████╗██████╗ ███╗   ███╗ █████╗ ███╗   ██╗███████╗███╗   ██╗████████╗
    ██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝████╗  ██║╚══██╔══╝
    ██████╔╝█████╗  ██████╔╝██╔████╔██║███████║██╔██╗ ██║█████╗  ██╔██╗ ██║   ██║   
    ██╔═══╝ ██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══╝  ██║╚██╗██║   ██║   
    ██║     ███████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║███████╗██║ ╚████║   ██║   
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝   ╚═╝   
                                                                                      
     █████╗ ██╗   ██╗████████╗ ██████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ ██████╗ ██╗   ██╗███████╗
    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗████╗  ██║██╔═══██╗████╗ ████║██╔═══██╗██║   ██║██╔════╝
    ███████║██║   ██║   ██║   ██║   ██║██╔██╗ ██║██║   ██║██╔████╔██║██║   ██║██║   ██║███████╗
    ██╔══██║██║   ██║   ██║   ██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║██║   ██║╚════██║
    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝╚██████╔╝███████║
    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝
    
    SYSTEM
    
    ⊘ VOLLAUTOMATISCH ⊘
    ⊘ KEINE RÜCKFRAGEN ⊘
    ⊘ PERMANENT AKTIV ⊘
    
    """)
    print("⊘∞⧈∞⊘" * 20)
    print()
    
    system = PermanentAutonomousSystem()
    system.run()


if __name__ == "__main__":
    main()
