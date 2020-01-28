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


@client.event
async def on_ready():
    client.load_extension("cogs.user_info")
    client.load_extension("cogs.faq")
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity('Leaking salc\'s base in progress'))
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_memeber_join(member):
    print(f'{member} has joined the server.')

@client.event
async def on_memeber_remove(member):
    print(f'{member} has left the server.')

#Ping Command (Ex: Pong! 93ms)
@client.command()
async def ping(ctx):
    await ctx.send(f'> Pong! {round(client.latency * 1000)}ms')

@client.command()
@commands.has_any_role("Moderator","Private Chat Access","Administrator")
async def addmember(ctx, member : discord.Member = None, *,reason=None):
    #await ctx.message.delete()
    role = get(member.guild.roles, name="Member")
    await member.add_roles(role)
    await ctx.send(f'> Added member role for {member.name}')


@client.command()
@commands.has_any_role("Moderator","Private Chat Access","Administrator")
async def removemember(ctx, member : discord.Member = None, *, reason=None):
    #await ctx.message.delete()
    role = get(member.guild.roles, name="Member")
    await member.remove_roles(role)
    await ctx.send(f'> Removed member role for {member.name}')



## ----------------------------------- DONT EDIT PAST THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING! --------------------------------------------
if __name__ == "__main__": # only run bot if this file wasn't imported
    try: 
        client.run( get_secret() )
    except discord.errors.LoginFailure as error:
        print( f"Error logging in! Error: {error}" )
