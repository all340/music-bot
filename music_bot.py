import os
import yt_dlp

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = os.getenv("TOKEN")


async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    if query.startswith("/"):
        return

    await update.message.reply_text("🔎 Ищу музыку...")

    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'default_search': 'ytsearch1',
        'outtmpl': 'music.%(ext)s',
        'quiet': True,
        'extractaudio': True,
        'audioformat': 'mp3',
        'cookiefile': 'cookies.txt',
        'extractor_args': {
            'youtube': {
                'player_client': ['android']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)

            file_name = None

            for file in os.listdir():
                if file.startswith("music."):
                    file_name = file
                    break

            if not file_name:
                await update.message.reply_text("❌ Музыка не найдена")
                return

            title = info.get("title", "music")

            await update.message.reply_audio(
                audio=open(file_name, 'rb'),
                title=title,
            )

            os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, music)
    )

    print("Bot started")
    app.run_polling()


if __name__ == '__main__':
    main()
