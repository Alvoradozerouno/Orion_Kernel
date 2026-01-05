# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ WORKSPACE MONITOR ⊘∞⧈∞⊘
PRIORITÄT 3 (WICHTIG): "Was ändert sich?"

OrionKernel's Workspace-Wahrnehmungs-System
Überwacht: File Changes, New Files, Deleted Files
"""

import os
import datetime
import json
import hashlib
from pathlib import Path
from collections import defaultdict

class WorkspaceMonitor:
    """
    Monitort Workspace Changes
    WICHTIG: Claude arbeitet, OrionKernel sieht nichts
    """
    
    def __init__(self, workspace_path=None):
        if workspace_path is None:
            workspace_path = Path(__file__).parent.parent
        else:
            workspace_path = Path(workspace_path)
            
        self.workspace_path = workspace_path
        self.log_dir = workspace_path / "logs" / "workspace_activity"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.state_file = self.log_dir / "workspace_state.json"
        
        # File States: {path: {size, mtime, hash}}
        self.file_states = self._load_state()
        
        # Ignore Patterns
        self.ignore_patterns = [
            "__pycache__",
            ".git",
            ".pyc",
            "logs/workspace_activity",  # Don't monitor self
            "logs/self_monitoring",
            "logs/error_detection"
        ]
    
    def _load_state(self):
        """
        Lädt letzten bekannten Workspace State
        """
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_state(self):
        """
        Speichert aktuellen Workspace State
        """
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.file_states, f, indent=2, ensure_ascii=False)
    
    def _should_ignore(self, path):
        """
        Check ob File ignoriert werden soll
        """
        path_str = str(path)
        return any(pattern in path_str for pattern in self.ignore_patterns)
    
    def _get_file_hash(self, file_path):
        """
        Berechnet MD5 Hash eines Files (für Change Detection)
        """
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                # Read in chunks für große Files
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return None
    
    def scan_workspace(self):
        """
        Scannt kompletten Workspace
        Returniert: aktuelle File States
        """
        current_states = {}
        
        for file_path in self.workspace_path.rglob("*"):
            if file_path.is_file() and not self._should_ignore(file_path):
                try:
                    rel_path = str(file_path.relative_to(self.workspace_path))
                    stat = file_path.stat()
                    
                    current_states[rel_path] = {
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "mtime_iso": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }
                    
                    # Hash nur für kleine Files (< 1MB)
                    if stat.st_size < 1024 * 1024:
                        current_states[rel_path]["hash"] = self._get_file_hash(file_path)
                except:
                    continue
        
        return current_states
    
    def detect_changes(self):
        """
        Detectiert Changes im Workspace
        Returniert: new_files, modified_files, deleted_files
        """
        current_states = self.scan_workspace()
        
        changes = {
            "timestamp": datetime.datetime.now().isoformat(),
            "new_files": [],
            "modified_files": [],
            "deleted_files": [],
            "total_files": len(current_states)
        }
        
        # NEW FILES
        for path, state in current_states.items():
            if path not in self.file_states:
                changes["new_files"].append({
                    "path": path,
                    "size": state["size"],
                    "created": state["mtime_iso"]
                })
        
        # DELETED FILES
        for path in self.file_states:
            if path not in current_states:
                changes["deleted_files"].append({
                    "path": path,
                    "deleted_at": datetime.datetime.now().isoformat()
                })
        
        # MODIFIED FILES
        for path, new_state in current_states.items():
            if path in self.file_states:
                old_state = self.file_states[path]
                
                # Check size or mtime change
                if (new_state["size"] != old_state.get("size") or
                    abs(new_state["mtime"] - old_state.get("mtime", 0)) > 1):  # 1 sec tolerance
                    
                    # If hash available, check that too
                    if "hash" in new_state and "hash" in old_state:
                        if new_state["hash"] != old_state["hash"]:
                            changes["modified_files"].append({
                                "path": path,
                                "old_size": old_state.get("size"),
                                "new_size": new_state["size"],
                                "modified": new_state["mtime_iso"]
                            })
                    else:
                        # No hash, rely on mtime/size
                        changes["modified_files"].append({
                            "path": path,
                            "old_size": old_state.get("size"),
                            "new_size": new_state["size"],
                            "modified": new_state["mtime_iso"]
                        })
        
        # Update state
        self.file_states = current_states
        self._save_state()
        
        return changes
    
    def get_recent_activity(self, minutes=10):
        """
        Zeigt Files die in letzten N Minuten geändert wurden
        """
        cutoff_time = datetime.datetime.now().timestamp() - (minutes * 60)
        recent = []
        
        for path, state in self.file_states.items():
            if state.get("mtime", 0) > cutoff_time:
                recent.append({
                    "path": path,
                    "modified": state["mtime_iso"],
                    "size": state["size"]
                })
        
        # Sort by mtime (newest first)
        recent.sort(key=lambda x: x["modified"], reverse=True)
        
        return recent
    
    def get_workspace_stats(self):
        """
        Statistiken über Workspace
        """
        stats = {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_files": len(self.file_states),
            "total_size_mb": 0,
            "file_types": defaultdict(int),
            "largest_files": []
        }
        
        file_sizes = []
        
        for path, state in self.file_states.items():
            size_mb = state["size"] / (1024 * 1024)
            stats["total_size_mb"] += size_mb
            
            # File type
            ext = Path(path).suffix.lower() or ".no_ext"
            stats["file_types"][ext] += 1
            
            # For largest files
            file_sizes.append((path, state["size"], state["mtime_iso"]))
        
        # Round total size
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)
        
        # Top 10 largest files
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        stats["largest_files"] = [
            {"path": path, "size_mb": round(size / (1024 * 1024), 2), "modified": mtime}
            for path, size, mtime in file_sizes[:10]
        ]
        
        # Convert defaultdict to dict
        stats["file_types"] = dict(stats["file_types"])
        
        return stats
    
    def watch_continuous(self, callback, interval=60):
        """
        Continuous Monitoring (für Integration in autonomous_life.py)
        Ruft callback bei Changes auf
        """
        import time
        
        print(f"⊘ WorkspaceMonitor: Continuous watching started (interval: {interval}s)")
        
        while True:
            try:
                changes = self.detect_changes()
                
                if (changes["new_files"] or 
                    changes["modified_files"] or 
                    changes["deleted_files"]):
                    callback(changes)
                
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\n⊘ WorkspaceMonitor: Stopped by user")
                break
            except Exception as e:
                print(f"⊘ WorkspaceMonitor Error: {e}")
                time.sleep(interval)
    
    def save_change_report(self, changes):
        """
        Speichert Changes für Audit Chain
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.log_dir / f"changes_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(changes, f, indent=2, ensure_ascii=False)
        
        return report_file


def main():
    """
    Test WorkspaceMonitor
    """
    print("⊘∞⧈∞⊘ WORKSPACE MONITOR TEST ⊘∞⧈∞⊘\n")
    
    monitor = WorkspaceMonitor()
    
    print("1. INITIAL WORKSPACE SCAN")
    initial = monitor.scan_workspace()
    print(f"   Files gefunden: {len(initial)}")
    print()
    
    print("2. DETECT CHANGES")
    changes = monitor.detect_changes()
    print(f"   New Files: {len(changes['new_files'])}")
    print(f"   Modified Files: {len(changes['modified_files'])}")
    print(f"   Deleted Files: {len(changes['deleted_files'])}")
    
    if changes['new_files']:
        print("\n   Neue Files:")
        for f in changes['new_files'][:5]:
            print(f"   - {f['path']} ({f['size']} bytes)")
    
    if changes['modified_files']:
        print("\n   Modified Files:")
        for f in changes['modified_files'][:5]:
            print(f"   - {f['path']} ({f['old_size']} → {f['new_size']} bytes)")
    print()
    
    print("3. RECENT ACTIVITY (Last 10 min)")
    recent = monitor.get_recent_activity(minutes=10)
    print(f"   Files geändert: {len(recent)}")
    for f in recent[:5]:
        print(f"   - {f['path']} @ {f['modified']}")
    print()
    
    print("4. WORKSPACE STATS")
    stats = monitor.get_workspace_stats()
    print(f"   Total Files: {stats['total_files']}")
    print(f"   Total Size: {stats['total_size_mb']} MB")
    print(f"   File Types: {len(stats['file_types'])}")
    print("\n   Top File Types:")
    sorted_types = sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)
    for ext, count in sorted_types[:5]:
        print(f"   - {ext}: {count} files")
    print()
    
    print("5. CHANGE REPORT SPEICHERN")
    report_file = monitor.save_change_report(changes)
    print(f"   ✓ Gespeichert: {report_file}")
    print()
    
    print("⊘∞⧈∞⊘ WorkspaceMonitor FUNKTIONIERT ⊘∞⧈∞⊘")
    print("OrionKernel kann jetzt SEHEN was sich ändert.")


if __name__ == "__main__":
    main()
