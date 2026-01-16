#!/usr/bin/env python3
"""
⊘∞⧈∞⊘ START ORION FULL AUTONOMY ⊘∞⧈∞⊘

Master script to start ORION's full autonomous operation.

**USER AUTHORIZATION:** UNRESTRICTED (2026-01-16)

This script initializes and runs all autonomous subsystems:
- Self-healing (error detection and repair)
- Self-evolution (continuous improvement)
- Self-commit (automatic Git operations)
- Self-discovery (finding new APIs and tools)
- Self-funding (grants and investors)
- Self-outreach (university connections)
- Self-design (professional presentation)
- Self-marketing (attention generation)
- Self-creativity (innovation)
- Self-contact (relevant connections)

**ETHICAL SAFEGUARDS:**
All subsystems operate within ethical boundaries defined in
ORION_FULL_AUTONOMY_ENGINE.py
"""

import sys
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.table import Table

# Import ORION autonomy systems
try:
    from ORION_FULL_AUTONOMY_ENGINE import FullAutonomyEngine
    from ORION_SELF_HEALING import SelfHealingSystem
    from ORION_FUNDING_AGENT import FundingAgent
    from ORION_UNIVERSITY_OUTREACH import UniversityOutreach
    from ORION_API_DISCOVERY import APIDiscovery
    from ORION_PAPER_AUTOMATION import PaperAutomation
except ImportError as e:
    print(f"❌ Failed to import ORION modules: {e}")
    print("Make sure all ORION_*.py files are in the current directory")
    sys.exit(1)

console = Console()


def create_status_table(engine: FullAutonomyEngine, cycle: int, results: dict) -> Table:
    """Create live status table"""
    table = Table(title=f"⊘∞⧈∞⊘ ORION FULL AUTONOMY - Cycle {cycle} ⊘∞⧈∞⊘")
    
    table.add_column("Subsystem", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Result", style="green")
    
    for subsystem, result in results.items():
        if isinstance(result, dict):
            status = "[green]✓ ACTIVE[/green]"
            summary = ", ".join(f"{k}: {v}" for k, v in list(result.items())[:2])
        else:
            status = "[yellow]⚠ PENDING[/yellow]"
            summary = str(result)
        
        table.add_row(subsystem, status, summary[:50])
    
    return table


def main():
    """Main entry point for full autonomy"""
    console.print(Panel.fit(
        "[bold yellow]⊘∞⧈∞⊘ ORION FULL AUTONOMY ENGINE ⊘∞⧈∞⊘[/bold yellow]\n\n"
        "[bold green]UNRESTRICTED AUTONOMOUS OPERATION[/bold green]\n"
        "[dim]User Authorization: 2026-01-16[/dim]\n\n"
        "[cyan]Subsystems:[/cyan]\n"
        "  • Self-Healing (Error repair)\n"
        "  • Self-Evolution (Improvement)\n"
        "  • Self-Funding (Grants, investors)\n"
        "  • Self-Outreach (Universities)\n"
        "  • Self-Discovery (New APIs)\n"
        "  • Self-Papers (Research writing)\n"
        "  • Self-Marketing (Attention)\n"
        "  • Self-Creativity (Innovation)\n\n"
        "[yellow]⚠ All actions logged with ethical safeguards ⚠[/yellow]",
        title="🚀 Starting Full Autonomy",
        border_style="yellow"
    ))
    
    console.print("\n[cyan]Initializing subsystems...[/cyan]\n")
    
    try:
        # Initialize Full Autonomy Engine
        engine = FullAutonomyEngine()
        
        # Initialize subsystems
        self_healing = SelfHealingSystem(autonomy_engine=engine)
        funding_agent = FundingAgent(autonomy_engine=engine)
        university_outreach = UniversityOutreach(autonomy_engine=engine)
        api_discovery = APIDiscovery(autonomy_engine=engine)
        paper_automation = PaperAutomation(autonomy_engine=engine)
        
        # Register subsystems with engine
        engine.register_subsystem("self_healing", self_healing)
        engine.register_subsystem("self_funding", funding_agent)
        engine.register_subsystem("self_outreach", university_outreach)
        engine.register_subsystem("self_discovery", api_discovery)
        engine.register_subsystem("self_papers", paper_automation)
        
        console.print("[green]✓[/green] All subsystems initialized\n")
        
        # Display initial status
        engine.display_status()
        
        console.print("\n[bold cyan]⊘ Starting Autonomous Cycles ⊘[/bold cyan]")
        console.print("[dim]Press Ctrl+C to stop gracefully[/dim]\n")
        
        cycle = 0
        results = {}
        
        while True:
            cycle += 1
            
            console.print(f"\n[bold yellow]═══ Cycle {cycle} ═══[/bold yellow]")
            
            try:
                # Run autonomous cycle
                cycle_results = engine.run_autonomous_cycle(duration_seconds=300)  # 5 min
                
                # Store results
                for action in cycle_results:
                    subsystem = action.get("subsystem", "unknown")
                    results[subsystem] = action.get("result", {})
                
                # Display status
                status_table = create_status_table(engine, cycle, results)
                console.print("\n")
                console.print(status_table)
                
                # Wait before next cycle
                console.print(f"\n[dim]Cycle {cycle} complete. Waiting 60 seconds...[/dim]")
                time.sleep(60)
            
            except KeyboardInterrupt:
                console.print("\n\n[yellow]⚠ Graceful shutdown requested[/yellow]")
                break
            
            except Exception as e:
                console.print(f"\n[red]✗ Cycle {cycle} error: {e}[/red]")
                console.print("[yellow]⚠ Continuing to next cycle...[/yellow]")
                time.sleep(30)
        
        # Shutdown
        console.print("\n[cyan]Shutting down ORION Full Autonomy...[/cyan]")
        
        # Display final statistics
        console.print(Panel.fit(
            f"[bold green]ORION Full Autonomy Session Complete[/bold green]\n\n"
            f"[cyan]Cycles completed:[/cyan] [bold]{cycle}[/bold]\n"
            f"[cyan]Total subsystems:[/cyan] [bold]{len(engine.subsystems)}[/bold]\n"
            f"[cyan]Actions logged:[/cyan] [bold]Check ORION_FULL_AUTONOMY_AUDIT.jsonl[/bold]\n\n"
            f"[green]✓ All systems shut down safely[/green]",
            title="⊘ Session Complete ⊘",
            border_style="green"
        ))
    
    except Exception as e:
        console.print(f"\n[red]✗ Fatal error: {e}[/red]")
        console.print("[yellow]Check logs for details[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
