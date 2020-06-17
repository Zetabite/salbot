import discord
from discord.ext import commands
class ValidSeed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="validate", aliases=["v"])
    @commands.has_any_role("Administrator", "Moderator", "Private Chat Access")
    async def cactusheight(self, ctx, wowthiswasnotfun):
        a = int(wowthiswasnotfun)
        if(a>0):
            inta = a % -2147483648
            b = 18218081
            c = 281474976710656
            d = 7847617
            howtonotmakeanrce = (a >> 32)
            e = ((((d*(((24667315*(howtonotmakeanrce)+b*inta+67552711)>>32))-b*(((-4824621*howtonotmakeanrce+d*inta+d)>>32))-11))*246154705703781 % 9223372036854775808))%281474976710656

            if((((((25214903917*e+11)%9223372036854775808))%281474976710656>>16)<<32)+((((205749139540585*e+277363943098)%-281474976710656)>>16)))==a:
                await ctx.channel.send("Valid Seed")
            else:
                await ctx.channel.send("Invalid Seed")
        else:
            inta = a % -2147483648
            b = 18218081
            c = 281474976710656
            d = 7847617
            howtonotmakeanrce = (a >> 32)+(2 << 31)
            e = ((((d*(((24667315*(howtonotmakeanrce)+b*inta+67552711)>>32))-b*(((-4824621*howtonotmakeanrce+d*inta+d)>>32))-11))*246154705703781 % -9223372036854775808))%-281474976710656

            if(((((((25214903917*e+11) % 9223372036854775808))%-281474976710656)>>16)<<32)+(((205749139540585*e+277363943098)%-281474976710656)>>16))==a:
                await ctx.channel.send("Valid Seed")
            else:
                await ctx.channel.send("Invalid Seed")

def setup(bot):
    bot.add_cog(ValidSeed(bot))