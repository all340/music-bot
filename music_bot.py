import os
import requests
import yt_dlp

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
        "🎵 Музыкальный бот\n\n"
        "Отправь название песни."
    )


async def search_deezer(query):
    try:
        url = f"https://api.deezer.com/search?q={query}"

        response = requests.get(url).json()

        if response.get("data"):
            track = response["data"][0]

            return {
                "title": track["title"],
                "artist": track["artist"]["name"],
                "preview": track["preview"],
            }

    except:
        return None

    return None


async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("🔎 Ищу музыку...")

    # =========================
    # 1. Deezer Preview
    # =========================

    deezer = await search_deezer(query)

    if deezer:
        try:
            audio_data = requests.get(deezer["preview"]).content

            with open("preview.mp3", "wb") as f:
                f.write(audio_data)

            with open("preview.mp3", "rb") as audio:
                await update.message.reply_audio(
                    audio=audio,
                    title=deezer["title"],
                    performer=deezer["artist"],
                )

            os.remove("preview.mp3")

            return

        except:
            pass

    # =========================
    # 2. YouTube fallback
    # =========================

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

        if file_name:
            with open(file_name, "rb") as audio:
                await update.message.reply_audio(
                    audio=audio,
                    title=query
                )

            os.remove(file_name)

            return

    except:
        pass

    # =========================
    # Nothing found
    # =========================

    await update.message.reply_text(
        "❌ Не удалось найти музыку"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            music
        )
    )

    print("Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()
