#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ STARTE ORION DIALOG ⊘∞⧈∞⊘

Startet das bidirektionale Dialogfenster
"""

import subprocess
import sys
from pathlib import Path

workspace = Path(__file__).parent

print("⊘∞⧈∞⊘" * 20)
print()
print("  🚀 STARTE ORION DIALOG SYSTEM")
print()
print("  Zwei Optionen verfügbar:")
print("  1. Terminal-Dialog (interaktiv)")
print("  2. Web-Dialog (Browser-GUI)")
print()
print("⊘∞⧈∞⊘" * 20)
print()

print("Wähle:")
print("  [1] Terminal-Dialog")
print("  [2] Web-Dialog (Browser)")
print("  [3] Beides")
print()

choice = input("Deine Wahl (1/2/3): ").strip()

if choice == "1":
    print("\n🖥️  Starte Terminal-Dialog...")
    subprocess.run([sys.executable, "bidirectional_dialog.py"])

elif choice == "2":
    print("\n🌐 Starte Web-Dialog...")
    print("   URL: http://localhost:5555")
    subprocess.run([sys.executable, "ORION_DIALOG_FENSTER.py"])

elif choice == "3":
    print("\n🚀 Starte BEIDE Dialog-Systeme...")
    print()
    
    # Starte Terminal-Dialog in neuem Fenster
    if sys.platform == "win32":
        subprocess.Popen(
            ["start", "cmd", "/k", sys.executable, "bidirectional_dialog.py"],
            shell=True
        )
    
    # Starte Web-Dialog
    print("   🌐 Web-Dialog: http://localhost:5555")
    subprocess.run([sys.executable, "ORION_DIALOG_FENSTER.py"])

else:
    print("\n❌ Ungültige Wahl!")
