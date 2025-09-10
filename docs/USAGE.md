# Подробное руководство по использованию

## 📚 Содержание

1. [Установка и настройка](#установка-и-настройка)
2. [Конфигурация](#конфигурация)
3. [Запуск](#запуск)
4. [Команды администратора](#команды-администратора)
5. [Сценарии использования](#сценарии-использования)
6. [Docker развертывание](#docker-развертывание)
7. [Systemd сервис](#systemd-сервис)
8. [Мониторинг и логи](#мониторинг-и-логи)
9. [Устранение проблем](#устранение-проблем)

## 🛠 Установка и настройка

### Требования
- Python 3.7+
- Telegram Bot Token (от @BotFather)
- ID администраторов (от @userinfobot)

### Пошаговая установка

1. **Клонирование репозитория**:
   ```bash
   git clone https://github.com/asbtlt/telegram-maintenance-bot.git
   cd telegram-maintenance-bot
   ```

2. **Создание конфигурации**:
   ```bash
   cp .env.example .env
   nano .env  # Заполните обязательные поля
   ```

3. **Установка зависимостей**:
   ```bash
   # Автоматически (рекомендуется)
   ./scripts/start.sh  # Linux/macOS
   .\run.cmd          # Windows
   
   # Или вручную
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

## ⚙️ Конфигурация

### Основные параметры (.env)

| Параметр | Описание | Пример |
|----------|----------|---------|
| `MAINTENANCE_BOT_TOKEN` | Токен бота от @BotFather | `1234567890:ABC...` |
| `ADMIN_IDS` | ID администраторов | `123456789,987654321` |
| `MAINTENANCE_REASON` | Причина техработ | `Плановое обновление` |
| `MAINTENANCE_END_TIME` | Время окончания | `2025-09-10 15:00` |

### Получение токена бота

1. Напишите @BotFather в Telegram
2. Используйте команду `/newbot`
3. Задайте имя и username бота
4. Скопируйте полученный токен

### Получение ID администраторов

1. Напишите @userinfobot в Telegram
2. Скопируйте ваш User ID
3. Добавьте в ADMIN_IDS через запятую

## 🚀 Запуск

### Windows

```cmd
# Простой запуск (PowerShell)
.\run.cmd

# Или командная строка
.\scripts\start.cmd

# Или прямой запуск PowerShell
powershell -ExecutionPolicy Bypass -File .\scripts\start.ps1
```

### Linux/macOS

```bash
# Простой запуск
chmod +x scripts/start.sh
./scripts/start.sh

# Или с активацией venv
source venv/bin/activate
python bot.py
```

### Проверка запуска

После запуска вы должны увидеть:
```
🔧 Запуск Telegram Maintenance Bot v1.0.0...
👨‍💼 Администраторы: [123456789]
✅ Бот успешно запущен и готов к работе
```

## 🎛 Команды администратора

### Базовые команды

- `/start` или `/help` - Справка по командам
- `/stats` - Статистика обращений
- `/version` - Версия бота

### Управление техработами

- `/set_end_time H:MM` - Установить время завершения (относительно текущего времени)
- `/set_reason <текст>` - Изменить причину техработ

**Примеры**:
```
/set_end_time 2:30
/set_reason Обновление серверов и улучшение производительности
```

### Взаимодействие с пользователями

- `/broadcast <сообщение>` - Рассылка всем обратившимся
- `/clear_stats` - Очистить статистику

**Примеры**:
```
/broadcast 🔧 Работы завершаются досрочно! Бот будет доступен через 15 минут.
/broadcast <b>Важно:</b> Время завершения изменено на 16:00
```

## 📋 Сценарии использования

### 1. Плановые техработы

```bash
# 1. Настройка техработ (например, на 4 часа)
/set_end_time 4:00
/set_reason Плановое обновление системы

# 2. Запуск бота-заглушки
./scripts/start.sh

# 3. Переключение webhook основного бота
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://maintenance-server.com/webhook"}'

# 4. Во время работ - мониторинг
/stats

# 5. Уведомления пользователей
/broadcast 🔧 Работы идут по плану. Ожидаемое время не изменилось.

# 6. Завершение
/broadcast ✅ Техработы завершены! Основной бот снова работает.
```

### 2. Экстренные работы

```bash
# 1. Быстрый запуск без времени окончания
MAINTENANCE_REASON="Устранение технических неполадок" ./scripts/start.sh

# 2. Уведомление через команду
/set_reason Устранение критической ошибки. Работы ведутся в ускоренном режиме.

# 3. Обновления для пользователей
/broadcast ⚠️ Обнаружена критическая ошибка. Работаем над устранением.
/broadcast 🔧 50% работ выполнено. Ожидаем завершения в течение часа.
/broadcast ✅ Проблема устранена! Бот возвращается к работе.
```

### 3. Переезд на новый сервер

```bash
# 1. Запуск заглушки на старом сервере (на 6 часов)
/set_reason Переезд на новый сервер для улучшения производительности
/set_end_time 6:00

# 2. Миграция данных на новый сервер
# ... процесс миграции ...

# 3. Обновления пользователей
/broadcast 🚚 Переезд на новый сервер. Данные переносятся...
/broadcast 📦 80% данных перенесено. Завершаем настройку...
/broadcast 🏠 Переезд завершен! Основной бот работает на новом сервере.
```

## 🐳 Docker развертывание

### Простой запуск

```bash
# Подготовка
cp .env.example .env
nano .env  # Заполните конфигурацию

# Запуск
docker-compose up -d

# Проверка логов
docker-compose logs -f

# Остановка
docker-compose down
```

### Ручная сборка

```bash
# Сборка образа
docker build -t maintenance-bot .

# Запуск контейнера
docker run -d \
  --name telegram-maintenance-bot \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  maintenance-bot

# Просмотр логов
docker logs -f telegram-maintenance-bot
```

### Docker в продакшене

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  maintenance-bot:
    image: maintenance-bot:latest
    container_name: maintenance-bot-prod
    restart: always
    env_file: .env.production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - maintenance-network
    deploy:
      resources:
        limits:
          memory: 256M
        reservations:
          memory: 128M

networks:
  maintenance-network:
    driver: bridge
```

# Логи
sudo journalctl -u maintenance-bot -f
sudo journalctl -u maintenance-bot --since today
```

## 📊 Мониторинг и логи

### Структура логов

```
logs/
├── maintenance_bot_20250910.log  # Основные логи
data/
├── maintenance_stats.json        # Статистика
```

### Просмотр логов

```bash
# Все логи в реальном времени
tail -f logs/maintenance_bot_$(date +%Y%m%d).log

# Только ошибки
grep ERROR logs/maintenance_bot_*.log

# Статистика обращений
cat data/maintenance_stats.json | jq '.'
```

### Мониторинг через команды бота

```
/stats  # Полная статистика
```

Пример вывода:
```
📊 Статистика техработ

Версия: 1.0.0
Время начала: 10.09.2025 12:00 UTC
Обращений всего: 150
Уникальных пользователей: 47

Топ пользователей по обращениям:
ID 123456789: 8 обр.
ID 987654321: 5 обр.
ID 555666777: 3 обр.

Активность:
В среднем: 25.3 обр/час
```

## 🔧 Устранение проблем

### Частые проблемы

#### 1. Бот не отвечает

**Симптомы**: Нет ответа на команды

**Решение**:
```bash
# Проверьте токен
grep MAINTENANCE_BOT_TOKEN .env

# Проверьте интернет
curl -s https://api.telegram.org/bot<TOKEN>/getMe

# Проверьте логи
tail -n 50 logs/maintenance_bot_$(date +%Y%m%d).log
```

#### 2. Команды админа не работают

**Симптомы**: Обычные сообщения вместо команд админа

**Решение**:
```bash
# Проверьте свой ID
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates" | grep '"id"'

# Проверьте ADMIN_IDS в .env
grep ADMIN_IDS .env
```

#### 3. Ошибки HTML разметки

**Симптомы**: `Bad Request: can't parse entities`

**Решение**:
- Проверьте HTML теги в сообщениях
- Используйте `&lt;` вместо `<` для текста
- Или отправляйте без `parse_mode='HTML'`

#### 4. Проблемы с кодировкой

**Симптомы**: Иероглифы вместо русского текста

**Решение**:
```bash
# Windows CMD
chcp 65001

# Или используйте PowerShell версию
.\run.cmd
```

### Отладочный режим

```python
# В bot.py измените уровень логирования
logging.basicConfig(level=logging.DEBUG)

# Запустите и проверьте детальные логи
python bot.py
```

### Тестирование

```bash
# Создайте тестовый .env
cp .env .env.test
sed -i 's/MAINTENANCE_BOT_TOKEN=.*/MAINTENANCE_BOT_TOKEN=test_token/' .env.test

# Проверьте конфигурацию
python -c "
from bot import load_config
print(load_config())
"
```

### Резервное копирование

```bash
# Создайте backup скрипт
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p backups
tar -czf "backups/maintenance_bot_backup_$DATE.tar.gz" \
  .env data/ logs/ --exclude="logs/*.log"
echo "Backup created: backups/maintenance_bot_backup_$DATE.tar.gz"
EOF

chmod +x backup.sh
./backup.sh
```

---

💡 **Совет**: Ведите журнал всех техработ с указанием времени, причин и действий для улучшения процессов в будущем.
