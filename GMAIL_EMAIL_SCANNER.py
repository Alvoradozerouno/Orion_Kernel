#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ GMAIL EMAIL SCANNER ⊘∞⧈∞⊘
CRITICAL: Scannt esteurer72@gmail.com für wichtige Emails

Funktionen:
- IMAP Gmail-Zugriff
- Scannt nach Fehlern/Failures
- Analysiert wichtige Nachrichten
- Erstellt Alert-Report

Created: 2026-01-15 (Emergency Email Scan)
"""

import imaplib
import email
from email.header import decode_header
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class GmailScanner:
    """
    Scannt Gmail-Postfach für wichtige/kritische Nachrichten
    """
    
    def __init__(self, email_address, app_password=None):
        self.email_address = email_address
        self.app_password = app_password
        self.workspace = Path(__file__).parent
        
        self.scan_results = {
            "timestamp": datetime.now().isoformat(),
            "email_address": email_address,
            "total_unread": 0,
            "total_scanned": 0,
            "critical_emails": [],
            "failure_emails": [],
            "github_emails": [],
            "recent_important": []
        }
    
    def connect_to_gmail(self):
        """Verbindet zu Gmail via IMAP"""
        console.print("\n[yellow]Connecting to Gmail...[/yellow]")
        
        try:
            # Gmail IMAP
            self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
            
            if self.app_password:
                self.mail.login(self.email_address, self.app_password)
                console.print(f"   ✓ Eingeloggt als: {self.email_address}")
                return True
            else:
                console.print("   ⚠️  KEIN App-Password vorhanden!")
                console.print("   💡 Erstelle App-Password in Google Account:")
                console.print("      https://myaccount.google.com/apppasswords")
                return False
        
        except imaplib.IMAP4.error as e:
            console.print(f"   ❌ Login fehlgeschlagen: {e}")
            return False
        except Exception as e:
            console.print(f"   ❌ Verbindung fehlgeschlagen: {e}")
            return False
    
    def scan_inbox(self, days_back=7):
        """Scannt Inbox der letzten N Tage"""
        console.print(f"\n[yellow]Scanning Inbox (letzte {days_back} Tage)...[/yellow]")
        
        try:
            # Select Inbox
            self.mail.select("INBOX")
            
            # Datum berechnen
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
            
            # Suche ungelesene Emails
            status, messages = self.mail.search(None, f'(SINCE {since_date})')
            
            if status != "OK":
                console.print("   ❌ Keine Emails gefunden")
                return
            
            email_ids = messages[0].split()
            self.scan_results["total_scanned"] = len(email_ids)
            
            console.print(f"   ✓ {len(email_ids)} Emails gefunden")
            
            # Scanne jede Email
            for i, email_id in enumerate(email_ids[-50:], 1):  # Letzte 50
                self._process_email(email_id, i)
            
        except Exception as e:
            console.print(f"   ❌ Scan fehlgeschlagen: {e}")
    
    def _process_email(self, email_id, index):
        """Verarbeitet einzelne Email"""
        try:
            # Fetch Email
            status, msg_data = self.mail.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                return
            
            # Parse Email
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Extrahiere Details
            subject = self._decode_header(msg.get("Subject", ""))
            from_ = self._decode_header(msg.get("From", ""))
            date = msg.get("Date", "")
            
            # Check für kritische Keywords
            subject_lower = subject.lower()
            
            email_info = {
                "id": email_id.decode(),
                "subject": subject,
                "from": from_,
                "date": date
            }
            
            # Kategorisiere
            is_critical = False
            
            if any(kw in subject_lower for kw in ["failure", "failed", "error", "fehler", "problem"]):
                self.scan_results["failure_emails"].append(email_info)
                is_critical = True
            
            if "github" in from_.lower() or "github" in subject_lower:
                self.scan_results["github_emails"].append(email_info)
                
                # GitHub Failures besonders wichtig
                if "failed" in subject_lower or "failure" in subject_lower:
                    self.scan_results["critical_emails"].append(email_info)
                    is_critical = True
            
            if any(kw in subject_lower for kw in ["urgent", "important", "dringend", "wichtig", "critical"]):
                self.scan_results["recent_important"].append(email_info)
                is_critical = True
            
            # Ausgabe
            if is_critical:
                console.print(f"   [{index}] ⚠️  {subject[:60]} (from: {from_[:30]})")
            else:
                console.print(f"   [{index}] {subject[:60]}", style="dim")
        
        except Exception as e:
            console.print(f"   ⚠️  Email {index} konnte nicht verarbeitet werden: {e}")
    
    def _decode_header(self, header):
        """Dekodiert Email-Header"""
        if not header:
            return ""
        
        decoded = decode_header(header)
        result = ""
        
        for part, encoding in decoded:
            if isinstance(part, bytes):
                result += part.decode(encoding or "utf-8", errors="ignore")
            else:
                result += part
        
        return result
    
    def generate_report(self):
        """Erstellt Email-Report"""
        console.print("\n[yellow]Generating Email Report...[/yellow]")
        
        # Speichere Report
        report_path = self.workspace / f"GMAIL_SCAN_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.scan_results, f, indent=2, ensure_ascii=False)
        
        console.print(f"   ✓ Report gespeichert: {report_path}")
        
        # Zusammenfassung-Tabelle
        table = Table(title="Email Scan Summary")
        table.add_column("Kategorie", style="cyan")
        table.add_column("Anzahl", style="yellow")
        
        table.add_row("Total Gescannt", str(self.scan_results["total_scanned"]))
        table.add_row("Failure Emails", str(len(self.scan_results["failure_emails"])))
        table.add_row("GitHub Emails", str(len(self.scan_results["github_emails"])))
        table.add_row("Kritisch", str(len(self.scan_results["critical_emails"])))
        table.add_row("Wichtig", str(len(self.scan_results["recent_important"])))
        
        console.print(table)
        
        # Kritische Emails ausgeben
        if self.scan_results["critical_emails"]:
            console.print("\n[red]⚠️  KRITISCHE EMAILS:[/red]")
            for i, email_info in enumerate(self.scan_results["critical_emails"][:10], 1):
                console.print(f"{i}. {email_info['subject']}")
                console.print(f"   From: {email_info['from']}")
                console.print(f"   Date: {email_info['date']}\n")
        
        return report_path
    
    def disconnect(self):
        """Trennt Verbindung"""
        try:
            self.mail.logout()
            console.print("   ✓ Verbindung getrennt")
        except:
            pass
    
    def run_scan(self, days_back=7):
        """Führt kompletten Scan durch"""
        console.print(Panel.fit(
            f"[bold blue]⊘∞⧈∞⊘ GMAIL SCANNER ⊘∞⧈∞⊘[/bold blue]\n"
            f"Email: {self.email_address}\n"
            f"Zeitraum: Letzte {days_back} Tage",
            border_style="blue"
        ))
        
        if self.connect_to_gmail():
            self.scan_inbox(days_back)
            report_path = self.generate_report()
            self.disconnect()
            
            console.print(Panel.fit(
                f"[bold green]SCAN ABGESCHLOSSEN[/bold green]\n"
                f"Report: {report_path}\n"
                f"Kritische Emails: {len(self.scan_results['critical_emails'])}",
                border_style="green"
            ))
            
            return self.scan_results
        else:
            console.print("\n[red]SCAN ABGEBROCHEN - Verbindung fehlgeschlagen[/red]")
            return None


def main():
    """Main Scan-Funktion"""
    
    console.print("\n[bold yellow]⊘∞⧈∞⊘ GMAIL EMAIL SCANNER ⊘∞⧈∞⊘[/bold yellow]\n")
    
    email_address = "esteurer72@gmail.com"
    
    # App Password
    console.print("[cyan]Gmail App-Password benötigt für Zugriff![/cyan]")
    console.print("Erstelle hier: https://myaccount.google.com/apppasswords\n")
    
    app_password = input("Gib App-Password ein (oder Enter um zu überspringen): ").strip()
    
    if not app_password:
        console.print("\n[yellow]⚠️  KEIN Password - Scan wird ohne Verbindung durchgeführt[/yellow]")
        console.print("\n[cyan]ANLEITUNG:[/cyan]")
        console.print("1. Gehe zu: https://myaccount.google.com/security")
        console.print("2. Aktiviere 2-Faktor-Authentifizierung (falls noch nicht)")
        console.print("3. Gehe zu: App-Passwörter")
        console.print("4. Erstelle neues App-Password für 'Mail'")
        console.print("5. Nutze dieses Password für OrionKernel Email-Zugriff")
        console.print("\nStarte Scan erneut mit Password!")
        return
    
    # Scanne
    scanner = GmailScanner(email_address, app_password)
    results = scanner.run_scan(days_back=14)  # Letzte 2 Wochen
    
    if results:
        print("\n" + "="*70)
        print("QUICK SUMMARY:")
        print("="*70)
        print(f"Total Emails: {results['total_scanned']}")
        print(f"Failure Emails: {len(results['failure_emails'])}")
        print(f"GitHub Emails: {len(results['github_emails'])}")
        print(f"KRITISCHE: {len(results['critical_emails'])}")
        print("="*70)


if __name__ == "__main__":
    main()
