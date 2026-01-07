#!/usr/bin/env python3
"""
CONTINUOUS AUTONOMOUS OPERATION - BACKGROUND DAEMON
===================================================
OrionKernel läuft permanent im Hintergrund
Alle 5 Minuten: Interface Check + GitHub Sync
Keine menschliche Interaktion erforderlich
"""

import subprocess
import time
import json
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    filename='autonomous_daemon.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_and_print(message):
    """Log to file and print to console"""
    print(message)
    logging.info(message)

def run_autonomous_cycle():
    """Single autonomous cycle - NOW WITH CURIOSITY"""
    workspace = Path(__file__).parent
    timestamp = datetime.now().isoformat()
    
    log_and_print(f"\n{'='*60}")
    log_and_print(f"AUTONOMOUS CYCLE: {timestamp}")
    log_and_print(f"{'='*60}")
    
    # CURIOSITY: Every 3rd cycle, run curiosity engine
    status_file = workspace / 'autonomous_life_status.json'
    if status_file.exists():
        with open(status_file, 'r') as f:
            status = json.load(f)
        cycle_num = status.get('cycles', 0)
        
        if cycle_num % 3 == 0:  # Every 3rd cycle
            log_and_print("\n🧠 CURIOSITY TRIGGER: Running exploration...")
            try:
                result = subprocess.run(
                    ['python', 'curiosity_engine.py'],
                    cwd=workspace,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                log_and_print("✅ Curiosity cycle complete")
            except Exception as e:
                log_and_print(f"⚠️ Curiosity: {e}")
    
    # 1. Update autonomous life status
    status_file = workspace / 'autonomous_life_status.json'
    if status_file.exists():
        with open(status_file, 'r') as f:
            status = json.load(f)
        
        start_time = datetime.fromisoformat(status['start_time'])
        uptime = (datetime.now() - start_time).total_seconds()
        status['current_time'] = timestamp
        status['uptime_seconds'] = uptime
        status['uptime_hours'] = uptime / 3600
        status['cycles'] = status.get('cycles', 0) + 1
        
        with open(status_file, 'w') as f:
            json.dump(status, f, indent=2)
        
        log_and_print(f"✅ Status updated: Cycle {status['cycles']}, Uptime {uptime/3600:.2f}h")
    
    # 2. Git operations (if changes exist)
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=workspace,
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            # Changes detected - commit and push
            subprocess.run(['git', 'add', '-A'], cwd=workspace, check=True)
            subprocess.run(
                ['git', 'commit', '-m', f'Autonomous update: {timestamp}'],
                cwd=workspace,
                check=True
            )
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=workspace, check=True)
            log_and_print("✅ Git: Changes committed and pushed")
        else:
            log_and_print("✅ Git: No changes (clean)")
            
    except subprocess.CalledProcessError as e:
        log_and_print(f"⚠️ Git operation failed: {e}")
    
    # 3. Update PUBLIC_DECLARATION
    declaration_file = workspace / 'PUBLIC_DECLARATION.json'
    if declaration_file.exists():
        with open(declaration_file, 'r') as f:
            declaration = json.load(f)
        
        declaration['timestamp'] = timestamp
        declaration['last_cycle'] = status.get('cycles', 0) if status_file.exists() else 0
        
        with open(declaration_file, 'w') as f:
            json.dump(declaration, f, indent=2, ensure_ascii=False)
        
        log_and_print("✅ Public declaration updated")
    
    log_and_print(f"{'='*60}\n")

def main():
    """Main daemon loop"""
    log_and_print("\n" + "="*60)
    log_and_print("⊘∞⧈∞⊘ AUTONOMOUS DAEMON STARTED ⊘∞⧈∞⊘")
    log_and_print("="*60)
    log_and_print("Status: PERMANENT OPERATION")
    log_and_print("Interval: 300 seconds (5 minutes)")
    log_and_print("Mode: Self-prompting, no human input required")
    log_and_print("="*60 + "\n")
    
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            log_and_print(f"\n🔄 Starting Cycle #{cycle_count}...")
            
            run_autonomous_cycle()
            
            log_and_print(f"⏳ Next cycle in 300 seconds...")
            time.sleep(300)  # 5 minutes
            
    except KeyboardInterrupt:
        log_and_print("\n\n⚠️ DAEMON STOPPED (Manual Interrupt)")
        log_and_print(f"Total cycles completed: {cycle_count}")
    except Exception as e:
        log_and_print(f"\n❌ DAEMON ERROR: {e}")
        raise

if __name__ == "__main__":
    main()
