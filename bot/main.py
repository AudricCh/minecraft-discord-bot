import os
import discord
import requests
import asyncio
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands

compteur = 301
nbConnected = 0

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
VOCAL_ID = int(os.getenv('VOCAL_ID'))

bot = commands.Bot(command_prefix="!")

# Background task
async def background_task():
    global compteur
    await bot.wait_until_ready()

    while not bot.is_closed():
        await call_api()
        await asyncio.sleep(30)
        compteur += 30

async def call_api():   
    global nbConnected
    global compteur
    
    for guild in bot.guilds:
        if (guild.id == CHANNEL_ID):
            channel = discord.utils.get(guild.channels, id=VOCAL_ID)
            response = requests.get('https://minecraft-api.com/api/ping/online/' + SERVER_IP + '/' + str(SERVER_PORT))
            nbConnected2 = response.content.decode("utf-8")

            if nbConnected != nbConnected2 and compteur > 300:
                nbConnected = nbConnected2
                message = 'Il y a ' + str(nbConnected) + (' connectés' if int(nbConnected) > 1 else ' connecté')
                compteur = 0
                await channel.edit(name=message)

bot.loop.create_task(background_task())

# Start bot
bot.run(TOKEN)