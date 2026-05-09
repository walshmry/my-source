from pyrogram import Client, filters
import yt_dlp
from youtube_search import YoutubeSearch
import os, asyncio, time

# --- [ إعدادات الحساب ] ---
# هذه البيانات مستخرجة من جلساتك السابقة لضمان عمل السورس لك حصراً
API_ID = 25683510
API_HASH = "6405172b1e76ad73eb0034a88a5b2357"
BOT_TOKEN = "8787315888:AAFW-4pnLyfbSNTbaSO6vojI9HGvEbO1PWE"
DEV_ID = 8453143670 

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)
bot = Client("helper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ أمر اليوتيوب المطور ] ---
@app.on_message(filters.command("يوتيوب", prefixes=".") & filters.me)
async def yt_download(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ **يرجى كتابة اسم الأغنية!**")
    
    query = message.text.split(None, 1)[1]
    m = await message.edit(f"🔍 **جاري البحث عن:** `{query}`")
    
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]['title']
        
        await m.edit(f"📥 **جاري تحميل:**\n`{title}`")
        
        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'song.mp3'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        await client.send_audio(message.chat.id, "song.mp3", caption=f"🎵 **تم التحميل بواسطة سورس غرامي**\n📌 **{title}**")
        await m.delete()
        os.remove("song.mp3")
    except Exception as e:
        await m.edit(f"❌ **حدث خطأ:** `{e}`")

# --- [ أمر الأيدي المزخرف ] ---
@app.on_message(filters.command("ا", prefixes="") & filters.me)
async def my_id(client, message):
    await message.edit(
        "┏━━━━━━━┓\n"
        "┃ ✨ **مـعلومات الـمطور**\n"
        "┃──━━━━━━━──\n"
        f"┃ 👤 **الاسـم :** غـرآمـي\n"
        f"┃ 🆔 **الايـدي :** `{DEV_ID}`\n"
        "┃ 🛡️ **الرتبة :** مـطور ملكي\n"
        "┃──━━━━━━━──\n"
        "┃ 🇮🇶 **الـبصرة - الـزبير**\n"
        "┗━━━━━━━┛"
    )

# --- [ تشغيل السورس ] ---
async def start_all():
    await app.start()
    await bot.start()
    print("✅ سورس غرامي المطور يعمل الآن!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_all())
