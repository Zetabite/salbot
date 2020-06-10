import discord
from discord.ext import commands
from subprocess import *

class ValidSeed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ValidSeed", aliases=["vs"])
    @commands.has_any_role("Administrator", "Moderator", "Private Chat Access")
    async def cactusheight(self, ctx, seed):
        if 1 == 1:
            await ctx.channel.send("<@459235187469975572> fix me")
            return
        args = ['validseedchecker.jar', str(seed)]
        p = Popen(['java', '-jar']+list(args), stdout=PIPE, stderr=PIPE)
        for line in p.stdout:
            line = str(line)
            noooogal=line.strip("b'")
            rest = noooogal.split("...", 1)[0]
            print(rest)
            await ctx.channel.send(noooogal)

def setup(bot):
    bot.add_cog(ValidSeed(bot))