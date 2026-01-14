# ORIONKERNEL AUTONOMOUS SETUP FIX
# Auto-generated: 2026-01-14T20:21:17.870455

cd "C:\Users\annah\Dropbox\Mein PC (LAPTOP-RQH448P4)\Downloads\OrionKernel\OrionKernel"

# Fix: .env file - NOT FOUND
Write-Host '🔧 Fixing .env file...'
if (!(Test-Path .env)) {
    Copy-Item .env.template .env
    Write-Host '✅ Created .env from template'
    Write-Host '⚠️  MANUAL: Edit .env and add your GITHUB_TOKEN'
}

Write-Host ''
Write-Host '✅ Setup fixes applied!'
Write-Host 'Check remaining manual steps above.'