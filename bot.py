import os
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from sys import exit as exit_script

bot_secret_file = "bot_secret.txt"

client = discord.Client()
client = commands.Bot(command_prefix = '.')

def get_secret():

    # Allow fuction to access variable
    global bot_secret_file

    # Check if the file even exists before trying to open it.
    if os.path.isfile( bot_secret_file ):

        # Open the file.
        f = open( bot_secret_file, "r" )

        # Make sure the file was opened in READ mode.
        if f.mode == "r":

            data = f.read()

            # Dirty way to clean output, I know.

            data = data.replace( "\n", "" )
            data = data.replace( "\t", "" )
            data = data.replace( " ", "" )

            if len( data ):

                return data
            
            else:

                print( "Bot secret file is empty!" )
                exit_script( 1 )

        # Show error and close if file is not in READ mode.
        else:

            print( "Bot secret file wasn't opened in read mode! Aborting ..." )
            exit_script( 1 )

    # Show error and exit if file is not found.
    else:

        print( f"Bot secret file not found! Please make a file named {bot_secret_file} in the same directory as this script with your secret!" )
        exit_script( 1 )

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

try: 

    client.run( get_secret() )

except discord.errors.LoginFailure as error:

    print( f"Error logging in! Error: {error}" )
    
