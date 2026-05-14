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

# ===================================
# TOKENS
# ===================================

TOKEN = "ТВОЙ_ТЕЛЕГРАМ_ТОКЕН"

GENIUS_TOKEN = "ТВОЙ_GENIUS_TOKEN"

genius = lyricsgenius.Genius(GENIUS_TOKEN)

# ===================================
# START
# ===================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🎵 Музыкальный бот\n\n"
        "📌 Отправь:\n"
        "- название песни\n"
        "- или строчку из песни\n\n"
        "Бот найдёт и отправит полный трек 🔥"
    )

# ===================================
# ПОИСК ПЕСНИ ПО ТЕКСТУ
# ===================================

async def find_song_by_lyrics(text):

    try:

        song = genius.search_song(text)

        if song:
            return f"{song.artist} {song.title}"

    except:
        return None

    return None

# ===================================
# СКАЧИВАНИЕ МУЗЫКИ
# ===================================

async def download_song(query):

    try:

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "song.%(ext)s",
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                f"ytsearch:{query}",
                download=True
            )

            entry = info["entries"][0]

            filename = ydl.prepare_filename(entry)

            return {
                "file": filename,
                "title": entry.get("title"),
            }

    except:
        return None

# ===================================
# MUSIC HANDLER
# ===================================

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.message.text

    await update.message.reply_text(
        "🔎 Ищу песню..."
    )

    # =========================
    # ПОИСК ПО ТЕКСТУ
    # =========================

    lyrics_result = await find_song_by_lyrics(query)

    if lyrics_result:
        query = lyrics_result

    await update.message.reply_text(
        "⬇️ Скачиваю музыку..."
    )

    # =========================
    # СКАЧИВАНИЕ
    # =========================

    song = await download_song(query)

    if song:

        try:

            with open(song["file"], "rb") as audio:

                await update.message.reply_audio(
                    audio=audio,
                    title=song["title"],
                    caption=f"🎵 {song['title']}"
                )

            os.remove(song["file"])

            return

        except Exception as e:

            await update.message.reply_text(
                f"❌ Ошибка:\n{e}"
            )

            return

    # =========================
    # ЕСЛИ НЕ НАЙДЕНО
    # =========================

    await update.message.reply_text(
        "❌ Песня не найдена"
    )

# ===================================
# MAIN
# ===================================

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

# ===================================
# START BOT
# ===================================

if __name__ == "__main__":
    main()
