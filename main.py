import discord
from discord.ext import commands
import requests
import os
from flask import Flask
from threading import Thread

# --- جزء الويب لخدعة ريندر ---
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل الآن!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# -------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} متصل الآن')

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
                await message.channel.send("❌ تأكد من اسم السورة ورقم الآية.")
        except:
            pass

    await bot.process_commands(message)

# تشغيل سيرفر الويب ثم البوت
keep_alive()
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
