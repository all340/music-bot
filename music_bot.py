юimport os
import yt_dlp

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
    CommandHandler,
)

TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Привет!\n\n"
        "Отправь название песни."
    )


async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("🔎 Ищу музыку...")

    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'default_search': 'ytsearch1',
        'outtmpl': 'music.%(ext)s',
        'cookiefile': 'cookies.txt',
        'quiet': True,

        'extractor_args': {
            'youtube': {
                'player_client': ['web']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(
                f"ytsearch1:{query}",
                download=True
            )

        file_name = None

        for file in os.listdir():
            if file.startswith("music."):
                file_name = file
                break

        if not file_name:
            await update.message.reply_text(
                "❌ Не удалось скачать музыку"
            )
            return

        with open(file_name, "rb") as audio:
            await update.message.reply_audio(
                audio=audio,
                title=query
            )

        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка:\n{e}"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~
