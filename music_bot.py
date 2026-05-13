import os
import requests

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Музыкальный бот\n\n"
        "Отправь название песни.\n"
        "Бот ищет музыку через Deezer."
    )


# =========================
# DEEZER SEARCH
# =========================

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


# =========================
# MUSIC HANDLER
# =========================

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("🔎 Ищу музыку...")

    deezer = await search_deezer(query)

    if deezer:
        try:
            audio_data = requests.get(
                deezer["preview"]
            ).content

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

        except Exception as e:
            await update.message.reply_text(
                f"❌ Ошибка Deezer:\n{e}"
            )

            return

    await update.message.reply_text(
        "❌ Музыка не найдена"
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
