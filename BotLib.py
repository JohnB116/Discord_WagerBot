#WagersBot 
import asyncio
from logging import NullHandler
import os, time, random, discord, math
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
    #member.add_score(1)

    await bot.process_commands(message)

@bot.command(name='stats', help = ' -- Get your personal member statistics')
async def stats(ctx):
    for member in member_statistics:
        if str(ctx.message.author) == member.uname:
            break

    await ctx.channel.send(member.output())

@bot.command(name='rankings', help = ' -- Display server seniority/rankings')
async def rankings(ctx):

    member_statistics.sort(key=lambda x: x.score, reverse=True)

    idx = 1
    for m in member_statistics:
        #I know this is a cheap way to check for a bot, I'll try and change this later
        if 'bot' in m.uname.lower():
            continue
        await(ctx.channel.send(f'#{idx}: {m.uname} --> {m.score}'))
        idx += 1

@bot.command(name='gift', help = ' -- Give points to another member ( e.g. --> ?gift username 10 )')
async def gift(ctx, user: str, points: int):
    
    #Member find
    for member in member_statistics:
        if str(ctx.author) == member.uname:
            break
    #Recipient find
    for recipient in member_statistics:
        if user == recipient.uname:
            if recipient.uname == str(ctx.author):
                await ctx.channel.send(f'Nice try {recipient.uname}')
                return
            else:
                found = True
                recipient.score += points
                member.score -= points
                await ctx.channel.send(f'@{member.uname} sent @{recipient.uname} {points} points')
                return
    await ctx.channel.send(f'@{member.uname} , the user you entered is not found')
    return
    

@bot.command(name='hilo', help = ' -- Play Hi-Lo and stake points ( e.g. --> ?hilo 15 )')
async def hilo(ctx, bet: int):
    
    #Member find and preliminary error handling
    for member in member_statistics:
        if str(ctx.author) == member.uname:
            break
    if member.score <= bet:
        await ctx.channel.send('You do not have enough points for this bet')
        return 
    points = 0

    while(1):
        #Send card and value
        rand_val = random.randrange(len(card_deck))
        await ctx.channel.send(file=card_deck[rand_val])
        val_ch = card_deck[rand_val].filename[0]
        value = values[val_ch]
        
        await ctx.channel.send(f'You have {value}, higher/same(h), lower/same(l), or cash out(c)?')
        
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
            if selection.lower() == 'h':
                rand_val = random.randrange(len(card_deck))
                await ctx.channel.send(file=card_deck[rand_val])
                val_ch = card_deck[rand_val].filename[0]
                value_next = values[val_ch]

                if value_next >= value:
                    await ctx.channel.send('Winner!')
                    points += math.ceil(bet/2)
                else:
                    await ctx.channel.send('You lose!')
                    member.score -= bet
                    return
                
            elif selection.lower() == 'l':
                rand_val = random.randrange(len(card_deck))
                await ctx.channel.send(file=card_deck[rand_val])
                val_ch = card_deck[rand_val].filename[0]
                value_next = values[val_ch]

                if value_next <= value:
                    await ctx.channel.send('Winner!')
                    points += math.ceil(bet/2)
                else:
                    await ctx.channel.send('You lose!')
                    member.score -= points
                    return
            elif selection.lower() == 'c':
                member.score += points
                await ctx.channel.send(f'{ctx.author} won {points} points')
                return        
            else:
                await ctx.channel.send("Not a valid selection, refund")

#TODO: Round up multiplier precision to a point
@bot.command(name='limbo', help = ' -- Play Limbo and stake points ( e.g. --> ?limbo 15 )')
async def limbo(ctx, bet: int):
    
    #Member find and preliminary error handling
    for member in member_statistics:
        if str(ctx.author) == member.uname:
            break
    if member.score <= bet:
        await ctx.channel.send('You do not have enough points for this bet')
        return 

    while(1):
        
        await ctx.channel.send(f'@{member.uname}, pick your multiplier(1.01-10)')
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        #Exception handler for no response
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f'{ctx.author}, you did not make reply in time. You will be refunded')
            return 
        else:
            mult = float(msg.content)
            res = 0
            #generate multiplier
            weight = random.randint(0, 2)
            if weight == 0:
                res = 1.00
            elif weight == 1:
                res = random.uniform(1.01, 2.01)
                res = round(res, 2)
            else:
                res = random.uniform(2.02, 10.01)
                res = round(res, 2)

            time.sleep(1)    
            await ctx.channel.send(f'Your mulitpler: {mult}x\nBot multiplier: {res}x')

            if res >= mult:
                points = math.ceil(bet*mult)
                member.score += points
                await ctx.channel.send(f'{member.uname} won {points} points')
            else:
                member.score -= bet
                await ctx.channel.send(f'{member.uname} lost {bet} points')
            
            return 
    

bot.run(TOKEN)