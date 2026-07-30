# main.py ichida:

# YouTube, TikTok, Instagram linklarini qabul qilish
@dp.message(F.text.contains("tiktok.com") | F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def download_video(message: types.Message):
    url = message.text.strip()
    status_msg = await message.answer("Video qidirilmoqda va yuklanmoqda, kuting...")

    ydl_opts = {
        # TikTok va YouTube uchun eng yaxshi formatni tanlash
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'TikTok Video')

        await status_msg.edit_text("Video yuklab olindi, Telegram'ga yuborilmoqda...")

        video_file = types.FSInputFile(filename)
        await message.answer_video(video=video_file, caption=f"🎬 <b>{title}</b>", parse_mode="HTML")

        # Xotirani tozalash
        if os.path.exists(filename):
            os.remove(filename)
            
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text("Videoni yuklab olishda xatolik yuz berdi. Linkni tekshirib qaytadan urinib ko'ring.")
