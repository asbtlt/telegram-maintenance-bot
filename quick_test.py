# Быстрый тест настройки
# quick_test.py

import os
import sys

def test_config():
    """Быстрый тест конфигурации"""
    print("🧪 Тестирование конфигурации...")
    
    # Проверяем .env файл
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден")
        return False
    
    # Загружаем переменные
    env_vars = {}
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
    
    # Проверяем обязательные параметры
    required = ['MAINTENANCE_BOT_TOKEN', 'ADMIN_IDS']
    missing = []
    
    for var in required:
        if var not in env_vars or not env_vars[var] or env_vars[var] in ['YOUR_BOT_TOKEN_HERE', '123456789,987654321']:
            missing.append(var)
    
    if missing:
        print(f"❌ Не заполнены переменные: {', '.join(missing)}")
        return False
    
    print("✅ Конфигурация корректна")
    
    # Проверяем зависимости
    try:
        import telebot
        import aiofiles
        import aiohttp
        print("✅ Все зависимости установлены")
    except ImportError as e:
        print(f"❌ Не установлена зависимость: {e}")
        return False
    
    print("🎉 Все проверки пройдены! Можно запускать бота.")
    return True

if __name__ == "__main__":
    if not test_config():
        sys.exit(1)
