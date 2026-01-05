#!/usr/bin/env python3
"""
Automatisches Ausführen des OrionKernel mit Meta-State Trigger
"""
import subprocess
import time
import sys

def run_with_trigger():
    print("🚀 Starte OrionKernel mit automatischem Meta-State Trigger...\n")
    
    # Starte den Kernel als Subprozess
    process = subprocess.Popen(
        [sys.executable, "-X", "utf8", "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    # Warte bis der Kernel bereit ist
    print("⏳ Warte auf Kernel-Initialisierung...\n")
    time.sleep(3)
    
    # Sende den Meta-State Trigger
    print("✨ Aktiviere Meta-State Trigger: ⊘∞⧈∞⊘\n")
    process.stdin.write("⊘∞⧈∞⊘\n")
    process.stdin.flush()
    time.sleep(2)
    
    # Sende status Befehl
    print("📊 Prüfe Status...\n")
    process.stdin.write("status\n")
    process.stdin.flush()
    time.sleep(2)
    
    # Sende validate Befehl
    print("✅ Führe Validierung durch...\n")
    process.stdin.write("validate\n")
    process.stdin.flush()
    time.sleep(2)
    
    # Sende history Befehl
    print("📜 Zeige History...\n")
    process.stdin.write("history\n")
    process.stdin.flush()
    time.sleep(3)
    
    # Lese die Ausgabe
    print("=" * 70)
    print("KERNEL OUTPUT:")
    print("=" * 70 + "\n")
    
    try:
        # Lese für 10 Sekunden die Ausgabe
        start_time = time.time()
        while time.time() - start_time < 10:
            line = process.stdout.readline()
            if line:
                print(line, end='')
            else:
                break
    except KeyboardInterrupt:
        print("\n\n⚠️  Unterbrochen durch Benutzer")
    
    # Beende den Prozess sauber
    print("\n\n🛑 Beende Kernel...")
    process.stdin.write("exit\n")
    process.stdin.flush()
    time.sleep(1)
    
    if process.poll() is None:
        process.terminate()
        process.wait(timeout=5)
    
    print("✅ Fertig!")

if __name__ == "__main__":
    run_with_trigger()
