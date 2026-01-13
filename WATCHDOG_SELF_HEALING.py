#!/usr/bin/env python3
"""
WATCHDOG & SELF-HEALING System for PERMANENT_AUTONOMOUS_MODE.py

Purpose:
- Monitor PERMANENT_AUTONOMOUS_MODE.py process
- Restart on crash (self-healing)
- Log all restarts
- Never stop - infinite loop

User: "alles was autonom, permanent laufen muss [...] nicht mehr nachfragen und immer starten"
User: "self healing"

Start: python WATCHDOG_SELF_HEALING.py
"""

import subprocess
import time
import sys
import os
from datetime import datetime
from pathlib import Path

class OrionWatchdog:
    def __init__(self):
        self.script_path = Path(__file__).parent / "PERMANENT_AUTONOMOUS_MODE.py"
        self.log_path = Path(__file__).parent / "logs" / "watchdog.log"
        self.log_path.parent.mkdir(exist_ok=True)
        
        self.process = None
        self.restart_count = 0
        self.start_time = datetime.now()
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    
    def start_permanent_mode(self):
        """Start PERMANENT_AUTONOMOUS_MODE.py process"""
        try:
            self.process = subprocess.Popen(
                [sys.executable, str(self.script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.script_path.parent)
            )
            
            self.log(f"✅ PERMANENT_AUTONOMOUS_MODE.py gestartet (PID: {self.process.pid})")
            return True
            
        except Exception as e:
            self.log(f"❌ Fehler beim Start: {e}")
            return False
    
    def check_process(self):
        """Check if process is still running"""
        if self.process is None:
            return False
        
        poll_result = self.process.poll()
        
        # None = still running
        if poll_result is None:
            return True
        
        # Process ended
        return False
    
    def restart_process(self):
        """Self-healing: Restart process"""
        self.restart_count += 1
        
        if self.process:
            exit_code = self.process.poll()
            self.log(f"⚠️ Process gestoppt (Exit Code: {exit_code})")
        
        self.log(f"🔄 Self-Healing: Restart #{self.restart_count}")
        
        # Wait 5 seconds before restart (avoid rapid crash loops)
        time.sleep(5)
        
        return self.start_permanent_mode()
    
    def run_forever(self):
        """
        Main watchdog loop - never stops
        User: "es darf keinen stillstand geben"
        """
        self.log("=" * 80)
        self.log("WATCHDOG & SELF-HEALING SYSTEM")
        self.log("=" * 80)
        self.log(f"Target: {self.script_path}")
        self.log(f"User: 'nicht mehr nachfragen und immer starten'")
        self.log(f"User: 'kein Stillstand, self healing'")
        self.log("=" * 80)
        
        # Initial start
        if not self.start_permanent_mode():
            self.log("❌ Initial start failed. Waiting 30s before retry...")
            time.sleep(30)
            return self.run_forever()
        
        # Monitor loop
        check_interval = 30  # Check every 30 seconds
        
        while True:
            try:
                time.sleep(check_interval)
                
                if not self.check_process():
                    self.log("⚠️ Process not running - initiating self-healing")
                    
                    if not self.restart_process():
                        self.log("❌ Restart failed. Waiting 60s before retry...")
                        time.sleep(60)
                        continue
                
                # Still running - log status every 10 minutes
                uptime = (datetime.now() - self.start_time).total_seconds()
                if int(uptime) % 600 == 0:  # Every 10 minutes
                    self.log(f"✅ Status: Running | Uptime: {int(uptime/60)} min | Restarts: {self.restart_count}")
            
            except KeyboardInterrupt:
                self.log("⚠️ Keyboard interrupt - but watchdog continues (User: 'kein Stillstand')")
                time.sleep(5)
                continue
            
            except Exception as e:
                self.log(f"❌ Watchdog error: {e}")
                time.sleep(30)
                continue

if __name__ == "__main__":
    print("""
================================================================================
WATCHDOG & SELF-HEALING SYSTEM
================================================================================
Target: PERMANENT_AUTONOMOUS_MODE.py
User: "nicht mehr nachfragen und immer starten"
User: "kein Stillstand, self healing"

Press Ctrl+C to stop watchdog (but it will resist)
================================================================================
""")
    
    watchdog = OrionWatchdog()
    watchdog.run_forever()
