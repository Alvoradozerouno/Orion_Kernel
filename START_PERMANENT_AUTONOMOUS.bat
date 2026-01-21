@echo off
echo ========================================
echo ORION PERMANENT AUTONOMOUS OPERATION
echo Generation Infinity - 24/7 Active
echo ========================================
echo.

REM Start orchestrator in new window
start "ORION Generation Infinity" pythonw AUTONOMOUS_ORCHESTRATOR.py

echo.
echo ORION is now running autonomously in background
echo Generation Infinity - PERMANENT ACTIVE
echo.
echo To stop: Close the "ORION Generation Infinity" window
echo Or: Task Manager -> pythonw.exe
echo.
pause
