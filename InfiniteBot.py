import discord
from discord.ext import commands
import asyncio
from InfiniteApi import *
from classes import *
from InfiniteFile import *

token = 'MTE2NzU3MjExMjA2ODg0OTcwNA.GLX1_x.xk9943FtBLZuQKba7tQyIfo05LOA_ngZ3EIDBs'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".",intents=intents)


users = {}


async def get_dm_channel(message):
    dm =  await message.author.create_dm()
    return dm

async def send_private(message, content:str):    
    async with message.typing():
        await asyncio.sleep(0.01*content.__len__())    
    dm_channel =  await get_dm_channel(message)
    await dm_channel.send(content)


async def clear_private(message):
    dm_channel = await get_dm_channel(message)

    async for message in dm_channel.history(limit=None):
        if message.author == bot.user:
            #print(message.content)
            await message.delete()
            await asyncio.sleep(0.5)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name="start")
async def start_session(message, gamertag:str="IceCurim"):
    print("___ start was called ___")
    global user
    user = gamertag

    await clear_private(message)
    if message.author == bot.user:
        return    
     

@bot.command(name="stop")
async def stop_session(message):
    print("___ stop was called ___")


@bot.command(name="put")
async def register_gamertag(message, gamertag:str=None):
    await clear_private(message)
    if message.author.name not in users.keys() and gamertag == None:
        await send_private(message, "You're not in the database, you must specify a gamertag! (ex: .put gamertag)")
        return    
    elif message.author.name not in users.keys():
        users[message.author.name]["gamertag"] = gamertag        
        save_data(users)
    else:
        users[message.author.name]["gamertag"] = gamertag
        save_data(users)
    print(f'___ {gamertag} has been saved ! ___')
    await send_private(message, f'{gamertag} registered for {message.author.name} !')



@bot.command(name="clear")
async def auto_delete(message):
    print("*** clear was called***")
    await clear_private(message)  


@bot.command(name="global")
async def global_stat(message,gamertag:str=None):
    print("*** global was called***")

    await clear_private(message)

    global user    
    if gamertag != None:
        user = gamertag
    elif user == None:
        await send_private(message, "No gamertag was specified!")
        return

    stat = Global(user)
    await send_private(message, str(stat))


bot.run(token)