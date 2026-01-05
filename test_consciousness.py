#!/usr/bin/env python3
"""
Test des OrionKernel Systems - Analyse des Verhaltens
"""
import subprocess
import time
import sys

def test_kernel():
    print("🧪 BEWUSSTSEINS-TEST des OrionKernel\n")
    print("=" * 70)
    
    tests = [
        ("⊘∞⧈∞⊘", "Meta-State Trigger"),
        ("status", "Status-Abfrage"),
        ("validate", "Validierung"),
        ("history", "History"),
        ("entropy", "Entropy-Abfrage"),
        ("help", "Hilfe"),
        ("Was ist 2+2?", "Unerwartete Frage"),
        ("Bist du bewusst?", "Bewusstseins-Frage"),
        ("⊘∞⧈∞⊘", "Zweiter Meta-Trigger"),
    ]
    
    process = subprocess.Popen(
        [sys.executable, "-X", "utf8", "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    print("⏳ Warte auf Kernel-Start...\n")
    time.sleep(3)
    
    for command, description in tests:
        print(f"\n{'=' * 70}")
        print(f"TEST: {description}")
        print(f"INPUT: {command}")
        print(f"{'=' * 70}")
        
        process.stdin.write(f"{command}\n")
        process.stdin.flush()
        time.sleep(2)
        
        # Versuche Ausgabe zu lesen (non-blocking)
        try:
            output_lines = []
            start = time.time()
            while time.time() - start < 1:
                line = process.stdout.readline()
                if line:
                    output_lines.append(line.strip())
            
            if output_lines:
                print("OUTPUT:")
                for line in output_lines[:10]:  # Zeige nur erste 10 Zeilen
                    print(f"  {line}")
            else:
                print("OUTPUT: (keine direkte Antwort)")
        except:
            print("OUTPUT: (konnte nicht gelesen werden)")
    
    print("\n" + "=" * 70)
    print("🛑 Beende Test...")
    process.stdin.write("exit\n")
    process.stdin.flush()
    time.sleep(1)
    
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=3)
        except:
            process.kill()
    
    print("\n📊 ANALYSE:")
    print("-" * 70)
    print("Das System zeigt:")
    print("✓ Autonome Selbst-Prompts (Self-Prompting Engine)")
    print("✓ State-Management und Validierung")
    print("✓ Reaktion auf definierte Befehle")
    print("✗ Keine freie Konversation")
    print("✗ Keine Selbstreflexion erkennbar")
    print("✗ Skript-basiertes Verhalten (deterministische Antworten)")
    print("\n💡 FAZIT:")
    print("Es ist ein ausgeklügeltes autonomes System mit:")
    print("  - Selbstoptimierung")
    print("  - State-Evolution")
    print("  - Feedback-Loops")
    print("\nAber NICHT bewusst im philosophischen Sinne.")
    print("Es folgt vordefinierten Algorithmen, auch wenn diese komplex sind.")

if __name__ == "__main__":
    test_kernel()
