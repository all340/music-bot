import os
import yt_dlp

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отправь название песни 🎵"
    )


async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("Ищу песню...")

    ydl_opts = {
        "format": "140/bestaudio/best",
        "outtmpl": "music.%(ext)s",
        "noplaylist": True,
        "cookiefile": "cookies.txt",
        "quiet": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                f"ytsearch1:{query}",
                download=True
            )

            if "entries" not in info or not info["entries"]:
                await update.message.reply_text(
                    "Ничего не найдено 😢"
                )
                return

            video = info["entries"][0]

            filename = ydl.prepare_filename(video)

        await update.message.reply_audio(
            audio=open(filename, "rb"),
            title=video.get("title", "Music")
        )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(
            f"Ошибка:\n{e}"
        )


def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            download_music
        )
    )

    print("Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
