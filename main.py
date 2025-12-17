import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Настройка логирования (полезно для отладки в Railway)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Текст, который бот отправляет при старте
CLOSED_MESSAGE = (
    "К сожалению, данное исследование уже закрыто.\n\n"
    "Но вы можете написать свои пожелания и предложения по темам для будущих постов! "
    "Я обязательно их рассмотрю ❤️\n\n"
    "Просто напишите ваше сообщение здесь!"
)

# ID админа (вас), куда будут приходить сообщения.
# Будет браться из переменных окружения Railway.
ADMIN_ID = os.getenv('ADMIN_ID')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает команду /start"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CLOSED_MESSAGE
    )

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылает любые текстовые сообщения админу"""
    if update.message and update.message.text:
        # Уведомляем пользователя, что сообщение принято (опционально)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Спасибо! Ваше сообщение отправлено."
        )
        
        # Пересылаем сообщение админу
        # forward_message сохраняет ссылку на оригинального автора
        if ADMIN_ID:
            await context.bot.forward_message(
                chat_id=ADMIN_ID,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )
        else:
            logging.error("ADMIN_ID не найден в переменных окружения!")

if __name__ == '__main__':
    # Получаем токен из переменных окружения
    TOKEN = os.getenv('BOT_TOKEN')
    
    if not TOKEN:
        logging.error("BOT_TOKEN не найден! Проверьте переменные окружения.")
        exit(1)

    application = ApplicationBuilder().token(TOKEN).build()
    
    # Хендлер для команды /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    # Хендлер для всех остальных текстовых сообщений (кроме команд)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), forward_to_admin)
    application.add_handler(echo_handler)
    
    # Запуск бота (polling)
    application.run_polling()
