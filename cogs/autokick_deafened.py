from discord.ext import commands
import discord
import logging
automation_logger = logging.getLogger('salc1bot.automated')

class Antideafen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, state_before, state_after):
        if state_after.self_deaf and state_before.channel != None:
            await member.move_to(None, reason="Anti Deafen")
            automation_logger.info(f"Deafen AutoKick triggered by user {member} ({member.id})")

def setup(bot):
    bot.add_cog(Antideafen(bot))