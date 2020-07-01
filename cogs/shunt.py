from discord.ext import commands
import discord

class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clownpull")
    @commands.has_any_role("Moderator", "Administrator")
    async def lol(self, ctx, channelto=None, *channelsfrom):
        if channelto:
            if len(channelsfrom) == 0:
                channelsfrom = [436405308894478339, 547915037528948777, 666695042156462103]
            ct = self.bot.get_channel(int(channelto))
            allmembers = []
            for channel in channelsfrom:
                for member in self.bot.get_channel(int(channel)).members:
                    allmembers.append(member)
            for member in allmembers:
                await member.move_to(ct)
        else:
            VoiceChannel1 = self.bot.get_channel(436405308894478339)
            VoiceChannel2 = self.bot.get_channel(547915037528948777)
            VoiceChannel3 = self.bot.get_channel(666695042156462103)
            VoiceChannel4 = self.bot.get_channel(666695142887129088)
            members1 = VoiceChannel1.members
            members2 = VoiceChannel2.members
            members3 = VoiceChannel3.members
            for member in members1:
                await member.move_to(VoiceChannel4)
            for member in members2:
                await member.move_to(VoiceChannel4)
            for member in members3:
                await member.move_to(VoiceChannel4)

def setup(bot):
    bot.add_cog(Lol(bot))