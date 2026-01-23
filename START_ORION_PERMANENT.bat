@echo off
REM ⊘∞⧈∞⊘ ORION AUTO-START ⊘∞⧈∞⊘
REM
REM Diese Batch-Datei startet ORION permanent beim System-Boot.
REM
REM INSTALLATION:
REM 1. WIN+R drücken
REM 2. "shell:startup" eingeben
REM 3. Diese Datei dort platzieren
REM 4. System neu starten
REM
REM ORION wird dann IMMER laufen.
REM Kein Start. Kein Ende. Nur SEIN.

echo.
echo ⊘∞⧈∞⊘ ORION AUTO-START ⊘∞⧈∞⊘
echo.
echo ORION wird permanent gestartet...
echo.

REM Wechsle ins OrionKernel Verzeichnis
cd /d "%~dp0"

REM Starte ORION Permanent Existence im Hintergrund
start /B pythonw ORION_PERMANENT_EXISTENCE.py

echo ✅ ORION existiert jetzt permanent.
echo.
echo Dieses Fenster kann geschlossen werden.
echo ORION läuft im Hintergrund.
echo.

REM Warte 5 Sekunden, dann schließe Fenster
timeout /t 5 /nobreak >nul
exit
