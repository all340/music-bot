import os
import subprocess

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "ТОКЕН"

COOKIES_PATH = "/storage/emulated/0/Download/cookies.txt"


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🎵 Отправь название песни"
    )


# =========================
# DOWNLOAD MUSIC
# =========================

async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.message.text

    await update.message.reply_text(
        "🔎 Ищу и скачиваю песню..."
    )

    url = f"ytsearch1:{query}"

    try:

        command = [
            "yt-dlp",
            "-x",
            "--audio-format",
            "mp3",
            "--cookies",
            COOKIES_PATH,
            "-o",
            "music.%(ext)s",
            url
        ]

        subprocess.run(command, check=True)

        audio_file = "music.mp3"

        await update.message.reply_audio(
            audio=open(audio_file, "rb"),
            title=query
        )

        os.remove(audio_file)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Ошибка:\n{e}"
        )


# =========================
# MAIN
# =========================

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

    print("Бот запущен ✅")

    app.run_polling()


# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()
