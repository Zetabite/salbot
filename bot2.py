bot = commands.Bot(command_prefix='>')


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
