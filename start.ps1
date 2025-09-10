# PowerShell script for launching Telegram Maintenance Bot
# start.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "Starting Telegram Maintenance Bot..." -ForegroundColor Cyan
Write-Host "Time: $(Get-Date -Format 'dd.MM.yyyy HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

Set-Location $PSScriptRoot\..

# Check .env file
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "Error: .env file not found." -ForegroundColor Red
        Write-Host "Copy .env.example to .env and fill in the settings:" -ForegroundColor Yellow
        Write-Host "Copy-Item .env.example .env" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    } else {
        Write-Host "Error: Configuration files not found!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check Python
try {
    $pythonVersion = python --version 2>$null
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found. Install Python 3.7+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create venv if not exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error creating virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# Create directories
@("logs", "data") | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}

# Check internet connection
Write-Host "Checking connection to Telegram..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "https://api.telegram.org" -TimeoutSec 5 -UseBasicParsing | Out-Null
    Write-Host "Connection works" -ForegroundColor Green
} catch {
    Write-Host "Warning: Could not verify connection" -ForegroundColor Yellow
}

# Load .env
Write-Host "Loading configuration..." -ForegroundColor Yellow
Get-Content ".env" | ForEach-Object {
    if ($_ -match "^([^#].*)=(.*)$") {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
    }
}

# Check required parameters
$requiredVars = @("MAINTENANCE_BOT_TOKEN", "ADMIN_IDS")
$missingVars = @()

foreach ($var in $requiredVars) {
    $value = [Environment]::GetEnvironmentVariable($var, "Process")
    if ([string]::IsNullOrEmpty($value) -or $value -eq "YOUR_BOT_TOKEN_HERE" -or $value -eq "123456789,987654321") {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "Error: Missing parameters in .env file:" -ForegroundColor Red
    foreach ($var in $missingVars) {
        Write-Host "   - $var" -ForegroundColor Red
    }
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "All checks passed!" -ForegroundColor Green
Write-Host "Starting bot..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

# Launch
try {
    python bot.py
} catch {
    Write-Host "Launch error: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
