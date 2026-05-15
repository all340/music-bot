import os
import yt_dlp

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("TOKEN")

COOKIE_FILE = "cookies.txt"


async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("🔍 Ищу музыку...")

    if "youtube.com" in query or "youtu.be" in query:
        url = query
    else:
        url = f"ytsearch1:{query}"

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
        "cookiefile": COOKIE_FILE,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if "entries" in info:
                info = info["entries"][0]

            filename = ydl.prepare_filename(info)
            filename = os.path.splitext(filename)[0] + ".mp3"

        await update.message.reply_audio(
            audio=open(filename, "rb")
        )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка:\n{e}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            download_music
        )
    )

    print("✅ Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
