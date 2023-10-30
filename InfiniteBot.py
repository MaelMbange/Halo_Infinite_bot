import discord
from discord.ext import commands
import asyncio
from InfiniteApi import *
from InfiniteClasses import *
from InfiniteFile import *
import os

"""
Résume des commandes:
@start: start the game session
@stop: stop the game session
@global: get global stats
@put: register your gamertag
@clear: clear the bot's messages
"""



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


async def send_image(message, image):
	dm_channel = await message.author.create_dm()
	await dm_channel.send(file=image)


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
    if gamertag not in users.keys():
        await send_private(message, f"{gamertag}'s session started !")
        session[gamertag] = {"lastgame":Game(gamertag,False)}
        last_game = session[gamertag]["lastgame"]
        while gamertag in session.keys():
            last_game.update()
            if last_game.changed:
                print("Game changed !")
                await clear_private(message)
                await send_private(message, str(last_game))
                if last_game.medal_count > 0:
                    print("Medals found !")
                    await send_private(message, "Medals found !")
                    img = Medal(last_game).retrieve_image(last_game.medal_count)
                    async with message.typing(): await send_image(message, discord.File(img, filename=f"{gamertag}_medals.png"))
            print("Sleeps for 30 seconds...")
            await asyncio.sleep(30)
    else: 
        await send_private(message, "You must add your gamertag first! (ex: .put gamertag)")  
    

@bot.command(name="stop")
async def stop_session(message,gamertag_:str=None):
    print("*** stop was called ***")
    await clear_private(message)
    gamertag = get_gamertag(message, gamertag_)
    if gamertag in session.keys():
        del session[gamertag]
        await send_private(message, f"{gamertag}'s session stopped")
    else:
        await send_private(message, f"{gamertag} has no session")


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
async def global_stat(message,gamertag:str=None, clear:bool=True):
    print("*** global was called***")

    if clear:
        await clear_private(message)
        
    user = get_gamertag(message,gamertag)
    print(f"{user}s' global stats informations")

    if user not in users.keys() and user == message.author.name:
        await send_private(message, "No gamertag was specified!")
        return
    elif user in users.keys():
        print("User found in database !")
        user = users[user]["gamertag"]
    stat = Global(user)
    await send_private(message, str(stat))


bot.run(token)