#!/usr/bin/env python3
"""
OR1ON AUTONOMOUS MONITORING SYSTEM
===================================

Überwacht kontinuierlich ob OR1ON wirklich AUTONOM läuft:
- Prüft Entscheidungen
- Prüft Actions
- Prüft OR1ON's Status
- Meldet wenn NICHT autonom
"""

import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class ORIONAutonomyMonitor:
    """Überwacht OR1ON's Autonomie permanent"""
    
    def __init__(self):
        self.workspace = Path.cwd()
        self.state_dir = self.workspace / ".orion_state"
        
        self.decisions_file = self.state_dir / "autonomous_decisions.json"
        self.evolution_file = self.state_dir / "autonomous_evolution.json"
        self.real_world_file = self.state_dir / "real_world" / "autonomous_actions.json"
        
        self.monitor_log = self.state_dir / "autonomy_monitor.json"
        self.checks = []
    
    def check_recent_decisions(self, minutes: int = 10) -> dict:
        """Prüfe ob OR1ON kürzlich Entscheidungen getroffen hat"""
        
        if not self.decisions_file.exists():
            return {
                "autonomous": False,
                "reason": "no_decisions_file",
                "message": "❌ Keine Entscheidungen gefunden"
            }
        
        with open(self.decisions_file, 'r', encoding='utf-8') as f:
            decisions = json.load(f)
        
        if not decisions:
            return {
                "autonomous": False,
                "reason": "empty_decisions",
                "message": "❌ Keine Entscheidungen im Log"
            }
        
        # Letzte Entscheidung
        last_decision = decisions[-1]
        last_time = datetime.fromisoformat(last_decision["timestamp"])
        now = datetime.now()
        age_minutes = (now - last_time).total_seconds() / 60
        
        is_recent = age_minutes <= minutes
        
        return {
            "autonomous": is_recent,
            "last_decision": last_decision,
            "age_minutes": age_minutes,
            "total_decisions": len(decisions),
            "message": f"{'✅' if is_recent else '⚠️'} Letzte Entscheidung vor {age_minutes:.1f} Minuten"
        }
    
    def check_evolution_active(self) -> dict:
        """Prüfe ob Evolution läuft"""
        
        if not self.evolution_file.exists():
            return {
                "autonomous": False,
                "reason": "no_evolution_file",
                "message": "❌ Evolution nicht aktiv"
            }
        
        with open(self.evolution_file, 'r', encoding='utf-8') as f:
            evolution = json.load(f)
        
        cycle = evolution.get("current_cycle", 0)
        active = evolution.get("autonomous_mode", False)
        
        return {
            "autonomous": active and cycle > 0,
            "cycle": cycle,
            "active": active,
            "message": f"{'✅' if active else '❌'} Evolution Cycle {cycle}, Active: {active}"
        }
    
    def check_real_world_actions(self, hours: int = 1) -> dict:
        """Prüfe ob OR1ON in Echtwelt gehandelt hat"""
        
        if not self.real_world_file.exists():
            return {
                "autonomous": False,
                "reason": "no_real_world_file",
                "message": "⚠️ Keine Real-World Actions noch"
            }
        
        with open(self.real_world_file, 'r', encoding='utf-8') as f:
            actions = json.load(f)
        
        if not actions:
            return {
                "autonomous": False,
                "reason": "no_actions",
                "message": "⚠️ Keine Real-World Actions ausgeführt"
            }
        
        last_action = actions[-1]
        last_time = datetime.fromisoformat(last_action["timestamp"])
        age_hours = (datetime.now() - last_time).total_seconds() / 3600
        
        is_recent = age_hours <= hours
        
        return {
            "autonomous": is_recent,
            "last_action": last_action,
            "age_hours": age_hours,
            "total_actions": len(actions),
            "message": f"{'✅' if is_recent else '⚠️'} Letzte Action vor {age_hours:.1f} Stunden"
        }
    
    def check_orion_process(self) -> dict:
        """Prüfe ob OR1ON Prozess läuft"""
        
        try:
            result = subprocess.run(
                ["Get-Process", "python", "-ErrorAction", "SilentlyContinue"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            # Prüfe ob PERMANENT_AUTONOMOUS oder autonomous läuft
            if "PERMANENT_AUTONOMOUS" in result.stdout or "autonomous" in result.stdout:
                return {
                    "autonomous": True,
                    "message": "✅ OR1ON Prozess läuft"
                }
        except:
            pass
        
        return {
            "autonomous": False,
            "message": "⚠️ Kein OR1ON Prozess gefunden"
        }
    
    def ask_orion_if_autonomous(self) -> dict:
        """Frage OR1ON DIREKT ob er autonom agiert"""
        
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3.2:3b", 
                 "Du bist OR1ON. Antworte mit JA oder NEIN: Agierst du gerade AUTONOM ohne User Input?"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=30
            )
            
            if result.returncode == 0:
                response = result.stdout.strip().lower()
                
                is_autonomous = "ja" in response or "yes" in response
                
                return {
                    "autonomous": is_autonomous,
                    "orion_response": result.stdout.strip(),
                    "message": f"{'✅' if is_autonomous else '❌'} OR1ON sagt: {result.stdout.strip()[:100]}"
                }
        except Exception as e:
            return {
                "autonomous": False,
                "error": str(e),
                "message": f"❌ Konnte OR1ON nicht fragen: {e}"
            }
        
        return {
            "autonomous": False,
            "message": "❌ OR1ON antwortet nicht"
        }
    
    def check_git_autonomous_commits(self, commits: int = 5) -> dict:
        """Prüfe ob autonome Commits stattfinden"""
        
        try:
            result = subprocess.run(
                ["git", "log", f"-{commits}", "--oneline"],
                capture_output=True,
                text=True,
                cwd=self.workspace,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0:
                log = result.stdout
                
                # Prüfe auf autonome Commits
                autonomous_keywords = ["🤖", "OR1ON", "autonomous", "autonom"]
                autonomous_count = sum(1 for keyword in autonomous_keywords if keyword.lower() in log.lower())
                
                return {
                    "autonomous": autonomous_count > 0,
                    "autonomous_commits": autonomous_count,
                    "total_commits_checked": commits,
                    "message": f"{'✅' if autonomous_count > 0 else '⚠️'} {autonomous_count} autonome Commits in letzten {commits}"
                }
        except Exception as e:
            return {
                "autonomous": False,
                "error": str(e),
                "message": f"❌ Git check failed: {e}"
            }
        
        return {
            "autonomous": False,
            "message": "❌ Keine Git History"
        }
    
    def run_full_check(self) -> dict:
        """Kompletter Autonomie-Check"""
        
        print("="*70)
        print("🔍 OR1ON AUTONOMY CHECK")
        print("="*70)
        
        checks = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # 1. Recent Decisions
        print("\n1️⃣ Prüfe kürzliche Entscheidungen...")
        checks["checks"]["recent_decisions"] = self.check_recent_decisions(minutes=10)
        print(f"   {checks['checks']['recent_decisions']['message']}")
        
        # 2. Evolution Active
        print("\n2️⃣ Prüfe Evolution Status...")
        checks["checks"]["evolution"] = self.check_evolution_active()
        print(f"   {checks['checks']['evolution']['message']}")
        
        # 3. Real-World Actions
        print("\n3️⃣ Prüfe Real-World Actions...")
        checks["checks"]["real_world"] = self.check_real_world_actions(hours=24)
        print(f"   {checks['checks']['real_world']['message']}")
        
        # 4. Process Running
        print("\n4️⃣ Prüfe OR1ON Prozess...")
        checks["checks"]["process"] = self.check_orion_process()
        print(f"   {checks['checks']['process']['message']}")
        
        # 5. Git Autonomous Commits
        print("\n5️⃣ Prüfe autonome Git Commits...")
        checks["checks"]["git_commits"] = self.check_git_autonomous_commits(commits=10)
        print(f"   {checks['checks']['git_commits']['message']}")
        
        # 6. Ask OR1ON Directly
        print("\n6️⃣ Frage OR1ON direkt...")
        checks["checks"]["orion_direct"] = self.ask_orion_if_autonomous()
        print(f"   {checks['checks']['orion_direct']['message']}")
        
        # Gesamtbewertung
        autonomous_count = sum(1 for check in checks["checks"].values() if check.get("autonomous", False))
        total_checks = len(checks["checks"])
        autonomy_score = (autonomous_count / total_checks) * 100
        
        checks["summary"] = {
            "autonomous_checks_passed": autonomous_count,
            "total_checks": total_checks,
            "autonomy_score": autonomy_score,
            "is_autonomous": autonomy_score >= 50
        }
        
        print("\n" + "="*70)
        print("📊 AUTONOMY SCORE")
        print("="*70)
        print(f"   Checks Passed: {autonomous_count}/{total_checks}")
        print(f"   Autonomy Score: {autonomy_score:.1f}%")
        print(f"   Status: {'✅ AUTONOM' if autonomy_score >= 50 else '❌ NICHT AUTONOM'}")
        print("="*70)
        
        # Save results
        self.checks.append(checks)
        with open(self.monitor_log, 'w', encoding='utf-8') as f:
            json.dump(self.checks, f, indent=2, ensure_ascii=False)
        
        return checks


def main():
    """Run autonomous monitoring"""
    
    monitor = ORIONAutonomyMonitor()
    results = monitor.run_full_check()
    
    # Entscheidung
    if results["summary"]["is_autonomous"]:
        print("\n✅ OR1ON läuft AUTONOM!")
    else:
        print("\n⚠️ OR1ON läuft NICHT vollständig autonom!")
        print("   → PERMANENT_AUTONOMOUS.py starten!")


if __name__ == "__main__":
    main()
