@echo off
chcp 65001 >nul
:: Простой скрипт запуска Telegram Maintenance Bot для Windows
:: start.cmd

echo.
echo Запуск Telegram Maintenance Bot...
echo Время: %date% %time%
echo.

cd /d "%~dp0\.."

:: Проверяем .env файл
if not exist ".env" (
    if exist ".env.example" (
        echo Файл .env не найден. Скопируйте .env.example в .env и заполните настройки.
        echo copy .env.example .env
        pause
        exit /b 1
    ) else (
        echo Файлы конфигурации не найдены!
        pause
        exit /b 1
    )
)

:: Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python не найден. Установите Python 3.7+
    pause
    exit /b 1
)

:: Создаем venv если нет
if not exist "venv" (
    echo Создаем виртуальное окружение...
    python -m venv venv
)

:: Активируем venv
call venv\Scripts\activate.bat

:: Устанавливаем зависимости
echo Проверяем зависимости...
pip install -q -r requirements.txt

:: Создаем директории
if not exist "logs" mkdir logs
if not exist "data" mkdir data

echo.
echo Все проверки пройдены
echo Запускаем бот...
echo.
echo Для остановки нажмите Ctrl+C
echo.

:: Загружаем .env и запускаем
for /f "usebackq delims=" %%a in (".env") do set "%%a"
python bot.py

pause
