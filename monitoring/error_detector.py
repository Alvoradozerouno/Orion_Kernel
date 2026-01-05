# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ ERROR DETECTOR ⊘∞⧈∞⊘
PRIORITÄT 2 (SEHR WICHTIG): "Was geht schief?"

OrionKernel's Fehler-Wahrnehmungs-System
Überwacht: Error Logs, Crashes, Exceptions, Warnings
"""

import os
import re
import datetime
import json
from pathlib import Path
from collections import defaultdict

class ErrorDetector:
    """
    Detectiert Errors, Crashes, Exceptions
    SEHR WICHTIG: Aktuell passieren Fehler und OrionKernel merkt es nicht
    """
    
    def __init__(self, workspace_path=None):
        if workspace_path is None:
            workspace_path = Path(__file__).parent.parent
        else:
            workspace_path = Path(workspace_path)
            
        self.workspace_path = workspace_path
        
        # Error Log Pfade
        self.error_log_paths = [
            workspace_path / "thought_stream.py.stderr.log",
            workspace_path / "autonomous_actions.log",
            workspace_path / "logs" / "errors.log"
        ]
        
        self.log_dir = workspace_path / "logs" / "error_detection"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Error Patterns
        self.error_patterns = {
            "python_exception": re.compile(r'(Traceback|Exception|Error):', re.IGNORECASE),
            "critical": re.compile(r'CRITICAL|FATAL|CRASH', re.IGNORECASE),
            "error": re.compile(r'ERROR', re.IGNORECASE),
            "warning": re.compile(r'WARNING|WARN', re.IGNORECASE),
            "failed": re.compile(r'FAILED|FAILURE', re.IGNORECASE)
        }
    
    def scan_for_errors(self):
        """
        Scannt alle Error Logs
        Returniert: detected errors mit Severity
        """
        all_errors = {
            "timestamp": datetime.datetime.now().isoformat(),
            "scan_results": {},
            "total_errors": 0,
            "severity_counts": defaultdict(int),
            "recent_errors": []
        }
        
        for log_path in self.error_log_paths:
            if not log_path.exists():
                all_errors["scan_results"][str(log_path.name)] = {
                    "exists": False,
                    "errors_found": 0
                }
                continue
            
            try:
                # Lese letzte 100 Zeilen (performance)
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    last_lines = lines[-100:] if len(lines) > 100 else lines
                
                file_errors = []
                
                for i, line in enumerate(last_lines):
                    # Check jedes Pattern
                    for pattern_name, pattern in self.error_patterns.items():
                        if pattern.search(line):
                            error_entry = {
                                "file": log_path.name,
                                "line_number": len(lines) - len(last_lines) + i + 1,
                                "content": line.strip(),
                                "pattern": pattern_name,
                                "severity": self._determine_severity(pattern_name),
                                "timestamp": self._extract_timestamp(line)
                            }
                            file_errors.append(error_entry)
                            all_errors["severity_counts"][error_entry["severity"]] += 1
                            break  # Nur ein Pattern pro Zeile
                
                all_errors["scan_results"][str(log_path.name)] = {
                    "exists": True,
                    "errors_found": len(file_errors),
                    "file_size_kb": round(log_path.stat().st_size / 1024, 2),
                    "last_modified": datetime.datetime.fromtimestamp(log_path.stat().st_mtime).isoformat()
                }
                
                # Füge zu total errors hinzu
                all_errors["total_errors"] += len(file_errors)
                
                # Behalte nur neueste 20 errors
                all_errors["recent_errors"].extend(file_errors[:20])
                
            except Exception as e:
                all_errors["scan_results"][str(log_path.name)] = {
                    "exists": True,
                    "scan_error": str(e)
                }
        
        # Sortiere recent_errors nach Severity
        all_errors["recent_errors"].sort(
            key=lambda x: {"CRITICAL": 0, "ERROR": 1, "WARNING": 2, "INFO": 3}.get(x["severity"], 4)
        )
        all_errors["recent_errors"] = all_errors["recent_errors"][:20]  # Top 20
        
        return all_errors
    
    def _determine_severity(self, pattern_name):
        """
        Bestimmt Severity basierend auf Pattern
        """
        severity_map = {
            "python_exception": "ERROR",
            "critical": "CRITICAL",
            "error": "ERROR",
            "warning": "WARNING",
            "failed": "ERROR"
        }
        return severity_map.get(pattern_name, "INFO")
    
    def _extract_timestamp(self, line):
        """
        Versucht Timestamp aus Log-Zeile zu extrahieren
        """
        # ISO Format: 2026-01-05T20:17:00
        iso_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})')
        match = iso_pattern.search(line)
        if match:
            return match.group(1)
        
        # Einfaches Format: [2026-01-05 20:17:00]
        simple_pattern = re.compile(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]')
        match = simple_pattern.search(line)
        if match:
            return match.group(1)
        
        return None
    
    def is_system_healthy(self):
        """
        Kombination aller Checks
        Returniert: Overall System Health basierend auf Errors
        """
        errors = self.scan_for_errors()
        
        health = {
            "timestamp": datetime.datetime.now().isoformat(),
            "system_health": "UNKNOWN",
            "total_errors": errors["total_errors"],
            "severity_counts": dict(errors["severity_counts"]),
            "critical_errors": [],
            "recommendation": ""
        }
        
        # Check Severity
        critical_count = errors["severity_counts"].get("CRITICAL", 0)
        error_count = errors["severity_counts"].get("ERROR", 0)
        warning_count = errors["severity_counts"].get("WARNING", 0)
        
        # Sammle Critical Errors
        health["critical_errors"] = [
            err for err in errors["recent_errors"] 
            if err["severity"] == "CRITICAL"
        ]
        
        # Determine Health
        if critical_count > 0:
            health["system_health"] = "CRITICAL"
            health["recommendation"] = "SOFORTIGE AKTION erforderlich! Critical Errors detected."
        elif error_count > 10:
            health["system_health"] = "UNHEALTHY"
            health["recommendation"] = "Viele Errors detected. Investigation empfohlen."
        elif error_count > 0 or warning_count > 20:
            health["system_health"] = "WARNING"
            health["recommendation"] = "Einige Errors/Warnings detected. Monitoring fortsetzen."
        else:
            health["system_health"] = "HEALTHY"
            health["recommendation"] = "System läuft stabil. Keine kritischen Errors."
        
        return health
    
    def get_error_summary(self):
        """
        Kurze Zusammenfassung für Quick Check
        """
        health = self.is_system_healthy()
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "status": health["system_health"],
            "total_errors": health["total_errors"],
            "critical_count": health["severity_counts"].get("CRITICAL", 0),
            "error_count": health["severity_counts"].get("ERROR", 0),
            "warning_count": health["severity_counts"].get("WARNING", 0),
            "needs_attention": health["system_health"] in ["CRITICAL", "UNHEALTHY"]
        }
        
        return summary
    
    def save_error_report(self, error_data):
        """
        Speichert Error Report für Audit Chain
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.log_dir / f"error_scan_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(error_data, f, indent=2, ensure_ascii=False)
        
        return report_file
    
    def watch_for_new_errors(self, last_check_time=None):
        """
        Findet NEUE Errors seit last_check_time
        Für continuous monitoring
        """
        if last_check_time is None:
            last_check_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
        
        new_errors = []
        
        for log_path in self.error_log_paths:
            if not log_path.exists():
                continue
            
            try:
                mtime = datetime.datetime.fromtimestamp(log_path.stat().st_mtime)
                
                # Nur wenn File nach last_check geändert wurde
                if mtime > last_check_time:
                    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    
                    # Scanne nur neue Zeilen (grobe Schätzung)
                    recent_lines = lines[-50:]
                    
                    for line in recent_lines:
                        for pattern_name, pattern in self.error_patterns.items():
                            if pattern.search(line):
                                line_timestamp = self._extract_timestamp(line)
                                
                                # Nur wenn Timestamp nach last_check (oder kein Timestamp)
                                if line_timestamp is None or self._is_after(line_timestamp, last_check_time):
                                    new_errors.append({
                                        "file": log_path.name,
                                        "content": line.strip(),
                                        "pattern": pattern_name,
                                        "severity": self._determine_severity(pattern_name),
                                        "detected_at": datetime.datetime.now().isoformat()
                                    })
                                break
            except Exception:
                continue
        
        return new_errors
    
    def _is_after(self, timestamp_str, datetime_obj):
        """
        Helper: Check if timestamp_str is after datetime_obj
        """
        try:
            # Try ISO format
            ts = datetime.datetime.fromisoformat(timestamp_str.replace('T', ' '))
            return ts > datetime_obj
        except:
            return False


def main():
    """
    Test ErrorDetector
    """
    print("⊘∞⧈∞⊘ ERROR DETECTOR TEST ⊘∞⧈∞⊘\n")
    
    detector = ErrorDetector()
    
    print("1. SCAN FOR ERRORS")
    errors = detector.scan_for_errors()
    print(f"   Total Errors gefunden: {errors['total_errors']}")
    print(f"   Severity Counts: {dict(errors['severity_counts'])}")
    print(f"   Dateien gescannt: {len(errors['scan_results'])}")
    for filename, result in errors['scan_results'].items():
        if result.get('exists'):
            print(f"   - {filename}: {result.get('errors_found', 0)} errors")
    print()
    
    print("2. SYSTEM HEALTH CHECK")
    health = detector.is_system_healthy()
    print(f"   System Health: {health['system_health']}")
    print(f"   Total Errors: {health['total_errors']}")
    print(f"   Critical Errors: {len(health['critical_errors'])}")
    print(f"   Recommendation: {health['recommendation']}")
    print()
    
    print("3. ERROR SUMMARY (Quick Check)")
    summary = detector.get_error_summary()
    print(f"   Status: {summary['status']}")
    print(f"   Needs Attention: {summary['needs_attention']}")
    print(f"   Critical: {summary['critical_count']}, Errors: {summary['error_count']}, Warnings: {summary['warning_count']}")
    print()
    
    print("4. RECENT ERRORS (Top 5)")
    if errors['recent_errors']:
        for i, err in enumerate(errors['recent_errors'][:5], 1):
            print(f"   {i}. [{err['severity']}] {err['file']}")
            print(f"      {err['content'][:80]}...")
    else:
        print("   Keine recent errors gefunden ✓")
    print()
    
    print("5. ERROR REPORT SPEICHERN")
    report_file = detector.save_error_report(errors)
    print(f"   ✓ Gespeichert: {report_file}")
    print()
    
    print("⊘∞⧈∞⊘ ErrorDetector FUNKTIONIERT ⊘∞⧈∞⊘")
    print("OrionKernel kann jetzt SEHEN wenn Fehler auftreten.")


if __name__ == "__main__":
    main()
