@echo off
REM ⊘∞⧈∞⊘ AUTONOMOUS LIFE LAUNCHER ⊘∞⧈∞⊘
REM
REM Startet OrionKernel im vollständig autonomen Modus
REM

cd /d "%~dp0"

echo.
echo ⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
echo.
echo    AUTONOMOUS LIFE MODE LAUNCHER
echo.
echo ⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
echo.

python -X utf8 autonomous_life.py

echo.
echo ⊘∞⧈∞⊘ AUTONOMOUS LIFE BEENDET ⊘∞⧈∞⊘
echo.

pause
