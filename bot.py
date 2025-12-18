import os
import html
import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(level=logging.INFO)

CLOSED_TEXT = (
    "К сожалению, данное исследование уже закрыто. "
    "Но вы можете написать свои пожелания и предложения по темам для будущих постов прямо здесь! "
    "Я обязательно их рассмотрю!"
)
THANKS_TEXT = "Спасибо за предложение! Ваше сообщение направленно администратору!"

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ADMIN_CHAT_ID = int(os.environ["ADMIN_CHAT_ID"])  # ваш user id (число)


def user_label(update: Update) -> str:
    u = update.effective_user
    if not u:
        return "unknown"
    username = f"@{u.username}" if u.username else "—"
    full_name = " ".join([x for x in [u.first_name, u.last_name] if x]) or "—"
    return f"{html.escape(full_name)} | {html.escape(username)} | id={u.id}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(CLOSED_TEXT)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    text = (msg.text or "").strip()

    # 1) Отправляем вам в личку: кто + что написал
    admin_text = (
        f"<b>Сообщение с предложением</b>\n"
        f"<b>От:</b> {user_label(update)}\n"
        f"<b>Текст:</b> {html.escape(text)}"
    )
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_text,
        parse_mode=ParseMode.HTML,
    )

    # 2) Отвечаем пользователю
    await msg.reply_text(THANKS_TEXT)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()  # типичный способ запуска в PTB [web:32]

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))  # фильтр текста [web:21]

    app.run_polling(allowed_updates=Update.ALL_TYPES)  # polling-режим [web:26]


if __name__ == "__main__":
    main()
