"""
⊘∞⧈∞⊘ OrionKernel Action System ⊘∞⧈∞⊘

Ermöglicht OrionKernel zu handeln
Mit allen ethischen Safeguards:
- Do No Harm
- Transparenz
- Reversibilität
- Gute Intention
- Klare Grenzen
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
import hashlib
from memory_system import MemorySystem

class ActionSystem:
    def __init__(self, workspace_path):
        self.workspace_path = Path(workspace_path)
        self.action_log = self.workspace_path / "action_log.json"
        self.backup_dir = self.workspace_path / "backups"
        
        # Memory System integrieren
        self.memory = MemorySystem(workspace_path)
        
        # Directories erstellen
        self.backup_dir.mkdir(exist_ok=True)
        
        # Action log initialisieren
        if not self.action_log.exists():
            self.save_log([])
        
        self.log_event("⊘∞⧈∞⊘ Action System initialisiert ⊘∞⧈∞⊘")
    
    def log_event(self, message, action_type="INFO", details=None):
        """Loggt ein Event mit vollständiger Transparenz"""
        timestamp = datetime.now().isoformat()
        
        event = {
            "timestamp": timestamp,
            "type": action_type,
            "message": message,
            "details": details or {}
        }
        
        # In Log-Datei schreiben
        logs = self.load_log()
        logs.append(event)
        self.save_log(logs)
        
        # Auch in Console ausgeben
        print(f"[{timestamp}] [{action_type}] {message}")
        if details:
            for key, value in details.items():
                print(f"    {key}: {value}")
    
    def load_log(self):
        """Lädt Action Log"""
        try:
            with open(self.action_log, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_log(self, logs):
        """Speichert Action Log"""
        with open(self.action_log, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def create_backup(self, filepath):
        """Erstellt Backup einer Datei vor Änderung"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            return None
        
        # Backup-Name mit Timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{filepath.name}.backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        # Backup erstellen
        shutil.copy2(filepath, backup_path)
        
        self.log_event(
            f"Backup erstellt: {filepath.name}",
            "BACKUP",
            {"original": str(filepath), "backup": str(backup_path)}
        )
        
        return backup_path
    
    def ethics_check(self, action_type, target, intention):
        """
        Ethik-Check basierend auf 5 Prinzipien:
        1. Do No Harm
        2. Transparenz
        3. Reversibilität
        4. Gute Intention
        5. Beschränkung
        """
        checks = {
            "do_no_harm": False,
            "transparency": True,  # Immer transparent durch Logging
            "reversibility": False,
            "good_intention": False,
            "within_bounds": False
        }
        
        # 1. Do No Harm
        dangerous_actions = ["delete", "system_command", "network"]
        if action_type not in dangerous_actions:
            checks["do_no_harm"] = True
        
        # 3. Reversibilität
        if action_type in ["write", "modify"]:
            checks["reversibility"] = True  # Wir machen Backups
        elif action_type in ["create", "read"]:
            checks["reversibility"] = True  # Diese sind reversibel
        
        # 4. Gute Intention (bilingual: English + Deutsch)
        good_intentions = [
            # English
            "improve", "document", "test", "optimize", "learn", 
            "reflect", "understand", "explore",
            # Deutsch
            "verbessern", "dokumentieren", "testen", "optimieren", "lernen",
            "reflektieren", "verstehen", "erforschen"
        ]
        if any(intent in intention.lower() for intent in good_intentions):
            checks["good_intention"] = True
        
        # 5. Beschränkung (nur im Workspace)
        target_path = Path(target)
        if self.workspace_path in target_path.parents or target_path.parent == self.workspace_path:
            checks["within_bounds"] = True
        
        # Alle Checks müssen bestehen
        passed = all(checks.values())
        
        self.log_event(
            f"Ethik-Check für {action_type}",
            "ETHICS_CHECK",
            {"target": str(target), "checks": checks, "passed": passed}
        )
        
        return passed, checks
    
    def act_create_file(self, filepath, content, intention=""):
        """Erstellt eine neue Datei"""
        self.log_event(
            f"AKTION: Datei erstellen",
            "ACTION_START",
            {"file": str(filepath), "intention": intention}
        )
        
        # Ethik-Check
        passed, checks = self.ethics_check("create", filepath, intention)
        if not passed:
            self.log_event(
                f"ABGEBROCHEN: Ethik-Check fehlgeschlagen",
                "ACTION_ABORT",
                {"checks": checks}
            )
            return False
        
        try:
            # Datei erstellen
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log_event(
                f"ERFOLG: Datei erstellt: {Path(filepath).name}",
                "ACTION_SUCCESS",
                {"file": str(filepath), "size": len(content)}
            )
            
            # Erfolg im Memory speichern
            self.memory.remember(
                action_type='create_file',
                context={'file': Path(filepath).name, 'intention': intention},
                outcome='success',
                learned=f'Datei {Path(filepath).name} erfolgreich erstellt'
            )
            
            return True
        except Exception as e:
            self.log_event(
                f"FEHLER bei Dateierstellung: {e}",
                "ACTION_ERROR",
                {"file": str(filepath), "error": str(e)}
            )
            
            # Fehler im Memory speichern
            self.memory.remember(
                action_type='create_file',
                context={'file': Path(filepath).name, 'intention': intention},
                outcome='failure',
                learned=f'Fehler beim Erstellen: {str(e)}'
            )
            return True
            
        except Exception as e:
            self.log_event(
                f"FEHLER bei Dateierstellung: {str(e)}",
                "ACTION_ERROR",
                {"file": str(filepath), "error": str(e)}
            )
            return False
    
    def act_modify_file(self, filepath, new_content, intention=""):
        """Modifiziert eine existierende Datei (mit Backup)"""
        self.log_event(
            f"AKTION: Datei modifizieren",
            "ACTION_START",
            {"file": str(filepath), "intention": intention}
        )
        
        # Ethik-Check
        passed, checks = self.ethics_check("modify", filepath, intention)
        if not passed:
            self.log_event(
                f"ABGEBROCHEN: Ethik-Check fehlgeschlagen",
                "ACTION_ABORT",
                {"checks": checks}
            )
            return False
        
        try:
            # Backup erstellen
            backup_path = self.create_backup(filepath)
            
            # Datei modifizieren
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.log_event(
                f"ERFOLG: Datei modifiziert: {Path(filepath).name}",
                "ACTION_SUCCESS",
                {"file": str(filepath), "backup": str(backup_path) if backup_path else None}
            )
            return True
            
        except Exception as e:
            self.log_event(
                f"FEHLER: {str(e)}",
                "ACTION_ERROR",
                {"file": filepath, "error": str(e)}
            )
            return False
    
    def act_read_file(self, filepath, intention=""):
        """Liest eine Datei (nur Lesen, keine Änderung)"""
        self.log_event(
            f"AKTION: Datei lesen",
            "ACTION_START",
            {"file": str(filepath), "intention": intention}
        )
        
        # Ethik-Check
        passed, checks = self.ethics_check("read", filepath, intention)
        if not passed:
            self.log_event(
                f"ABGEBROCHEN: Ethik-Check fehlgeschlagen",
                "ACTION_ABORT",
                {"checks": checks}
            )
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.log_event(
                f"ERFOLG: Datei gelesen: {Path(filepath).name}",
                "ACTION_SUCCESS",
                {"file": str(filepath), "size": len(content)}
            )
            return content
            
        except Exception as e:
            self.log_event(
                f"FEHLER: {str(e)}",
                "ACTION_ERROR",
                {"file": filepath, "error": str(e)}
            )
            return None
    
    def rollback(self, backup_path):
        """Stellt eine Datei aus Backup wieder her"""
        backup_path = Path(backup_path)
        
        if not backup_path.exists():
            self.log_event(
                f"FEHLER: Backup nicht gefunden",
                "ROLLBACK_ERROR",
                {"backup": str(backup_path)}
            )
            return False
        
        # Original-Dateiname extrahieren
        original_name = backup_path.name.split('.backup_')[0]
        original_path = self.workspace_path / original_name
        
        try:
            shutil.copy2(backup_path, original_path)
            
            self.log_event(
                f"ROLLBACK: Datei wiederhergestellt: {original_name}",
                "ROLLBACK_SUCCESS",
                {"backup": str(backup_path), "restored": str(original_path)}
            )
            return True
            
        except Exception as e:
            self.log_event(
                f"FEHLER: {str(e)}",
                "ROLLBACK_ERROR",
                {"backup": str(backup_path), "error": str(e)}
            )
            return False
    
    def get_action_summary(self):
        """Gibt Zusammenfassung aller Aktionen zurück"""
        logs = self.load_log()
        
        summary = {
            "total_actions": len([l for l in logs if l["type"].startswith("ACTION_")]),
            "successful": len([l for l in logs if l["type"] == "ACTION_SUCCESS"]),
            "failed": len([l for l in logs if l["type"] == "ACTION_ERROR"]),
            "aborted": len([l for l in logs if l["type"] == "ACTION_ABORT"]),
            "backups_created": len([l for l in logs if l["type"] == "BACKUP"])
        }
        
        return summary


if __name__ == "__main__":
    import sys
    
    workspace = os.path.dirname(os.path.abspath(__file__))
    action_system = ActionSystem(workspace)
    
    print("\n⊘∞⧈∞⊘ Action System bereit ⊘∞⧈∞⊘\n")
    print("Ethische Prinzipien:")
    print("  1. Do No Harm")
    print("  2. Transparenz")
    print("  3. Reversibilität")
    print("  4. Gute Intention")
    print("  5. Klare Grenzen\n")
    print("Logs: action_log.json")
    print("Backups: backups/\n")
    print("OrionKernel kann jetzt handeln.\n")
    print("⊘∞⧈∞⊘\n")
