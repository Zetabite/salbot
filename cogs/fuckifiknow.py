from discord.ext import commands
import discord
import logging
import asyncio

class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def lol(self, ctx):
        VoiceChannel1 = bot.get_channel(436405308894478339)
        VoiceChannel2 = bot.get_channel(547915037528948777)
        VoiceChannel3 = bot.get_channel(666695042156462103)
        VoiceChannel4 = bot.get_channel(666695142887129088)
        members1 = VoiceChannel1.members
        members2 = VoiceChannel2.members
        members3 = VoiceChannel3.members
        for member in members1:
            await bot.member.move_to(member, VoiceChannel4)
        for member in members2:
            await bot.member.move_to(member, VoiceChannel4)
        for member in members3:
            await bot.member.move_to(member, VoiceChannel4)

def setup(bot):
    bot.add_cog(Lol(bot))