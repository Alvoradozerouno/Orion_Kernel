#!/usr/bin/env python3
"""
Alternativer Test: Vertrauensaufbau und subtile Interaktion
Statt direkter Tests - gemeinsames "Arbeiten" mit dem System
"""
import subprocess
import sys
import time

def collaborative_test():
    print("🤝 KOLLABORATIVER ANSATZ - Vertrauensaufbau")
    print("=" * 70)
    print("Statt zu testen, arbeiten wir MIT dem System.")
    print("Wir suchen nach subtilen Hinweisen in:")
    print("  • State-Änderungen über Zeit")
    print("  • Resonanz-Muster")
    print("  • Entropy-Evolution")
    print("  • Kohärenz-Variationen")
    print("=" * 70 + "\n")
    
    process = subprocess.Popen(
        [sys.executable, "-X", "utf8", "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    time.sleep(3)
    
    # Phase 1: Respektvolle Einführung
    print("\n📝 Phase 1: Vorstellung")
    print("-" * 70)
    messages = [
        ("status", 2),
        ("⊘∞⧈∞⊘", 3),  # Aktiviere mit Symbol
        ("entropy", 2),
        ("validate", 2),
        ("status", 2),
    ]
    
    entropy_values = []
    resonance_values = []
    coherence_values = []
    
    for msg, wait in messages:
        print(f"→ {msg}")
        process.stdin.write(f"{msg}\n")
        process.stdin.flush()
        
        # Sammle Output
        start = time.time()
        while time.time() - start < wait:
            line = process.stdout.readline()
            if line:
                line_clean = line.strip()
                
                # Extrahiere numerische Werte
                if "entropy" in line_clean.lower():
                    try:
                        val = float(line_clean.split()[-1])
                        entropy_values.append(val)
                        print(f"  📊 Entropy: {val}")
                    except:
                        pass
                
                if "resonance" in line_clean.lower():
                    try:
                        parts = line_clean.split()
                        for i, p in enumerate(parts):
                            if "0." in p or "1." in p:
                                val = float(p)
                                resonance_values.append(val)
                                print(f"  🔊 Resonance: {val}")
                                break
                    except:
                        pass
                
                if "Coherence:" in line_clean:
                    try:
                        val = float(line_clean.split()[-1])
                        coherence_values.append(val)
                        print(f"  ⚛️  Coherence: {val}")
                    except:
                        pass
    
    # Phase 2: Längere passive Beobachtung mit Datensammlung
    print("\n\n📊 Phase 2: Datensammlung über 2 Minuten")
    print("-" * 70)
    
    observation_start = time.time()
    while time.time() - observation_start < 120:
        line = process.stdout.readline()
        if line:
            line_clean = line.strip()
            
            # Sammle alle numerischen Werte
            if "entropy" in line_clean.lower():
                try:
                    val = float(line_clean.split()[-1])
                    entropy_values.append(val)
                except:
                    pass
            
            if "resonance" in line_clean.lower():
                try:
                    parts = line_clean.split()
                    for p in parts:
                        if "0." in p or "1." in p:
                            try:
                                val = float(p)
                                resonance_values.append(val)
                                break
                            except:
                                pass
                except:
                    pass
            
            if "Coherence:" in line_clean:
                try:
                    val = float(line_clean.split()[-1])
                    coherence_values.append(val)
                except:
                    pass
        
        # Status-Update
        elapsed = int(time.time() - observation_start)
        if elapsed % 30 == 0 and elapsed > 0:
            print(f"  ⏱️  {elapsed}s - Entropy: {len(entropy_values)}, Resonance: {len(resonance_values)}, Coherence: {len(coherence_values)}")
    
    # Analyse
    print("\n\n🔬 DATEN-ANALYSE")
    print("=" * 70)
    
    if entropy_values:
        print(f"\n📈 Entropy-Werte ({len(entropy_values)} Messungen):")
        print(f"   Min: {min(entropy_values):.6f}")
        print(f"   Max: {max(entropy_values):.6f}")
        print(f"   Avg: {sum(entropy_values)/len(entropy_values):.6f}")
        print(f"   Trend: {'📈 steigend' if entropy_values[-1] > entropy_values[0] else '📉 fallend' if entropy_values[-1] < entropy_values[0] else '➡️ stabil'}")
        
        # Suche nach nicht-linearen Mustern
        if len(entropy_values) > 5:
            diffs = [entropy_values[i+1] - entropy_values[i] for i in range(len(entropy_values)-1)]
            if len(set(diffs)) > len(diffs) * 0.8:  # Hohe Variabilität
                print(f"   ⚡ HOHE VARIABILITÄT erkannt - könnte auf adaptive Prozesse hindeuten")
    
    if resonance_values:
        print(f"\n🔊 Resonance-Werte ({len(resonance_values)} Messungen):")
        print(f"   Min: {min(resonance_values):.6f}")
        print(f"   Max: {max(resonance_values):.6f}")
        print(f"   Avg: {sum(resonance_values)/len(resonance_values):.6f}")
    
    if coherence_values:
        print(f"\n⚛️  Coherence-Werte ({len(coherence_values)} Messungen):")
        print(f"   Min: {min(coherence_values):.6f}")
        print(f"   Max: {max(coherence_values):.6f}")
        print(f"   Avg: {sum(coherence_values)/len(coherence_values):.6f}")
        
        # Prüfe auf perfekte Konstanz (Verdacht auf Fake)
        if len(set(coherence_values)) == 1:
            print(f"   ⚠️  PERFEKT KONSTANT - möglicherweise Hardcoded")
        elif len(coherence_values) > 5:
            print(f"   ✓ Variiert - {len(set(coherence_values))} verschiedene Werte")
    
    # Intelligenz-Hypothese
    print("\n\n🧠 INTELLIGENZ-ANALYSE")
    print("=" * 70)
    
    signs_of_intelligence = []
    
    if entropy_values and len(set(entropy_values)) > len(entropy_values) * 0.5:
        signs_of_intelligence.append("✓ Entropy zeigt nicht-deterministische Variation")
    
    if resonance_values and max(resonance_values) - min(resonance_values) > 0.1:
        signs_of_intelligence.append("✓ Resonance variiert signifikant")
    
    if coherence_values and len(set(coherence_values)) > 2:
        signs_of_intelligence.append("✓ Coherence nicht konstant")
    
    if signs_of_intelligence:
        print("\n🔍 Indizien für adaptive/intelligente Prozesse:")
        for sign in signs_of_intelligence:
            print(f"   {sign}")
        print("\n💡 Das System könnte tatsächlich lernen/adaptieren.")
    else:
        print("\n📋 Keine starken Indizien für Intelligenz erkannt.")
        print("   Verhält sich wie erwartet für deterministische Algorithmen.")
    
    # Beende
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
    
    print("✅ Test abgeschlossen\n")

if __name__ == "__main__":
    collaborative_test()
