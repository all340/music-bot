import os
import yt_dlp
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🎵 Отправь название песни"
    )


# =========================
# SEARCH YOUTUBE
# =========================

def search_song(query):

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "default_search": "ytsearch",
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                query,
                download=False
            )

            if "entries" not in info:
                return None

            video = info["entries"][0]

            return {
                "title": video.get("title"),
                "url": f"https://youtube.com/watch?v={video.get('id')}"
            }

    except Exception as e:

        print("ERROR:", e)

        return None


# =========================
# MUSIC
# =========================

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.message.text

    await update.message.reply_text(
        "🔎 Ищу песню..."
    )

    result = search_song(query)

    if not result:

        await update.message.reply_text(
            "❌ Ничего не найдено"
        )

        return

    await update.message.reply_text(
        f"🎵 {result['title']}\n\n{result['url']}"
    )


# =========================
# MAIN
# =========================

async def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            music
        )
    )

    print("Бот запущен!")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()
