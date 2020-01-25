import os
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from sys import exit as exit_script

bot_secret_file = "bot_secret.txt"

bot = commands.Bot(command_prefix = '.')

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


@bot.command()
async def ping(ctx):
    await ctx.send(f'> Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def ding(ctx):
    await ctx.send('dong ')


@bot.command()
async def pepe(ctx):                                                           #this function
    file_path = 'path to picture folder'
    picture_names = os.listdir(file_path)
    await ctx.send(file=discord.File(file_path + random.choice(picture_names)))


@bot.command()
async def be(ctx):
    await ctx.send(">me")

@bot.event
async def on_ready():
    print('%s %s is online' % (bot.user.name,bot.user.id))  

@bot.command()
async def fuck(ctx):
    fuck = """
 ```
 H
　 O
　　 O
　　　 o
　　 　　o
　　　 　    o
　　　　　o
　　　　 。
　　　 。
　　　.
　　　.
　　　 .
　　　　LY SHIT (╯°□°）╯︵ ┻━┻
```
    """
    await ctx.send(fuck)

@bot.command()
async def say(ctx, *, message: commands.clean_content()):
    '''I say what you want me to say. Oh boi...'''
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass
    finally:
        await ctx.send(message)    

@bot.command()
async def test(ctx):
    """Allow my bot to join the hood. YOUR hood."""
    em = discord.Embed(color=ctx.author.color, title="test")
    em.description = "test message"
    em.set_footer(text=f"Requested by: {str(ctx.author)}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)
    
try: 

    client.run( get_secret() )

except discord.errors.LoginFailure as error:

    print( f"Error logging in! Error: {error}" )
