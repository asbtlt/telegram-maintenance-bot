# PowerShell скрипт для запуска Telegram Maintenance Bot
# start.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "🔧 Запуск Telegram Maintenance Bot..." -ForegroundColor Cyan
Write-Host "Время: $(Get-Date -Format 'dd.MM.yyyy HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

Set-Location $PSScriptRoot\..

# Проверяем .env файл
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "❌ Файл .env не найден." -ForegroundColor Red
        Write-Host "Скопируйте .env.example в .env и заполните настройки:" -ForegroundColor Yellow
        Write-Host "Copy-Item .env.example .env" -ForegroundColor Yellow
        Read-Host "Нажмите Enter для выхода"
        exit 1
    } else {
        Write-Host "❌ Файлы конфигурации не найдены!" -ForegroundColor Red
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
}

# Проверяем Python
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python найден: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python не найден. Установите Python 3.7+" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

# Создаем venv если нет
if (-not (Test-Path "venv")) {
    Write-Host "📦 Создаем виртуальное окружение..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Ошибка создания виртуального окружения" -ForegroundColor Red
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
}

# Активируем venv
Write-Host "🔄 Активируем виртуальное окружение..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Устанавливаем зависимости
Write-Host "📦 Устанавливаем зависимости..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# Создаем директории
@("logs", "data") | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}

# Проверяем интернет
Write-Host "🌐 Проверяем подключение к Telegram..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "https://api.telegram.org" -TimeoutSec 5 -UseBasicParsing | Out-Null
    Write-Host "✅ Подключение работает" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Предупреждение: Не удалось проверить подключение" -ForegroundColor Yellow
}

# Загружаем .env
Write-Host "⚙️  Загружаем конфигурацию..." -ForegroundColor Yellow
Get-Content ".env" | ForEach-Object {
    if ($_ -match "^([^#].*)=(.*)$") {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
    }
}

# Проверяем обязательные параметры
$requiredVars = @("MAINTENANCE_BOT_TOKEN", "ADMIN_IDS")
$missingVars = @()

foreach ($var in $requiredVars) {
    $value = [Environment]::GetEnvironmentVariable($var, "Process")
    if ([string]::IsNullOrEmpty($value) -or $value -eq "YOUR_BOT_TOKEN_HERE" -or $value -eq "123456789,987654321") {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "❌ Не заполнены параметры в .env файле:" -ForegroundColor Red
    foreach ($var in $missingVars) {
        Write-Host "   - $var" -ForegroundColor Red
    }
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host ""
Write-Host "✅ Все проверки пройдены!" -ForegroundColor Green
Write-Host "🚀 Запускаем бот..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Для остановки нажмите Ctrl+C" -ForegroundColor Gray
Write-Host ""

# Запуск
try {
    python bot.py
} catch {
    Write-Host "❌ Ошибка запуска: $_" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}
