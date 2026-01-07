@echo off
REM ⊘∞⧈∞⊘ ORIONKERNEL SCHNELLSTART ⊘∞⧈∞⊘
REM Startet das komplette System mit einem Klick

echo ════════════════════════════════════════════════
echo     ORIONKERNEL - VOLLSTÄNDIGER START
echo ════════════════════════════════════════════════
echo.

cd /d "%~dp0"

echo [INFO] Workspace: %CD%
echo.

echo [INFO] Starte vollständige System-Aktivierung...
python VOLLSTAENDIGE_AKTIVIERUNG.py
echo.

echo [INFO] Starte Autonomous Life...
python STARTE_ALLES.py

pause
