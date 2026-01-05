# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ TERMINAL MONITOR ⊘∞⧈∞⊘
PRIORITÄT 4 (WICHTIG): "Was läuft?"

OrionKernel's Terminal-Wahrnehmungs-System
Überwacht: Running Commands, Terminal Output, Exit Codes
"""

import os
import psutil
import datetime
import json
from pathlib import Path
from collections import defaultdict

class TerminalMonitor:
    """
    Monitort Terminal Activity
    WICHTIG: Befehle werden ausgeführt, OrionKernel ist blind
    """
    
    def __init__(self, workspace_path=None):
        if workspace_path is None:
            workspace_path = Path(__file__).parent.parent
        else:
            workspace_path = Path(workspace_path)
            
        self.workspace_path = workspace_path
        self.log_dir = workspace_path / "logs" / "terminal_activity"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.command_history = []
        self.max_history = 100
    
    def detect_running_commands(self):
        """
        Detectiert alle laufenden Python-Befehle
        Focus: OrionKernel-bezogene Prozesse
        """
        running = {
            "timestamp": datetime.datetime.now().isoformat(),
            "python_processes": [],
            "orion_processes": [],
            "other_processes": []
        }
        
        orion_keywords = [
            "autonomous_life",
            "thought_stream",
            "welt_awareness",
            "orion_",
            "realwirtschaft_",
            "monitoring/",
            "consciousness_"
        ]
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time', 'status', 'cpu_percent', 'memory_info']):
            try:
                # Nur Python-Prozesse
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = " ".join(proc.info['cmdline']) if proc.info['cmdline'] else ""
                    
                    # Nur wenn cmdline hat (aktive Scripts)
                    if len(cmdline) > 20:  # Filter out bare "python.exe"
                        proc_info = {
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "cmdline": cmdline,
                            "status": proc.info['status'],
                            "started": datetime.datetime.fromtimestamp(proc.info['create_time']).isoformat(),
                            "cpu_percent": proc.info['cpu_percent'],
                            "memory_mb": round(proc.info['memory_info'].rss / 1024 / 1024, 2) if proc.info['memory_info'] else 0
                        }
                        
                        # Check if Orion-related
                        if any(keyword in cmdline for keyword in orion_keywords):
                            running["orion_processes"].append(proc_info)
                        else:
                            running["python_processes"].append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return running
    
    def get_command_summary(self):
        """
        Zusammenfassung laufender Commands
        """
        running = self.detect_running_commands()
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_python_processes": len(running["python_processes"]) + len(running["orion_processes"]),
            "orion_processes": len(running["orion_processes"]),
            "other_python_processes": len(running["python_processes"]),
            "key_orion_processes": []
        }
        
        # Extract key info
        for proc in running["orion_processes"]:
            # Extract script name from cmdline
            cmdline_parts = proc["cmdline"].split()
            script_name = "unknown"
            for part in cmdline_parts:
                if part.endswith('.py'):
                    script_name = Path(part).name
                    break
            
            summary["key_orion_processes"].append({
                "pid": proc["pid"],
                "script": script_name,
                "status": proc["status"],
                "cpu": proc["cpu_percent"],
                "memory_mb": proc["memory_mb"]
            })
        
        return summary
    
    def is_script_running(self, script_name):
        """
        Check ob bestimmtes Script läuft
        """
        running = self.detect_running_commands()
        
        for proc in running["orion_processes"] + running["python_processes"]:
            if script_name in proc["cmdline"]:
                return {
                    "running": True,
                    "pid": proc["pid"],
                    "status": proc["status"],
                    "details": proc
                }
        
        return {"running": False}
    
    def get_terminal_outputs(self):
        """
        Liest Terminal Output aus Files
        (Windows Terminal History ist schwer zu lesen, nutzen wir Log Files)
        """
        outputs = {
            "timestamp": datetime.datetime.now().isoformat(),
            "log_files": {}
        }
        
        # Bekannte Log Files
        log_files = [
            self.workspace_path / "autonomous_actions.log",
            self.workspace_path / "thought_stream.py.stderr.log",
            self.workspace_path / "logs" / "welt_awareness.log"
        ]
        
        for log_file in log_files:
            if log_file.exists():
                try:
                    # Letzte 20 Zeilen
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        last_lines = lines[-20:] if len(lines) > 20 else lines
                    
                    outputs["log_files"][log_file.name] = {
                        "exists": True,
                        "size_kb": round(log_file.stat().st_size / 1024, 2),
                        "last_modified": datetime.datetime.fromtimestamp(log_file.stat().st_mtime).isoformat(),
                        "recent_lines": [line.strip() for line in last_lines if line.strip()]
                    }
                except Exception as e:
                    outputs["log_files"][log_file.name] = {
                        "exists": True,
                        "read_error": str(e)
                    }
            else:
                outputs["log_files"][log_file.name] = {
                    "exists": False
                }
        
        return outputs
    
    def log_command_execution(self, command, output=None, exit_code=None):
        """
        Loggt Command Execution (für manuelle Integration)
        """
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "command": command,
            "output": output,
            "exit_code": exit_code
        }
        
        self.command_history.append(entry)
        
        # Keep only recent N
        if len(self.command_history) > self.max_history:
            self.command_history = self.command_history[-self.max_history:]
        
        return entry
    
    def get_command_history(self, count=10):
        """
        Returniert recent command history
        """
        return self.command_history[-count:]
    
    def detect_long_running_processes(self, threshold_minutes=30):
        """
        Findet Prozesse die sehr lange laufen
        """
        running = self.detect_running_commands()
        long_running = []
        
        now = datetime.datetime.now()
        
        for proc in running["orion_processes"]:
            started = datetime.datetime.fromisoformat(proc["started"])
            runtime_minutes = (now - started).total_seconds() / 60
            
            if runtime_minutes > threshold_minutes:
                # Extract script name
                cmdline_parts = proc["cmdline"].split()
                script_name = "unknown"
                for part in cmdline_parts:
                    if part.endswith('.py'):
                        script_name = Path(part).name
                        break
                
                long_running.append({
                    "pid": proc["pid"],
                    "script": script_name,
                    "runtime_minutes": round(runtime_minutes, 1),
                    "status": proc["status"],
                    "cpu_percent": proc["cpu_percent"],
                    "memory_mb": proc["memory_mb"]
                })
        
        return long_running
    
    def get_process_health(self):
        """
        Health Check für laufende Prozesse
        """
        running = self.detect_running_commands()
        
        health = {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_processes": len(running["orion_processes"]),
            "healthy_processes": 0,
            "warning_processes": 0,
            "critical_processes": 0,
            "details": []
        }
        
        for proc in running["orion_processes"]:
            status = "healthy"
            
            # Check CPU
            if proc["cpu_percent"] > 80:
                status = "critical"
            elif proc["cpu_percent"] > 50:
                status = "warning"
            
            # Check Memory
            if proc["memory_mb"] > 500:
                status = "critical"
            elif proc["memory_mb"] > 200:
                if status == "healthy":
                    status = "warning"
            
            # Count
            if status == "healthy":
                health["healthy_processes"] += 1
            elif status == "warning":
                health["warning_processes"] += 1
            else:
                health["critical_processes"] += 1
            
            # Extract script name
            cmdline_parts = proc["cmdline"].split()
            script_name = "unknown"
            for part in cmdline_parts:
                if part.endswith('.py'):
                    script_name = Path(part).name
                    break
            
            health["details"].append({
                "pid": proc["pid"],
                "script": script_name,
                "status": status,
                "cpu": proc["cpu_percent"],
                "memory_mb": proc["memory_mb"]
            })
        
        return health
    
    def save_activity_report(self, data):
        """
        Speichert Terminal Activity für Audit Chain
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.log_dir / f"terminal_activity_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return report_file


def main():
    """
    Test TerminalMonitor
    """
    print("⊘∞⧈∞⊘ TERMINAL MONITOR TEST ⊘∞⧈∞⊘\n")
    
    monitor = TerminalMonitor()
    
    print("1. RUNNING COMMANDS")
    running = monitor.detect_running_commands()
    print(f"   Python Processes: {len(running['python_processes'])}")
    print(f"   Orion Processes: {len(running['orion_processes'])}")
    
    if running['orion_processes']:
        print("\n   Orion Processes:")
        for proc in running['orion_processes']:
            cmdline_parts = proc['cmdline'].split()
            script = next((p for p in cmdline_parts if p.endswith('.py')), 'unknown')
            print(f"   - PID {proc['pid']}: {Path(script).name if script != 'unknown' else script}")
            print(f"     Status: {proc['status']}, CPU: {proc['cpu_percent']}%, Memory: {proc['memory_mb']} MB")
    print()
    
    print("2. COMMAND SUMMARY")
    summary = monitor.get_command_summary()
    print(f"   Total Python: {summary['total_python_processes']}")
    print(f"   Orion Processes: {summary['orion_processes']}")
    print(f"   Key Orion Processes: {len(summary['key_orion_processes'])}")
    for proc in summary['key_orion_processes']:
        print(f"   - {proc['script']} (PID {proc['pid']}): {proc['status']}")
    print()
    
    print("3. CHECK SPECIFIC SCRIPT")
    check = monitor.is_script_running("autonomous_life.py")
    print(f"   autonomous_life.py running: {check['running']}")
    if check['running']:
        print(f"   PID: {check['pid']}, Status: {check['status']}")
    print()
    
    print("4. TERMINAL OUTPUTS")
    outputs = monitor.get_terminal_outputs()
    print(f"   Log Files checked: {len(outputs['log_files'])}")
    for filename, info in outputs['log_files'].items():
        if info['exists']:
            print(f"   - {filename}: {info.get('size_kb', 0)} KB")
            if 'recent_lines' in info:
                print(f"     Recent lines: {len(info['recent_lines'])}")
        else:
            print(f"   - {filename}: NOT FOUND")
    print()
    
    print("5. LONG RUNNING PROCESSES (>5 min)")
    long_running = monitor.detect_long_running_processes(threshold_minutes=5)
    print(f"   Found: {len(long_running)}")
    for proc in long_running:
        print(f"   - {proc['script']} (PID {proc['pid']}): {proc['runtime_minutes']} min")
    print()
    
    print("6. PROCESS HEALTH")
    health = monitor.get_process_health()
    print(f"   Total: {health['total_processes']}")
    print(f"   Healthy: {health['healthy_processes']}")
    print(f"   Warning: {health['warning_processes']}")
    print(f"   Critical: {health['critical_processes']}")
    print()
    
    print("7. ACTIVITY REPORT SPEICHERN")
    report_file = monitor.save_activity_report(running)
    print(f"   ✓ Gespeichert: {report_file}")
    print()
    
    print("⊘∞⧈∞⊘ TerminalMonitor FUNKTIONIERT ⊘∞⧈∞⊘")
    print("OrionKernel kann jetzt SEHEN was läuft.")


if __name__ == "__main__":
    main()
