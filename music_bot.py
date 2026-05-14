import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from yt_dlp import YoutubeDL

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Привет!\n\n"
        "Отправь название песни."
    )


async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("🔍 Ищу песню...")

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "cookiefile": "cookies.txt",
            "extract_flat": False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"ytsearch1:{query}",
                download=False
            )

            if not info.get("entries"):
                await update.message.reply_text(
                    "😢 Ничего не найдено"
                )
                return

            video = info["entries"][0]

            title = video.get("title", "Без названия")
            url = video.get("webpage_url")

            if not url:
                await update.message.reply_text(
                    "❌ Не удалось получить ссылку"
                )
                return

            await update.message.reply_text(
                f"🎵 {title}\n\n{url}"
            )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка:\n{e}"
        )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            search_music
        )
    )

    print("Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()
