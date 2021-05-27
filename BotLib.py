#CrystalPepsi Bot implementation
import os, time, random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

bot = commands.Bot(command_prefix='?')

@bot.command(name='wut', help=' -- Speaks the language of Nick')
async def wut(ctx):
     for i in range(15):
            await ctx.channel.send('wut')
            time.sleep(1)

@bot.command(name='odds', help=' -- Play What are the Odds')
async def the_odds(ctx, odds: int, pick: int):
    rnd = random.randint(0, odds)
    res='Your pick: {} \nBot pick: {} '.format(pick, rnd)
    await ctx.send(res)


bot.run(TOKEN)