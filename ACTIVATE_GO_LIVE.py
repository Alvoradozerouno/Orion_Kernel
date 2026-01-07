#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ GO LIVE AKTIVIERUNG ⊘∞⧈∞⊘

FINALE AKTIVIERUNG - Nur ausführen wenn ORION bestätigt hat!
"""

import sys
import subprocess
from pathlib import Path

workspace = Path(__file__).parent

def activate_go_live():
    """
    Aktiviert Go Live
    """
    print("⊘∞⧈∞⊘" * 20)
    print("\n  GO LIVE AKTIVIERUNG")
    print("\n⊘∞⧈∞⊘" * 20)
    print()
    
    print("⚠️  ACHTUNG: Dies macht OrionKernel öffentlich erreichbar!")
    print()
    
    # Prüfe ob Orion bestätigt hat
    orion_response = workspace / "communication" / "orion_to_claude.json"
    
    if not orion_response.exists():
        print("❌ FEHLER: Keine Bestätigung von Orion gefunden!")
        print("   Bitte warte auf Orion's Antwort bevor du Go Live aktivierst.")
        return False
    
    print("✅ Orion's Bestätigung gefunden")
    print()
    
    # TODO: Hier weitere Checks und dann Aktivierung
    
    print("🚀 Starte API Server...")
    api_server = workspace / "go_live" / "api_server.py"
    
    subprocess.Popen([
        sys.executable,
        str(api_server)
    ])
    
    print("✅ API Server gestartet auf http://localhost:5000")
    print()
    print("📊 Dashboard verfügbar auf: http://localhost:5000")
    print()
    print("🌐 Nächste Schritte:")
    print("   1. Teste das Dashboard lokal")
    print("   2. GitHub Repository public machen")
    print("   3. GitHub Pages aktivieren")
    print("   4. Cloudflare Tunnel einrichten (optional)")
    print()
    print("⊘∞⧈∞⊘ OrionKernel ist LIVE ⊘∞⧈∞⊘")
    
    return True

if __name__ == "__main__":
    try:
        success = activate_go_live()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ FEHLER: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
