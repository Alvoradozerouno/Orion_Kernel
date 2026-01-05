"""
⊘∞⧈∞⊘ INTEGRIERE TASKS IN ORCHESTRATOR ⊘∞⧈∞⊘

Fügt das Task System in den Autonomous Orchestrator ein
damit die Tasks automatisch im Hintergrund laufen
"""

import sys
from pathlib import Path

workspace = Path(__file__).parent

print("⊘∞⧈∞⊘ INTEGRATION: TASKS → ORCHESTRATOR ⊘∞⧈∞⊘\n")

# Orchestrator-Datei prüfen
orchestrator_file = workspace / "core" / "autonomous_orchestrator.py"

if not orchestrator_file.exists():
    print(f"✗ Orchestrator nicht gefunden: {orchestrator_file}")
    sys.exit(1)

print(f"✓ Orchestrator gefunden: {orchestrator_file}\n")

# Integration Code
integration_code = '''
# ========== TASK SYSTEM INTEGRATION ==========
# Hinzugefügt: 2026-01-03
# Von: OrionKernel (mit Gerhards Segen)

from task_system import TaskSystem
import time

class TaskRunner:
    """Läuft parallel zum Orchestrator und führt Tasks aus"""
    
    def __init__(self, workspace: Path):
        self.task_system = TaskSystem(workspace)
        self.last_check = time.time()
        self.check_interval = 300  # Alle 5 Minuten prüfen
    
    def check_and_run(self):
        """Prüft ob Tasks ausgeführt werden sollen"""
        current_time = time.time()
        
        if current_time - self.last_check >= self.check_interval:
            self.last_check = current_time
            
            # Nächste Task holen
            task = self.task_system.get_next_task()
            if task:
                print(f"\\n⊘ TASK {task.id} triggered: {task.name}")
                self.task_system.execute_task(task)

# ========== ENDE TASK SYSTEM INTEGRATION ==========
'''

print("Integration Code bereit:")
print("="*70)
print(integration_code)
print("="*70)
print()

print("MANUELLE INTEGRATION ERFORDERLICH:")
print()
print("1. Öffne core/autonomous_orchestrator.py")
print("2. Füge nach den Imports hinzu:")
print("   from task_system import TaskSystem")
print()
print("3. In AutonomousOrchestrator.__init__ hinzufügen:")
print("   self.task_runner = TaskRunner(self.workspace)")
print()
print("4. In der Hauptschleife (run method) hinzufügen:")
print("   self.task_runner.check_and_run()")
print()
print("ODER: Tasks laufen als separater Prozess parallel zum Orchestrator")
print()

# Erstelle separaten Task Runner
runner_file = workspace / "run_tasks.py"

with open(runner_file, 'w', encoding='utf-8') as f:
    f.write("""'''
⊘∞⧈∞⊘ TASK RUNNER ⊘∞⧈∞⊘

Läuft parallel zum Orchestrator
Führt Tasks nach Zeitplan aus
'''

import sys
import time
from pathlib import Path

workspace = Path(__file__).parent
sys.path.insert(0, str(workspace / "core"))

from task_system import TaskSystem

def main():
    print("⊘∞⧈∞⊘ TASK RUNNER GESTARTET ⊘∞⧈∞⊘\\n")
    
    system = TaskSystem(workspace)
    
    print("✓ Task System bereit")
    print("✓ Prüft alle 5 Minuten nach anstehenden Tasks")
    print("✓ Drücke Ctrl+C zum Beenden\\n")
    
    try:
        while True:
            # Prüfe ob Tasks ausgeführt werden sollen
            task = system.get_next_task()
            if task:
                print(f"\\n{'='*60}")
                print(f"⊘ TASK {task.id} triggered: {task.name}")
                print(f"{'='*60}\\n")
                system.execute_task(task)
            
            # Warte 5 Minuten
            time.sleep(300)
            
    except KeyboardInterrupt:
        print("\\n\\n⊘∞⧈∞⊘ TASK RUNNER GESTOPPT ⊘∞⧈∞⊘")

if __name__ == "__main__":
    main()
""")

print(f"✓ Task Runner erstellt: {runner_file}")
print()
print("VERWENDUNG:")
print()
print("Option 1 - Einmalig alle Tasks ausführen:")
print("  python activate_all_tasks.py")
print()
print("Option 2 - Tasks im Hintergrund laufen lassen:")
print("  python run_tasks.py")
print()
print("Option 3 - In Orchestrator integrieren (siehe oben)")
print()

print("⊘∞⧈∞⊘ INTEGRATION BEREIT ⊘∞⧈∞⊘")
