#WagersBot implementation
import asyncio
import os, time, random, discord
from discord.ext.commands.core import check
from discord.file import File
from UserStats import UserStats
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

#Global variables
member_statistics = []
card_deck = []
values = {
    'A':1,
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
    '7':7,
    '8':8,
    '9':9,
    '1':10,
    'J':11,
    'Q':12,
    'K':13
}

@bot.event
async def on_ready():
    for server in bot.guilds:
        if server == SERVER:
            break 

    #Initialize card deck
    with os.scandir('cards_png') as cards:
        for card in cards:
            card_deck.append(File(card))

    print("Connected to " + server.name)

    print("Members: ")
    for member in server.members:
        user = UserStats(str(member), 100)
        member_statistics.append(user)
        print(member)

@bot.event
async def on_message(message):
    for member in member_statistics:
        if str(message.author) == member.uname:
            break
        
    #Score updates and tracking
    member.add_score(1)
    member_statistics.sort(key=lambda x: x.score)

    await bot.process_commands(message)

@bot.command(name='stats', help = ' -- Get your personal member statistics')
async def stats(ctx):
    for member in member_statistics:
        if str(ctx.message.author) == member.uname:
            break

    await ctx.channel.send(member.output())

@bot.command(name='hilo', help = ' -- Play Hi-Lo and Stake points ( e.g. --> ?hilo 15 )')
async def hilo(ctx, points: int):
    
    rand_val = random.randrange(len(card_deck))
    await ctx.channel.send(file=card_deck[rand_val])

    val_ch = card_deck[rand_val].filename[0]
    value = values[val_ch]
    print(value)
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel 

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send(f'{ctx.author}, you did not make reply in time. You will be refunded')
    else:
        print(msg.content)
        #Here we will handle the cases


bot.run(TOKEN)