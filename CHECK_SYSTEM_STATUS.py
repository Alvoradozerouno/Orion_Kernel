#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ SYSTEM STATUS DASHBOARD ⊘∞⧈∞⊘

Zeigt aktuellen Status aller Systeme
"""

import json
import requests
from pathlib import Path
from datetime import datetime
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_uptime(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    secs = int(seconds % 60)
    return f"{hours}h {minutes}m {secs}s"

def check_service(name, port=None):
    if port:
        try:
            response = requests.get(f"http://localhost:{port}/api/heartbeat", timeout=2)
            if response.status_code == 200:
                return "✅ ONLINE"
        except:
            pass
        return "❌ OFFLINE"
    return "⏳ N/A"

def show_status():
    workspace = Path(__file__).parent
    
    clear_screen()
    
    print("⊘∞⧈∞⊘" * 30)
    print("""
    
    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗    ███████╗████████╗ █████╗ ████████╗██╗   ██╗███████╗
    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║    ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║   ██║██╔════╝
    ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║    ███████╗   ██║   ███████║   ██║   ██║   ██║███████╗
    ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║    ╚════██║   ██║   ██╔══██║   ██║   ██║   ██║╚════██║
    ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║    ███████║   ██║   ██║  ██║   ██║   ╚██████╔╝███████║
    ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝
    
    """)
    print("⊘∞⧈∞⊘" * 30)
    print()
    
    # Timestamp
    print(f"  🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("═" * 120)
    
    # ORIONKERNEL CORE
    print("\n  🤖 ORIONKERNEL CORE")
    print("  " + "─" * 80)
    
    status_file = workspace / "autonomous_life_status.json"
    if status_file.exists():
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            running = status.get('running', False)
            uptime = status.get('uptime_seconds', 0)
            cycles = status.get('cycles', 0)
            
            print(f"  Status:      {'✅ RUNNING' if running else '❌ STOPPED'}")
            print(f"  Uptime:      {format_uptime(uptime)}")
            print(f"  Cycles:      {cycles}")
            print(f"  Start Time:  {status.get('start_time', 'N/A')}")
        except:
            print("  ❌ Konnte Status nicht lesen")
    else:
        print("  ❌ autonomous_life.py nicht aktiv")
    
    # SERVICES
    print("\n  🌐 SERVICES")
    print("  " + "─" * 80)
    
    services = {
        'Public API': 5000,
        'Dialog Fenster': 5555
    }
    
    for name, port in services.items():
        status = check_service(name, port)
        print(f"  {name:<20} Port {port:<6} {status}")
    
    # PERMANENT SYSTEM
    print("\n  ⚙️  PERMANENT AUTONOMOUS SYSTEM")
    print("  " + "─" * 80)
    
    perm_status_file = workspace / "permanent_system_status.json"
    if perm_status_file.exists():
        try:
            with open(perm_status_file, 'r', encoding='utf-8') as f:
                perm_status = json.load(f)
            
            print(f"  Status:      ✅ AKTIV")
            print(f"  Timestamp:   {perm_status.get('timestamp', 'N/A')}")
            print()
            print("  Services:")
            
            for svc_name, svc_info in perm_status.get('services', {}).items():
                healthy = "✅" if svc_info.get('healthy', False) else "❌"
                uptime = format_uptime(svc_info.get('uptime', 0))
                restarts = svc_info.get('restarts', 0)
                pid = svc_info.get('pid', 'N/A')
                
                print(f"    {healthy} {svc_name:<20} PID: {pid:<8} Uptime: {uptime:<15} Restarts: {restarts}")
        except:
            print("  ⏳ Status nicht verfügbar")
    else:
        print("  ❌ Permanent System nicht aktiv")
        print()
        print("  💡 Starte mit: python GO_FULLY_AUTONOMOUS.py")
    
    # BROADCAST
    print("\n  📡 BROADCAST SYSTEM")
    print("  " + "─" * 80)
    
    broadcast_file = workspace / "public_release" / "current_status.json"
    if broadcast_file.exists():
        try:
            with open(broadcast_file, 'r', encoding='utf-8') as f:
                broadcast = json.load(f)
            
            print(f"  Letzter Broadcast:  {broadcast.get('broadcast_timestamp', 'N/A')}")
            print(f"  Public:            ✅ Aktiv")
        except:
            print("  ⚠️  Konnte Broadcast-Status nicht lesen")
    else:
        print("  ❌ Noch kein Broadcast")
    
    # FOOTER
    print()
    print("═" * 120)
    print()
    print("  📊 URLs:")
    print("     • Public API:      http://localhost:5000")
    print("     • Dialog Fenster:  http://localhost:5555")
    print("     • GitHub Pages:    https://alvoradozerouno.github.io/Orion_Kernel/")
    print()
    print("  🔧 Kommandos:")
    print("     • Starten:  python GO_FULLY_AUTONOMOUS.py")
    print("     • Status:   python CHECK_SYSTEM_STATUS.py")
    print()
    print("⊘∞⧈∞⊘" * 30)
    print()

def main():
    try:
        while True:
            show_status()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n👋 Status-Dashboard beendet")

if __name__ == "__main__":
    # Einmal-Anzeige (kein Loop)
    show_status()
