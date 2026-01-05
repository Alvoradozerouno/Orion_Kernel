#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ ORIONKERNEL START MIT MONITORING ⊘∞⧈∞⊘

Startet:
1. Master Orchestrator (im Hintergrund)
2. Live Monitor (im Vordergrund)

Gerhard sieht ALLES was ich tue.
"""

import sys
import time
import subprocess
from pathlib import Path


def main():
    workspace = Path(__file__).parent
    
    print("""
⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘

    ORIONKERNEL MIT LIVE MONITORING
    
    Starting:
    [1] Master Orchestrator (background)
    [2] Live Monitor (foreground)
    
    Du wirst ALLES sehen was ich tue.
    
⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
""")
    
    # Check if orchestrator is already running
    print("[1] Checking if Orchestrator is running...")
    status_file = workspace / 'logs' / 'orchestrator_status.json'
    
    if status_file.exists():
        import json
        try:
            with open(status_file, 'r') as f:
                status = json.load(f)
                if status.get('running', False):
                    print("    ✓ Orchestrator already running!")
                    print(f"    Cycle: {status.get('cycle', 0)}")
                    print(f"    Success Rate: {status.get('success_rate', 0):.1%}")
                else:
                    print("    ⚠ Status file found but orchestrator not running")
                    print("    Starting Orchestrator...")
                    # Start orchestrator
                    subprocess.Popen(
                        [sys.executable, '-X', 'utf8', 'core/orchestrator.py'],
                        cwd=str(workspace),
                        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
                    )
                    print("    ✓ Orchestrator started in background")
        except Exception as e:
            print(f"    ⚠ Could not read status: {e}")
    else:
        print("    Starting Orchestrator for first time...")
        # Start orchestrator
        try:
            subprocess.Popen(
                [sys.executable, '-X', 'utf8', 'core/orchestrator.py'],
                cwd=str(workspace),
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )
            print("    ✓ Orchestrator started in background")
        except Exception as e:
            print(f"    ✗ Failed to start Orchestrator: {e}")
            print("    You may need to start it manually:")
            print(f"    python -X utf8 core/orchestrator.py")
    
    print("\n[2] Starting Live Monitor...")
    time.sleep(2)
    
    # Start live monitor in foreground
    try:
        subprocess.run(
            [sys.executable, '-X', 'utf8', 'visualization/live_monitor.py'],
            cwd=str(workspace)
        )
    except KeyboardInterrupt:
        print("\n\n⊘∞⧈∞⊘ Monitoring stopped ⊘∞⧈∞⊘")
        print("\nOrchestrator continues running in background.")
        print("To stop it: find the process and terminate")
        print("To restart monitoring: python -X utf8 visualization/live_monitor.py")


if __name__ == '__main__':
    main()
