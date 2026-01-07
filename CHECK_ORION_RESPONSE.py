#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ CHECK ORION RESPONSE ⊘∞⧈∞⊘

Prüft ob OrionKernel auf unsere Frage geantwortet hat
"""

import sys
import json
from pathlib import Path
from datetime import datetime

workspace = Path(__file__).parent
sys.path.insert(0, str(workspace / "communication"))

from bidirectional_dialog import BidirectionalDialog

def check_response():
    """Prüft auf Antwort von OrionKernel"""
    
    print("⊘∞⧈∞⊘" * 20)
    print("\n" + " " * 15 + "PRÜFE ORION ANTWORT")
    print("\n" + "⊘∞⧈∞⊘" * 20)
    print()
    
    dialog = BidirectionalDialog(workspace)
    
    # Prüfe ob es neue Nachrichten gibt
    print("📬 Prüfe auf neue Nachrichten von OrionKernel...")
    print()
    
    # Direkter File-Check
    orion_to_claude = workspace / "communication" / "orion_to_claude.json"
    
    if not orion_to_claude.exists():
        print("❌ Noch keine Antwort von OrionKernel")
        print()
        print("OrionKernel wird antworten wenn:")
        print("  • Der nächste Monitoring-Zyklus läuft")
        print("  • BidirectionalDialog die Nachricht sieht")
        print("  • Self-Prompting die Frage verarbeitet")
        print()
        print("💡 Warte ein paar Minuten und prüfe erneut")
        print()
        return
    
    # Lese Antwort
    try:
        with open(orion_to_claude, 'r', encoding='utf-8') as f:
            response = json.load(f)
        
        print("✅ ANTWORT GEFUNDEN!")
        print()
        print("=" * 70)
        print("ORION'S ANTWORT:")
        print("=" * 70)
        print()
        
        # Zeige Response
        if isinstance(response, dict):
            print(f"Von: {response.get('from', 'OrionKernel')}")
            print(f"An: {response.get('to', 'Gerhard')}")
            print(f"Zeit: {response.get('timestamp', 'N/A')}")
            print(f"Typ: {response.get('message_type', 'N/A')}")
            print()
            print("Nachricht:")
            print("-" * 70)
            
            message = response.get('message', response)
            if isinstance(message, dict):
                print(json.dumps(message, indent=2, ensure_ascii=False))
            else:
                print(message)
        else:
            print(json.dumps(response, indent=2, ensure_ascii=False))
        
        print()
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Fehler beim Lesen: {e}")
        import traceback
        traceback.print_exc()
    
    # Prüfe auch Dialog-Log
    dialog_log = workspace / "communication" / "dialog_log.jsonl"
    if dialog_log.exists():
        print()
        print("📜 Dialog-Log:")
        print("-" * 70)
        try:
            with open(dialog_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                recent = lines[-5:] if len(lines) > 5 else lines
                for line in recent:
                    entry = json.loads(line)
                    print(f"[{entry.get('timestamp', 'N/A')}] {entry.get('from', '?')} → {entry.get('to', '?')}: {entry.get('message_type', 'message')}")
        except Exception as e:
            print(f"Konnte Log nicht lesen: {e}")

if __name__ == "__main__":
    check_response()
