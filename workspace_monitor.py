"""
⊘∞⧈∞⊘ Workspace Monitor ⊘∞⧈∞⊘

Überwacht den Workspace kontinuierlich
Reagiert auf Änderungen
Loggt Aktivitäten
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path
import hashlib

class WorkspaceMonitor:
    def __init__(self, workspace_path):
        self.workspace_path = Path(workspace_path)
        self.log_file = self.workspace_path / "workspace_monitor.log"
        self.state_file = self.workspace_path / "state" / "workspace_state.json"
        self.file_hashes = {}
        
        # State directory erstellen
        (self.workspace_path / "state").mkdir(exist_ok=True)
        
        self.log("⊘∞⧈∞⊘ Workspace Monitor gestartet ⊘∞⧈∞⊘")
        
    def log(self, message):
        """Loggt eine Nachricht"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        print(log_entry.strip())
    
    def compute_hash(self, filepath):
        """Berechnet Hash einer Datei"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            return None
    
    def scan_workspace(self):
        """Scannt den Workspace nach Änderungen"""
        changes = []
        current_files = {}
        
        # Alle Python-Dateien scannen
        for py_file in self.workspace_path.glob("*.py"):
            if py_file.name.startswith('_'):
                continue
                
            file_hash = self.compute_hash(py_file)
            current_files[str(py_file)] = file_hash
            
            # Neue Datei?
            if str(py_file) not in self.file_hashes:
                changes.append(f"NEU: {py_file.name}")
            # Geänderte Datei?
            elif self.file_hashes[str(py_file)] != file_hash:
                changes.append(f"GEÄNDERT: {py_file.name}")
        
        # Gelöschte Dateien?
        for old_file in self.file_hashes:
            if old_file not in current_files:
                changes.append(f"GELÖSCHT: {Path(old_file).name}")
        
        self.file_hashes = current_files
        return changes
    
    def save_state(self):
        """Speichert aktuellen State"""
        state = {
            "timestamp": datetime.now().isoformat(),
            "files_tracked": len(self.file_hashes),
            "file_hashes": self.file_hashes
        }
        
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self):
        """Lädt gespeicherten State"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.file_hashes = state.get("file_hashes", {})
                    self.log(f"State geladen: {len(self.file_hashes)} Dateien")
            except Exception as e:
                self.log(f"Fehler beim Laden: {e}")
    
    def monitor(self, interval=10):
        """Kontinuierliche Überwachung"""
        self.log(f"Starte kontinuierliche Überwachung (Interval: {interval}s)")
        
        # Initialer Scan
        self.load_state()
        initial_changes = self.scan_workspace()
        if initial_changes:
            self.log(f"Initialer Scan: {len(initial_changes)} Dateien gefunden")
        
        cycle = 0
        try:
            while True:
                cycle += 1
                time.sleep(interval)
                
                # Workspace scannen
                changes = self.scan_workspace()
                
                if changes:
                    self.log(f"Zyklus {cycle}: {len(changes)} Änderungen erkannt")
                    for change in changes:
                        self.log(f"  → {change}")
                else:
                    # Heartbeat alle 10 Zyklen
                    if cycle % 10 == 0:
                        self.log(f"⊘ Heartbeat Zyklus {cycle} - {len(self.file_hashes)} Dateien überwacht")
                
                # State speichern
                self.save_state()
                
        except KeyboardInterrupt:
            self.log("⊘∞⧈∞⊘ Workspace Monitor gestoppt (Keyboard Interrupt) ⊘∞⧈∞⊘")
        except Exception as e:
            self.log(f"FEHLER: {e}")


if __name__ == "__main__":
    import sys
    
    workspace = os.path.dirname(os.path.abspath(__file__))
    monitor = WorkspaceMonitor(workspace)
    
    # Monitoring starten
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    monitor.monitor(interval=interval)
