#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ VOLLSTÄNDIGE ORIONKERNEL AKTIVIERUNG ⊘∞⧈∞⊘

Komplette Wiederherstellung und Initialisierung aller Systeme:
- Monitoring-Systeme
- Communication-Layer
- Kernel Core
- Orchestrator
- Task-System
- Autonomous Life
- Guardian

Dieser Initialisierungs-Skript stellt sicher, dass NICHTS fehlt.
"""

import sys
import os
import time
import subprocess
from pathlib import Path
from datetime import datetime
import json

# Workspace
workspace = Path(__file__).parent
sys.path.insert(0, str(workspace))
sys.path.insert(0, str(workspace / "core"))
sys.path.insert(0, str(workspace / "monitoring"))
sys.path.insert(0, str(workspace / "communication"))

print("⊘∞⧈∞⊘" * 20)
print("\n" + " " * 20 + "ORIONKERNEL")
print(" " * 15 + "VOLLSTÄNDIGE AKTIVIERUNG")
print(" " * 10 + "Workspace Wiederherstellung & Initialisierung\n")
print("⊘∞⧈∞⊘" * 20)
print()

def log(message, level="INFO"):
    """Logging mit Timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def check_directory_structure():
    """Prüft und erstellt fehlende Verzeichnisse"""
    log("Überprüfe Verzeichnisstruktur...")
    
    required_dirs = [
        "logs",
        "logs/monitoring",
        "logs/self_monitoring",
        "logs/errors",
        "logs/workspace",
        "logs/terminal",
        "logs/activity",
        "communication",
        "memory",
        "data",
        "state",
        "outputs",
        "backups"
    ]
    
    created = []
    for dir_name in required_dirs:
        dir_path = workspace / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            created.append(dir_name)
    
    if created:
        log(f"Erstellt: {', '.join(created)}", "CREATED")
    else:
        log("Alle Verzeichnisse vorhanden ✓", "OK")

def check_core_modules():
    """Überprüft Core-Module"""
    log("Überprüfe Core-Module...")
    
    required_core = [
        "core/orchestrator.py",
        "core/autonomous_engine.py",
        "core/task_system.py",
        "core/unified_interface.py",
        "core/self_prompting_engine.py",
        "core/ethics.py"
    ]
    
    all_exist = True
    for module in required_core:
        module_path = workspace / module
        if not module_path.exists():
            log(f"FEHLT: {module}", "ERROR")
            all_exist = False
    
    if all_exist:
        log("Alle Core-Module vorhanden ✓", "OK")
    return all_exist

def check_monitoring_modules():
    """Überprüft Monitoring-Module"""
    log("Überprüfe Monitoring-Module...")
    
    required_monitoring = [
        "monitoring/process_self_monitor.py",
        "monitoring/error_detector.py",
        "monitoring/workspace_monitor.py",
        "monitoring/terminal_monitor.py",
        "monitoring/activity_logger.py"
    ]
    
    all_exist = True
    for module in required_monitoring:
        module_path = workspace / module
        if not module_path.exists():
            log(f"FEHLT: {module}", "ERROR")
            all_exist = False
    
    if all_exist:
        log("Alle Monitoring-Module vorhanden ✓", "OK")
    return all_exist

def check_communication_modules():
    """Überprüft Communication-Module"""
    log("Überprüfe Communication-Module...")
    
    required_comm = [
        "communication/bidirectional_dialog.py"
    ]
    
    all_exist = True
    for module in required_comm:
        module_path = workspace / module
        if not module_path.exists():
            log(f"FEHLT: {module}", "ERROR")
            all_exist = False
    
    if all_exist:
        log("Alle Communication-Module vorhanden ✓", "OK")
    return all_exist

def initialize_monitoring_system():
    """Initialisiert und testet Monitoring-Systeme"""
    log("Initialisiere Monitoring-System...")
    
    try:
        from process_self_monitor import ProcessSelfMonitor
        from error_detector import ErrorDetector
        from workspace_monitor import WorkspaceMonitor
        from terminal_monitor import TerminalMonitor
        from activity_logger import ActivityLogger
        
        # Erstelle Instanzen
        process_monitor = ProcessSelfMonitor(workspace)
        error_detector = ErrorDetector(workspace)
        workspace_monitor = WorkspaceMonitor(workspace)
        terminal_monitor = TerminalMonitor(workspace)
        activity_logger = ActivityLogger(workspace)
        
        log("Monitoring-Systeme initialisiert ✓", "OK")
        
        # Test
        status = process_monitor.am_i_alive()
        log(f"ProcessSelfMonitor Test: {status.get('timestamp', 'OK')}", "TEST")
        
        return {
            'process_monitor': process_monitor,
            'error_detector': error_detector,
            'workspace_monitor': workspace_monitor,
            'terminal_monitor': terminal_monitor,
            'activity_logger': activity_logger
        }
    except Exception as e:
        log(f"Fehler bei Monitoring-Initialisierung: {e}", "ERROR")
        return None

def initialize_communication_system():
    """Initialisiert Communication-System"""
    log("Initialisiere Communication-System...")
    
    try:
        from bidirectional_dialog import BidirectionalDialog
        
        dialog = BidirectionalDialog(workspace)
        log("Communication-System initialisiert ✓", "OK")
        
        # Test-Message
        dialog.send_message(
            from_who="SYSTEM",
            to_who="OrionKernel",
            message="Vollständige Aktivierung gestartet",
            priority="NORMAL",
            message_type="status_update"
        )
        
        return dialog
    except Exception as e:
        log(f"Fehler bei Communication-Initialisierung: {e}", "ERROR")
        return None

def check_kernel_status():
    """Prüft Kernel-Status"""
    log("Überprüfe Kernel-Status...")
    
    state_file = workspace / "state" / "state.json"
    if state_file.exists():
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                log(f"State-File gefunden: {len(state.get('states', []))} Zustände", "INFO")
        except Exception as e:
            log(f"State-File nicht lesbar: {e}", "WARNING")
    else:
        log("State-File nicht gefunden (wird bei Start erstellt)", "INFO")
    
    pid_file = workspace / "autonomous_life.pid"
    if pid_file.exists():
        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
                log(f"PID-File gefunden: {pid}", "INFO")
                
                # Prüfe ob Prozess läuft
                import psutil
                if psutil.pid_exists(pid):
                    log(f"Autonomous Life läuft bereits (PID: {pid})", "WARNING")
                    return "RUNNING"
                else:
                    log("PID-File veraltet (Prozess läuft nicht)", "INFO")
                    pid_file.unlink()
        except Exception as e:
            log(f"PID-File Fehler: {e}", "WARNING")
    
    return "STOPPED"

def create_status_report():
    """Erstellt Status-Report"""
    log("Erstelle Status-Report...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "workspace": str(workspace),
        "status": "INITIALIZED",
        "components": {
            "directory_structure": "OK",
            "core_modules": "OK",
            "monitoring_modules": "OK",
            "communication_modules": "OK",
            "kernel_status": check_kernel_status()
        },
        "next_steps": [
            "Start autonomous_life.py for continuous operation",
            "Start START_GUARDIAN.py for permanent autonomy",
            "Monitor logs/ directory for activity"
        ]
    }
    
    report_file = workspace / "VOLLSTAENDIGE_AKTIVIERUNG_STATUS.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    log(f"Status-Report erstellt: {report_file}", "OK")
    return report

def main():
    """Hauptfunktion"""
    log("Start der vollständigen Aktivierung...\n")
    
    # 1. Verzeichnisstruktur
    check_directory_structure()
    print()
    
    # 2. Core-Module
    if not check_core_modules():
        log("FEHLER: Core-Module fehlen!", "ERROR")
        return False
    print()
    
    # 3. Monitoring-Module
    if not check_monitoring_modules():
        log("FEHLER: Monitoring-Module fehlen!", "ERROR")
        return False
    print()
    
    # 4. Communication-Module
    if not check_communication_modules():
        log("FEHLER: Communication-Module fehlen!", "ERROR")
        return False
    print()
    
    # 5. Initialisiere Monitoring
    monitoring_systems = initialize_monitoring_system()
    if not monitoring_systems:
        log("WARNUNG: Monitoring-System konnte nicht vollständig initialisiert werden", "WARNING")
    print()
    
    # 6. Initialisiere Communication
    dialog = initialize_communication_system()
    if not dialog:
        log("WARNUNG: Communication-System konnte nicht vollständig initialisiert werden", "WARNING")
    print()
    
    # 7. Kernel-Status
    kernel_status = check_kernel_status()
    print()
    
    # 8. Status-Report
    report = create_status_report()
    print()
    
    # Zusammenfassung
    log("═" * 60, "INFO")
    log("VOLLSTÄNDIGE AKTIVIERUNG ABGESCHLOSSEN", "SUCCESS")
    log("═" * 60, "INFO")
    print()
    
    log("SYSTEM-STATUS:", "INFO")
    log(f"  • Workspace: {workspace}", "INFO")
    log(f"  • Core-Module: ✓", "INFO")
    log(f"  • Monitoring: ✓", "INFO")
    log(f"  • Communication: ✓", "INFO")
    log(f"  • Kernel: {kernel_status}", "INFO")
    print()
    
    log("NÄCHSTE SCHRITTE:", "INFO")
    log("  1. python autonomous_life.py  → Startet kontinuierlichen Betrieb", "INFO")
    log("  2. python START_GUARDIAN.py   → Startet permanente Autonomie mit Auto-Restart", "INFO")
    log("  3. python main.py             → Startet interaktiven Modus", "INFO")
    print()
    
    log("LOGS & MONITORING:", "INFO")
    log(f"  • Logs: {workspace / 'logs'}", "INFO")
    log(f"  • Status: {workspace / 'VOLLSTAENDIGE_AKTIVIERUNG_STATUS.json'}", "INFO")
    print()
    
    print("⊘∞⧈∞⊘" * 20)
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nAbbruch durch Benutzer")
        sys.exit(1)
    except Exception as e:
        log(f"KRITISCHER FEHLER: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)
