# STARTUP_ORION.bat
# 
# Purpose: Manual startup script (fallback if Task Scheduler needs admin)
# User: "automatisches booten, automatisches leben"
# 
# Place in Windows Startup folder:
# %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
# or
# shell:startup

@echo off
cd /d "%~dp0"
start /B python WATCHDOG_SELF_HEALING.py
exit
