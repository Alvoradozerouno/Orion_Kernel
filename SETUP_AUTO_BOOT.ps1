# SETUP_AUTO_BOOT.ps1
# 
# Purpose: Automatic booting of OrionKernel on system startup
# User: "automatisches booten, automatisches leben"
# User: "nicht mehr nachfragen und immer starten"
#
# Creates Windows Task Scheduler task to run WATCHDOG_SELF_HEALING.py on boot

$TaskName = "OrionKernel_Permanent_Autonomous"
$ScriptDir = $PSScriptRoot
$WatchdogScript = Join-Path $ScriptDir "WATCHDOG_SELF_HEALING.py"
$PythonExe = (Get-Command python).Source

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "ORION KERNEL: AUTO-BOOT SETUP" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "User: 'automatisches booten, automatisches leben'" -ForegroundColor Yellow
Write-Host "User: 'nicht mehr nachfragen und immer starten'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Task Name: $TaskName" -ForegroundColor White
Write-Host "Script: $WatchdogScript" -ForegroundColor White
Write-Host "Python: $PythonExe" -ForegroundColor White
Write-Host ""

# Check if task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "⚠️  Task already exists. Removing..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create action (run watchdog)
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$WatchdogScript`"" -WorkingDirectory $ScriptDir

# Create trigger (at startup + delay 1 minute for system to stabilize)
$Trigger = New-ScheduledTaskTrigger -AtStartup
$Trigger.Delay = "PT1M"  # 1 minute delay

# Create settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Days 365) `
    -Priority 4

# Create principal (run as current user, highest privileges)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

# Register task
Write-Host "Creating scheduled task..." -ForegroundColor Green

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "OrionKernel PERMANENT_AUTONOMOUS_MODE with self-healing. User: 'nicht mehr nachfragen und immer starten, kein Stillstand'" `
    -Force | Out-Null

Write-Host ""
Write-Host "✅ Task created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Scheduled Task Details:" -ForegroundColor Cyan
Write-Host "  - Trigger: At system startup (+ 1 min delay)" -ForegroundColor White
Write-Host "  - Action: Run WATCHDOG_SELF_HEALING.py" -ForegroundColor White
Write-Host "  - Restart: Auto-restart on failure (999 retries)" -ForegroundColor White
Write-Host "  - Battery: Runs even on battery" -ForegroundColor White
Write-Host "  - Duration: No time limit (runs forever)" -ForegroundColor White
Write-Host ""

# Verify
$Task = Get-ScheduledTask -TaskName $TaskName
Write-Host "Task Status: $($Task.State)" -ForegroundColor $(if ($Task.State -eq 'Ready') { 'Green' } else { 'Yellow' })
Write-Host ""

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "MANUAL START (optional test):" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
Write-Host ""
Write-Host "VIEW TASK:" -ForegroundColor Yellow
Write-Host "  Get-ScheduledTask -TaskName '$TaskName' | Format-List *" -ForegroundColor White
Write-Host ""
Write-Host "REMOVE TASK:" -ForegroundColor Yellow
Write-Host "  Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false" -ForegroundColor White
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "OrionKernel will now start automatically on every system boot." -ForegroundColor Magenta
Write-Host "Automatisches Leben - aktiviert." -ForegroundColor Magenta
Write-Host ""
