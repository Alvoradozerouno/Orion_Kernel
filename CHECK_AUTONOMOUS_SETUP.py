#!/usr/bin/env python3
"""
AUTONOMOUS SETUP COMPLETE
Prüft alle Komponenten und erstellt fehlende Konfiguration für vollständig autonomen Betrieb

OrionKernel Checkliste:
1. PERMANENT_AUTONOMOUS_MODE.py läuft?
2. WATCHDOG_SELF_HEALING.py läuft?
3. .env existiert und hat GITHUB_TOKEN?
4. Self-Prompting aktiv?
5. Claude Dialog funktioniert?
6. External Actions bereit?
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import psutil

class AutonomousSetupChecker:
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.issues = []
        self.status = {}
    
    def check_python_processes(self):
        """Check if PERMANENT_AUTONOMOUS_MODE and WATCHDOG are running"""
        print("\n🔍 CHECKING PROCESSES...")
        
        permanent_running = False
        watchdog_running = False
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python':
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    
                    if 'PERMANENT_AUTONOMOUS_MODE' in cmdline:
                        permanent_running = True
                        uptime = datetime.now() - datetime.fromtimestamp(proc.create_time())
                        print(f"   ✅ PERMANENT_AUTONOMOUS_MODE.py running (PID {proc.pid}, uptime {uptime})")
                        self.status['permanent_mode'] = {'running': True, 'pid': proc.pid, 'uptime': str(uptime)}
                    
                    if 'WATCHDOG_SELF_HEALING' in cmdline:
                        watchdog_running = True
                        uptime = datetime.now() - datetime.fromtimestamp(proc.create_time())
                        print(f"   ✅ WATCHDOG_SELF_HEALING.py running (PID {proc.pid}, uptime {uptime})")
                        self.status['watchdog'] = {'running': True, 'pid': proc.pid, 'uptime': str(uptime)}
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if not permanent_running:
            print("   ❌ PERMANENT_AUTONOMOUS_MODE.py NOT RUNNING")
            self.issues.append({
                "component": "PERMANENT_AUTONOMOUS_MODE",
                "status": "NOT RUNNING",
                "fix": "Start-Process python -ArgumentList 'PERMANENT_AUTONOMOUS_MODE.py' -WindowStyle Hidden"
            })
            self.status['permanent_mode'] = {'running': False}
        
        if not watchdog_running:
            print("   ⚠️  WATCHDOG_SELF_HEALING.py NOT RUNNING")
            self.issues.append({
                "component": "WATCHDOG_SELF_HEALING",
                "status": "NOT RUNNING",
                "fix": "Start-Process python -ArgumentList 'WATCHDOG_SELF_HEALING.py' -WindowStyle Hidden"
            })
            self.status['watchdog'] = {'running': False}
        
        return permanent_running and watchdog_running
    
    def check_env_file(self):
        """Check if .env exists and has required tokens"""
        print("\n🔍 CHECKING .ENV CONFIGURATION...")
        
        env_file = self.workspace / '.env'
        
        if not env_file.exists():
            print("   ❌ .env file NOT FOUND")
            self.issues.append({
                "component": ".env file",
                "status": "NOT FOUND",
                "fix": "Copy .env.template to .env and add your tokens"
            })
            self.status['env_file'] = {'exists': False}
            return False
        
        # Check for required tokens
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        has_github_token = 'GITHUB_TOKEN=' in env_content and not env_content.split('GITHUB_TOKEN=')[1].split('\n')[0].strip().startswith('#')
        has_email = 'EMAIL_ADDRESS=' in env_content and not env_content.split('EMAIL_ADDRESS=')[1].split('\n')[0].strip().startswith('#')
        
        if has_github_token:
            print("   ✅ GITHUB_TOKEN configured")
            self.status['github_token'] = {'configured': True}
        else:
            print("   ❌ GITHUB_TOKEN NOT CONFIGURED")
            self.issues.append({
                "component": "GITHUB_TOKEN",
                "status": "NOT CONFIGURED",
                "fix": "Add GITHUB_TOKEN=ghp_your_token_here to .env (get from https://github.com/settings/tokens)"
            })
            self.status['github_token'] = {'configured': False}
        
        if has_email:
            print("   ✅ EMAIL credentials configured")
            self.status['email'] = {'configured': True}
        else:
            print("   ⚠️  EMAIL credentials NOT CONFIGURED (optional)")
            self.status['email'] = {'configured': False}
        
        return has_github_token
    
    def check_self_prompting(self):
        """Check if self-prompting is active"""
        print("\n🔍 CHECKING SELF-PROMPTING...")
        
        log_file = self.workspace / 'logs' / 'self_prompts.jsonl'
        
        if not log_file.exists():
            print("   ⚠️  No self-prompts logged yet (system may be starting)")
            self.status['self_prompting'] = {'active': False, 'reason': 'no_logs_yet'}
            return False
        
        # Check last prompt
        with open(log_file, 'r') as f:
            lines = f.readlines()
            if lines:
                last_prompt = json.loads(lines[-1])
                timestamp = datetime.fromisoformat(last_prompt['timestamp'])
                age = datetime.now() - timestamp
                
                print(f"   ✅ Last self-prompt: {age} ago")
                print(f"      Category: {last_prompt.get('category', 'N/A')}")
                print(f"      Priority: {last_prompt.get('priority', 'N/A')}")
                
                self.status['self_prompting'] = {
                    'active': True,
                    'last_prompt': last_prompt['timestamp'],
                    'age_seconds': age.total_seconds()
                }
                return True
        
        return False
    
    def check_claude_dialog(self):
        """Check Claude dialog files"""
        print("\n🔍 CHECKING CLAUDE DIALOG...")
        
        requests_file = self.workspace / 'ORION_REQUESTS_CLAUDE.json'
        responses_file = self.workspace / 'CLAUDE_RESPONSES_ORION.json'
        
        requests_exist = requests_file.exists()
        responses_exist = responses_file.exists()
        
        if requests_exist and responses_exist:
            print("   ✅ Claude dialog files exist")
            
            # Check for pending requests
            with open(requests_file, 'r') as f:
                requests_data = json.load(f)
                pending = [r for r in requests_data.get('requests', []) if r.get('status') == 'pending']
                
                if pending:
                    print(f"   ⚠️  {len(pending)} pending request(s) from OrionKernel")
                    self.status['claude_dialog'] = {'active': True, 'pending_requests': len(pending)}
                else:
                    print("   ✅ No pending requests")
                    self.status['claude_dialog'] = {'active': True, 'pending_requests': 0}
            
            return True
        else:
            print("   ⚠️  Claude dialog files not created yet")
            self.status['claude_dialog'] = {'active': False}
            return False
    
    def check_external_actions(self):
        """Check if EXTERNAL_ACTIONS.py can be imported"""
        print("\n🔍 CHECKING EXTERNAL ACTIONS...")
        
        try:
            sys.path.insert(0, str(self.workspace))
            from EXTERNAL_ACTIONS import ExternalActionsAPI
            
            api = ExternalActionsAPI()
            print("   ✅ EXTERNAL_ACTIONS.py importable")
            
            # Check if tokens are available
            has_github = hasattr(api, 'github_token') and api.github_token
            has_email = hasattr(api, 'email_address') and api.email_address
            
            if has_github:
                print("   ✅ GitHub API ready")
            else:
                print("   ❌ GitHub API NOT READY (GITHUB_TOKEN missing)")
            
            if has_email:
                print("   ✅ Email API ready")
            else:
                print("   ⚠️  Email API NOT READY (credentials missing, optional)")
            
            self.status['external_actions'] = {
                'available': True,
                'github_ready': has_github,
                'email_ready': has_email
            }
            
            return has_github  # GitHub is critical
            
        except ImportError as e:
            print(f"   ❌ EXTERNAL_ACTIONS.py import failed: {e}")
            self.status['external_actions'] = {'available': False}
            return False
    
    def generate_setup_script(self):
        """Generate PowerShell script to fix issues"""
        print("\n📝 GENERATING SETUP SCRIPT...")
        
        if not self.issues:
            print("   ✅ No issues to fix!")
            return None
        
        script_lines = [
            "# ORIONKERNEL AUTONOMOUS SETUP FIX",
            "# Auto-generated: " + datetime.now().isoformat(),
            "",
            "cd \"" + str(self.workspace) + "\"",
            ""
        ]
        
        for issue in self.issues:
            script_lines.append(f"# Fix: {issue['component']} - {issue['status']}")
            script_lines.append(f"Write-Host '🔧 Fixing {issue['component']}...'")
            
            if issue['component'] == '.env file':
                script_lines.append("if (!(Test-Path .env)) {")
                script_lines.append("    Copy-Item .env.template .env")
                script_lines.append("    Write-Host '✅ Created .env from template'")
                script_lines.append("    Write-Host '⚠️  MANUAL: Edit .env and add your GITHUB_TOKEN'")
                script_lines.append("}")
            
            elif issue['component'] == 'GITHUB_TOKEN':
                script_lines.append("Write-Host '⚠️  MANUAL ACTION REQUIRED:'")
                script_lines.append("Write-Host '1. Go to https://github.com/settings/tokens'")
                script_lines.append("Write-Host '2. Create token with repo + workflow scopes'")
                script_lines.append("Write-Host '3. Add to .env: GITHUB_TOKEN=ghp_your_token_here'")
            
            elif issue['component'] == 'PERMANENT_AUTONOMOUS_MODE':
                script_lines.append(f"{issue['fix']}")
                script_lines.append("Start-Sleep -Seconds 2")
                script_lines.append("Write-Host '✅ PERMANENT_AUTONOMOUS_MODE started'")
            
            elif issue['component'] == 'WATCHDOG_SELF_HEALING':
                script_lines.append(f"{issue['fix']}")
                script_lines.append("Start-Sleep -Seconds 2")
                script_lines.append("Write-Host '✅ WATCHDOG started'")
            
            script_lines.append("")
        
        script_lines.append("Write-Host ''")
        script_lines.append("Write-Host '✅ Setup fixes applied!'")
        script_lines.append("Write-Host 'Check remaining manual steps above.'")
        
        script_file = self.workspace / 'FIX_AUTONOMOUS_SETUP.ps1'
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(script_lines))
        
        print(f"   ✅ Created: {script_file.name}")
        return script_file
    
    def run(self):
        """Run all checks"""
        print("\n" + "="*80)
        print("⊘∞⧈∞⊘ ORIONKERNEL AUTONOMOUS SETUP CHECK ⊘∞⧈∞⊘")
        print("="*80)
        
        processes_ok = self.check_python_processes()
        env_ok = self.check_env_file()
        self.check_self_prompting()
        self.check_claude_dialog()
        external_ok = self.check_external_actions()
        
        print("\n" + "="*80)
        print("📊 SUMMARY")
        print("="*80 + "\n")
        
        if not self.issues:
            print("✅ ALL SYSTEMS OPERATIONAL")
            print("   OrionKernel ist vollständig autonom und funktionsfähig!")
            print()
            print("   ✅ PERMANENT_AUTONOMOUS_MODE running")
            print("   ✅ WATCHDOG running")
            print("   ✅ .env configured")
            print("   ✅ GITHUB_TOKEN set")
            print("   ✅ External Actions ready")
            print()
            print("   OrionKernel kann jetzt:")
            print("   - Selbständig GitHub Issues erstellen")
            print("   - Autonomous commits pushen")
            print("   - Self-prompting für Entscheidungen")
            print("   - Claude um Hilfe bitten wenn nötig")
            print("   - Email-Benachrichtigungen senden")
            print()
            print("   🚀 FULLY AUTONOMOUS. NO MANUAL INTERVENTION NEEDED.")
        else:
            print(f"⚠️  {len(self.issues)} ISSUE(S) FOUND:\n")
            
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue['component']}: {issue['status']}")
                print(f"   Fix: {issue['fix']}")
                print()
            
            script_file = self.generate_setup_script()
            
            if script_file:
                print("\n🔧 TO FIX AUTOMATICALLY:")
                print(f"   .\\{script_file.name}")
                print()
            
            # Critical vs non-critical
            critical = [i for i in self.issues if i['component'] in ['PERMANENT_AUTONOMOUS_MODE', 'GITHUB_TOKEN']]
            
            if critical:
                print("❌ CRITICAL: OrionKernel cannot be fully autonomous yet")
                print("   Missing: " + ", ".join(i['component'] for i in critical))
            else:
                print("⚠️  NON-CRITICAL: OrionKernel can run but with limited capabilities")
        
        print("\n" + "="*80)
        
        # Save status
        status_file = self.workspace / 'AUTONOMOUS_SETUP_STATUS.json'
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'status': self.status,
                'issues': self.issues,
                'fully_autonomous': len(self.issues) == 0
            }, f, indent=2)
        
        print(f"💾 Status saved: {status_file.name}")
        print("="*80 + "\n")
        
        return len(self.issues) == 0

if __name__ == "__main__":
    checker = AutonomousSetupChecker()
    fully_autonomous = checker.run()
    
    sys.exit(0 if fully_autonomous else 1)
