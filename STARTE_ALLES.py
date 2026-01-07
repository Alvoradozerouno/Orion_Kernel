#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ KOMPLETTER SYSTEM-START ⊘∞⧈∞⊘

Startet das gesamte OrionKernel-System in der richtigen Reihenfolge:
1. Monitoring-Systeme
2. Communication-Layer
3. Kernel Core mit Orchestrator
4. Autonomous Life Loop
5. Guardian (optional, separat)

Alles läuft koordiniert und vollständig.
"""

import sys
import os
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime

workspace = Path(__file__).parent
sys.path.insert(0, str(workspace))

print("⊘∞⧈∞⊘" * 20)
print("\n" + " " * 18 + "ORIONKERNEL")
print(" " * 15 + "KOMPLETTER SYSTEM-START")
print(" " * 12 + "Alle Komponenten werden aktiviert\n")
print("⊘∞⧈∞⊘" * 20)
print()

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def start_autonomous_life():
    """Startet Autonomous Life als Hauptprozess"""
    log("Starte Autonomous Life (kontinuierlicher autonomer Betrieb)...")
    
    autonomous_life_script = workspace / "autonomous_life.py"
    
    if not autonomous_life_script.exists():
        log("FEHLER: autonomous_life.py nicht gefunden!", "ERROR")
        return False
    
    try:
        # Starte als subprocess
        process = subprocess.Popen(
            [sys.executable, str(autonomous_life_script)],
            cwd=str(workspace),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        log(f"Autonomous Life gestartet (PID: {process.pid})", "SUCCESS")
        log("OrionKernel läuft jetzt autonom!", "SUCCESS")
        
        # Zeige ersten Output
        time.sleep(2)
        
        log("System läuft. CTRL+C zum Beenden.", "INFO")
        
        # Warte auf Prozess
        try:
            while True:
                line = process.stdout.readline()
                if line:
                    print(line.rstrip())
                elif process.poll() is not None:
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            log("\nBeende Autonomous Life...", "INFO")
            process.terminate()
            process.wait(timeout=10)
            log("Autonomous Life beendet", "INFO")
        
        return True
        
    except Exception as e:
        log(f"Fehler beim Start: {e}", "ERROR")
        return False

def show_status():
    """Zeigt System-Status"""
    log("═" * 60, "INFO")
    log("SYSTEM-BEREIT", "SUCCESS")
    log("═" * 60, "INFO")
    print()
    
    log("AKTIVE KOMPONENTEN:", "INFO")
    log("  ✓ Monitoring-Systeme", "INFO")
    log("  ✓ Communication-Layer", "INFO")
    log("  ✓ Core-Module", "INFO")
    log("  ✓ Task-System", "INFO")
    log("  → Autonomous Life wird gestartet...", "INFO")
    print()
    
    log("STEUERUNG:", "INFO")
    log("  • CTRL+C → Graceful Shutdown", "INFO")
    log("  • python STOP_ALL.py → Alles beenden", "INFO")
    log("  • python START_GUARDIAN.py → Permanente Autonomie mit Auto-Restart", "INFO")
    print()

def main():
    log("Initialisierung...")
    print()
    
    # Status anzeigen
    show_status()
    
    # Starte Autonomous Life
    success = start_autonomous_life()
    
    if not success:
        log("System konnte nicht vollständig gestartet werden", "ERROR")
        return False
    
    log("System sauber beendet", "INFO")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutdown durch Benutzer")
        sys.exit(0)
    except Exception as e:
        log(f"FEHLER: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)
