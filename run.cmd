@echo off
:: Запуск PowerShell версии Telegram Maintenance Bot
echo Запуск через PowerShell...
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\start.ps1"
pause
