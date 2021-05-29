#CrystalPepsi Bot implementation
import os, time, random, discord
from UserStats import UserStats
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

bot = commands.Bot(command_prefix='?', intents=intents)

#Global variables
member_statistics = []

@bot.event
async def on_ready():
    for server in bot.guilds:
        if server == SERVER:
            break 

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
        
    member.add_score(1)
    await bot.process_commands(message)

@bot.command(name='stats', help = ' -- Get your personal member statistics')
async def stats(ctx):
    for member in member_statistics:
        if str(ctx.message.author) == member.uname:
            break

    await ctx.channel.send(member.output())

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