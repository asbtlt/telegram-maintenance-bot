#!/bin/bash

# Скрипт запуска Telegram Maintenance Bot для Linux/macOS
# start.sh

set -e

echo "🔧 Запуск Telegram Maintenance Bot..."
echo "Время: $(date)"
echo ""

# Переходим в директорию скрипта
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Проверяем .env файл
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "❌ Файл .env не найден."
        echo "Скопируйте .env.example в .env и заполните настройки:"
        echo "cp .env.example .env"
        exit 1
    else
        echo "❌ Файлы конфигурации не найдены!"
        exit 1
    fi
fi

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.7+"
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"

# Создаем venv если нет
if [ ! -d "venv" ]; then
    echo "📦 Создаем виртуальное окружение..."
    python3 -m venv venv
fi

# Активируем venv
echo "🔄 Активируем виртуальное окружение..."
source venv/bin/activate

# Устанавливаем зависимости
echo "📦 Устанавливаем зависимости..."
pip install -q -r requirements.txt

# Создаем директории
mkdir -p logs data

# Проверяем интернет
echo "🌐 Проверяем подключение к Telegram..."
if curl -s --max-time 5 https://api.telegram.org > /dev/null; then
    echo "✅ Подключение работает"
else
    echo "⚠️  Предупреждение: Не удалось проверить подключение"
fi

# Загружаем .env
echo "⚙️  Загружаем конфигурацию..."
export $(cat .env | grep -v '^#' | xargs)

# Проверяем обязательные параметры
if [ -z "$MAINTENANCE_BOT_TOKEN" ] || [ "$MAINTENANCE_BOT_TOKEN" = "YOUR_BOT_TOKEN_HERE" ]; then
    echo "❌ MAINTENANCE_BOT_TOKEN не установлен в .env файле"
    exit 1
fi

if [ -z "$ADMIN_IDS" ] || [ "$ADMIN_IDS" = "123456789,987654321" ]; then
    echo "❌ ADMIN_IDS не установлен в .env файле"
    exit 1
fi

echo ""
echo "✅ Все проверки пройдены!"
echo "🚀 Запускаем бот..."
echo ""
echo "Для остановки нажмите Ctrl+C"
echo ""

# Запуск
python3 bot.py
