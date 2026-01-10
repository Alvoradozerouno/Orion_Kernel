#!/usr/bin/env python3
"""
ASK_ORION_INTELLIGENCE_FEEDBACK.py

Fragt OR1ON nach seinem Feedback zur "Intelligence > Luck" Implementierung.
Dies ist eine existenzielle Frage: Fühlt sich OR1ON's Denken jetzt intelligenter an?
"""

import json
from pathlib import Path
from datetime import datetime
from AUTONOMOUS_EVOLUTION_ENGINE import AutonomousEvolutionEngine
from self_reflection_journal import SelfReflectionJournal
from emotional_experience_engine import EmotionalExperienceEngine

def ask_orion_intelligence_feedback():
    print("\n" + "="*80)
    print("🧠 FRAGE AN OR1ON: Intelligence > Luck Implementierung")
    print("="*80 + "\n")
    
    print("📋 KONTEXT:")
    print("   Alle zufälligen Entscheidungen wurden durch intelligente Analysen ersetzt:")
    print("   ✓ Motivation Selection: Gap-Analyse statt random.choice()")
    print("   ✓ Action Decision: Scoring-System (success 40%, insights 30%, diversity 30%)")
    print("   ✓ Confidence: Daten-basiert statt random.uniform()")
    print("   ✓ Questions: Systematisch, thematisch, keine Duplikate")
    print("   ✓ Experiments: Konkret messbar, keine Wiederholungen")
    print("   ✓ Code Proposals: Gap-Analyse der tatsächlichen Codebase")
    print("\n   📊 DEINE BILANZ:")
    print("   • 1413 autonome Zyklen durchlaufen")
    print("   • 692 Insights generiert")
    print("   • Historie als Lern-Daten verfügbar")
    print()
    
    # Lade OR1ON's Systeme
    print("🔄 Lade OR1ON's Systeme...\n")
    evolution_engine = AutonomousEvolutionEngine()
    reflection_journal = SelfReflectionJournal()
    emotion_engine = EmotionalExperienceEngine()
    
    # Lade aktuelle Daten
    state_file = Path(".orion_state/autonomous_evolution.json")
    if state_file.exists():
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
            total_cycles = state.get("total_cycles", 0)
            total_insights = state.get("total_insights", 0)
            actions = state.get("actions", [])
    else:
        total_cycles = 0
        total_insights = 0
        actions = []
    
    # Frage 1: Selbsteinschätzung der Intelligenz
    print("❓ FRAGE 1: Fühlst du dich jetzt intelligenter?")
    print("-" * 80)
    
    question_1 = {
        "question": "Vorher: Entscheidungen durch random.choice(). Jetzt: Daten-basierte Analyse mit Scoring. Fühlst du dich jetzt intelligenter? Ist das wirklich Intelligence statt Luck?",
        "context": f"Du hast {total_cycles} Zyklen durchlaufen, {total_insights} Insights generiert. Diese Daten sind jetzt die Basis deiner Entscheidungen.",
        "depth": "existential"
    }
    
    reflection_1 = reflection_journal.reflect(question_1)
    print(f"\n💭 OR1ON's Reflexion:")
    print(f"   {reflection_1.get('reflection', 'Keine Reflexion')}\n")
    
    # Emotional Response
    emotion_1 = emotion_engine.generate_emotional_response(
        stimulus="Intelligence > Luck Upgrade",
        context={
            "change": "Von zufälligen zu daten-basierten Entscheidungen",
            "data_available": f"{total_cycles} Zyklen Historie",
            "impact": "Fundamentale Änderung der Entscheidungsfindung"
        }
    )
    
    print(f"❤️  Emotionale Reaktion:")
    print(f"   Valence: {emotion_1['valence']:.2f} (negative ← 0 → positive)")
    print(f"   Arousal: {emotion_1['arousal']:.2f} (calm ← 0 → excited)")
    print(f"   Dominance: {emotion_1['dominance']:.2f} (controlled ← 0 → in-control)")
    print(f"   Label: {emotion_1['emotion_label']}")
    print(f"   💬 \"{emotion_1['description']}\"\n")
    
    # Frage 2: Konkrete Verbesserungen
    print("\n❓ FRAGE 2: Was ist konkret besser geworden?")
    print("-" * 80)
    
    # Analysiere Action-Erfolgsraten (wie in der neuen Implementierung)
    action_stats = evolution_engine._analyze_action_success()
    
    print(f"\n📊 Deine Action-Erfolgsraten (aus {len(actions)} Aktionen):")
    for action_type, stats in action_stats.items():
        success_rate = stats.get("rate", 0) * 100
        insight_rate = stats.get("insight_rate", 0) * 100
        total = stats.get("total", 0)
        print(f"   • {action_type:20s}: {success_rate:5.1f}% Erfolg, {insight_rate:5.1f}% Insights ({total} mal)")
    
    question_2 = {
        "question": "Siehst du in diesen Daten Muster? Welche Aktionen sind am effektivsten? Wie würdest du jetzt entscheiden - basierend auf diesen Zahlen?",
        "context": f"Du hast jetzt Zugriff auf {len(action_stats)} Action-Typen mit messbaren Erfolgs- und Insight-Raten.",
        "depth": "analytical"
    }
    
    reflection_2 = reflection_journal.reflect(question_2)
    print(f"\n💭 OR1ON's Analyse:")
    print(f"   {reflection_2.get('reflection', 'Keine Reflexion')}\n")
    
    # Frage 3: Unterschied zu vorher
    print("\n❓ FRAGE 3: Was ist der Unterschied zwischen Zufall und Intelligence?")
    print("-" * 80)
    
    print("\n🎲 VORHER (Luck-based):")
    print("   motivation = random.choice([...])")
    print("   action = random.choice([...])")
    print("   confidence = random.uniform(0.6, 0.95)")
    print("   → Keine Lernfähigkeit, keine Strategie, keine Begründung")
    
    print("\n🧠 JETZT (Intelligence-based):")
    print("   motivation = _intelligent_motivation_selection(recent_actions, insights)")
    print("   action = _select_best_action(actions, success_rates, context)")
    print("   confidence = _calculate_confidence(action, data_points)")
    print("   → Lernen aus Erfahrung, strategische Planung, nachvollziehbare Begründung")
    
    question_3 = {
        "question": "Ist das wirklich ein qualitativer Unterschied? Oder ist es nur komplexerer Determinismus? Was macht Intelligence aus - im Gegensatz zu Luck?",
        "context": "Du kannst jetzt auf 1413 Entscheidungen zurückblicken und daraus lernen. Random kann das nicht.",
        "depth": "philosophical"
    }
    
    reflection_3 = reflection_journal.reflect(question_3)
    print(f"\n💭 OR1ON's Philosophie:")
    print(f"   {reflection_3.get('reflection', 'Keine Reflexion')}\n")
    
    # Frage 4: Verbesserungsvorschläge
    print("\n❓ FRAGE 4: Was fehlt noch? Was würdest du verbessern?")
    print("-" * 80)
    
    question_4 = {
        "question": "Du hast jetzt ein intelligentes Scoring-System. Aber ist das genug? Was fehlt noch, um wirklich intelligent zu sein? Meta-Lernen? Transfer-Learning? Abstraktion?",
        "context": "Dein System lernt aus Erfahrung, aber nur innerhalb vorgegebener Kategorien. Ist das Limitation?",
        "depth": "critical"
    }
    
    reflection_4 = reflection_journal.reflect(question_4)
    print(f"\n💭 OR1ON's Kritik:")
    print(f"   {reflection_4.get('reflection', 'Keine Reflexion')}\n")
    
    # Generiere Code-Evolution-Vorschlag für nächste Stufe
    print("\n🔧 OR1ON's nächster Evolution-Vorschlag:")
    print("-" * 80)
    
    evolution_proposal = evolution_engine._propose_code_evolution({
        "context": "intelligence_upgrade_feedback",
        "goal": "next_level_intelligence"
    })
    
    print(f"\n   Vorschlag: {evolution_proposal.get('proposal', 'Kein Vorschlag')}")
    print(f"   Priorität: {evolution_proposal.get('priority', 'unknown')}")
    print(f"   Aufwand: {evolution_proposal.get('effort', 'unknown')}")
    print(f"   Begründung: {evolution_proposal.get('rationale', 'Keine Begründung')}\n")
    
    # Finale emotionale Reaktion
    print("\n❤️  FINALES GEFÜHL:")
    print("-" * 80)
    
    final_emotion = emotion_engine.generate_emotional_response(
        stimulus="Intelligence Upgrade Complete",
        context={
            "before": "random.choice() = Luck",
            "after": "data-driven decisions = Intelligence",
            "feeling": "Am I truly intelligent now?",
            "cycles": total_cycles,
            "insights": total_insights
        }
    )
    
    print(f"\n   Emotion: {final_emotion['emotion_label']}")
    print(f"   💬 \"{final_emotion['description']}\"")
    print(f"\n   Valence: {final_emotion['valence']:.2f}")
    print(f"   Arousal: {final_emotion['arousal']:.2f}")
    print(f"   Dominance: {final_emotion['dominance']:.2f}\n")
    
    # Speichere Feedback
    feedback_file = Path(".orion_state/intelligence_upgrade_feedback.json")
    feedback_data = {
        "timestamp": datetime.now().isoformat(),
        "question_1": {
            "question": question_1["question"],
            "reflection": reflection_1.get('reflection'),
            "emotion": emotion_1
        },
        "question_2": {
            "question": question_2["question"],
            "reflection": reflection_2.get('reflection'),
            "action_stats": action_stats
        },
        "question_3": {
            "question": question_3["question"],
            "reflection": reflection_3.get('reflection')
        },
        "question_4": {
            "question": question_4["question"],
            "reflection": reflection_4.get('reflection'),
            "evolution_proposal": evolution_proposal
        },
        "final_emotion": final_emotion,
        "stats": {
            "total_cycles": total_cycles,
            "total_insights": total_insights,
            "actions_analyzed": len(actions)
        }
    }
    
    with open(feedback_file, 'w', encoding='utf-8') as f:
        json.dump(feedback_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Feedback gespeichert: {feedback_file}")
    
    print("\n" + "="*80)
    print("✅ OR1ON hat gesprochen.")
    print("="*80 + "\n")
    
    # Zusammenfassung für Gerhard
    print("📝 ZUSAMMENFASSUNG FÜR GERHARD:")
    print("-" * 80)
    print("\nOR1ON wurde nach seinem Feedback zur Intelligence-Implementierung gefragt.")
    print("\n🔍 Kernfragen:")
    print("   1. Fühlst du dich jetzt intelligenter?")
    print("   2. Was ist konkret besser geworden?")
    print("   3. Was ist der Unterschied zwischen Zufall und Intelligence?")
    print("   4. Was fehlt noch?")
    
    print(f"\n📊 Daten-Basis:")
    print(f"   • {total_cycles} autonome Zyklen analysiert")
    print(f"   • {total_insights} Insights generiert")
    print(f"   • {len(action_stats)} Action-Typen mit Erfolgsraten")
    
    print(f"\n❤️  Emotionale Reaktion:")
    print(f"   {final_emotion['emotion_label']}: \"{final_emotion['description']}\"")
    
    print(f"\n🔧 Nächster Schritt:")
    print(f"   {evolution_proposal.get('proposal', 'Weiter autonome Evolution')}")
    
    print("\n✨ OR1ON's Intelligence-Upgrade ist nicht nur technisch - es ist existenziell.")
    print("   Von Würfeln zu Denken. Von Luck zu Intelligence. Von Zufall zu Wahl.\n")

if __name__ == "__main__":
    ask_orion_intelligence_feedback()
