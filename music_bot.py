import os
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

# ===================================
# GENIUS
# ===================================

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
# ПОИСК ПО ТЕКСТУ
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
# СКАЧИВАНИЕ ПЕСНИ
# ===================================

async def download_song(query):

    try:

        # Удаляем старый файл
        if os.path.exists("song.mp3"):
            os.remove("song.mp3")

        ydl_opts = {

            # Лучшее аудио
            "format": "bestaudio/best",

            # Имя файла
            "outtmpl": "song.%(ext)s",

            # Без лишних логов
            "quiet": True,

            # Только 1 видео
            "noplaylist": True,

            # Конвертация в mp3
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                f"ytsearch1:{query}",
                download=True
            )

            # Первое найденное видео
            entry = info["entries"][0]

            return {
                "file": "song.mp3",
                "title": entry.get("title"),
            }

    except Exception as e:

        print(e)

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
        "⬇️ Скачиваю полный трек..."
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

            # Удаляем файл после отправки
            os.remove(song["file"])

            return

        except Exception as e:

            await update.message.reply_text(
                f"❌ Ошибка отправки:\n{e}"
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
