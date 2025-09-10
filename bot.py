#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Maintenance Bot
Профессиональный бот-заглушка для уведомления пользователей о технических работах

GitHub: https://github.com/asbtlt/telegram-maintenance-bot
License: MIT
"""

import asyncio
import logging
import os
import sys
from datetime import datetime, timezone, timedelta
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import json
import aiofiles
import html

__version__ = "1.0.0"
__author__ = "Your Name"

# Настройка логирования
def setup_logging():
    """Настраивает систему логирования"""
    # Создаем директорию для логов
    os.makedirs('logs', exist_ok=True)
    
    # Форматтер для логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Обработчик для файла
    file_handler = logging.FileHandler(
        f'logs/maintenance_bot_{datetime.now().strftime("%Y%m%d")}.log', 
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Настройка логгера
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logging.getLogger(__name__)

log = setup_logging()

# Конфигурация из переменных окружения
def load_config():
    """Загружает конфигурацию из переменных окружения"""
    config = {
        'BOT_TOKEN': os.getenv('MAINTENANCE_BOT_TOKEN'),
        'ADMIN_IDS': [],
        'MAINTENANCE_REASON': os.getenv('MAINTENANCE_REASON', 
            "Проводятся плановые технические работы для улучшения качества сервиса."),
        'MAINTENANCE_END_TIME': os.getenv('MAINTENANCE_END_TIME'),
    }
    
    # Парсим ID администраторов
    admin_ids_str = os.getenv('ADMIN_IDS', '')
    if admin_ids_str:
        try:
            config['ADMIN_IDS'] = [int(x.strip()) for x in admin_ids_str.split(',') if x.strip()]
        except ValueError as e:
            log.error(f"Ошибка парсинга ADMIN_IDS: {e}")
            sys.exit(1)
    
    # Проверяем обязательные параметры
    if not config['BOT_TOKEN'] or config['BOT_TOKEN'] == 'YOUR_MAINTENANCE_BOT_TOKEN':
        log.error("MAINTENANCE_BOT_TOKEN не установлен или имеет значение по умолчанию")
        sys.exit(1)
    
    if not config['ADMIN_IDS']:
        log.error("ADMIN_IDS не установлен")
        sys.exit(1)
    
    # Парсим время окончания если указано
    if config['MAINTENANCE_END_TIME']:
        try:
            config['MAINTENANCE_END_TIME'] = datetime.fromisoformat(config['MAINTENANCE_END_TIME'])
        except ValueError:
            log.warning("Неверный формат MAINTENANCE_END_TIME, игнорируется")
            config['MAINTENANCE_END_TIME'] = None
    
    return config

# Загружаем конфигурацию
config = load_config()
BOT_TOKEN = config['BOT_TOKEN']
ADMIN_IDS = config['ADMIN_IDS']
MAINTENANCE_END_TIME = config['MAINTENANCE_END_TIME']
MAINTENANCE_REASON = config['MAINTENANCE_REASON']

# Статистика обращений
stats = {
    'total_users': 0,
    'start_time': datetime.now(timezone.utc),
    'user_requests': {},
    'version': __version__
}

# Инициализация бота
bot = AsyncTeleBot(BOT_TOKEN)

# Сообщения на разных языках
MESSAGES = {
    'ru': {
        'maintenance': """🔧 <b>Технические работы</b>

К сожалению, бот временно недоступен.

<b>Причина:</b> {reason}

<b>Ожидаемое время завершения:</b> {end_time}

Мы работаем над улучшением сервиса. Спасибо за понимание!

<i>Вы получите уведомление, когда бот снова заработает.</i>""",
        
        'no_end_time': """🔧 <b>Технические работы</b>

К сожалению, бот временно недоступен.

<b>Причина:</b> {reason}

Работы ведутся в ускоренном режиме. Ожидаемое время восстановления будет сообщено дополнительно.

<i>Следите за обновлениями в нашем канале или попробуйте позже.</i>""",
        
        'admin_stats': """📊 <b>Статистика техработ</b>

<b>Версия:</b> {version}
<b>Время начала:</b> {start_time}
<b>Обращений всего:</b> {total_requests}
<b>Уникальных пользователей:</b> {unique_users}

<b>Топ пользователей по обращениям:</b>
{top_users}

<b>Активность:</b>
{hourly_stats}""",
        
        'maintenance_updated': "✅ Информация о техработах обновлена",
        'invalid_time_format': "❌ Неверный формат времени. Используйте: YYYY-MM-DD HH:MM",
        'help_admin': """🔧 <b>Команды администратора</b>

/stats - Статистика обращений
/set_end_time YYYY-MM-DD HH:MM - Установить время окончания
/set_reason &lt;текст&gt; - Изменить причину техработ
/broadcast &lt;сообщение&gt; - Отправить сообщение всем обратившимся
/clear_stats - Очистить статистику
/version - Версия бота""",
        
        'broadcast_sent': "📢 Сообщение отправлено {count} пользователям",
        'stats_cleared': "🧹 Статистика очищена",
        'version_info': "🤖 <b>Telegram Maintenance Bot</b>\n\n<b>Версия:</b> {version}\n<b>Автор:</b> {author}"
    },
    
    'en': {
        'maintenance': """🔧 <b>Maintenance Mode</b>

Sorry, the bot is temporarily unavailable.

<b>Reason:</b> {reason}

<b>Expected completion time:</b> {end_time}

We're working on improving the service. Thank you for your understanding!

<i>You will be notified when the bot is back online.</i>""",
        
        'no_end_time': """🔧 <b>Maintenance Mode</b>

Sorry, the bot is temporarily unavailable.

<b>Reason:</b> {reason}

Work is being carried out in accelerated mode. The expected recovery time will be announced separately.

<i>Stay tuned for updates or try again later.</i>""",
        
        'version_info': "🤖 <b>Telegram Maintenance Bot</b>\n\n<b>Version:</b> {version}\n<b>Author:</b> {author}"
    }
}

def get_user_language(user_id: int) -> str:
    """Определяет язык пользователя"""
    # В будущем можно добавить определение языка по locale пользователя
    return 'ru'  # По умолчанию русский

def safe_html_format(text: str, **kwargs) -> str:
    """Безопасно форматирует HTML текст, экранируя переменные"""
    escaped_kwargs = {}
    for key, value in kwargs.items():
        if isinstance(value, str):
            escaped_kwargs[key] = html.escape(value)
        else:
            escaped_kwargs[key] = value
    
    return text.format(**escaped_kwargs)

def format_time_remaining(end_time: datetime) -> str:
    """Форматирует оставшееся время до окончания техработ"""
    if not end_time:
        return "не определено"
    
    now = datetime.now(timezone.utc)
    if end_time <= now:
        return "скоро завершатся"
    
    diff = end_time - now
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    
    if diff.days > 0:
        return f"через {diff.days} дн. {hours} ч."
    elif hours > 0:
        return f"через {hours} ч. {minutes} мин."
    else:
        return f"через {minutes} мин."

def track_user_request(user_id: int):
    """Отслеживает обращения пользователей"""
    stats['total_users'] += 1
    if user_id not in stats['user_requests']:
        stats['user_requests'][user_id] = 0
    stats['user_requests'][user_id] += 1

async def save_stats():
    """Сохраняет статистику в файл"""
    try:
        os.makedirs('data', exist_ok=True)
        stats_data = {
            **stats,
            'start_time': stats['start_time'].isoformat(),
            'maintenance_end_time': MAINTENANCE_END_TIME.isoformat() if MAINTENANCE_END_TIME else None,
            'maintenance_reason': MAINTENANCE_REASON
        }
        
        async with aiofiles.open('data/maintenance_stats.json', 'w', encoding='utf-8') as f:
            await f.write(json.dumps(stats_data, ensure_ascii=False, indent=2))
    except Exception as e:
        log.error(f"Ошибка сохранения статистики: {e}")

async def load_stats():
    """Загружает статистику из файла"""
    global MAINTENANCE_END_TIME, MAINTENANCE_REASON, stats
    
    try:
        if os.path.exists('data/maintenance_stats.json'):
            async with aiofiles.open('data/maintenance_stats.json', 'r', encoding='utf-8') as f:
                content = await f.read()
                data = json.loads(content)
                
                stats.update({
                    'total_users': data.get('total_users', 0),
                    'user_requests': data.get('user_requests', {}),
                    'start_time': datetime.fromisoformat(data.get('start_time', datetime.now(timezone.utc).isoformat())),
                    'version': __version__
                })
                
                if data.get('maintenance_end_time'):
                    MAINTENANCE_END_TIME = datetime.fromisoformat(data['maintenance_end_time'])
                
                MAINTENANCE_REASON = data.get('maintenance_reason', MAINTENANCE_REASON)
                
                log.info("Статистика загружена из файла")
    except Exception as e:
        log.error(f"Ошибка загрузки статистики: {e}")

# Обработчики команд
@bot.message_handler(commands=['start', 'help'])
async def handle_start(message):
    """Обработчик команд start и help"""
    user_id = message.from_user.id
    track_user_request(user_id)
    
    if user_id in ADMIN_IDS:
        await bot.reply_to(message, MESSAGES['ru']['help_admin'], parse_mode='HTML')
        return
    
    lang = get_user_language(user_id)
    
    if MAINTENANCE_END_TIME:
        end_time_str = format_time_remaining(MAINTENANCE_END_TIME)
        text = safe_html_format(MESSAGES[lang]['maintenance'], 
                              reason=MAINTENANCE_REASON,
                              end_time=end_time_str)
    else:
        text = safe_html_format(MESSAGES[lang]['no_end_time'], reason=MAINTENANCE_REASON)
    
    # Добавляем кнопку для получения обновлений
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔄 Проверить статус", callback_data="check_status"))
    
    await bot.reply_to(message, text, parse_mode='HTML', reply_markup=keyboard)
    await save_stats()

@bot.callback_query_handler(func=lambda call: call.data == "check_status")
async def handle_status_check(call):
    """Обработчик проверки статуса"""
    user_id = call.from_user.id
    track_user_request(user_id)
    
    if MAINTENANCE_END_TIME:
        end_time_str = format_time_remaining(MAINTENANCE_END_TIME)
        text = f"🔧 Техработы продолжаются\n\n⏰ Ожидаемое время завершения: {end_time_str}"
    else:
        text = "🔧 Техработы продолжаются\n\n⏰ Время завершения уточняется"
    
    await bot.answer_callback_query(call.id, text, show_alert=True)
    await save_stats()

@bot.message_handler(commands=['stats'])
async def handle_stats(message):
    """Показывает статистику (только для админов)"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    # Топ пользователей по обращениям
    top_users = sorted(stats['user_requests'].items(), key=lambda x: x[1], reverse=True)[:5]
    top_users_text = "\n".join([f"ID {uid}: {count} обр." for uid, count in top_users])
    
    # Статистика по времени
    hours_passed = (datetime.now(timezone.utc) - stats['start_time']).total_seconds() / 3600
    avg_per_hour = stats['total_users'] / max(hours_passed, 1)
    
    text = MESSAGES['ru']['admin_stats'].format(
        version=__version__,
        start_time=stats['start_time'].strftime('%d.%m.%Y %H:%M UTC'),
        total_requests=stats['total_users'],
        unique_users=len(stats['user_requests']),
        top_users=top_users_text or "Нет данных",
        hourly_stats=f"В среднем: {avg_per_hour:.1f} обр/час"
    )
    
    await bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['version'])
async def handle_version(message):
    """Показывает версию бота"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    text = MESSAGES['ru']['version_info'].format(
        version=__version__,
        author=__author__
    )
    await bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['set_end_time'])
async def handle_set_end_time(message):
    """Устанавливает время окончания техработ"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    global MAINTENANCE_END_TIME
    
    try:
        time_str = message.text.split(' ', 1)[1]
        MAINTENANCE_END_TIME = datetime.strptime(time_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
        
        await bot.reply_to(message, MESSAGES['ru']['maintenance_updated'])
        await save_stats()
        
        log.info(f"Время окончания техработ установлено: {MAINTENANCE_END_TIME}")
    except (IndexError, ValueError):
        await bot.reply_to(message, MESSAGES['ru']['invalid_time_format'])

@bot.message_handler(commands=['set_reason'])
async def handle_set_reason(message):
    """Изменяет причину техработ"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    global MAINTENANCE_REASON
    
    try:
        reason = message.text.split(' ', 1)[1]
        MAINTENANCE_REASON = reason
        
        await bot.reply_to(message, MESSAGES['ru']['maintenance_updated'])
        await save_stats()
        
        log.info(f"Причина техработ обновлена: {MAINTENANCE_REASON}")
    except IndexError:
        await bot.reply_to(message, "❌ Укажите причину после команды")

@bot.message_handler(commands=['broadcast'])
async def handle_broadcast(message):
    """Рассылает сообщение всем обратившимся пользователям"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        broadcast_text = message.text.split(' ', 1)[1]
        sent_count = 0
        
        for user_id in stats['user_requests'].keys():
            try:
                # Пытаемся отправить с HTML форматированием
                try:
                    await bot.send_message(user_id, broadcast_text, parse_mode='HTML')
                except Exception:
                    # Если HTML невалидный, отправляем как обычный текст
                    await bot.send_message(user_id, broadcast_text)
                sent_count += 1
            except Exception as e:
                log.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
        
        await bot.reply_to(message, MESSAGES['ru']['broadcast_sent'].format(count=sent_count))
        
    except IndexError:
        await bot.reply_to(message, "❌ Укажите текст сообщения после команды")

@bot.message_handler(commands=['clear_stats'])
async def handle_clear_stats(message):
    """Очищает статистику"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    global stats
    stats = {
        'total_users': 0,
        'start_time': datetime.now(timezone.utc),
        'user_requests': {},
        'version': __version__
    }
    
    await bot.reply_to(message, MESSAGES['ru']['stats_cleared'])
    await save_stats()

@bot.message_handler(func=lambda message: True)
async def handle_any_message(message):
    """Обработчик всех остальных сообщений"""
    user_id = message.from_user.id
    track_user_request(user_id)
    
    if user_id in ADMIN_IDS:
        await bot.reply_to(message, MESSAGES['ru']['help_admin'], parse_mode='HTML')
        return
    
    lang = get_user_language(user_id)
    
    if MAINTENANCE_END_TIME:
        end_time_str = format_time_remaining(MAINTENANCE_END_TIME)
        text = safe_html_format(MESSAGES[lang]['maintenance'], 
                              reason=MAINTENANCE_REASON,
                              end_time=end_time_str)
    else:
        text = safe_html_format(MESSAGES[lang]['no_end_time'], reason=MAINTENANCE_REASON)
    
    # Добавляем кнопку для получения обновлений
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔄 Проверить статус", callback_data="check_status"))
    
    await bot.reply_to(message, text, parse_mode='HTML', reply_markup=keyboard)
    await save_stats()

async def periodic_stats_save():
    """Периодически сохраняет статистику"""
    while True:
        try:
            await asyncio.sleep(300)  # Каждые 5 минут
            await save_stats()
        except Exception as e:
            log.error(f"Ошибка в periodic_stats_save: {e}")

async def main():
    """Основная функция запуска бота"""
    log.info(f"🔧 Запуск Telegram Maintenance Bot v{__version__}...")
    log.info(f"👨‍💼 Администраторы: {ADMIN_IDS}")
    
    # Загружаем статистику
    await load_stats()
    
    # Запускаем периодическое сохранение статистики
    asyncio.create_task(periodic_stats_save())
    
    # Запускаем бота
    try:
        log.info("✅ Бот успешно запущен и готов к работе")
        await bot.polling(non_stop=True, interval=1, timeout=60)
    except Exception as e:
        log.error(f"❌ Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        log.error(f"💥 Критическая ошибка: {e}")
        sys.exit(1)
