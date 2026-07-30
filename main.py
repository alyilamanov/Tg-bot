import os
import asyncio
from threading import Thread
from flask import Flask
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL

# --- 1. UptimeRobot uchun kichik Flask Server ---
app = Flask('')

@app.route('/')
def home():
    return "Bot tirik va ishlamoqda!"

def run_flask():
    # Render avtomatik beradigan PORT ni oladi (bo'lmasa 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()
# ------------------------------------------------

BOT_TOKEN = os.getenv("BOT_TOKEN", "BOTFATHER_TOKENI")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Menga TikTok video havolasini yuboring. 🎵")

@dp.message(F.text)
async def handle_messages(message: types.Message):
    text = message.text.strip().lower()
    
    if "tiktok.com" in text:
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

            await status_msg.edit_text("Video tayyor, yuborilmoqda... 🚀")

            video_file = types.FSInputFile(filename)
            await message.answer_video(video=video_file, caption=f"🎵 <b>{title}</b>", parse_mode="HTML")

            if os.path.exists(filename):
                os.remove(filename)
                
            await status_msg.delete()

        except Exception as e:
            print(f"Xatolik: {e}")
            await status_msg.edit_text("❌ Videoni yuklab olishda xatolik yuz berdi.")
    else:
        await message.answer("⚠️ Iltimos, menga faqat TikTok videosining havolasini yuboring!")

async def main():
    # Flask serverni parallel ravishda ishga tushiramiz
    keep_alive()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
