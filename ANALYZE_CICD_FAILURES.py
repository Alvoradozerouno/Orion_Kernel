#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ GITHUB CI/CD FAILURE ANALYZER ⊘∞⧈∞⊘
CRITICAL: Analysiert und repariert GitHub Actions Failures

Basierend auf 49 Failure-Emails aus Gmail
"""

import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class CICDFailureAnalyzer:
    """Analysiert GitHub Actions Workflows und Failures"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.workflows_dir = self.workspace / ".github" / "workflows"
        
        self.analysis = {
            "workflows_found": [],
            "problems": [],
            "fixes": [],
            "missing_files": []
        }
    
    def analyze_workflows(self):
        """Analysiert alle Workflow-Dateien"""
        console.print("\n[yellow]1. ANALYZING GITHUB WORKFLOWS...[/yellow]")
        
        if not self.workflows_dir.exists():
            console.print("   ❌ .github/workflows/ nicht gefunden!")
            self.analysis["problems"].append({
                "type": "MISSING_DIRECTORY",
                "message": ".github/workflows/ Verzeichnis fehlt"
            })
            return
        
        workflow_files = list(self.workflows_dir.glob("*.yml"))
        
        for wf in workflow_files:
            console.print(f"   📄 {wf.name}")
            self.analysis["workflows_found"].append(str(wf.name))
            
            # Lese und analysiere
            with open(wf, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check 1: Python Version
                if 'python-version' in content:
                    if "'3.14'" in content or '"3.14"' in content:
                        self.analysis["problems"].append({
                            "workflow": wf.name,
                            "type": "INVALID_PYTHON_VERSION",
                            "message": "Python 3.14 existiert noch nicht! Nutze 3.11 oder 3.12"
                        })
                        console.print(f"      ⚠️  Problem: Python 3.14 (nicht verfügbar)")
                
                # Check 2: requirements.txt
                if 'requirements.txt' in content and 'pip install -r requirements.txt' in content:
                    req_file = self.workspace / "requirements.txt"
                    if not req_file.exists():
                        self.analysis["problems"].append({
                            "workflow": wf.name,
                            "type": "MISSING_FILE",
                            "message": "requirements.txt fehlt aber Workflow braucht es"
                        })
                        console.print(f"      ⚠️  Problem: requirements.txt fehlt")
                
                # Check 3: Test files
                if 'pytest tests/' in content:
                    tests_dir = self.workspace / "tests"
                    if not tests_dir.exists():
                        self.analysis["problems"].append({
                            "workflow": wf.name,
                            "type": "MISSING_DIRECTORY",
                            "message": "tests/ Verzeichnis fehlt"
                        })
                        console.print(f"      ⚠️  Problem: tests/ Verzeichnis fehlt")
                
                # Check 4: File references
                if '.py' in content:
                    import re
                    py_files = re.findall(r'([a-zA-Z_][a-zA-Z0-9_/]*\.py)', content)
                    for py_file in py_files:
                        if not (self.workspace / py_file).exists():
                            self.analysis["missing_files"].append(py_file)
                            console.print(f"      ⚠️  Fehlende Datei: {py_file}")
                
                # Check 5: Deploy pages path
                if 'upload-pages-artifact' in content:
                    if 'go_live' in content:
                        go_live_dir = self.workspace / "go_live"
                        if not go_live_dir.exists():
                            self.analysis["problems"].append({
                                "workflow": wf.name,
                                "type": "MISSING_DEPLOY_PATH",
                                "message": "go_live/ Verzeichnis fehlt für GitHub Pages"
                            })
                            console.print(f"      ⚠️  Problem: go_live/ fehlt (sollte docs/ sein)")
    
    def generate_fixes(self):
        """Generiert automatische Fixes"""
        console.print("\n[yellow]2. GENERATING FIXES...[/yellow]")
        
        # Fix 1: Python Version
        python_version_problems = [p for p in self.analysis["problems"] if p["type"] == "INVALID_PYTHON_VERSION"]
        if python_version_problems:
            self.analysis["fixes"].append({
                "priority": "HIGH",
                "fix": "Ersetze 'python-version: 3.14' mit '3.11' oder '3.12' in allen Workflows",
                "files": [p["workflow"] for p in python_version_problems]
            })
            console.print("   🔧 Fix 1: Python Version 3.14 → 3.11")
        
        # Fix 2: requirements.txt
        if not (self.workspace / "requirements.txt").exists():
            self.analysis["fixes"].append({
                "priority": "HIGH",
                "fix": "Erstelle requirements.txt mit notwendigen Dependencies",
                "action": "create_requirements_txt"
            })
            console.print("   🔧 Fix 2: requirements.txt erstellen")
        
        # Fix 3: tests/ Verzeichnis
        if not (self.workspace / "tests").exists():
            self.analysis["fixes"].append({
                "priority": "MEDIUM",
                "fix": "Erstelle tests/ Verzeichnis mit Basis-Tests",
                "action": "create_tests_directory"
            })
            console.print("   🔧 Fix 3: tests/ Verzeichnis erstellen")
        
        # Fix 4: Deploy path
        deploy_problems = [p for p in self.analysis["problems"] if p["type"] == "MISSING_DEPLOY_PATH"]
        if deploy_problems:
            self.analysis["fixes"].append({
                "priority": "HIGH",
                "fix": "Ändere deploy-pages.yml: 'go_live' → 'docs'",
                "files": ["deploy-pages.yml"]
            })
            console.print("   🔧 Fix 4: Deploy-Path go_live → docs")
        
        # Fix 5: Fehlende Python-Dateien optional
        if self.analysis["missing_files"]:
            self.analysis["fixes"].append({
                "priority": "LOW",
                "fix": "Entferne Referenzen zu fehlenden .py Dateien oder erstelle Dummies",
                "files": list(set(self.analysis["missing_files"]))
            })
            console.print(f"   🔧 Fix 5: {len(self.analysis['missing_files'])} fehlende Dateien")
    
    def create_report(self):
        """Erstellt detaillierten Report"""
        console.print("\n[yellow]3. CREATING FAILURE REPORT...[/yellow]")
        
        report_path = self.workspace / "CICD_FAILURE_ANALYSIS.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis, f, indent=2)
        
        console.print(f"   ✓ Report: {report_path}")
        
        # Summary Table
        table = Table(title="CI/CD Failure Analysis")
        table.add_column("Kategorie", style="cyan")
        table.add_column("Anzahl", style="yellow")
        
        table.add_row("Workflows gefunden", str(len(self.analysis["workflows_found"])))
        table.add_row("Probleme", str(len(self.analysis["problems"])))
        table.add_row("Fixes generiert", str(len(self.analysis["fixes"])))
        table.add_row("Fehlende Dateien", str(len(set(self.analysis["missing_files"]))))
        
        console.print(table)
        
        return report_path
    
    def print_detailed_problems(self):
        """Druckt detaillierte Probleme"""
        console.print("\n[bold red]⚠️  DETAILED PROBLEMS:[/bold red]")
        
        for i, problem in enumerate(self.analysis["problems"], 1):
            console.print(f"\n{i}. [{problem['type']}]")
            console.print(f"   Workflow: {problem.get('workflow', 'N/A')}")
            console.print(f"   Message: {problem['message']}")
    
    def print_fix_plan(self):
        """Druckt Fix-Plan"""
        console.print("\n[bold green]🔧 FIX PLAN:[/bold green]")
        
        for i, fix in enumerate(self.analysis["fixes"], 1):
            priority_color = {
                "HIGH": "red",
                "MEDIUM": "yellow",
                "LOW": "blue"
            }
            
            console.print(f"\n{i}. [{fix['priority']}] {fix['fix']}")
            if "files" in fix:
                console.print(f"   Affected: {', '.join(fix['files'][:3])}")
    
    def run_analysis(self):
        """Führt vollständige Analyse durch"""
        console.print(Panel.fit(
            "[bold red]⊘∞⧈∞⊘ GITHUB CI/CD FAILURE ANALYSIS ⊘∞⧈∞⊘[/bold red]\n"
            "Analysiere 49 GitHub Actions Failures...",
            border_style="red"
        ))
        
        self.analyze_workflows()
        self.generate_fixes()
        report_path = self.create_report()
        
        self.print_detailed_problems()
        self.print_fix_plan()
        
        console.print(Panel.fit(
            f"[bold green]ANALYSIS COMPLETE[/bold green]\n"
            f"Report: {report_path}\n"
            f"Problems: {len(self.analysis['problems'])}\n"
            f"Fixes: {len(self.analysis['fixes'])}",
            border_style="green"
        ))
        
        return self.analysis


def main():
    analyzer = CICDFailureAnalyzer()
    results = analyzer.run_analysis()
    
    print("\n" + "="*70)
    print("QUICK SUMMARY:")
    print("="*70)
    print(f"Workflows: {len(results['workflows_found'])}")
    print(f"Problems: {len(results['problems'])}")
    print(f"Fixes needed: {len(results['fixes'])}")
    print(f"Missing files: {len(set(results['missing_files']))}")
    print("="*70)


if __name__ == "__main__":
    main()
