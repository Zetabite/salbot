from discord.ext import commands
import discord
from discord.utils import get
import logging
logger = logging.getLogger('salc1bot')
import os

class Antideafen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, state_before, state_after):
        if state_after.self_deaf:
            await member.move_to(None, reason="Anti Deafen")

def setup(bot):
    bot.add_cog(Antideafen(bot))
