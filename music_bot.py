import os
import requests
import lyricsgenius
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
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")

genius = lyricsgenius.Genius(GENIUS_TOKEN)


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Музыкальный бот\n\n"
        "Отправь:\n"
        "- название песни\n"
        "- или строчку из песни"
    )


# =========================
# SEARCH BY LYRICS
# =========================

def find_song(text):
    try:
        song = genius.search_song(text)

        if not song:
            return None

        return f"{song.artist} - {song.title}"

    except:
        return None


# =========================
# DOWNLOAD MUSIC
# =========================

def download_music(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "song.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"ytsearch:{query}",
                download=True
            )

            entry = info["entries"][0]

            filename = ydl.prepare_filename(entry)

            return filename

    except:
        return None


# =========================
# MUSIC HANDLER
# =========================

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await update.message.reply_text(
        "🔎 Ищу песню..."
    )

    query = find_song(text)

    if not query:
        query = text

    await update.message.reply_text(
        f"🎵 Найдено:\n{query}\n\n⬇️ Загружаю..."
    )

    file_path = download_music(query)

    if not file_path:
        await update.message.reply_text(
            "❌ Не удалось скачать песню"
        )
        return

    try:
        with open(file_path, "rb") as audio:
            await update.message.reply_audio(
                audio=audio
            )

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(
            f"Ошибка:\n{e}"
        )


# =========================
# MAIN
# =========================

def main():
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

    app.run_polling()


if __name__ == "__main__":
    main()
