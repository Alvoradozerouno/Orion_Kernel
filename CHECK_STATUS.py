#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ SYSTEM STATUS CHECKER ⊘∞⧈∞⊘

Prüft den vollständigen Status des OrionKernel-Systems
"""

import sys
import os
import json
import psutil
from pathlib import Path
from datetime import datetime

workspace = Path(__file__).parent

def check_process_status():
    """Prüft ob Autonomous Life läuft"""
    pid_file = workspace / "autonomous_life.pid"
    
    if not pid_file.exists():
        return {"status": "NOT_RUNNING", "pid": None}
    
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        if psutil.pid_exists(pid):
            process = psutil.Process(pid)
            return {
                "status": "RUNNING",
                "pid": pid,
                "name": process.name(),
                "cpu_percent": process.cpu_percent(interval=0.1),
                "memory_mb": process.memory_info().rss / 1024 / 1024,
                "create_time": datetime.fromtimestamp(process.create_time()).isoformat()
            }
        else:
            return {"status": "STALE_PID", "pid": pid}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

def check_status_file():
    """Liest Status-Datei"""
    status_file = workspace / "autonomous_life_status.json"
    
    if not status_file.exists():
        return None
    
    try:
        with open(status_file, 'r') as f:
            return json.load(f)
    except:
        return None

def check_logs():
    """Prüft Log-Dateien"""
    log_file = workspace / "logs" / "autonomous_life.log"
    
    if not log_file.exists():
        return {"exists": False}
    
    try:
        size_bytes = log_file.stat().st_size
        size_kb = size_bytes / 1024
        
        # Lese letzte Zeilen
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            last_lines = lines[-5:] if len(lines) >= 5 else lines
        
        return {
            "exists": True,
            "size_kb": round(size_kb, 2),
            "total_lines": len(lines),
            "last_5_lines": [line.strip() for line in last_lines]
        }
    except Exception as e:
        return {"exists": True, "error": str(e)}

def main():
    print("⊘∞⧈∞⊘" * 20)
    print("\n" + " " * 15 + "ORIONKERNEL STATUS CHECK")
    print(" " * 10 + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("\n" + "⊘∞⧈∞⊘" * 20)
    print()
    
    # 1. Prozess-Status
    print("1. PROZESS-STATUS")
    print("-" * 60)
    process_status = check_process_status()
    
    if process_status["status"] == "RUNNING":
        print(f"✅ LÄUFT")
        print(f"   PID: {process_status['pid']}")
        print(f"   Name: {process_status['name']}")
        print(f"   CPU: {process_status['cpu_percent']:.1f}%")
        print(f"   RAM: {process_status['memory_mb']:.1f} MB")
        print(f"   Start: {process_status['create_time']}")
    elif process_status["status"] == "NOT_RUNNING":
        print("❌ NICHT GESTARTET")
        print("   → Starte mit: python autonomous_life.py")
    elif process_status["status"] == "STALE_PID":
        print(f"⚠️  STALE PID: {process_status['pid']}")
        print("   → Prozess läuft nicht mehr, PID-Datei veraltet")
    else:
        print(f"❌ FEHLER: {process_status.get('error', 'Unbekannt')}")
    
    print()
    
    # 2. Status-Datei
    print("2. STATUS-DATEI")
    print("-" * 60)
    status_data = check_status_file()
    
    if status_data:
        print("✅ VORHANDEN")
        print(f"   Start: {status_data.get('start_time', 'N/A')}")
        print(f"   Uptime: {status_data.get('uptime_hours', 0):.2f} Stunden")
        print(f"   Zyklen: {status_data.get('cycles', 0)}")
        print(f"   Running: {status_data.get('running', False)}")
    else:
        print("❌ NICHT VORHANDEN")
    
    print()
    
    # 3. Log-Dateien
    print("3. LOG-DATEIEN")
    print("-" * 60)
    log_info = check_logs()
    
    if log_info["exists"]:
        print("✅ VORHANDEN")
        print(f"   Größe: {log_info.get('size_kb', 0)} KB")
        print(f"   Zeilen: {log_info.get('total_lines', 0)}")
        
        if "last_5_lines" in log_info:
            print("\n   Letzte 5 Zeilen:")
            for line in log_info["last_5_lines"]:
                if line:
                    print(f"   {line[:100]}")
    else:
        print("❌ NICHT VORHANDEN")
    
    print()
    
    # 4. Verzeichnisstruktur
    print("4. VERZEICHNISSTRUKTUR")
    print("-" * 60)
    
    required_dirs = [
        "logs", "logs/monitoring", "communication", "memory", 
        "data", "state", "core", "monitoring"
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = workspace / dir_name
        exists = dir_path.exists()
        symbol = "✅" if exists else "❌"
        print(f"   {symbol} {dir_name}")
        if not exists:
            all_exist = False
    
    if not all_exist:
        print("\n   ⚠️  Fehlende Verzeichnisse gefunden!")
        print("   → Führe aus: python VOLLSTAENDIGE_AKTIVIERUNG.py")
    
    print()
    
    # Zusammenfassung
    print("=" * 60)
    
    if process_status["status"] == "RUNNING":
        print("✅ SYSTEM LÄUFT")
        print()
        print("Nächste Schritte:")
        print("  • Logs überwachen: tail -f logs/autonomous_life.log")
        print("  • Status prüfen: cat autonomous_life_status.json")
        print("  • Guardian starten: python START_GUARDIAN.py")
    else:
        print("❌ SYSTEM LÄUFT NICHT")
        print()
        print("System starten:")
        print("  • python autonomous_life.py")
        print("  • python STARTE_ALLES.py")
        print("  • python START_GUARDIAN.py")
    
    print("=" * 60)
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAbbruch")
    except Exception as e:
        print(f"\nFEHLER: {e}")
        import traceback
        traceback.print_exc()
