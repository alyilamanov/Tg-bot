import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL

# Tokenni Render parametrlaridan oladi
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Menga YouTube videosining havolasini (link) yuboring, men uni sizga yuklab beraman.")

@dp.message(F.text.startswith("http"))
async def download_video(message: types.Message):
    url = message.text.strip()
    status_msg = await message.answer("Video qidirilmoqda va yuklanmoqda, kuting...")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'Video')

        await status_msg.edit_text("Video yuklab olindi, Telegram'ga yuklanmoqda...")

        video_file = types.FSInputFile(filename)
        await message.answer_video(video=video_file, caption=f"🎬 <b>{title}</b>", parse_mode="HTML")

        if os.path.exists(filename):
            os.remove(filename)
            
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text("Videoni yuklab olishda xatolik yuz berdi. Linkni tekshirib qaytadan urinib ko'ring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
