import discord
from discord.ext import commands
from subprocess import *
import re

class CactusHeight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cactusheight", aliases=["ch"])
    @commands.has_any_role("Administrator", "Moderator", "Private Chat Access")
    async def cactusheight(self, ctx, stacccyboi):
        args = ['cactusseedjarfile.jar', stacccyboi]
        p = Popen(['java', '-jar']+list(args), stdout=PIPE, stderr=PIPE)
        for line in p.stdout:
            line = str(line)
            kekw=line.strip("b'")
            kekw = re.sub("\D", "", kekw)
            await ctx.channel.send(kekw)

def setup(bot):
    bot.add_cog(CactusHeight(bot))
