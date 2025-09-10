# Telegram Maintenance Bot

🔧 **Профессиональный бот-заглушка для технических работ Telegram ботов**

## 📖 Описание

Telegram Maintenance Bot - это готовое решение для уведомления пользователей о технических работах вашего основного Telegram бота. Бот автоматически отвечает на все сообщения, собирает статистику обращений и предоставляет удобные инструменты администрирования.

## ✨ Возможности

### 👥 Для пользователей:
- 🔔 Автоматические уведомления о техработах
- ⏰ Информация о времени завершения работ  
- 🔄 Проверка актуального статуса
- 🌐 Поддержка русского и английского языков

### 👨‍💼 Для администраторов:
- 📊 Детальная статистика обращений
- ⏱️ Управление временем завершения работ
- ✏️ Изменение причины техработ
- 📢 Рассылка уведомлений всем пользователям
- 🧹 Управление статистикой

## 🚀 Быстрый старт

### 1. Установка

```bash
git clone https://github.com/asbtlt/telegram-maintenance-bot.git
cd telegram-maintenance-bot
```

### 2. Настройка

```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте конфигурацию
nano .env
```

Заполните обязательные поля:
- `MAINTENANCE_BOT_TOKEN` - токен бота от @BotFather
- `ADMIN_IDS` - ваш Telegram ID через запятую

### 3. Запуск

#### Windows:
```cmd
# PowerShell (рекомендуется)
.\run.cmd

# Или командная строка
.\start.cmd
```

#### Linux/macOS:
```bash
chmod +x start.sh
./start.sh
```

#### Docker:
```bash
docker-compose up -d
```

## 📋 Команды администратора

| Команда | Описание |
|---------|----------|
| `/stats` | Статистика обращений |
| `/set_end_time YYYY-MM-DD HH:MM` | Установить время окончания |
| `/set_reason <текст>` | Изменить причину техработ |
| `/broadcast <сообщение>` | Рассылка всем пользователям |
| `/clear_stats` | Очистить статистику |

### Примеры:
```
/set_end_time 2025-09-10 15:30
/set_reason Обновление серверов и улучшение производительности  
/broadcast 🔧 Работы завершаются досрочно! Бот будет доступен через 15 минут.
```

## 🗂️ Структура проекта

```
telegram-maintenance-bot/
├── 📄 bot.py                 # Основной файл бота
├── 📄 requirements.txt       # Зависимости Python
├── 📄 .env.example          # Пример конфигурации
├── 📄 docker-compose.yml    # Docker Compose конфигурация
├── 📄 Dockerfile           # Docker образ
├── scripts/
│   ├── 🪟 start.cmd         # Запуск на Windows
│   ├── 🪟 run.cmd           # Запуск PowerShell версии
│   ├── 🪟 start.ps1         # PowerShell скрипт
│   └── 🐧 start.sh          # Запуск на Linux/macOS
├── systemd/
│   └── 📄 maintenance-bot.service  # Systemd сервис
└── docs/
    └── 📄 USAGE.md          # Подробная документация
```

## ⚙️ Конфигурация

### Основные переменные (.env):

```env
# Токен бота для техработ
MAINTENANCE_BOT_TOKEN=your_bot_token_here

# ID администраторов через запятую
ADMIN_IDS=123456789,987654321

# Причина техработ по умолчанию
MAINTENANCE_REASON=Проводятся плановые технические работы

# Время окончания (опционально)
MAINTENANCE_END_TIME=2025-09-10 15:00
```

## 📊 Статистика и мониторинг

Бот автоматически собирает и сохраняет:
- 📈 Количество обращений пользователей
- 👥 Уникальных пользователей
- 📅 Статистику по времени
- 💾 Данные в `maintenance_stats.json`

## 🐳 Docker

### Запуск с Docker Compose:
```bash
docker-compose up -d
```

### Ручной запуск:
```bash
docker build -t maintenance-bot .
docker run -d --env-file .env --name maintenance-bot maintenance-bot
```

## 🔄 Сценарии использования

### 1. Подготовка к техработам
```bash
# Настройте время окончания
/set_end_time 2025-09-10 12:00
/set_reason Плановое обновление для улучшения стабильности
```

### 2. Во время техработ
```bash
# Мониторинг обращений
/stats

# Уведомления пользователей
/broadcast 🔧 Работы идут по плану. Ожидаемое время не изменилось.
```

### 3. Завершение техработ
```bash
# Финальное уведомление
/broadcast ✅ Техработы завершены! Основной бот снова работает.
```

## 🔧 Системные требования

- **Python**: 3.7+
- **ОС**: Windows 10+, Ubuntu 18.04+, macOS 10.14+
- **RAM**: 128MB
- **Диск**: 50MB

## 📚 Документация

- [📖 Подробное руководство](docs/USAGE.md)
- [🐳 Развертывание с Docker](docs/DOCKER.md)
- [🔧 Настройка systemd](docs/SYSTEMD.md)

## 🤝 Участие в разработке

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Создайте Pull Request

## 📝 Лицензия

Распространяется под MIT License. См. `LICENSE` для подробностей.

## 💬 Поддержка

- 🐛 **Баги**: [GitHub Issues](https://github.com/asbtlt/telegram-maintenance-bot/issues)
- 💡 **Предложения**: [GitHub Discussions](https://github.com/asbtlt/telegram-maintenance-bot/discussions)
- 📧 **Email**: asbtlt@gmail.com

## ⭐ Благодарности

Если проект помог вам, поставьте ⭐ на GitHub!

---

**Сделано с ❤️ для Telegram сообщества**
