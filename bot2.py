import os
import asyncio
import discord
import random
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
    
from bot_secret import get_secret
from discord.utils import get

client_ = discord.Client()
client = commands.Bot(command_prefix = '!')

import sys
try:
    if sys.argv[1] != "sc":
        print("you need to start with the shell of batch script")
        exit(1)
except IndexError:
    print("you need to start with the shell of batch script")
    exit(1)

extensions = [
    "cogs.user_info",
    "cogs.faq",
    "cogs.badwords",
    "cogs.member_management",
    "cogs.general"
]

@client.event
async def on_ready():
    for exten in extensions:
        client.load_extension(exten)
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Leaking salc\'s base in progress'))
    print(f'{client.user} has connected to Discord!')


@client.command()
@commands.has_any_role("Moderator", "Administrator")
async def reload(ctx):
    for exten in extensions:
        client.reload_extension(exten)
    await ctx.send("Reload Succesfull")

## ----------------------------------- DONT EDIT PAST THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING! --------------------------------------------
if __name__ == "__main__": # only run bot if this file wasn't imported
    try: 
        client.run( get_secret() )
    except discord.errors.LoginFailure as error:
        print( f"Error logging in! Error: {error}" )
