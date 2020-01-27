import os
import asyncio
import discord
import random
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from bot_secret import get_secret

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    bot.load_extension("cogs.user_info")
    print('%s %s is online' % (bot.user.name,bot.user.id))  


# @bot.event
# async def on_raw_message_delete(raw_message):
#     """Deleted Messages log."""
#     if not raw_message.cached_message:
#         guild = bot.get_guild(raw_message.guild_id)
#         channel = bot.get_channel(raw_message.channel_id)
#         message = await channel.fetch_message(raw_message.message_id)
#     else:
#         message = raw_message.cached_message
#     # if not message.author.bot:  
#         em = discord.Embed(color=message.author.color, title=f":wastebasket: Message Deleted in {channel.id} for {message.author.name} ({message.author.id})")
#         em.description = f"{message.content}"
#         em.set_footer(text=f"Requested by: {str(message.author)}", icon_url=message.author.avatar_url)
#         await bot.get_guild(669119687530905610).get_channel(670895452547317777).send(embed=em)
#     print(f'Message deleted in {raw_message.channel.id}')    


@bot.event
async def on_message_delete(message):
    """Deleted Messages log."""
    # if not message.author.bot:  
    # await bot.get_guild(669119687530905610).get_channel(669372334616084520).send(f""":wastebasket: {message.author.name} ({message.author.id}) message deleted in #{message.channel.name}:```{message.content}```""")
    em = discord.Embed(color=message.author.color, title=f":wastebasket: Message Deleted in {message.channel.name}")
    em.description = f"View: {message.channel.mention}\n```{message.content}```"
    em.set_footer(text=f"Sender: {str(message.author)} ( {message.author.id} )", icon_url=message.author.avatar_url)
    await bot.get_guild(669119687530905610).get_channel(670895452547317777).send(embed=em)
    print(f'Message deleted in {message.channel.name}')   

@bot.event
async def on_message(message):
    guild = message.guild
    if guild:
        path = "chatlogs/{}.txt".format(guild.id)  
        with open(path, 'a+') as f:
            print(f"{message.author.name} : {message.content}".format(message), file=f)
    await bot.process_commands(message)

##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@bot.command()
async def ping(ctx):
    await ctx.send(f'> Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def ding(ctx):
    await ctx.send('dong ')

@bot.command()
async def meme(ctx):                                                           #this function
    file_path = 'memes/'
    picture_names = os.listdir(file_path)
    await ctx.send(file=discord.File(file_path + random.choice(picture_names)))

@bot.command()
async def clean(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send('> Chat Cleaned!')

@bot.command()
async def be(ctx):
    await ctx.send(">me")


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
async def announce(ctx, *, message: commands.clean_content()):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass
    finally:
        em = discord.Embed(color=ctx.author.color)
        em.description = f"{message}"
        em.set_footer(text=f"Requested by: {str(ctx.author)}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)



## ----------------------------------- DONT EDIT PAST THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING! --------------------------------------------
if __name__ == "__main__": # only run bot if this file wasn't imported
    try: 
        bot.run( get_secret() )
    except discord.errors.LoginFailure as error:
        print( f"Error logging in! Error: {error}" )
