import discord
from discord.ext import commands

class Autosponsor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        after_roles = after.roles
        has_yt = False
        has_sponsor = False

        for role in after_roles:
            if role.name == "YouTube Member":
                has_yt = True
            if role.name == "YouTube Sponsor":
                has_sponsor = True

        if has_yt and not has_sponsor:
            item = self.bot.get_guild(436405308458401803).get_role(674163197694967818)
            await after.add_roles(item, reason="Automatic youtube sponsor add")

    #For when it fucks itself because fuck this
    @commands.command(name="rolemod")
    @commands.has_any_role("Moderator", "Administrator")
    async def roletest(self, ctx, typ, member: discord.Member, *rolename):
        if typ == 'add':
            rolename = " ".join(rolename)
            sponsor_role = None
            for item in self.bot.get_guild(436405308458401803).roles:
                if item.name == rolename:
                    sponsor_role = item
                    print("found role")
                    await member.add_roles(sponsor_role, reason="Rolemod")
        elif typ == 'remove':
            rolename = " ".join(rolename)
            sponsor_role = None
            for item in self.bot.get_guild(436405308458401803).roles:
                if item.name == rolename:
                    sponsor_role = item
                    print("found role")
                    await member.remove_roles(sponsor_role, reason="Rolemod")

def setup(bot):
    bot.add_cog(Autosponsor(bot))