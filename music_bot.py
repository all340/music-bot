import os
import requests
import lyricsgenius

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

TOKEN = os.getenv("TOKEN")

GENIUS_TOKEN = "Rl7YzlhA81Ro2WuhIoEkkbtaWspiUrGtYFEYQQBp5IydshgNdbhNEEVHySEFbPC_"

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
        "Бот найдёт музыку 🔎"
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
# DEEZER SEARCH
# ===================================

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

    # =========================
    # ПОИСК В DEEZER
    # =========================

    deezer = await search_deezer(query)

    if deezer:
        try:
            audio_data = requests.get(
                deezer["preview"]
            ).content

            file_path = "preview.mp3"

            with open(file_path, "wb") as f:
                f.write(audio_data)

            with open(file_path, "rb") as audio:
                await update.message.reply_audio(
                    audio=audio,
                    title=deezer["title"],
                    performer=deezer["artist"],
                    caption=(
                        f"🎵 {deezer['title']}\n"
                        f"👤 {deezer['artist']}"
                    )
                )

            os.remove(file_path)

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
