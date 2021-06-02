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
    #Server located in .env
    for server in bot.guilds:
        if server == SERVER:
            break 

    #Initialize card deck
    with os.scandir('cards_png') as cards:
        for card in cards:
            card_deck.append(File(card))

    #Initialize member list
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
    member_statistics.sort(key=lambda x: x.score, reverse=True)

    await bot.process_commands(message)

@bot.command(name='stats', help = ' -- Get your personal member statistics')
async def stats(ctx):
    for member in member_statistics:
        if str(ctx.message.author) == member.uname:
            break

    await ctx.channel.send(member.output())

@bot.command(name='rankings', help = ' -- Display server seniority/rankings')
async def rankings(ctx):
    idx = 1
    for m in member_statistics:
        await(ctx.channel.send(f'#{idx}: {m.uname} --> {m.score}'))
        idx += 1


@bot.command(name='hilo', help = ' -- Play Hi-Lo and Stake points ( e.g. --> ?hilo 15 )')
async def hilo(ctx, points: int):
    
    #Member find and preliminary error handling
    for member in member_statistics:
        if str(ctx.author) == member.uname:
            break
    if member.score <= points:
        await ctx.channel.send('You do not have enough points for this bet')
        return 

    #Send card and value
    rand_val = random.randrange(len(card_deck))
    await ctx.channel.send(file=card_deck[rand_val])
    val_ch = card_deck[rand_val].filename[0]
    value = values[val_ch]
    
    await ctx.channel.send(f'You have {value}, higher/same(h) or lower/same(l)?')
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    #Exception handler for no response
    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send(f'{ctx.author}, you did not make reply in time. You will be refunded')
        return 
    else:
        #Handle replies and check for invalid characters
        selection = str(msg.content).lower()
        if selection == 'h':
            rand_val = random.randrange(len(card_deck))
            await ctx.channel.send(file=card_deck[rand_val])
            val_ch = card_deck[rand_val].filename[0]
            value_next = values[val_ch]

            if value_next >= value:
                await ctx.channel.send('Winner!')
                member.score += points
            else:
                await ctx.channel.send('You lose!')
                member.score -= points
            return 
        elif selection == 'l':
            rand_val = random.randrange(len(card_deck))
            await ctx.channel.send(file=card_deck[rand_val])
            val_ch = card_deck[rand_val].filename[0]
            value_next = values[val_ch]

            if value_next <= value:
                await ctx.channel.send('Winner!')
                member.score += points
            else:
                await ctx.channel.send('You lose!')
                member.score -= points
            return 

        else:
            await ctx.channel.send("Not a valid selection, refund")


bot.run(TOKEN)