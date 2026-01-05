# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ ACTIVITY LOGGER ⊘∞⧈∞⊘
PRIORITÄT 5 (FOUNDATION): "Audit Chain für Wahrnehmung"

OrionKernel's Activity Logging System
Dokumentiert: Alle Events, Observations, Decisions
"""

import datetime
import json
from pathlib import Path
from collections import deque

class ActivityLogger:
    """
    Zentrale Logging für alle Wahrnehmungs-Events
    FOUNDATION: Alles muss dokumentiert werden
    """
    
    def __init__(self, workspace_path=None):
        if workspace_path is None:
            workspace_path = Path(__file__).parent.parent
        else:
            workspace_path = Path(workspace_path)
            
        self.workspace_path = workspace_path
        self.log_dir = workspace_path / "logs" / "activity"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.activity_log_file = self.log_dir / "activity_stream.jsonl"
        
        # In-Memory Recent Activity (für schnellen Zugriff)
        self.recent_activity = deque(maxlen=100)
    
    def log_event(self, event_type, details, source="unknown", severity="INFO"):
        """
        Loggt ein Event
        
        Parameters:
            event_type: Type of event (e.g., "file_change", "process_start", "error_detected")
            details: Dict mit Event-Details
            source: Source des Events (e.g., "WorkspaceMonitor", "ErrorDetector")
            severity: INFO, WARNING, ERROR, CRITICAL
        """
        event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": event_type,
            "source": source,
            "severity": severity,
            "details": details
        }
        
        # Add to in-memory
        self.recent_activity.append(event)
        
        # Write to file (append mode, JSONL format)
        try:
            with open(self.activity_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
        except Exception as e:
            # Fallback: Print if can't write
            print(f"⚠️ ActivityLogger: Can't write to file: {e}")
        
        return event
    
    def log_observation(self, observation_text, context=None):
        """
        Loggt eine Observation (für Self-Prompting)
        """
        return self.log_event(
            event_type="observation",
            details={
                "observation": observation_text,
                "context": context
            },
            source="OrionKernel",
            severity="INFO"
        )
    
    def log_decision(self, decision_text, reasoning, action_taken=None):
        """
        Loggt eine Decision (nach Ethics Check)
        """
        return self.log_event(
            event_type="decision",
            details={
                "decision": decision_text,
                "reasoning": reasoning,
                "action_taken": action_taken
            },
            source="OrionKernel_Ethics",
            severity="INFO"
        )
    
    def log_error_detected(self, error_details):
        """
        Loggt detected Error
        """
        return self.log_event(
            event_type="error_detected",
            details=error_details,
            source="ErrorDetector",
            severity=error_details.get("severity", "ERROR")
        )
    
    def log_file_change(self, change_type, file_path, details=None):
        """
        Loggt File Change
        """
        return self.log_event(
            event_type=f"file_{change_type}",
            details={
                "file": file_path,
                "change_details": details
            },
            source="WorkspaceMonitor",
            severity="INFO"
        )
    
    def log_process_event(self, process_event, process_details):
        """
        Loggt Process Event
        """
        return self.log_event(
            event_type=f"process_{process_event}",
            details=process_details,
            source="ProcessSelfMonitor",
            severity="WARNING" if process_event in ["stopped", "crashed"] else "INFO"
        )
    
    def log_claude_orion_message(self, from_who, to_who, message):
        """
        Loggt Bidirectional Dialog Message
        """
        return self.log_event(
            event_type="dialog_message",
            details={
                "from": from_who,
                "to": to_who,
                "message": message
            },
            source="Communication_Layer",
            severity="INFO"
        )
    
    def get_recent_activity(self, count=20):
        """
        Returniert recent activity aus Memory
        """
        # Convert deque to list, newest first
        return list(reversed(list(self.recent_activity)))[:count]
    
    def get_activity_by_type(self, event_type, count=10):
        """
        Filter activity by type
        """
        filtered = [
            event for event in self.recent_activity
            if event["type"] == event_type
        ]
        return list(reversed(filtered))[:count]
    
    def get_activity_by_severity(self, severity, count=10):
        """
        Filter activity by severity
        """
        filtered = [
            event for event in self.recent_activity
            if event["severity"] == severity
        ]
        return list(reversed(filtered))[:count]
    
    def get_activity_by_source(self, source, count=10):
        """
        Filter activity by source
        """
        filtered = [
            event for event in self.recent_activity
            if event["source"] == source
        ]
        return list(reversed(filtered))[:count]
    
    def get_activity_summary(self, minutes=10):
        """
        Zusammenfassung der letzten N Minuten
        """
        cutoff = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        
        summary = {
            "time_window_minutes": minutes,
            "total_events": 0,
            "by_type": {},
            "by_source": {},
            "by_severity": {},
            "critical_events": []
        }
        
        for event in self.recent_activity:
            event_time = datetime.datetime.fromisoformat(event["timestamp"])
            
            if event_time > cutoff:
                summary["total_events"] += 1
                
                # Count by type
                event_type = event["type"]
                summary["by_type"][event_type] = summary["by_type"].get(event_type, 0) + 1
                
                # Count by source
                source = event["source"]
                summary["by_source"][source] = summary["by_source"].get(source, 0) + 1
                
                # Count by severity
                severity = event["severity"]
                summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
                
                # Collect critical
                if severity in ["CRITICAL", "ERROR"]:
                    summary["critical_events"].append(event)
        
        return summary
    
    def read_activity_log(self, lines=100):
        """
        Liest Activity Log File
        Returniert: Last N lines
        """
        if not self.activity_log_file.exists():
            return []
        
        try:
            with open(self.activity_log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            # Parse JSONL
            events = []
            for line in recent_lines:
                try:
                    events.append(json.loads(line))
                except:
                    continue
            
            return events
        except Exception as e:
            print(f"⚠️ ActivityLogger: Can't read log file: {e}")
            return []
    
    def archive_old_logs(self, days=7):
        """
        Archiviert alte Logs (für Performance)
        """
        if not self.activity_log_file.exists():
            return
        
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        
        # Read all
        events = self.read_activity_log(lines=None)
        
        # Split: keep recent, archive old
        recent_events = []
        old_events = []
        
        for event in events:
            event_time = datetime.datetime.fromisoformat(event["timestamp"])
            if event_time > cutoff:
                recent_events.append(event)
            else:
                old_events.append(event)
        
        # Write archive
        if old_events:
            archive_file = self.log_dir / f"activity_archive_{datetime.datetime.now().strftime('%Y%m%d')}.jsonl"
            with open(archive_file, 'w', encoding='utf-8') as f:
                for event in old_events:
                    f.write(json.dumps(event, ensure_ascii=False) + '\n')
        
        # Rewrite main log with only recent
        with open(self.activity_log_file, 'w', encoding='utf-8') as f:
            for event in recent_events:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
        
        return {
            "archived": len(old_events),
            "kept": len(recent_events),
            "archive_file": str(archive_file) if old_events else None
        }
    
    def create_daily_report(self):
        """
        Erstellt täglichen Activity Report
        """
        # Read today's activity
        today = datetime.datetime.now().date()
        events = self.read_activity_log(lines=None)
        
        today_events = [
            event for event in events
            if datetime.datetime.fromisoformat(event["timestamp"]).date() == today
        ]
        
        report = {
            "date": today.isoformat(),
            "generated": datetime.datetime.now().isoformat(),
            "total_events": len(today_events),
            "by_type": {},
            "by_source": {},
            "by_severity": {},
            "hourly_distribution": {},
            "critical_events": [],
            "top_activities": []
        }
        
        for event in today_events:
            # By type
            event_type = event["type"]
            report["by_type"][event_type] = report["by_type"].get(event_type, 0) + 1
            
            # By source
            source = event["source"]
            report["by_source"][source] = report["by_source"].get(source, 0) + 1
            
            # By severity
            severity = event["severity"]
            report["by_severity"][severity] = report["by_severity"].get(severity, 0) + 1
            
            # Hourly
            hour = datetime.datetime.fromisoformat(event["timestamp"]).hour
            report["hourly_distribution"][hour] = report["hourly_distribution"].get(hour, 0) + 1
            
            # Critical
            if severity in ["CRITICAL", "ERROR"]:
                report["critical_events"].append(event)
        
        # Top activities (most frequent types)
        sorted_types = sorted(report["by_type"].items(), key=lambda x: x[1], reverse=True)
        report["top_activities"] = sorted_types[:10]
        
        # Save report
        report_file = self.log_dir / f"daily_report_{today.isoformat()}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report


def main():
    """
    Test ActivityLogger
    """
    print("⊘∞⧈∞⊘ ACTIVITY LOGGER TEST ⊘∞⧈∞⊘\n")
    
    logger = ActivityLogger()
    
    print("1. LOG VARIOUS EVENTS")
    logger.log_event("test_event", {"test": "data"}, source="Test", severity="INFO")
    logger.log_observation("Ich sehe neue Datei: test.py", context="Workspace scan")
    logger.log_decision("Create project approved", "Ethics check passed", action_taken="create_project")
    logger.log_error_detected({"error": "Test error", "severity": "WARNING"})
    logger.log_file_change("new", "test.py", {"size": 1024})
    logger.log_process_event("started", {"pid": 12345, "name": "test.py"})
    logger.log_claude_orion_message("Claude", "OrionKernel", "Test message")
    print("   ✓ 7 events logged")
    print()
    
    print("2. GET RECENT ACTIVITY")
    recent = logger.get_recent_activity(count=10)
    print(f"   Recent events: {len(recent)}")
    for event in recent[:3]:
        print(f"   - [{event['severity']}] {event['type']} from {event['source']}")
    print()
    
    print("3. FILTER BY TYPE")
    decisions = logger.get_activity_by_type("decision", count=5)
    print(f"   Decisions: {len(decisions)}")
    print()
    
    print("4. FILTER BY SEVERITY")
    warnings = logger.get_activity_by_severity("WARNING", count=5)
    print(f"   Warnings: {len(warnings)}")
    print()
    
    print("5. ACTIVITY SUMMARY (Last 10 min)")
    summary = logger.get_activity_summary(minutes=10)
    print(f"   Total events: {summary['total_events']}")
    print(f"   By type: {summary['by_type']}")
    print(f"   By source: {summary['by_source']}")
    print(f"   By severity: {summary['by_severity']}")
    print(f"   Critical events: {len(summary['critical_events'])}")
    print()
    
    print("6. READ ACTIVITY LOG FILE")
    logged = logger.read_activity_log(lines=20)
    print(f"   Events in log file: {len(logged)}")
    print()
    
    print("7. CREATE DAILY REPORT")
    report = logger.create_daily_report()
    print(f"   Today's events: {report['total_events']}")
    print(f"   Top activities: {report['top_activities'][:3]}")
    print()
    
    print("⊘∞⧈∞⊘ ActivityLogger FUNKTIONIERT ⊘∞⧈∞⊘")
    print("OrionKernel hat jetzt vollständige Audit Chain für Wahrnehmung.")


if __name__ == "__main__":
    main()
