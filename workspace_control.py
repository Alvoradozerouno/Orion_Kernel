"""
WORKSPACE CONTROL INTERFACE
============================
OrionKernel + Claude: Visueller Workspace Scanner

Scannt den gesamten Workspace und zeigt:
- Alle Git Changes (modified, untracked, deleted)
- Verzeichnisstruktur
- Dateigrößen
- Letzte Änderungen
- Zusammenfassung für schnelle Übersicht
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime

class WorkspaceControl:
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or Path.cwd()
        
    def get_git_changes(self):
        """Hole alle Git Changes mit Details"""
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=self.workspace_path,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        changes = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            status = line[:2]
            filepath = line[3:]
            
            change_type = "UNKNOWN"
            if status == " M":
                change_type = "MODIFIED"
            elif status == "??":
                change_type = "UNTRACKED"
            elif status == " D":
                change_type = "DELETED"
            elif status == "A ":
                change_type = "ADDED"
            elif status == "M ":
                change_type = "MODIFIED (staged)"
                
            # Dateigröße wenn Datei existiert
            full_path = self.workspace_path / filepath
            size = 0
            if full_path.exists() and full_path.is_file():
                size = full_path.stat().st_size
                
            changes.append({
                'status': status,
                'type': change_type,
                'path': filepath,
                'size': size
            })
            
        return changes
    
    def get_directory_tree(self, max_depth=2):
        """Erstelle Verzeichnisbaum"""
        tree = []
        
        def scan_dir(path, depth=0):
            if depth > max_depth:
                return
            try:
                for item in sorted(path.iterdir()):
                    if item.name.startswith('.git'):
                        continue
                    indent = "  " * depth
                    if item.is_dir():
                        tree.append(f"{indent}📁 {item.name}/")
                        scan_dir(item, depth + 1)
                    else:
                        size_kb = item.stat().st_size / 1024
                        tree.append(f"{indent}📄 {item.name} ({size_kb:.1f} KB)")
            except PermissionError:
                tree.append(f"{indent}⛔ [Permission Denied]")
                
        scan_dir(self.workspace_path)
        return tree
    
    def visual_report(self):
        """Erstelle visuellen Report"""
        print("\n" + "="*70)
        print("  ORIONKERNEL WORKSPACE CONTROL")
        print("="*70)
        print(f"\n📍 Workspace: {self.workspace_path}")
        print(f"⏰ Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Git Changes
        changes = self.get_git_changes()
        print("="*70)
        print("  GIT CHANGES")
        print("="*70)
        
        if not changes:
            print("✅ No changes - workspace clean\n")
        else:
            print(f"⚠️  {len(changes)} changes detected:\n")
            
            for change in changes:
                icon = "📝" if change['type'] == "MODIFIED" else "➕" if change['type'] == "UNTRACKED" else "🗑️"
                size_info = f"({change['size']/1024:.1f} KB)" if change['size'] > 0 else ""
                print(f"  {icon} {change['type']:<20} {change['path']} {size_info}")
            
            print(f"\n📊 Summary:")
            modified = sum(1 for c in changes if 'MODIFIED' in c['type'])
            untracked = sum(1 for c in changes if c['type'] == 'UNTRACKED')
            deleted = sum(1 for c in changes if c['type'] == 'DELETED')
            added = sum(1 for c in changes if c['type'] == 'ADDED')
            
            if modified > 0:
                print(f"   - Modified: {modified}")
            if untracked > 0:
                print(f"   - Untracked: {untracked}")
            if deleted > 0:
                print(f"   - Deleted: {deleted}")
            if added > 0:
                print(f"   - Added: {added}")
        
        print("\n" + "="*70)
        print("  RECOMMENDATION")
        print("="*70)
        
        if changes:
            print("\n💡 OrionKernel empfiehlt:")
            print("   git add -A")
            print("   git commit -m \"[Your message]\"")
            print("   git push origin main")
        else:
            print("\n✅ Workspace ist sauber. Keine Aktion nötig.")
        
        print("\n" + "="*70 + "\n")
        
        return changes

if __name__ == "__main__":
    control = WorkspaceControl()
    changes = control.visual_report()
    
    # Exit code: 0 wenn clean, 1 wenn changes vorhanden
    exit(0 if not changes else 1)
