import discord
from discord.ext import commands
import asyncio
from InfiniteApi import *
from classes import *
from InfiniteFile import *
import os

token = os.getenv("INFINITE_BOT_TOKEN")
if token is not None:
    print("Token found !")
else:
    print("Token not found !")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".",intents=intents)

session = {}
users = {}


async def get_dm_channel(message):
    dm =  await message.author.create_dm()
    return dm

async def send_private(message, content:str):    
    async with message.typing():  
        dm_channel =  await get_dm_channel(message)
        await dm_channel.send(content)


async def clear_private(message):
    dm_channel = await get_dm_channel(message)

    async for message in dm_channel.history(limit=None):
        if message.author == bot.user:
            #print(message.content)
            await message.delete()
            #await asyncio.sleep(0.5)


def get_gamertag(message,gamertag:str=None):
    if gamertag != None: return gamertag
    if users != {}:
        if message.author.name in users.keys():
            return users[message.author.name]["gamertag"]
    return message.author.name


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    global users    
    users = load_data()


@bot.command(name="start")
async def start_session(message, gamertag_:str=None):
    print("*** start was called ***")
    await clear_private(message)
    if message.author == bot.user:
        return
    
    gamertag = get_gamertag(message,gamertag_)
    print(users.items()["gamertag"])
    if gamertag not in users.keys():
        await send_private(message, f"{gamertag}s' sessiom started !")
        session[gamertag] = {"lastgame":Game(gamertag)}
        game = session[gamertag]["lastgame"]
        while gamertag in session.keys():
            game.update()
            if game.changed:         
                await send_private(message, str(game))
            print("Sleeps for 30 seconds...")
            await asyncio.sleep(30)
    else: 
        await send_private(message, "You must add your gamertag first! (ex: .put gamertag)")  
    

@bot.command(name="stop")
async def stop_session(message):
    print("*** stop was called ***")
    await clear_private(message)
    pseudo = get_gamertag(message, pseudo)
    if pseudo in session.keys():
        del session[pseudo]
        await send_private(message, f"{pseudo}'s session stopped")
    else:
        await send_private(message, f"{pseudo} has no session")


@bot.command(name="put")
async def register_gamertag(message, gamertag:str=None):
    print("*** put was called ***")

    await clear_private(message)
    if message.author.name not in users.keys() and gamertag == None:
        print("You must at least specify a gamertag!")
        await send_private(message, "You're not in the database, you must specify a gamertag! (ex: .put gamertag)")
        return    
    elif message.author.name in users.keys():
        print("Modifying " + gamertag + " for " + message.author.name + " !")
        users[str(message.author.name)]["gamertag"] = gamertag        
        save_data(users)
    else:
        print("Registering " + gamertag + " for " + message.author.name + " !")
        users[str(message.author.name)]["gamertag"] = gamertag
        save_data(users)
    print(f'{gamertag} has been saved !')
    await send_private(message, f'{gamertag} registered for {message.author.name} !')



@bot.command(name="clear")
async def auto_delete(message):
    print("*** clear was called***")
    await clear_private(message)


@bot.command(name="sayMyName")
async def say_my_name(message):
    print("*** sayMyName was called***")
    gamertag = get_gamertag(message)
    await send_private(message, gamertag)


@bot.command(name="global")
async def global_stat(message,gamertag:str=None):
    print("*** global was called***")
    await clear_private(message)

    user = get_gamertag(message,gamertag)
    print("User: " + user)

    if user not in users.keys() and user == message.author.name:
        await send_private(message, "No gamertag was specified!")
        return
    elif user in users.keys():
        print("User found in database !")
        user = users[user]["gamertag"]
    stat = Global(user)
    await send_private(message, str(stat))


bot.run(token)