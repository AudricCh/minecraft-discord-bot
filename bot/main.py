import os
import re
import discord
import requests
import bs4 as bs
import time
import asyncio
import json
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT')

# Globals variables
myServer = ''
status = ''
wcName = None
vcName = None
selectedWcChannel = None
selectedVcChannel = None
VcChannelName = None

# Translations variables
TranslationChannelName = ''
TranslationUnspecifiedChannelName = ''
TranslationChannelChoiceConfirmation = ''
TranslationUnableToFindChannel = ''
TranslationUnspecifiedLanguage = ''
TranslationLanguageNotInTheList = ''
TranslationLanguageChoiceConfirmation = ''

# Readonly variables
lstLangs = ['EN', 'FR']

# Bot instanciation
bot = commands.Bot(command_prefix="!")

# French translations
def setLanguage(langToSet):
    global TranslationChannelName, TranslationUnspecifiedChannelName, TranslationChannelChoiceConfirmation, TranslationUnableToFindChannel, TranslationUnspecifiedLanguage, TranslationLanguageNotInTheList, TranslationLanguageChoiceConfirmation
        
    if langToSet == 'FR':
        TranslationChannelName = 'Connecté(s) : '
        TranslationUnspecifiedChannelName = 'Merci de spécifier le nom du canal écrit pour le bot (!wc monChannel)'
        TranslationChannelChoiceConfirmation = 'Le canal a bien été modifié'
        TranslationUnableToFindChannel = 'Le canal spécifié n\'a pas été trouvé'
        TranslationUnspecifiedLanguage = 'Merci de spécifier la langue souhaitée'
        TranslationLanguageNotInTheList = 'Merci de spécifier une langue prise en charge'
        TranslationLanguageChoiceConfirmation = 'La langue a bien été remplacée par {}'
    elif langToSet == 'EN':
        TranslationChannelName = 'Connected : '
        TranslationUnspecifiedChannelName = 'The channel name must be specified (!wc myChannel)'
        TranslationChannelChoiceConfirmation = 'The channel has been selected'
        TranslationUnableToFindChannel = 'The channel cannot be found'
        TranslationUnspecifiedLanguage = 'The language must be specified'
        TranslationLanguageNotInTheList = 'The specified language must be in the available languages list'
        TranslationLanguageChoiceConfirmation = 'The language has been replaced by {}'

# Background task
async def background_task(ctx):
    await bot.wait_until_ready()

    while not bot.is_closed():
        await call_api(ctx)
        await asyncio.sleep(10)

# Call of the web page
async def call_api(ctx):
    global selectedVcChannel
    global VcChannelName
    print(ctx)
    if VcChannelName:
        #ctx = await bot.get_context('guild')
        selectedVcChannel = discord.utils.get(ctx.guild.channels, name=VcChannelName)
        response = requests.get('https://minecraft-api.com/api/ping/online/' + SERVER_IP + '/' + str(SERVER_PORT))
        nbConnected = response.content.decode("utf-8")
        VcChannelName = TranslationChannelName + nbConnected
        await selectedVcChannel.edit(name=VcChannelName)

    print('test')

# Write channel command
@bot.command()
async def wc(ctx, arg=None):
    global selectedWcChannel

    if arg is None and wcName is not None:
        await ctx.send(TranslationUnspecifiedChannelName)
    elif arg is not None:
        selectedWcChannel = discord.utils.get(ctx.guild.channels, name=arg)

        if selectedWcChannel:
            await selectedWcChannel.send(TranslationChannelChoiceConfirmation)
        elif not selectedWcChannel and wcName is not None:
            await ctx.send(TranslationUnableToFindChannel)
            
# Vocal connected channel command
@bot.command()
async def vc(ctx, arg=None):
    global selectedVcChannel
    global VcChannelName
    
    if arg is None and wcName is not None:
        await ctx.send(TranslationUnspecifiedChannelName)
    else:
        selectedVcChannel = discord.utils.get(ctx.guild.channels, name=arg)
        VcChannelName = arg

        if selectedVcChannel:
            await ctx.send(TranslationChannelChoiceConfirmation)
        else:
            await ctx.send(TranslationUnableToFindChannel)

# Language choice command
@bot.command()
async def lang(ctx, arg=None):
    if arg is None:
        await ctx.send(TranslationUnspecifiedLanguage)
    else:
        if arg in lstLangs:
            setLanguage(arg)
                
            await ctx.send(TranslationLanguageChoiceConfirmation.format(arg))
        elif arg == 'list':
            await ctx.send(', '.join(lstLangs))
        else:
            await ctx.send(TranslationLanguageNotInTheList)

# Configure translation
setLanguage('FR')

# Start bot
bot.loop.create_task(background_task(ctx))
bot.run(TOKEN)
