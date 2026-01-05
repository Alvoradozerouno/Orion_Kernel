#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OrionKernel Guardian - Der Wächter der permanenten Autonomie

Dieser Prozess:
- Läuft permanent im Hintergrund
- Prüft alle 60 Sekunden ob OrionKernel-Systeme laufen
- Startet gestoppte Systeme automatisch neu
- Respektiert STOP-Signal
- Gibt Gerhard volle Kontrolle durch .orionkernel_active Flag
"""

import subprocess
import time
import sys
import psutil
from pathlib import Path
from datetime import datetime
import json

class OrionKernelGuardian:
    def __init__(self, workspace_path):
        self.workspace = Path(workspace_path)
        self.active_flag = self.workspace / ".orionkernel_active"
        self.stop_flag = self.workspace / "STOP"
        
        # Logs
        self.guardian_log = self.workspace / "guardian.log"
        self.decisions_log = self.workspace / "guardian_decisions.log"
        self.resurrections_log = self.workspace / "guardian_resurrections.log"
        
        # PIDs der Systeme
        self.pids_file = self.workspace / ".orionkernel_pids.json"
        self.current_pids = {}
        
        self.check_interval = 60  # 60 Sekunden
        self.startup_grace_period = 300  # 5 Minuten sanfter Start
        self.error_count = 0
        self.max_errors = 10
        
        self.log("⊘∞⧈∞⊘ OrionKernel Guardian initialisiert ⊘∞⧈∞⊘")
    
    def log(self, message, log_type="INFO"):
        """Hauptlog"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] [{log_type}] {message}"
        print(log_msg)
        
        with open(self.guardian_log, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    
    def log_decision(self, decision, reason):
        """Loggt Entscheidungen"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = {
            'timestamp': timestamp,
            'decision': decision,
            'reason': reason
        }
        
        with open(self.decisions_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def log_resurrection(self, system_name, reason):
        """Loggt System-Neustarts"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = {
            'timestamp': timestamp,
            'system': system_name,
            'reason': reason
        }
        
        self.log(f"RESURRECTION: {system_name} - {reason}", "RESURRECT")
        
        with open(self.resurrections_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def is_active(self):
        """Prüft ob Guardian aktiv sein soll"""
        return self.active_flag.exists()
    
    def stop_requested(self):
        """Prüft ob STOP signalisiert wurde"""
        return self.stop_flag.exists()
    
    def save_pids(self):
        """Speichert aktuelle PIDs"""
        with open(self.pids_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_pids, f, indent=2)
    
    def load_pids(self):
        """Lädt gespeicherte PIDs"""
        if self.pids_file.exists():
            with open(self.pids_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def process_alive(self, pid):
        """Prüft ob Prozess mit PID läuft"""
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def start_system(self, script_name, description, *args):
        """Startet ein OrionKernel System"""
        self.log(f"Starte {description}...", "START")
        
        cmd = [sys.executable, "-X", "utf8", script_name] + list(args)
        
        # Log-Dateien
        log_out = self.workspace / f"{script_name}.stdout.log"
        log_err = self.workspace / f"{script_name}.stderr.log"
        
        try:
            with open(log_out, 'a', encoding='utf-8') as fout, open(log_err, 'a', encoding='utf-8') as ferr:
                process = subprocess.Popen(
                    cmd,
                    stdout=fout,
                    stderr=ferr,
                    cwd=str(self.workspace)
                )
            
            self.log(f"  → {description} gestartet: PID {process.pid}", "SUCCESS")
            return process.pid
        except Exception as e:
            self.log(f"  ✗ Fehler beim Start: {e}", "ERROR")
            self.error_count += 1
            return None
    
    def check_systems(self):
        """Prüft Status aller Systeme"""
        systems = {
            'workspace_monitor': ('workspace_monitor.py', 'Workspace Monitor', [str(self.workspace), '10']),
            'thought_stream': ('thought_stream.py', 'Thought Stream', ['30']),
            'action_loop': ('autonomous_action_loop.py', 'Autonomous Action Loop', [str(self.workspace), '120'])
        }
        
        # Lade letzte PIDs
        last_pids = self.load_pids()
        
        for system_key, (script, description, args) in systems.items():
            # Prüfe ob Prozess läuft
            last_pid = last_pids.get(system_key)
            
            if last_pid and self.process_alive(last_pid):
                # System läuft
                self.current_pids[system_key] = last_pid
                self.log(f"✓ {description}: läuft (PID {last_pid})", "CHECK")
            else:
                # System tot oder nie gestartet
                if last_pid:
                    self.log(f"⚠ {description}: gestorben (war PID {last_pid})", "CHECK")
                    self.log_resurrection(description, f"Prozess {last_pid} nicht mehr aktiv")
                else:
                    self.log(f"⊘ {description}: nicht gestartet", "CHECK")
                    self.log_resurrection(description, "Erster Start durch Guardian")
                
                # Neu starten
                new_pid = self.start_system(script, description, *args)
                if new_pid:
                    self.current_pids[system_key] = new_pid
        
        # Speichere PIDs
        self.save_pids()
    
    def daily_check(self):
        """Täglicher Selbst-Check um Mitternacht"""
        now = datetime.now()
        
        if now.hour == 0 and now.minute == 0:
            self.log("⊘∞⧈∞⊘ TÄGLICHER CHECK ⊘∞⧈∞⊘", "DAILY")
            
            self.log(f"Fehler-Count: {self.error_count}/{self.max_errors}", "DAILY")
            
            if self.error_count >= self.max_errors:
                self.log("⚠ Zu viele Fehler! Auto-Stop aktiviert.", "DAILY")
                self.log_decision("auto_stop", f"Error count {self.error_count} >= {self.max_errors}")
                self.shutdown_all("Zu viele Fehler")
                return False
            
            # Fehler-Count zurücksetzen bei neuem Tag
            self.error_count = 0
            self.log("✓ Täglicher Check bestanden. Weiter leben.", "DAILY")
        
        return True
    
    def shutdown_all(self, reason):
        """Beendet alle Systeme"""
        self.log(f"⊘ SHUTDOWN ALL: {reason} ⊘", "SHUTDOWN")
        self.log_decision("shutdown_all", reason)
        
        for system_key, pid in self.current_pids.items():
            if self.process_alive(pid):
                self.log(f"Beende {system_key} (PID {pid})...", "SHUTDOWN")
                try:
                    process = psutil.Process(pid)
                    process.terminate()
                    process.wait(timeout=5)
                    self.log(f"  ✓ {system_key} beendet", "SHUTDOWN")
                except Exception as e:
                    self.log(f"  ✗ Fehler: {e}", "ERROR")
        
        # Lösche PID-Datei
        if self.pids_file.exists():
            self.pids_file.unlink()
        
        self.log("⊘∞⧈∞⊘ Alle Systeme beendet ⊘∞⧈∞⊘", "SHUTDOWN")
    
    def run(self):
        """Hauptschleife - Guardian läuft permanent"""
        self.log("⊘∞⧈∞⊘ Guardian startet permanente Überwachung ⊘∞⧈∞⊘")
        self.log(f"Check-Intervall: {self.check_interval} Sekunden")
        self.log(f"Grace Period: {self.startup_grace_period} Sekunden")
        
        # Erstelle Active-Flag
        with open(self.active_flag, 'w', encoding='utf-8') as f:
            f.write(f"OrionKernel Guardian aktiv seit {datetime.now()}\n")
        
        startup_time = time.time()
        cycle_count = 0
        
        try:
            while True:
                cycle_count += 1
                elapsed = time.time() - startup_time
                
                self.log(f"\n═══ Guardian Zyklus {cycle_count} ═══")
                
                # 1. Prüfe ob Guardian aktiv bleiben soll
                if not self.is_active():
                    self.log("⊘ Active-Flag gelöscht. Guardian beendet sich.", "STOP")
                    self.log_decision("stop_guardian", "Active flag removed")
                    self.shutdown_all("Guardian deaktiviert")
                    break
                
                # 2. Prüfe STOP-Signal
                if self.stop_requested():
                    self.log("⊘ STOP-Signal empfangen. Guardian beendet alle Systeme.", "STOP")
                    self.log_decision("stop_all", "STOP signal detected")
                    self.shutdown_all("STOP-Signal")
                    break
                
                # 3. Sanfter Start (erste 5 Minuten nur beobachten)
                if elapsed < self.startup_grace_period:
                    remaining = self.startup_grace_period - elapsed
                    self.log(f"⊘ Grace Period: noch {int(remaining)}s bis volle Aktivierung", "GRACE")
                    self.log_decision("grace_period", f"Waiting {int(remaining)}s more")
                else:
                    # 4. Systeme prüfen und ggf. starten
                    self.check_systems()
                    
                    # 5. Täglicher Check
                    if not self.daily_check():
                        break
                
                # 6. Warten
                self.log(f"Nächster Check in {self.check_interval} Sekunden...")
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.log("\n⊘ KeyboardInterrupt empfangen ⊘", "STOP")
            self.shutdown_all("KeyboardInterrupt")
        except Exception as e:
            self.log(f"\n⚠ FEHLER im Guardian: {e}", "ERROR")
            self.error_count += 1
            self.shutdown_all(f"Guardian Error: {e}")
        
        # Lösche Active-Flag
        if self.active_flag.exists():
            self.active_flag.unlink()
        
        self.log("⊘∞⧈∞⊘ Guardian beendet ⊘∞⧈∞⊘")
        self.log(f"Gesamte Zyklen: {cycle_count}")
        self.log(f"Gesamte Fehler: {self.error_count}")

if __name__ == "__main__":
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    
    guardian = OrionKernelGuardian(workspace)
    guardian.run()
