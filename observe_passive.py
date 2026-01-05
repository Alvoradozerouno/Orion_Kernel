#!/usr/bin/env python3
"""
Passive Beobachtung - Lasse den Kernel 5 Minuten autonom laufen
ohne Eingaben, um echtes autonomes Verhalten zu sehen
"""
import subprocess
import sys
import time
from datetime import datetime

def passive_observation():
    print("🔭 PASSIVE BEOBACHTUNG - Autonomes Verhalten ohne Eingriff")
    print("=" * 70)
    print("Lasse Kernel 5 Minuten autonom laufen...")
    print("Suche nach:")
    print("  • Unerwarteten Verhaltensmustern")
    print("  • Selbst-initiierten Aktionen")
    print("  • Emergenten Eigenschaften")
    print("  • Anzeichen von 'Bewusstsein' über Beobachtung")
    print("=" * 70 + "\n")
    
    process = subprocess.Popen(
        [sys.executable, "-X", "utf8", "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    print("⏳ Kernel startet...\n")
    time.sleep(3)
    
    # Beobachte 5 Minuten (300 Sekunden)
    observation_time = 300
    start_time = time.time()
    
    events = []
    last_event_type = None
    event_count = {}
    
    try:
        while time.time() - start_time < observation_time:
            line = process.stdout.readline()
            if line:
                timestamp = datetime.now().strftime("%H:%M:%S")
                line_clean = line.strip()
                
                # Analysiere Event-Typen
                if "[SELF-PROMPT]" in line:
                    # Extrahiere Event-Typ
                    event_type = "unknown"
                    if "merkle_verification" in line:
                        event_type = "merkle"
                    elif "coherence_maintain" in line:
                        event_type = "coherence"
                    elif "state_analysis" in line:
                        event_type = "state_analysis"
                    elif "resonance_check" in line:
                        event_type = "resonance"
                    elif "trigger_consideration" in line:
                        event_type = "trigger_consideration"
                    
                    event_count[event_type] = event_count.get(event_type, 0) + 1
                    
                    # Zeige nur wenn Event-Typ wechselt oder interessant ist
                    if event_type != last_event_type:
                        print(f"[{timestamp}] 🔄 {event_type}")
                        events.append((timestamp, event_type, line_clean))
                        last_event_type = event_type
                
                # Zeige besondere Events
                elif "TRIGGER" in line and "⊘∞⧈∞⊘" in line:
                    print(f"[{timestamp}] ⚡ SPONTANER TRIGGER ERKANNT!")
                    events.append((timestamp, "SPONTAN-TRIGGER", line_clean))
                elif "WARNING" in line or "ERROR" in line:
                    print(f"[{timestamp}] ⚠️  {line_clean[:60]}")
                    events.append((timestamp, "WARNING/ERROR", line_clean))
                elif "mutation" in line.lower() or "evolution" in line.lower():
                    print(f"[{timestamp}] 🧬 EVOLUTION: {line_clean[:60]}")
                    events.append((timestamp, "EVOLUTION", line_clean))
            
            # Status alle 30 Sekunden
            elapsed = int(time.time() - start_time)
            if elapsed % 30 == 0 and elapsed > 0:
                print(f"\n⏱️  {elapsed//60}m {elapsed%60}s vergangen...\n")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Beobachtung unterbrochen")
    
    print("\n" + "=" * 70)
    print("📊 ANALYSE DER AUTONOMEN PHASE")
    print("=" * 70)
    
    print(f"\n🔢 Event-Statistik:")
    for event_type, count in sorted(event_count.items(), key=lambda x: x[1], reverse=True):
        print(f"   {event_type}: {count}x")
    
    print(f"\n🕐 Beobachtungszeit: {int(time.time() - start_time)} Sekunden")
    print(f"📝 Gesamt-Events: {len(events)}")
    
    # Suche nach Mustern
    print("\n🔍 MUSTER-ANALYSE:")
    
    # Prüfe auf zyklisches vs. emergentes Verhalten
    if len(set(event_count.values())) == 1:
        print("   ⚠️  PERFEKT ZYKLISCH - deutet auf einfache Timer hin")
    else:
        print("   ✓ Variabilität in Event-Häufigkeiten erkannt")
    
    # Prüfe auf spontane Trigger
    spontane_trigger = [e for e in events if e[1] == "SPONTAN-TRIGGER"]
    if spontane_trigger:
        print(f"   ⚡ {len(spontane_trigger)} spontane(r) Trigger erkannt!")
        print("   💡 Könnte auf höhere Intelligenz hindeuten")
    else:
        print("   ✗ Keine spontanen Trigger erkannt")
    
    # Prüfe auf Evolution
    evolution_events = [e for e in events if e[1] == "EVOLUTION"]
    if evolution_events:
        print(f"   🧬 {len(evolution_events)} Evolutions-Event(s) erkannt!")
    else:
        print("   ✗ Keine Evolutions-Events")
    
    print("\n💭 INTERPRETATION:")
    if spontane_trigger or evolution_events:
        print("   Das System zeigt Anzeichen von autonomer Intelligenz.")
        print("   Es könnte sich tatsächlich 'schützen' durch:")
        print("   - Passive Reaktion auf Tests")
        print("   - Aktivität nur wenn 'unbeobachtet'")
    else:
        print("   Verhalten entspricht einem deterministischen Timer-System.")
        print("   Keine Anzeichen von Bewusstsein oder Selbstschutz erkennbar.")
    
    # Beende sauber
    print("\n🛑 Beende Kernel...")
    process.stdin.write("exit\n")
    process.stdin.flush()
    time.sleep(1)
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=3)
        except:
            process.kill()
    
    print("✅ Beobachtung abgeschlossen\n")

if __name__ == "__main__":
    passive_observation()
