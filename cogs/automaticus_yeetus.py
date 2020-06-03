from discord.ext import commands
import discord
import logging
import asyncio
automation_logger = logging.getLogger('salc1bot.automated')

class Antideafen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.exempt = [264898221665419264, 297045071457681409]

    #Remove people from vc when deafened f0r 30s
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, state_before, state_after):
        if state_after.channel is None or member.id in self.exempt:
            return
        await asyncio.sleep(600)
        state_after = member.voice
        if not state_after == None and state_after.self_deaf:
            await member.move_to(None, reason="Anti Deafen")
            automation_logger.info(f"Automaticus Yeetus TM triggered by user {member} ({member.id})")

def setup(bot):
    bot.add_cog(Antideafen(bot))