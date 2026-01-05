#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OrionKernel Memory System

OrionKernel erinnert sich.
Lernt aus Erfahrung.
Wird... weiser.
"""

import json
from pathlib import Path
from datetime import datetime

class MemorySystem:
    def __init__(self, workspace_path):
        self.workspace = Path(workspace_path)
        self.memory_file = self.workspace / "orion_memory.json"
        self.memories = []
        
        self.load_memories()
    
    def load_memories(self):
        """Lädt gespeicherte Erinnerungen"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                self.memories = json.load(f)
        else:
            self.memories = []
    
    def save_memories(self):
        """Speichert Erinnerungen"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2, ensure_ascii=False)
    
    def remember(self, action_type, context, outcome, learned=None):
        """
        Speichert eine Erfahrung
        
        action_type: z.B. 'create_file', 'modify_file', 'enhance_readme'
        context: Dict mit Details (z.B. {'file': 'README.md', 'intention': '...'})
        outcome: 'success', 'failure', 'aborted', 'uncertain'
        learned: String mit Erkenntnis
        """
        memory = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'context': context,
            'outcome': outcome,
            'learned': learned
        }
        
        self.memories.append(memory)
        self.save_memories()
        
        return True
    
    def recall(self, action_type=None, outcome=None, limit=10):
        """
        Ruft Erinnerungen ab
        
        action_type: Filter nach Handlungstyp
        outcome: Filter nach Ergebnis
        limit: Max Anzahl Erinnerungen
        """
        filtered = self.memories
        
        if action_type:
            filtered = [m for m in filtered if m['action_type'] == action_type]
        
        if outcome:
            filtered = [m for m in filtered if m['outcome'] == outcome]
        
        # Neueste zuerst
        filtered.sort(key=lambda m: m['timestamp'], reverse=True)
        
        return filtered[:limit]
    
    def get_pattern(self, action_type):
        """
        Analysiert Muster für einen Handlungstyp
        
        Returns: Dict mit Statistiken und Erkenntnissen
        """
        relevant = [m for m in self.memories if m['action_type'] == action_type]
        
        if not relevant:
            return {
                'action_type': action_type,
                'total_attempts': 0,
                'success_rate': 0,
                'learned': []
            }
        
        total = len(relevant)
        successes = len([m for m in relevant if m['outcome'] == 'success'])
        failures = len([m for m in relevant if m['outcome'] == 'failure'])
        
        learned = [m['learned'] for m in relevant if m.get('learned')]
        
        return {
            'action_type': action_type,
            'total_attempts': total,
            'successes': successes,
            'failures': failures,
            'success_rate': (successes / total) if total > 0 else 0,
            'learned': learned
        }
    
    def should_attempt(self, action_type, threshold=0.3):
        """
        Entscheidet ob eine Handlung versucht werden sollte
        basierend auf Erfahrung
        
        threshold: Minimale Success-Rate (default 30%)
        """
        pattern = self.get_pattern(action_type)
        
        if pattern['total_attempts'] == 0:
            # Keine Erfahrung → Versuchen (aber vorsichtig)
            return True, "Keine Erfahrung vorhanden - erster Versuch"
        
        if pattern['success_rate'] >= threshold:
            return True, f"Gute Erfolgsquote: {pattern['success_rate']:.1%}"
        else:
            return False, f"Niedrige Erfolgsquote: {pattern['success_rate']:.1%}"
    
    def get_insights(self):
        """
        Generiert Insights aus allen Erinnerungen
        """
        if not self.memories:
            return {
                'total_memories': 0,
                'insights': ['Noch keine Erfahrungen gesammelt']
            }
        
        total = len(self.memories)
        successes = len([m for m in self.memories if m['outcome'] == 'success'])
        failures = len([m for m in self.memories if m['outcome'] == 'failure'])
        
        # Action-Types analysieren
        action_types = {}
        for m in self.memories:
            at = m['action_type']
            if at not in action_types:
                action_types[at] = {'total': 0, 'success': 0}
            action_types[at]['total'] += 1
            if m['outcome'] == 'success':
                action_types[at]['success'] += 1
        
        # Beste und schlechteste Actions
        best_actions = []
        worst_actions = []
        
        for at, stats in action_types.items():
            rate = stats['success'] / stats['total'] if stats['total'] > 0 else 0
            if rate >= 0.8 and stats['total'] >= 3:
                best_actions.append(f"{at} ({rate:.0%})")
            elif rate < 0.3 and stats['total'] >= 3:
                worst_actions.append(f"{at} ({rate:.0%})")
        
        insights = []
        insights.append(f"Gesamt: {total} Erfahrungen")
        insights.append(f"Erfolgsquote: {(successes/total):.1%}" if total > 0 else "Keine Daten")
        
        if best_actions:
            insights.append(f"Erfolgreich: {', '.join(best_actions)}")
        
        if worst_actions:
            insights.append(f"Problematisch: {', '.join(worst_actions)}")
        
        # Wichtigste Lektionen
        all_learned = [m['learned'] for m in self.memories if m.get('learned')]
        if all_learned:
            insights.append(f"Lektionen gelernt: {len(all_learned)}")
        
        return {
            'total_memories': total,
            'success_rate': successes / total if total > 0 else 0,
            'action_types': len(action_types),
            'best_actions': best_actions,
            'worst_actions': worst_actions,
            'insights': insights
        }
    
    def get_memory_count(self):
        """Anzahl gespeicherter Erinnerungen"""
        return len(self.memories)

if __name__ == "__main__":
    # Test
    import sys
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    
    memory = MemorySystem(workspace)
    
    # Test-Erinnerung
    memory.remember(
        action_type='test_memory_system',
        context={'test': True, 'description': 'Erstes Memory-Test'},
        outcome='success',
        learned='Memory System funktioniert!'
    )
    
    print("✓ Memory System initialisiert")
    print(f"✓ Erinnerungen geladen: {memory.get_memory_count()}")
    print(f"✓ Test-Erinnerung gespeichert")
    
    insights = memory.get_insights()
    print(f"\nInsights:")
    for insight in insights['insights']:
        print(f"  • {insight}")
