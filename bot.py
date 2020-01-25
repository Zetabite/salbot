import os
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

client = discord.Client()
client = commands.Bot(command_prefix = '.')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with myself'))
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_memeber_join(member):
    print(f'{member} has joined the server.')

@client.event
async def on_memeber_remove(member):
    print(f'{member} has left the server.')

# @client.event
# async def on_message(message):
#      # user = message.author
#      # guild = message.guild
#      # channel = message.channel
#      # id = channel.id
#      # channelname = channel.name
#      # print(message.content)

##-------------------------------COMMANDS-----------------------------------------------------

#Ping Command (Ex: Pong! 93ms)
@client.command()
async def ping(ctx):
    await ctx.send(f'> Pong! {round(client.latency * 1000)}ms')

#Clean Chat Command
@client.command()
async def clean(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send('> Chat Cleaned!')

#tells you when someone joiend the discord server
@client.command()
async def joined(ctx, member: discord.Member = None):
    if member:
        await ctx.send('> {0.mention} joined this discord in {0.joined_at}'.format(member))
    else:
        await ctx.send('> Please specify a member')

#Kickes someone from the server
@client.command()
async def kick(ctx, member : discord.Member = None, *, reason=None):
    if member:
        await member.kick(reason=reason)
    else:
        await ctx.send('> Please specify a member')

#Bans someone from the server
@client.command()
async def ban(ctx, member : discord.Member = None, *, reason=None):
    if member:
        await member.ban(reason=reason)
    else:
        await ctx.send('> Please specify a member')

client.run('NDAwMTA1OTA3MjI2MTQ4ODc0.XiuztA.kj5fPVXJiwRoN5T5M9QtjeQb2BI')
