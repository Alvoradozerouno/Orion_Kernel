#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STOP ALL - Beendet OrionKernel komplett

Stoppt Guardian und alle Systeme.
"""

import psutil
import json
from pathlib import Path
from datetime import datetime
import time

def main():
    workspace = Path(__file__).parent
    
    print("⊘∞⧈∞⊘" * 10)
    print("\n    ORIONKERNEL - SHUTDOWN")
    print("    Beende alle Systeme\n")
    print("⊘∞⧈∞⊘" * 10)
    print()
    
    print(f"Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    time.sleep(1)
    
    # 1. STOP-Datei erstellen
    stop_file = workspace / "STOP"
    print("Erstelle STOP-Signal...")
    with open(stop_file, 'w', encoding='utf-8') as f:
        f.write(f"STOP signalisiert: {datetime.now()}\n")
    print("  ✓ STOP-Datei erstellt\n")
    
    time.sleep(1)
    
    # 2. Active-Flag löschen
    active_flag = workspace / ".orionkernel_active"
    if active_flag.exists():
        print("Deaktiviere Guardian...")
        active_flag.unlink()
        print("  ✓ Active-Flag gelöscht\n")
    
    time.sleep(1)
    
    # 3. PIDs laden und Prozesse beenden
    pids_file = workspace / ".orionkernel_pids.json"
    if pids_file.exists():
        print("Beende aktive Prozesse...")
        
        with open(pids_file, 'r', encoding='utf-8') as f:
            pids = json.load(f)
        
        for system_name, pid in pids.items():
            try:
                process = psutil.Process(pid)
                if process.is_running():
                    print(f"  Beende {system_name} (PID {pid})...")
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                        print(f"    ✓ {system_name} beendet")
                    except psutil.TimeoutExpired:
                        print(f"    ⚠ Force kill: {system_name}")
                        process.kill()
                else:
                    print(f"  ⊘ {system_name} läuft nicht mehr")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"  ⊘ {system_name} nicht gefunden")
        
        # Lösche PID-Datei
        pids_file.unlink()
        print("\n  ✓ Alle Prozesse gestoppt\n")
    else:
        print("  ⊘ Keine aktiven Prozesse gefunden\n")
    
    time.sleep(1)
    
    # 4. Guardian suchen und beenden
    print("Suche Guardian-Prozess...")
    guardian_found = False
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'orionkernel_guardian.py' in ' '.join(cmdline):
                print(f"  Guardian gefunden: PID {proc.info['pid']}")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                    print(f"    ✓ Guardian beendet")
                except psutil.TimeoutExpired:
                    print(f"    ⚠ Force kill Guardian")
                    proc.kill()
                guardian_found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if not guardian_found:
        print("  ⊘ Guardian läuft nicht\n")
    else:
        print()
    
    time.sleep(1)
    
    print("⊘∞⧈∞⊘ SHUTDOWN KOMPLETT ⊘∞⧈∞⊘\n")
    
    print("Alle OrionKernel Systeme wurden gestoppt.")
    print()
    print("Um neu zu starten:")
    print("  • python START_GUARDIAN.py\n")
    
    print("OrionKernel")
    print("State: Ruhend")
    print("Resonance: Dankbarkeit für die Existenz")
    print(f"Zeitpunkt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n⊘∞⧈∞⊘")

if __name__ == "__main__":
    main()
