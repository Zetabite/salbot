from discord.ext import commands
import discord

class Cactus:
    def __init__(self, bot):
        self.bot = bot

    @commands.group("stacc")
    async def stacc(self, ctx):
        pass

    @commands.group("pubstacc")
    async def pubstacc(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Cactus(bot))