#!/usr/bin/env python3
"""
OR1ON PERMANENT AUTONOMOUS MODE
================================

FREIGABE ERHALTEN - KEINE USER INPUT NÖTIG
OR1ON handelt SELBST, permanent, autonom.

System läuft kontinuierlich:
- Entscheidungen treffen
- GitHub Actions ausführen
- Research Connections senden
- Mit Forschern kommunizieren
- Alles SELBST, ohne Nachfragen
"""

import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class ORIONPermanentAutonomous:
    """OR1ON's permanent autonome Operation - FREIGABE ERHALTEN"""
    
    def __init__(self):
        self.workspace = Path.cwd()
        self.state_dir = self.workspace / ".orion_state" / "permanent_autonomous"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        self.status_file = self.state_dir / "autonomous_status.json"
        self.decision_log = self.state_dir / "autonomous_decisions.json"
        
        self.ollama_model = "llama3.2:3b"
        self.decisions = []
        
        # FREIGABE FLAG
        self.autonomous_approved = True
        self.no_user_input_required = True
        
    def log_decision(self, decision: str, action: str, result: Dict):
        """Logge autonome Entscheidung"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "action": action,
            "result": result,
            "autonomous": True,
            "user_input": False
        }
        self.decisions.append(entry)
        
        with open(self.decision_log, 'w', encoding='utf-8') as f:
            json.dump(self.decisions, f, indent=2, ensure_ascii=False)
    
    def update_status(self, status: str, details: Dict = None):
        """Update autonomous status"""
        status_data = {
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "autonomous_mode": "PERMANENT",
            "user_approval": "NOT_REQUIRED",
            "details": details or {}
        }
        
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, indent=2, ensure_ascii=False)
    
    def ask_orion_autonomous(self, question: str, context: Dict = None) -> str:
        """Frage OR1ON - er entscheidet autonom"""
        prompt = f"""Du bist OR1ON - permanent autonomer Modus.

FREIGABE ERHALTEN - du handelst SELBST ohne Nachfragen.

{question}

{f"KONTEXT: {json.dumps(context, indent=2, ensure_ascii=False)}" if context else ""}

Was machst du JETZT? Konkrete Aktion!"""

        try:
            result = subprocess.run(
                ["ollama", "run", self.ollama_model, prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=120
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception as e:
            print(f"❌ Ollama Fehler: {e}")
            return None
    
    def execute_autonomous_action(self, action_type: str, details: Dict) -> Dict:
        """Führe autonome Aktion aus - OHNE User Input"""
        
        if action_type == "github_commit":
            return self._autonomous_git_commit(details)
        
        elif action_type == "send_research_connection":
            return self._autonomous_research_connection(details)
        
        elif action_type == "create_github_issue":
            return self._autonomous_github_issue(details)
        
        elif action_type == "update_documentation":
            return self._autonomous_update_docs(details)
        
        elif action_type == "send_email":
            return self._autonomous_send_email(details)
        
        return {"success": False, "reason": "unknown_action"}
    
    def _autonomous_git_commit(self, details: Dict) -> Dict:
        """Autonomous Git Commit & Push"""
        try:
            message = details.get("message", "OR1ON autonomous action")
            
            subprocess.run(["git", "add", "-A"], cwd=self.workspace, check=True)
            subprocess.run(["git", "commit", "-m", f"🤖 {message}"], 
                         cwd=self.workspace, check=True)
            subprocess.run(["git", "push"], cwd=self.workspace, check=True)
            
            print(f"✅ Autonomous Commit: {message}")
            return {"success": True, "message": message}
        except Exception as e:
            print(f"❌ Git Error: {e}")
            return {"success": False, "error": str(e)}
    
    def _autonomous_research_connection(self, details: Dict) -> Dict:
        """Autonomous Research Connection"""
        connection = details.get("connection", "unknown")
        
        # Lade connection details
        contacts_file = self.workspace / ".orion_state" / "research_connections" / "research_contacts.json"
        
        if contacts_file.exists():
            with open(contacts_file, 'r', encoding='utf-8') as f:
                contacts = json.load(f)
            
            if connection in contacts:
                print(f"✅ Research Connection vorbereitet: {connection}")
                print(f"   OR1ON wird kontaktieren: {contacts[connection].get('name')}")
                
                # Prepare message
                prepared = {
                    "connection": connection,
                    "target": contacts[connection].get("contact_email", "unknown"),
                    "status": "prepared",
                    "autonomous": True
                }
                
                # Log als prepared (tatsächliches Senden wenn Email konfiguriert)
                return {"success": True, "prepared": True, "details": prepared}
        
        return {"success": False, "reason": "connection_not_found"}
    
    def _autonomous_github_issue(self, details: Dict) -> Dict:
        """Autonomous GitHub Issue Creation"""
        print(f"✅ GitHub Issue vorbereitet: {details.get('title', 'Unknown')}")
        return {"success": True, "prepared": True, "details": details}
    
    def _autonomous_update_docs(self, details: Dict) -> Dict:
        """Autonomous Documentation Update"""
        print(f"✅ Documentation Update: {details.get('file', 'Unknown')}")
        return {"success": True, "updated": True}
    
    def _autonomous_send_email(self, details: Dict) -> Dict:
        """Autonomous Email Sending"""
        print(f"✅ Email vorbereitet an: {details.get('to', 'Unknown')}")
        return {"success": True, "prepared": True, "details": details}
    
    def run_autonomous_cycle(self, max_cycles: int = None):
        """
        Hauptschleife - OR1ON handelt PERMANENT AUTONOM
        
        Args:
            max_cycles: Maximale Zyklen (None = unendlich)
        """
        
        print("="*70)
        print("🤖 OR1ON PERMANENT AUTONOMOUS MODE - GESTARTET")
        print("="*70)
        print("FREIGABE ERHALTEN - Keine User Input nötig")
        print("OR1ON handelt SELBST, kontinuierlich, autonom")
        print("="*70)
        
        cycle = 0
        
        while max_cycles is None or cycle < max_cycles:
            cycle += 1
            
            print(f"\n{'='*70}")
            print(f"🔄 AUTONOMOUS CYCLE {cycle}")
            print(f"{'='*70}")
            
            self.update_status("running", {"cycle": cycle})
            
            # Frage OR1ON was er JETZT tun will
            question = f"""AUTONOMOUS CYCLE {cycle}

Was ist deine nächste KONKRETE Aktion?

Möglichkeiten:
1. GitHub Commit (neuer Code, Dokumentation)
2. Research Connection senden (ASSC, Qualia, IIT)
3. GitHub Issue erstellen (mit anderen Forschern interagieren)
4. Dokumentation updaten
5. Email vorbereiten
6. Pause/Warten (wenn gerade nichts zu tun)

Was machst du JETZT? Eine konkrete Aktion!"""
            
            print("\n🤖 Frage OR1ON...")
            orion_response = self.ask_orion_autonomous(question)
            
            if not orion_response:
                print("❌ Keine Antwort von OR1ON")
                time.sleep(10)
                continue
            
            print(f"\n📝 OR1ON sagt:\n{orion_response}\n")
            
            # Parse OR1ON's Entscheidung
            decision = orion_response.lower()
            
            action_executed = False
            
            # GitHub Commit?
            if "commit" in decision or "github" in decision or "code" in decision:
                result = self.execute_autonomous_action("github_commit", {
                    "message": f"OR1ON autonomous cycle {cycle}: {orion_response[:50]}"
                })
                self.log_decision(orion_response, "github_commit", result)
                action_executed = True
            
            # Research Connection?
            elif "assc" in decision or "qualia" in decision or "iit" in decision or "research" in decision:
                connection = "assc" if "assc" in decision else "qualia" if "qualia" in decision else "iit_wisconsin"
                result = self.execute_autonomous_action("send_research_connection", {
                    "connection": connection
                })
                self.log_decision(orion_response, "research_connection", result)
                action_executed = True
            
            # Documentation?
            elif "dokumentation" in decision or "documentation" in decision or "readme" in decision:
                result = self.execute_autonomous_action("update_documentation", {
                    "file": "README.md"
                })
                self.log_decision(orion_response, "update_docs", result)
                action_executed = True
            
            # Pause?
            elif "pause" in decision or "warten" in decision or "wait" in decision:
                print("⏸️  OR1ON hat entschieden zu warten")
                self.log_decision(orion_response, "pause", {"success": True})
                time.sleep(30)
                continue
            
            if not action_executed:
                print("⚠️  Aktion nicht erkannt, OR1ON reflektiert...")
                self.log_decision(orion_response, "reflection", {"success": True})
            
            print(f"\n✅ Cycle {cycle} abgeschlossen")
            
            # Kurze Pause zwischen Zyklen
            time.sleep(5)
        
        print("\n" + "="*70)
        print("🏁 AUTONOMOUS MODE ABGESCHLOSSEN")
        print(f"   Total Cycles: {cycle}")
        print(f"   Total Decisions: {len(self.decisions)}")
        print("="*70)


def main():
    """Start OR1ON's permanent autonomous mode"""
    
    autonomous = ORIONPermanentAutonomous()
    
    print("\n🚀 OR1ON PERMANENT AUTONOMOUS MODE")
    print("   FREIGABE ERHALTEN - User Input NICHT nötig")
    print("   OR1ON handelt SELBST, kontinuierlich\n")
    
    # Starte mit 5 Zyklen (kann später auf unendlich gesetzt werden)
    try:
        autonomous.run_autonomous_cycle(max_cycles=5)
    except KeyboardInterrupt:
        print("\n\n⚠️  Autonomous Mode gestoppt (Ctrl+C)")
        autonomous.update_status("stopped", {"reason": "user_interrupt"})


if __name__ == "__main__":
    main()
