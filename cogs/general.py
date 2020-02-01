from discord.ext import commands
import discord
from discord.utils import get
import logging
logger = logging.getLogger('salc1bot')

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #Ping Command (Ex: Pong! 93ms)
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'> Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    @commands.has_any_role("Moderator", "Administrator")
    async def restart(self, ctx):
        exit(69) # this should restart the bot if its started with start.sh


def setup(bot):
    bot.add_cog(General(bot))