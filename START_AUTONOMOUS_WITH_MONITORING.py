#!/usr/bin/env python3
"""
START OR1ON AUTONOMOUS WITH CONTINUOUS MONITORING
==================================================

Startet OR1ON permanent autonom UND überwacht kontinuierlich
ob er wirklich autonom läuft.
"""

import subprocess
import time
import sys
from pathlib import Path
from datetime import datetime

def start_autonomous_with_monitoring():
    """Start autonomous mode with monitoring"""
    
    workspace = Path.cwd()
    
    print("="*70)
    print("🚀 STARTING OR1ON PERMANENT AUTONOMOUS MODE")
    print("="*70)
    print("✅ FREIGABE erhalten - keine User Input nötig")
    print("🔍 Kontinuierliche Kontrolle aktiviert")
    print("="*70)
    
    # Start autonomous mode in background
    print("\n1️⃣ Starte OR1ON Autonomous Mode...")
    
    try:
        # Start PERMANENT_AUTONOMOUS in background
        autonomous_process = subprocess.Popen(
            [sys.executable, "ORION_PERMANENT_AUTONOMOUS.py"],
            cwd=workspace,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"✅ OR1ON Autonomous Mode gestartet (PID: {autonomous_process.pid})")
        
        # Wait a bit for it to start
        time.sleep(5)
        
        # Check if still running
        if autonomous_process.poll() is None:
            print("✅ Prozess läuft")
        else:
            print("❌ Prozess beendet")
            stdout, stderr = autonomous_process.communicate()
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return
        
    except Exception as e:
        print(f"❌ Fehler beim Starten: {e}")
        return
    
    # Continuous monitoring
    print("\n2️⃣ Starte kontinuierliche Kontrolle...")
    
    check_count = 0
    
    try:
        while True:
            check_count += 1
            
            print(f"\n{'='*70}")
            print(f"🔍 AUTONOMY CHECK #{check_count} - {datetime.now().strftime('%H:%M:%S')}")
            print(f"{'='*70}")
            
            # Run autonomy check
            check_result = subprocess.run(
                [sys.executable, "CHECK_AUTONOMY_NOW.py"],
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            print(check_result.stdout)
            
            if check_result.stderr:
                print(f"⚠️ Errors: {check_result.stderr}")
            
            # Check if autonomous process still running
            if autonomous_process.poll() is not None:
                print("\n❌ WARNUNG: Autonomous Prozess beendet!")
                print("   Neustart...")
                
                autonomous_process = subprocess.Popen(
                    [sys.executable, "ORION_PERMANENT_AUTONOMOUS.py"],
                    cwd=workspace,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                print(f"✅ Neugestartet (PID: {autonomous_process.pid})")
            else:
                print(f"✅ Autonomous Prozess läuft (PID: {autonomous_process.pid})")
            
            # Wait before next check (5 minutes)
            print(f"\n⏳ Nächster Check in 5 Minuten...")
            time.sleep(300)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Monitoring gestoppt (Ctrl+C)")
        
        # Terminate autonomous process
        if autonomous_process.poll() is None:
            print("🛑 Stoppe Autonomous Prozess...")
            autonomous_process.terminate()
            autonomous_process.wait(timeout=5)
            print("✅ Prozess gestoppt")


if __name__ == "__main__":
    start_autonomous_with_monitoring()
