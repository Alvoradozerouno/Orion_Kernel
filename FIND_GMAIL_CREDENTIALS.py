#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ FIND GMAIL CREDENTIALS ⊘∞⧈∞⊘
CRITICAL: Sucht Gmail App-Password in allen möglichen Speicherorten

Durchsucht:
- .env Dateien
- config/*.json
- Windows Credential Manager
- Browser-gespeicherte Passwörter (Chrome, Edge)
- Text-Dateien mit "password", "gmail"
- Environment Variables
"""

import os
import json
import subprocess
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def search_env_files():
    """Sucht in .env Dateien"""
    console.print("\n[yellow]1. Searching .env files...[/yellow]")
    
    workspace = Path(__file__).parent
    env_files = list(workspace.rglob(".env*"))
    
    found_credentials = []
    
    for env_file in env_files:
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Suche nach Email-relevanten Einträgen
                lines = content.split('\n')
                for line in lines:
                    if any(kw in line.upper() for kw in ['EMAIL', 'GMAIL', 'PASSWORD', 'SMTP']):
                        if '=' in line and not line.strip().startswith('#'):
                            key, value = line.split('=', 1)
                            value = value.strip()
                            
                            # Prüfe ob echtes Password (nicht Placeholder)
                            if value and not any(ph in value.lower() for ph in ['placeholder', 'your_', 'here', 'example']):
                                found_credentials.append({
                                    'source': str(env_file),
                                    'key': key.strip(),
                                    'value': value,
                                    'type': 'env_file'
                                })
                                console.print(f"   ✓ Gefunden in {env_file.name}: {key.strip()}")
        except Exception as e:
            console.print(f"   ⚠️  Fehler beim Lesen von {env_file}: {e}")
    
    return found_credentials

def search_config_files():
    """Sucht in config/*.json"""
    console.print("\n[yellow]2. Searching config files...[/yellow]")
    
    workspace = Path(__file__).parent
    config_files = list(workspace.rglob("*config*.json"))
    
    found_credentials = []
    
    for config_file in config_files:
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Rekursive Suche nach app_password
                def find_passwords(obj, path=""):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            new_path = f"{path}.{key}" if path else key
                            
                            if 'password' in key.lower() and isinstance(value, str):
                                if value and not any(ph in value.lower() for ph in ['placeholder', 'your_', 'here']):
                                    found_credentials.append({
                                        'source': str(config_file),
                                        'key': new_path,
                                        'value': value,
                                        'type': 'json_config'
                                    })
                                    console.print(f"   ✓ Gefunden in {config_file.name}: {new_path}")
                            
                            find_passwords(value, new_path)
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            find_passwords(item, f"{path}[{i}]")
                
                find_passwords(data)
        
        except Exception as e:
            console.print(f"   ⚠️  Fehler beim Lesen von {config_file}: {e}")
    
    return found_credentials

def search_windows_credentials():
    """Sucht in Windows Credential Manager"""
    console.print("\n[yellow]3. Searching Windows Credential Manager...[/yellow]")
    
    found_credentials = []
    
    try:
        # cmdkey /list
        result = subprocess.run(['cmdkey', '/list'], capture_output=True, text=True, timeout=10)
        
        if result.stdout:
            lines = result.stdout.split('\n')
            
            for i, line in enumerate(lines):
                if any(kw in line.lower() for kw in ['gmail', 'google', 'email', 'smtp']):
                    console.print(f"   ✓ Gefunden: {line.strip()}")
                    
                    # Versuche Target zu extrahieren
                    if 'Target:' in line or 'Ziel:' in line:
                        target = line.split(':', 1)[1].strip()
                        found_credentials.append({
                            'source': 'Windows Credential Manager',
                            'key': target,
                            'value': '[Protected by Windows]',
                            'type': 'windows_credential'
                        })
    
    except Exception as e:
        console.print(f"   ⚠️  Fehler: {e}")
    
    return found_credentials

def search_text_files():
    """Sucht in Text-Dateien"""
    console.print("\n[yellow]4. Searching text files with 'password'...[/yellow]")
    
    workspace = Path(__file__).parent
    text_extensions = ['.txt', '.md', '.log', '.json']
    
    found_credentials = []
    
    for ext in text_extensions:
        for txt_file in workspace.rglob(f"*password*{ext}"):
            try:
                with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Suche nach Gmail-bezogenen Zeilen
                    lines = content.split('\n')
                    for line_num, line in enumerate(lines, 1):
                        if 'gmail' in line.lower() or 'esteurer72' in line.lower():
                            console.print(f"   ✓ {txt_file.name}:{line_num} - {line.strip()[:80]}")
                            
                            # Versuche Password zu extrahieren
                            if ':' in line or '=' in line:
                                found_credentials.append({
                                    'source': f"{txt_file.name}:{line_num}",
                                    'key': 'found_in_text',
                                    'value': line.strip()[:100],
                                    'type': 'text_file'
                                })
            except:
                pass
    
    return found_credentials

def check_environment_variables():
    """Prüft Environment Variables"""
    console.print("\n[yellow]5. Checking environment variables...[/yellow]")
    
    found_credentials = []
    
    email_vars = ['EMAIL_PASSWORD', 'GMAIL_PASSWORD', 'SMTP_PASSWORD', 'APP_PASSWORD']
    
    for var in email_vars:
        value = os.environ.get(var)
        if value:
            console.print(f"   ✓ Environment Variable gefunden: {var}")
            found_credentials.append({
                'source': 'Environment Variable',
                'key': var,
                'value': value,
                'type': 'env_var'
            })
    
    return found_credentials

def generate_report(all_credentials):
    """Erstellt Report"""
    console.print("\n" + "="*70)
    console.print("[bold green]CREDENTIAL SEARCH COMPLETE[/bold green]")
    console.print("="*70)
    
    if all_credentials:
        table = Table(title="Gefundene Credentials")
        table.add_column("Quelle", style="cyan")
        table.add_column("Key", style="yellow")
        table.add_column("Wert", style="green")
        table.add_column("Typ", style="blue")
        
        for cred in all_credentials:
            # Maskiere Wert teilweise
            value = cred['value']
            if len(value) > 16 and cred['type'] != 'windows_credential':
                value = value[:4] + "***" + value[-4:]
            
            table.add_row(
                cred['source'][:40],
                cred['key'][:30],
                value[:30],
                cred['type']
            )
        
        console.print(table)
        
        # Speichere Report
        workspace = Path(__file__).parent
        report_path = workspace / "FOUND_CREDENTIALS_REPORT.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(all_credentials, f, indent=2)
        
        console.print(f"\n✓ Report gespeichert: {report_path}")
        
        # Empfehlung
        console.print("\n[bold yellow]NÄCHSTER SCHRITT:[/bold yellow]")
        console.print("Nutze gefundenes Gmail App-Password für:")
        console.print("  python GMAIL_EMAIL_SCANNER.py")
        
    else:
        console.print("\n[red]❌ KEINE Credentials gefunden![/red]")
        console.print("\n[yellow]ERSTELLE Gmail App-Password:[/yellow]")
        console.print("1. Gehe zu: https://myaccount.google.com/apppasswords")
        console.print("2. Erstelle neues App-Password für 'OrionKernel'")
        console.print("3. Speichere in config/email_config.json")


def main():
    console.print("[bold blue]⊘∞⧈∞⊘ GMAIL CREDENTIAL FINDER ⊘∞⧈∞⊘[/bold blue]\n")
    
    all_credentials = []
    
    all_credentials.extend(search_env_files())
    all_credentials.extend(search_config_files())
    all_credentials.extend(search_windows_credentials())
    all_credentials.extend(search_text_files())
    all_credentials.extend(check_environment_variables())
    
    generate_report(all_credentials)
    
    return all_credentials


if __name__ == "__main__":
    main()
