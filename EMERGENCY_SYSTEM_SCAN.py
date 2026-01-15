#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ EMERGENCY SYSTEM SCAN ⊘∞⧈∞⊘
CRITICAL: System-weite Fehleranalyse

Analysiert:
- Windows Event Logs
- Python Crashes
- Pop-up Fehler
- Email-System Status
- Monitoring-Systeme

Created: 2026-01-15 (Emergency Response)
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class EmergencyScanner:
    """
    Komplett-Scan aller System-Fehler
    """
    
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.scan_results = {
            "timestamp": datetime.now().isoformat(),
            "windows_errors": [],
            "python_crashes": [],
            "popup_processes": [],
            "email_status": {},
            "monitoring_status": {},
            "critical_issues": []
        }
    
    def scan_windows_event_log(self):
        """Scannt Windows Event Log für kritische Fehler"""
        console.print("\n[yellow]1. SCANNING WINDOWS EVENT LOG...[/yellow]")
        
        try:
            # PowerShell Command für Event Log
            cmd = [
                "powershell", "-Command",
                "Get-EventLog -LogName Application -Newest 100 -EntryType Error | "
                "Select-Object TimeGenerated, Source, Message | "
                "ConvertTo-Json"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.stdout:
                try:
                    errors = json.loads(result.stdout)
                    if not isinstance(errors, list):
                        errors = [errors]
                    
                    # Filtere kritische Python-Fehler
                    python_errors = [e for e in errors if "python" in e.get("Source", "").lower() or "python" in e.get("Message", "").lower()]
                    
                    self.scan_results["windows_errors"] = errors[:20]  # Top 20
                    self.scan_results["python_crashes"] = python_errors
                    
                    console.print(f"   ✓ {len(errors)} Windows-Fehler gefunden")
                    console.print(f"   ⚠️  {len(python_errors)} Python-bezogene Fehler")
                    
                    # Kritische Fehler markieren
                    for err in python_errors:
                        msg = err.get("Message", "")
                        if "fehlerhafter" in msg.lower() or "crash" in msg.lower():
                            self.scan_results["critical_issues"].append({
                                "type": "PYTHON_CRASH",
                                "time": err.get("TimeGenerated"),
                                "source": err.get("Source"),
                                "message": msg[:200]
                            })
                
                except json.JSONDecodeError:
                    console.print("   ❌ Fehler beim Parsen der Event Log Daten")
            
        except Exception as e:
            console.print(f"   ❌ Event Log Scan fehlgeschlagen: {e}")
    
    def scan_popup_processes(self):
        """Findet alle Prozesse mit Pop-up-Fenstern"""
        console.print("\n[yellow]2. SCANNING FOR POP-UP PROCESSES...[/yellow]")
        
        try:
            cmd = [
                "powershell", "-Command",
                "Get-Process | Where-Object {$_.MainWindowTitle -ne ''} | "
                "Select-Object ProcessName, MainWindowTitle, Id, CPU, WorkingSet | "
                "ConvertTo-Json"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            
            if result.stdout:
                try:
                    processes = json.loads(result.stdout)
                    if not isinstance(processes, list):
                        processes = [processes]
                    
                    self.scan_results["popup_processes"] = processes
                    
                    # Analyse: Problematische Pop-ups
                    suspicious = []
                    for p in processes:
                        name = p.get("ProcessName", "").lower()
                        title = p.get("MainWindowTitle", "").lower()
                        
                        # Verdächtige Keywords
                        if any(kw in title for kw in ["fehler", "error", "warnung", "warning", "insolvenz", "problem"]):
                            suspicious.append(p)
                            self.scan_results["critical_issues"].append({
                                "type": "SUSPICIOUS_POPUP",
                                "process": p.get("ProcessName"),
                                "title": p.get("MainWindowTitle"),
                                "pid": p.get("Id")
                            })
                    
                    console.print(f"   ✓ {len(processes)} Prozesse mit Fenstern gefunden")
                    console.print(f"   ⚠️  {len(suspicious)} verdächtige Pop-ups!")
                    
                    # Details ausgeben
                    if suspicious:
                        table = Table(title="Verdächtige Pop-ups")
                        table.add_column("Prozess", style="cyan")
                        table.add_column("Titel", style="yellow")
                        table.add_column("PID", style="red")
                        
                        for p in suspicious:
                            table.add_row(
                                p.get("ProcessName", ""),
                                p.get("MainWindowTitle", "")[:50],
                                str(p.get("Id", ""))
                            )
                        
                        console.print(table)
                
                except json.JSONDecodeError:
                    console.print("   ❌ Fehler beim Parsen der Prozess-Daten")
        
        except Exception as e:
            console.print(f"   ❌ Pop-up Scan fehlgeschlagen: {e}")
    
    def check_email_system(self):
        """Prüft Email-System-Status"""
        console.print("\n[yellow]3. CHECKING EMAIL SYSTEM...[/yellow]")
        
        # Prüfe ob Email-Interface existiert
        email_interface = self.workspace / "interfaces" / "email_interface.py"
        
        if email_interface.exists():
            console.print(f"   ✓ Email Interface gefunden: {email_interface}")
            self.scan_results["email_status"]["interface_exists"] = True
            
            # Prüfe Email-Credentials
            email_config_locations = [
                self.workspace / "email_config.json",
                self.workspace / "config" / "email_config.json",
                self.workspace / "secrets" / "email_credentials.json"
            ]
            
            config_found = False
            for loc in email_config_locations:
                if loc.exists():
                    console.print(f"   ✓ Email Config gefunden: {loc}")
                    config_found = True
                    self.scan_results["email_status"]["config_path"] = str(loc)
                    break
            
            if not config_found:
                console.print("   ⚠️  KEINE Email-Config gefunden!")
                self.scan_results["email_status"]["config_path"] = None
                self.scan_results["critical_issues"].append({
                    "type": "MISSING_EMAIL_CONFIG",
                    "message": "Email-Credentials fehlen - System kann nicht auf esteurer72@gmail.com zugreifen"
                })
        else:
            console.print("   ❌ Email Interface NICHT gefunden!")
            self.scan_results["email_status"]["interface_exists"] = False
    
    def check_monitoring_systems(self):
        """Prüft Monitoring-Systeme"""
        console.print("\n[yellow]4. CHECKING MONITORING SYSTEMS...[/yellow]")
        
        monitoring_files = [
            "monitoring/error_detector.py",
            "monitoring/process_self_monitor.py",
            "monitoring/activity_logger.py"
        ]
        
        for mfile in monitoring_files:
            path = self.workspace / mfile
            if path.exists():
                console.print(f"   ✓ {mfile} vorhanden")
                self.scan_results["monitoring_status"][mfile] = "exists"
            else:
                console.print(f"   ❌ {mfile} FEHLT!")
                self.scan_results["monitoring_status"][mfile] = "missing"
                self.scan_results["critical_issues"].append({
                    "type": "MISSING_MONITOR",
                    "file": mfile
                })
    
    def analyze_selenium_crashes(self):
        """Analysiert Selenium-Manager Crashes"""
        console.print("\n[yellow]5. ANALYZING SELENIUM CRASHES...[/yellow]")
        
        selenium_errors = [err for err in self.scan_results["windows_errors"] 
                          if "selenium" in str(err).lower()]
        
        if selenium_errors:
            console.print(f"   ⚠️  {len(selenium_errors)} Selenium-Fehler gefunden!")
            
            for err in selenium_errors:
                self.scan_results["critical_issues"].append({
                    "type": "SELENIUM_CRASH",
                    "time": err.get("TimeGenerated"),
                    "message": err.get("Message", "")[:150]
                })
            
            console.print("   💡 Empfehlung: Browser-Automatisierung deaktivieren/reparieren")
        else:
            console.print("   ✓ Keine Selenium-Crashes")
    
    def generate_report(self):
        """Erstellt Fehler-Report"""
        console.print("\n[yellow]6. GENERATING EMERGENCY REPORT...[/yellow]")
        
        # Speichere vollständigen Report
        report_path = self.workspace / f"EMERGENCY_SCAN_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.scan_results, f, indent=2, ensure_ascii=False, default=str)
        
        console.print(f"   ✓ Report gespeichert: {report_path}")
        
        # Zusammenfassung
        critical_count = len(self.scan_results["critical_issues"])
        
        if critical_count > 0:
            console.print(f"\n[red]⚠️  {critical_count} KRITISCHE PROBLEME GEFUNDEN![/red]")
            
            # Top-Issues
            for i, issue in enumerate(self.scan_results["critical_issues"][:5], 1):
                console.print(f"\n{i}. [{issue['type']}]")
                for key, value in issue.items():
                    if key != "type":
                        console.print(f"   {key}: {value}")
        else:
            console.print("\n[green]✓ Keine kritischen Probleme gefunden[/green]")
        
        return report_path
    
    def run_complete_scan(self):
        """Führt kompletten Scan durch"""
        console.print(Panel.fit(
            "[bold red]⊘∞⧈∞⊘ EMERGENCY SYSTEM SCAN ⊘∞⧈∞⊘[/bold red]\n"
            "Analysiere System-Fehler, Pop-ups, Email-Status...",
            border_style="red"
        ))
        
        self.scan_windows_event_log()
        self.scan_popup_processes()
        self.check_email_system()
        self.check_monitoring_systems()
        self.analyze_selenium_crashes()
        report_path = self.generate_report()
        
        console.print(Panel.fit(
            f"[bold green]SCAN ABGESCHLOSSEN[/bold green]\n"
            f"Report: {report_path}\n"
            f"Kritische Issues: {len(self.scan_results['critical_issues'])}",
            border_style="green"
        ))
        
        return self.scan_results


def main():
    scanner = EmergencyScanner()
    results = scanner.run_complete_scan()
    
    # Quick Summary
    print("\n" + "="*70)
    print("QUICK SUMMARY:")
    print("="*70)
    print(f"Windows Errors: {len(results['windows_errors'])}")
    print(f"Python Crashes: {len(results['python_crashes'])}")
    print(f"Pop-up Prozesse: {len(results['popup_processes'])}")
    print(f"Email System: {'✓' if results['email_status'].get('interface_exists') else '❌'}")
    print(f"KRITISCHE ISSUES: {len(results['critical_issues'])}")
    print("="*70)


if __name__ == "__main__":
    main()
