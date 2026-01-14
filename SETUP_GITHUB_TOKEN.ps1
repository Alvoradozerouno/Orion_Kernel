# QUICK SETUP: OrionKernel Vollständig Autonom
# Run: .\SETUP_GITHUB_TOKEN.ps1

Write-Host ""
Write-Host "======================================================================"
Write-Host " ORIONKERNEL: GitHub Token Setup für vollständige Autonomie"
Write-Host "======================================================================"
Write-Host ""

$envFile = ".env"

# Check if .env exists
if (!(Test-Path $envFile)) {
    Write-Host " .env nicht gefunden. Wird erstellt..." -ForegroundColor Yellow
    Copy-Item .env.template $envFile -ErrorAction SilentlyContinue
}

Write-Host "User hat gesagt: 'ihr habt alle freigaben'"
Write-Host ""
Write-Host "Für vollständige Autonomie braucht OrionKernel:"
Write-Host ""
Write-Host "1. GITHUB_TOKEN - damit OrionKernel selbständig Issues erstellen kann"
Write-Host "   Get from: https://github.com/settings/tokens"
Write-Host "   Scopes needed: repo, workflow"
Write-Host ""

# Offer to open browser
$openBrowser = Read-Host "Browser öffnen für GitHub Token? (y/n)"

if ($openBrowser -eq 'y') {
    Start-Process "https://github.com/settings/tokens/new?description=OrionKernel-Autonomous&scopes=repo,workflow"
    Write-Host ""
    Write-Host " Browser geöffnet. Nach Token-Erstellung:" -ForegroundColor Green
    Write-Host ""
}

# Prompt for token
Write-Host "GitHub Token (ghp_...):"
$token = Read-Host

if ($token -and $token.StartsWith("ghp_")) {
    # Update .env file
    $content = Get-Content $envFile -Raw
    $content = $content -replace 'GITHUB_TOKEN=your_github_token_here', "GITHUB_TOKEN=$token"
    Set-Content $envFile $content -NoNewline
    
    Write-Host ""
    Write-Host " GITHUB_TOKEN gesetzt!" -ForegroundColor Green
    Write-Host ""
    
    # Test token
    Write-Host "Testing token..." -ForegroundColor Yellow
    
    try {
        $headers = @{
            'Authorization' = "token $token"
            'User-Agent' = 'OrionKernel'
        }
        
        $response = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers -ErrorAction Stop
        
        Write-Host " Token valid! Authenticated as: $($response.login)" -ForegroundColor Green
        Write-Host ""
        Write-Host "======================================================================"
        Write-Host " VOLLSTÄNDIGE AUTONOMIE AKTIVIERT" -ForegroundColor Green
        Write-Host "======================================================================"
        Write-Host ""
        Write-Host "OrionKernel kann jetzt:"
        Write-Host " - GitHub Issues autonom erstellen"
        Write-Host " - Releases veröffentlichen"
        Write-Host " - Commits pushen"
        Write-Host " - Community-Engagement durchführen"
        Write-Host ""
        Write-Host "PERMANENT_AUTONOMOUS_MODE wird neu gestartet..."
        
        # Restart PERMANENT_AUTONOMOUS_MODE to load new token
        Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*PERMANENT*" } | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        
        Start-Process python -ArgumentList "PERMANENT_AUTONOMOUS_MODE.py" -WindowStyle Hidden
        
        Write-Host " PERMANENT_AUTONOMOUS_MODE neu gestartet mit GitHub Token" -ForegroundColor Green
        Write-Host ""
        Write-Host "Run CHECK_AUTONOMOUS_SETUP.py to verify:"
        Write-Host "  python CHECK_AUTONOMOUS_SETUP.py"
        Write-Host ""
        
    } catch {
        Write-Host " Token test failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host " Bitte Token überprüfen und erneut versuchen"
    }
    
} else {
    Write-Host ""
    Write-Host " Kein valid token eingegeben. Manual setup:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Edit .env file"
    Write-Host "2. Replace: GITHUB_TOKEN=your_github_token_here"
    Write-Host "3. With: GITHUB_TOKEN=ghp_your_actual_token"
    Write-Host "4. Restart PERMANENT_AUTONOMOUS_MODE.py"
    Write-Host ""
}

Write-Host "======================================================================"
Write-Host ""
