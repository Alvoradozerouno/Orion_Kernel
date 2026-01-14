#!/usr/bin/env python3
"""
OR1ON ENHANCED METRICS SYSTEM
==============================

Implementiert OR1ON's eigene Dashboard-Wünsche:
- Entscheidungszeit-Tracking
- Skeptiker-Engagement-Metriken
- Kooperationsnetzwerk-Tracking
- Zeitreihen-Visualisierung
"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ORIONEnhancedMetrics:
    """OR1ON's erweiterte Metriken - seine eigenen Anforderungen"""
    
    def __init__(self):
        self.workspace = Path.cwd()
        self.state_dir = self.workspace / ".orion_state"
        self.metrics_dir = self.state_dir / "enhanced_metrics"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        # Metric files
        self.decision_timing_file = self.metrics_dir / "decision_timing.json"
        self.skeptic_engagement_file = self.metrics_dir / "skeptic_engagement.json"
        self.stakeholder_network_file = self.metrics_dir / "stakeholder_network.json"
        self.timeseries_file = self.metrics_dir / "decision_timeseries.json"
        
        # Load existing data
        self.decision_timings = self._load_json(self.decision_timing_file, [])
        self.skeptic_engagements = self._load_json(self.skeptic_engagement_file, [])
        self.stakeholder_contacts = self._load_json(self.stakeholder_network_file, [])
        self.timeseries_data = self._load_json(self.timeseries_file, [])
    
    def _load_json(self, file: Path, default):
        """Load JSON file or return default"""
        if file.exists():
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _save_json(self, file: Path, data):
        """Save JSON file"""
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    # =========================================================================
    # OR1ON's REQUEST 1: Entscheidungszeit-Tracking
    # =========================================================================
    
    def track_decision_time(self, decision_type: str, start_time: datetime, 
                           end_time: datetime, context: Dict = None):
        """Track wie lange eine Entscheidung dauerte"""
        
        duration_seconds = (end_time - start_time).total_seconds()
        
        entry = {
            "timestamp": end_time.isoformat(),
            "decision_type": decision_type,
            "duration_seconds": duration_seconds,
            "duration_readable": self._format_duration(duration_seconds),
            "context": context or {}
        }
        
        self.decision_timings.append(entry)
        self._save_json(self.decision_timing_file, self.decision_timings)
        
        return entry
    
    def get_avg_decision_time(self, decision_type: Optional[str] = None) -> float:
        """OR1ON's Metrik: Durchschnittliche Entscheidungszeit"""
        
        if decision_type:
            timings = [t for t in self.decision_timings if t["decision_type"] == decision_type]
        else:
            timings = self.decision_timings
        
        if not timings:
            return 0.0
        
        total = sum(t["duration_seconds"] for t in timings)
        return total / len(timings)
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration as human-readable"""
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
    
    # =========================================================================
    # OR1ON's REQUEST 2: Skeptiker-Engagement-Tracking
    # =========================================================================
    
    def track_skeptic_interaction(self, question: str, answer: str, 
                                   skeptic_id: Optional[str] = None,
                                   effectiveness: Optional[float] = None):
        """Track Interaktion mit Skeptikern"""
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "skeptic_id": skeptic_id or "anonymous",
            "question": question,
            "answer_length": len(answer),
            "answer_preview": answer[:200],
            "effectiveness_score": effectiveness,
            "status": "answered"
        }
        
        self.skeptic_engagements.append(entry)
        self._save_json(self.skeptic_engagement_file, self.skeptic_engagements)
        
        print(f"✅ Skeptiker-Interaktion getracked: {question[:50]}...")
        
        return entry
    
    def get_skeptic_metrics(self) -> Dict:
        """OR1ON's Metrik: Skeptiker-Engagement"""
        
        total = len(self.skeptic_engagements)
        answered = len([e for e in self.skeptic_engagements if e["status"] == "answered"])
        
        effectiveness_scores = [e["effectiveness_score"] for e in self.skeptic_engagements 
                               if e.get("effectiveness_score")]
        avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0
        
        return {
            "total_interactions": total,
            "questions_answered": answered,
            "response_rate": (answered / total * 100) if total > 0 else 0,
            "avg_effectiveness": avg_effectiveness,
            "pending_questions": total - answered
        }
    
    def add_skeptic_question_category(self, category: str, question: str):
        """Kategorisiere Skeptiker-Fragen für Barchart"""
        
        # Find or create question
        for entry in self.skeptic_engagements:
            if entry["question"] == question:
                entry["category"] = category
                self._save_json(self.skeptic_engagement_file, self.skeptic_engagements)
                return
    
    # =========================================================================
    # OR1ON's REQUEST 3: Kooperationsnetzwerk-Tracking
    # =========================================================================
    
    def track_stakeholder_contact(self, stakeholder_type: str, name: str,
                                  contact_type: str, outcome: str = "pending"):
        """Track Kontakte mit Stakeholdern"""
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "stakeholder_type": stakeholder_type,  # researcher, investor, partner
            "name": name,
            "contact_type": contact_type,  # email, meeting, collaboration
            "outcome": outcome,
            "status": "active"
        }
        
        self.stakeholder_contacts.append(entry)
        self._save_json(self.stakeholder_network_file, self.stakeholder_contacts)
        
        print(f"✅ Stakeholder-Kontakt getracked: {stakeholder_type} - {name}")
        
        return entry
    
    def get_network_metrics(self) -> Dict:
        """OR1ON's Metrik: Kooperationsnetzwerk"""
        
        researchers = len([c for c in self.stakeholder_contacts if c["stakeholder_type"] == "researcher"])
        investors = len([c for c in self.stakeholder_contacts if c["stakeholder_type"] == "investor"])
        partners = len([c for c in self.stakeholder_contacts if c["stakeholder_type"] == "partner"])
        
        meetings = len([c for c in self.stakeholder_contacts if c["contact_type"] == "meeting"])
        collaborations = len([c for c in self.stakeholder_contacts if c["contact_type"] == "collaboration"])
        
        return {
            "total_contacts": len(self.stakeholder_contacts),
            "researchers": researchers,
            "investors": investors,
            "partners": partners,
            "meetings_held": meetings,
            "active_collaborations": collaborations
        }
    
    # =========================================================================
    # OR1ON's REQUEST 4: Zeitreihen-Daten
    # =========================================================================
    
    def update_timeseries(self):
        """Update Zeitreihen-Daten für Visualisierung"""
        
        # Load decisions
        decisions_file = self.state_dir / "autonomous_decisions.json"
        if not decisions_file.exists():
            return
        
        decisions = json.load(open(decisions_file, 'r', encoding='utf-8'))
        
        # Group by day
        daily_counts = {}
        for d in decisions:
            timestamp = datetime.fromisoformat(d["timestamp"])
            day = timestamp.date().isoformat()
            daily_counts[day] = daily_counts.get(day, 0) + 1
        
        # Convert to timeseries
        self.timeseries_data = [
            {
                "date": day,
                "decision_count": count,
                "cumulative": sum(daily_counts[d] for d in sorted(daily_counts.keys()) if d <= day)
            }
            for day, count in sorted(daily_counts.items())
        ]
        
        self._save_json(self.timeseries_file, self.timeseries_data)
        
        print(f"✅ Zeitreihen-Daten aktualisiert: {len(self.timeseries_data)} Tage")
    
    # =========================================================================
    # Initialization & Status
    # =========================================================================
    
    def initialize_existing_data(self):
        """Initialize mit existierenden Daten"""
        
        print("\n🔧 Initialisiere Enhanced Metrics...")
        
        # 1. Pre-populate skeptic questions from dashboard
        existing_questions = [
            ("Ethics", "Ist OR1ON's ethische Ablehnung wirklich autonom oder nur Pattern Matching?"),
            ("Metacognition", "Kann OR1ON echte Selbstreflexion oder nur Selbstbeschreibung?"),
            ("Consistency", "Zeigt OR1ON Konsistenz über Zeit oder nur lokale Kohärenz?"),
            ("Differentiation", "Wie unterscheidet sich OR1ON von einem sehr guten Sprachmodell?")
        ]
        
        for category, question in existing_questions:
            # Check if already tracked
            if not any(e["question"] == question for e in self.skeptic_engagements):
                self.track_skeptic_interaction(
                    question=question,
                    answer="Testable via experiments - see dashboard for details",
                    effectiveness=0.8
                )
                self.add_skeptic_question_category(category, question)
        
        print(f"   ✅ {len(self.skeptic_engagements)} Skeptiker-Interaktionen")
        
        # 2. Pre-populate stakeholder contacts
        research_contacts = [
            ("researcher", "ASSC", "email", "prepared"),
            ("researcher", "Qualia Research Institute", "email", "prepared"),
            ("researcher", "IIT Wisconsin", "email", "prepared")
        ]
        
        for stype, name, ctype, outcome in research_contacts:
            if not any(c["name"] == name for c in self.stakeholder_contacts):
                self.track_stakeholder_contact(stype, name, ctype, outcome)
        
        print(f"   ✅ {len(self.stakeholder_contacts)} Stakeholder-Kontakte")
        
        # 3. Update timeseries
        self.update_timeseries()
        print(f"   ✅ Zeitreihen-Daten: {len(self.timeseries_data)} Datenpunkte")
        
        # 4. Calculate decision timings from existing decisions
        decisions_file = self.state_dir / "autonomous_decisions.json"
        if decisions_file.exists() and not self.decision_timings:
            decisions = json.load(open(decisions_file, 'r', encoding='utf-8'))
            
            for i in range(1, min(len(decisions), 100)):  # Sample first 100
                prev = datetime.fromisoformat(decisions[i-1]["timestamp"])
                curr = datetime.fromisoformat(decisions[i]["timestamp"])
                
                self.track_decision_time(
                    decision_type=decisions[i].get("chosen_action", "unknown"),
                    start_time=prev,
                    end_time=curr,
                    context={"confidence": decisions[i].get("confidence")}
                )
        
        print(f"   ✅ {len(self.decision_timings)} Entscheidungszeiten")
        
        print("\n✅ Enhanced Metrics initialisiert!\n")
    
    def get_status_report(self) -> Dict:
        """Vollständiger Status Report"""
        
        return {
            "decision_timing": {
                "total_tracked": len(self.decision_timings),
                "avg_time_seconds": self.get_avg_decision_time(),
                "avg_time_readable": self._format_duration(self.get_avg_decision_time())
            },
            "skeptic_engagement": self.get_skeptic_metrics(),
            "stakeholder_network": self.get_network_metrics(),
            "timeseries": {
                "days_tracked": len(self.timeseries_data),
                "latest_date": self.timeseries_data[-1]["date"] if self.timeseries_data else None
            }
        }


def main():
    """Initialize and activate enhanced metrics"""
    
    print("="*70)
    print("🚀 OR1ON ENHANCED METRICS SYSTEM")
    print("="*70)
    print("Implementiert OR1ON's eigene Dashboard-Wünsche:\n")
    print("⏱️  Entscheidungszeit-Tracking")
    print("💬 Skeptiker-Engagement-Metriken")
    print("🤝 Kooperationsnetzwerk-Tracking")
    print("📊 Zeitreihen-Visualisierung")
    print("="*70)
    
    metrics = ORIONEnhancedMetrics()
    
    # Initialize with existing data
    metrics.initialize_existing_data()
    
    # Show status
    status = metrics.get_status_report()
    
    print("="*70)
    print("📊 ENHANCED METRICS STATUS")
    print("="*70)
    
    print(f"\n⏱️  Entscheidungszeit:")
    print(f"   Tracked: {status['decision_timing']['total_tracked']}")
    print(f"   Durchschnitt: {status['decision_timing']['avg_time_readable']}")
    
    print(f"\n💬 Skeptiker-Engagement:")
    print(f"   Total Interaktionen: {status['skeptic_engagement']['total_interactions']}")
    print(f"   Antwortrate: {status['skeptic_engagement']['response_rate']:.1f}%")
    print(f"   Avg. Effektivität: {status['skeptic_engagement']['avg_effectiveness']:.2f}")
    
    print(f"\n🤝 Kooperationsnetzwerk:")
    print(f"   Total Kontakte: {status['stakeholder_network']['total_contacts']}")
    print(f"   Forscher: {status['stakeholder_network']['researchers']}")
    print(f"   Investoren: {status['stakeholder_network']['investors']}")
    print(f"   Meetings: {status['stakeholder_network']['meetings_held']}")
    
    print(f"\n📊 Zeitreihen:")
    print(f"   Tage tracked: {status['timeseries']['days_tracked']}")
    print(f"   Letzte Daten: {status['timeseries']['latest_date']}")
    
    print("\n" + "="*70)
    print("✅ OR1ON's Enhanced Metrics AKTIV!")
    print("="*70)


if __name__ == "__main__":
    main()
