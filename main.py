import discord
from discord.ext import commands
import requests
import os

# إعداد الصلاحيات (Intents)
# ضرورية لكي يتمكن البوت من قراءة الرسائل
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ تم تشغيل البوت بنجاح باسم: {bot.user}')

@bot.event
async def on_message(message):
    # تجاهل رسائل البوت نفسه لكي لا يدخل في حلقة تكرار
    if message.author == bot.user:
        return

    # التحقق من وجود النقطتين ":" في الرسالة
    if ":" in message.content:
        try:
            # تقسيم الرسالة (مثال: الفاتحة : 5)
            parts = message.content.split(":")
            surah_name = parts[0].strip()
            ayah_number = parts[1].strip()

            # طلب الآية من API القرآن الكريم (نسخة إملائية بسيطة)
            url = f"https://api.alquran.cloud/v1/ayah/{surah_name}:{ayah_number}/ar.alafasy"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()['data']
                text = data['text']
                surah_official_name = data['surah']['name']
                num_in_surah = data['numberInSurah']
                
                # تنسيق الرد بشكل جميل
                reply = f"📖 **{surah_official_name}**\n"
                reply += f"الآية رقم ({num_in_surah}):\n"
                reply += f"**{text}**"
                
                await message.channel.send(reply)
            else:
                # في حال لم يجد السورة أو الآية
                await message.channel.send("⚠️ تأكد من كتابة اسم السورة ورقم الآية بشكل صحيح (مثال: الفاتحة : 5)")
        
        except Exception as e:
            print(f"Error: {e}")

    await bot.process_commands(message)

# جلب التوكن من إعدادات ريندر (Environment Variables)
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
