import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Привет!\n"
        "Напиши название песни.\n\n"
        "Например:\n"
        "Alan Walker Faded"
    )


async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text(
        f"🔎 Ты ищешь: {query}\n\n"
        "❗ Сейчас Railway блокирует YouTube/SoundCloud.\n"
        "Для полноценного музыкального бота нужен VPS или cookies."
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, music)
    )

    print("Bot started")

    app.run_polling()


if __name__ == "__main__":
    main()
