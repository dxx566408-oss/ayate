import discord
from discord.ext import commands
import requests
import os
from flask import Flask
from threading import Thread

# --- إضافة سيرفر ويب لفتح المنفذ ---
app = Flask('')

@app.route('/')
def home():
    return "البوت مستيقظ ويعمل!"

def run():
    # Render يبحث تلقائياً عن المنفذ 8080 أو 10000
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --------------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ سجل البوت دخوله باسم: {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if ":" in message.content:
        try:
            parts = message.content.split(":")
            surah_name = parts[0].strip()
            ayah_num = parts[1].strip()

            url = f"https://api.alquran.cloud/v1/ayah/{surah_name}:{ayah_num}/ar.alafasy"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()['data']
                await message.channel.send(f"📖 **{data['surah']['name']}** ({data['numberInSurah']}):\n> {data['text']}")
            else:
                await message.channel.send("❌ عذراً، لم أجد هذه الآية. تأكد من كتابة: (اسم السورة : رقم الآية)")
        except:
            pass

    await bot.process_commands(message)

# البدء بتشغيل سيرفر الويب ثم البوت
keep_alive()
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
