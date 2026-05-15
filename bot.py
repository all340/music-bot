import os
import yt_dlp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode

from aiogram.client.default import DefaultBotProperties

TOKEN = os.getenv("TOKEN")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

COOKIE_FILE = "cookies.txt"


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("🎵 Отправь название песни")


@dp.message()
async def download_music(message: types.Message):

    query = message.text

    await message.answer("🔍 Ищу музыку...")

    url = f"ytsearch1:{query}"

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "music.%(ext)s",
        "noplaylist": True,
        "cookiefile": COOKIE_FILE,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            if "entries" in info:
                info = info["entries"][0]

            filename = ydl.prepare_filename(info)
            filename = os.path.splitext(filename)[0] + ".mp3"

        audio = FSInputFile(filename)

        await message.answer_audio(
            audio=audio,
            title=query
        )

        os.remove(filename)

    except Exception as e:

        await message.answer(
            f"❌ Ошибка:\n{e}"
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
