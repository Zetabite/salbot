from discord.ext import commands
import discord
from discord.utils import get

class MemberManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_memeber_join(self, member):
        print(f'{member} has joined the server.')

    @commands.Cog.listener()
    async def on_memeber_remove(self, member):
        print(f'{member} has left the server.')
    
    @commands.command()
    @commands.has_any_role("Moderator","Private Chat Access","Administrator")
    async def addmember(self, ctx, member : discord.Member = None):
        #await ctx.message.delete()
        role = get(member.guild.roles, name="Member")
        await member.add_roles(role)
        await ctx.send(f'> Added member role for {member.name}')

    @commands.command()
    @commands.has_any_role("Moderator","Private Chat Access","Administrator")
    async def removemember(self, ctx, member : discord.Member = None):
        #await ctx.message.delete()
        role = get(member.guild.roles, name="Member")
        await member.remove_roles(role)
        await ctx.send(f'> Removed member role for {member.name}')

def setup(bot):
    bot.add_cog(MemberManagement(bot))