#CrystalPepsi Bot implementation
import os
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    for server in client.guilds:
        if server == SERVER:
            break
    #channel = discord.utils.get(server.text_channels, name="general")
    #await channel.send('Crystal Pepsi Bot has arrived, beep boop or whatever')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    res = ["It tastes like no other!", "wut", 
    "This is your reminder to drink about 8oz of Crystal Pepsi to maintain optimal hydration."]
    if message.content == '!crystalpepsi':
        await message.channel.send(res[0])
    elif message.content == '!wut':
        for i in range(15):
            await message.channel.send(res[1])
            time.sleep(1)
    elif message.content == '!hydrate':
        await message.channel.send(res[2])




client.run(TOKEN)