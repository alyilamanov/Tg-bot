import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL

# 1. TOKEN SHU YERGA YOZILADI:
# Agar mahalliy kompyuter/telefonda runsangiz: BOT_TOKEN = "123456:ABC..."
# Agar Render.com ga joylasangiz: os.getenv("BOT_TOKEN") qolgani ma'qul.
BOT_TOKEN = os.getenv("BOT_TOKEN", "8889561169:AAEu2ZkdFoGXju86YTRjN_9DVjMGAiCmXKQ")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start buyrug'i uchun
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Menga YouTube yoki TikTok video havolasini yuboring.")

# YouTube, TikTok, Instagram linklarini qabul qilish
@dp.message(F.text.contains("tiktok.com") | F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def download_video(message: types.Message):
    url = message.text.strip()
    status_msg = await message.answer("Video qidirilmoqda va yuklanmoqda, kuting...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'Video')

        await status_msg.edit_text("Video yuklab olindi, Telegram'ga yuborilmoqda...")

        video_file = types.FSInputFile(filename)
        await message.answer_video(video=video_file, caption=f"🎬 <b>{title}</b>", parse_mode="HTML")

        # Xotirani tozalash
        if os.path.exists(filename):
            os.remove(filename)
            
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text("Videoni yuklab olishda xatolik yuz berdi. Linkni tekshirib qaytadan urinib ko'ring.")

# Botni ishga tushirish qismi
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
