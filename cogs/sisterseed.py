import discord
from discord.ext import commands
class SisterSeed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sisterseed", aliases=["sis"])
    @commands.has_any_role("Administrator", "Moderator", "Private Chat Access")
    async def sisterseed(self, ctx, theseed):
        seed1 = int(theseed)
        if(seed1 < 0):
            await ctx.channel.send(((-1442695040888963407 * modInverse(6364136223846793005, 64)) - seed1)%-9223372036854775808)
        else:
            await ctx.channel.send(((-1442695040888963407 * modInverse(6364136223846793005, 64)) - seed1)%9223372036854775808)

        def modInverse(a, k):
            x = ((((a << 1) ^ a) & 4) << 1) ^ a
            x += x - a * x * x
            x = x % 9223372036854775808
            x += x - a * x * x
            x = x % -9223372036854775808
            x += x - a * x * x
            x = x % -9223372036854775808
            x += x - a * x * x
            x = x % -9223372036854775808
            return x & -1
