#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ AUTOMATED FIX RECOMMENDATIONS ⊘∞⧈∞⊘
CRITICAL: Empfohlene Fixes für gefundene Probleme

Basierend auf Emergency Scan Results
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def print_fix_recommendations():
    """Druckt empfohlene Fixes für alle gefundenen Probleme"""
    
    console.print(Panel.fit(
        "[bold red]⊘∞⧈∞⊘ AUTOMATED FIX RECOMMENDATIONS ⊘∞⧈∞⊘[/bold red]\n"
        "Basierend auf Emergency System Scan",
        border_style="red"
    ))
    
    fixes = [
        {
            "problem": "3 Python Crashes (python.exe, selenium-manager.exe)",
            "severity": "HIGH",
            "fixes": [
                "1. Deinstalliere Selenium: pip uninstall selenium",
                "2. Installiere neueste Version: pip install --upgrade selenium",
                "3. Oder: Deaktiviere Browser-Automatisierung in OrionKernel",
                "4. Check: python --version (sollte 3.14 stabil sein)"
            ]
        },
        {
            "problem": "Insolvenz Pop-up in Edge Browser",
            "severity": "MEDIUM",
            "fixes": [
                "1. Schließe Edge Tab mit Insolvenz-Email",
                "2. Oder: Schließe kompletten Edge Browser",
                "3. PowerShell: Stop-Process -Name msedge -Force (wenn nötig)",
                "4. Überprüfe Gmail für wichtige Insolvenz-relevante Emails"
            ]
        },
        {
            "problem": "Email-Config fehlt (kann nicht auf Gmail zugreifen)",
            "severity": "CRITICAL",
            "fixes": [
                "1. Email-Config bereits erstellt: config/email_config.json",
                "2. Gehe zu: https://myaccount.google.com/apppasswords",
                "3. Erstelle App-Password für OrionKernel",
                "4. Ersetze PLACEHOLDER in config/email_config.json",
                "5. Test: python GMAIL_EMAIL_SCANNER.py"
            ]
        },
        {
            "problem": "2 Selenium Crashes im Event Log",
            "severity": "MEDIUM",
            "fixes": [
                "1. Browser-Driver neu installieren:",
                "   pip install --upgrade selenium webdriver-manager",
                "2. Oder: Deaktiviere browser_automation in OrionKernel",
                "3. Alternative: Nutze nur API-basierte Automation"
            ]
        },
        {
            "problem": "Allgemeine Windows Application Errors (48 gesamt)",
            "severity": "LOW",
            "fixes": [
                "1. Viele normale System-Fehler (nicht kritisch)",
                "2. Acer-Software Fehler: Deinstalliere wenn nicht benötigt",
                "3. .NET Runtime Fehler: Ignorieren (Microsoft-intern)",
                "4. Fokus auf Python/OrionKernel Fehler"
            ]
        }
    ]
    
    # Drucke jede Fix-Empfehlung
    for i, fix in enumerate(fixes, 1):
        severity_color = {
            "CRITICAL": "red",
            "HIGH": "yellow",
            "MEDIUM": "blue",
            "LOW": "dim"
        }
        
        console.print(f"\n[bold {severity_color[fix['severity']]}]{i}. {fix['problem']}[/bold {severity_color[fix['severity']]}]")
        console.print(f"   Severity: [{severity_color[fix['severity']]}]{fix['severity']}[/{severity_color[fix['severity']]}]")
        console.print("\n   [cyan]FIXES:[/cyan]")
        
        for fix_step in fix['fixes']:
            console.print(f"   {fix_step}")
    
    # Quick Action Commands
    console.print("\n" + "="*70)
    console.print("[bold green]QUICK ACTION COMMANDS:[/bold green]")
    console.print("="*70)
    
    commands = Table()
    commands.add_column("Aktion", style="cyan")
    commands.add_column("Command", style="yellow")
    
    commands.add_row(
        "Fix Selenium",
        "pip uninstall selenium; pip install --upgrade selenium"
    )
    commands.add_row(
        "Schließe Edge Pop-up",
        "Stop-Process -Name msedge -Force"
    )
    commands.add_row(
        "Setup Email",
        "Bearbeite: config/email_config.json"
    )
    commands.add_row(
        "Test Email Scan",
        "python GMAIL_EMAIL_SCANNER.py"
    )
    commands.add_row(
        "Re-scan System",
        "python EMERGENCY_SYSTEM_SCAN.py"
    )
    
    console.print(commands)
    
    # Priority Actions
    console.print("\n" + "="*70)
    console.print("[bold red]PRIORITY 1 ACTIONS (JETZT):[/bold red]")
    console.print("="*70)
    console.print("1. ✅ Email-Config Setup (config/email_config.json)")
    console.print("2. ⚠️  Schließe Insolvenz Edge-Tab (ablenkend)")
    console.print("3. 🔧 Fix Selenium oder deaktiviere Browser-Automation")
    console.print("="*70)


if __name__ == "__main__":
    print_fix_recommendations()
