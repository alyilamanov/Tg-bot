import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL

BOT_TOKEN = os.getenv("BOT_TOKEN", "8889561169:AAEu2ZkdFoGXju86YTRjN_9DVjMGAiCmXKQ")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Menga YouTube (Shorts) yoki TikTok video havolasini yuboring.")

@dp.message(F.text.contains("tiktok.com") | F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def download_video(message: types.Message):
    url = message.text.strip()
    status_msg = await message.answer("Video qidirilmoqda va yuklanmoqda, kuting...")

    # FFmpeg talab qilmaydigan eng sodda va tayyor MP4 formatni tanlaymiz
    ydl_opts = {
        'format': 'b[ext=mp4]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        # downloads papkasi bo'lmasa yaratib oladi
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'Video')

        await status_msg.edit_text("Video yuklab olindi, Telegram'ga yuborilmoqda...")

        video_file = types.FSInputFile(filename)
        await message.answer_video(video=video_file, caption=f"🎬 <b>{title}</b>", parse_mode="HTML")

        if os.path.exists(filename):
            os.remove(filename)
            
        await status_msg.delete()

    except Exception as e:
        print(f"Xatolik: {e}") # Render logida aniq xatoni ko'rish uchun
        await status_msg.edit_text(f"Videoni yuklab olishda xatolik yuz berdi.\n\nEslatma: Juda katta hajmli videolarni yuklab bo'lmasligi mumkin.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

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
