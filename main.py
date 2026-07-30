import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL

# Tokeningiz
BOT_TOKEN = os.getenv("BOT_TOKEN", "8889561169:AAEu2ZkdFoGXju86YTRjN_9DVjMGAiCmXKQ")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start buyrug'i uchun
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Menga faqat TikTok video havolasini (link) yuboring, men uni sizga yuklab beraman. 🎵")

# Faqat TikTok linklarini qabul qilish
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok_video(message: types.Message):
    url = message.text.strip()
    status_msg = await message.answer("TikTok videosi yuklanmoqda, kuting... ⏳")

    ydl_opts = {
        'format': 'b[ext=mp4]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'TikTok Video')

        await status_msg.edit_text("Video tayyor, Telegram'ga yuborilmoqda... 🚀")

        video_file = types.FSInputFile(filename)
        # Videoni yuborish
        await message.answer_video(video=video_file, caption=f"🎵 <b>{title}</b>", parse_mode="HTML")

        # Xotirani tozalash
        if os.path.exists(filename):
            os.remove(filename)
            
        await status_msg.delete()

    except Exception as e:
        print(f"Xatolik: {e}")
        await status_msg.edit_text("❌ Videoni yuklab olishda xatolik yuz berdi.\nLink to'g'riligini yoki video yopiq (private) emasligini tekshiring.")

# Agar TikTok bo'lmagan boshqa link yoki oddiy so'z yuborilsa
@dp.message()
async def handle_other_messages(message: types.Message):
    await message.answer("⚠️ Iltimos, menga faqat TikTok videosining havolasini yuboring!\n(Masalan: https://vm.tiktok.com/...)")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
