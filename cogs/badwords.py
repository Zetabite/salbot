from discord.ext import commands
import logging
import discord
import aiosqlite
from pathlib import Path
logger = logging.getLogger('salc1bot')
automation_logger = logging.getLogger('salc1bot.automated')

class Badwords(commands.Cog):
    def __init__(self, bot, badwords):
        self.bot = bot
        self.badwords = badwords
    
    async def deluser(self, id):
        await self.bot.sql_conn.execute(f"DELETE FROM messagecount WHERE user_id = {id};")
        logger.debug(f"Deleted database entry for {id}")
        
    def isExempt(self, author: discord.User):
        for role in ["Administrator", "Moderator"]:
            if role in author.roles:
                return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.author, discord.User) or message.author.bot:
            return

        if not self.isExempt(message.author) and any(word in message.content.lower() for word in self.badwords):
            # Remove the message which triggered the bot
            await message.delete()
            await message.author.send("There are some words discord doesn't like, we have to filter them out.")
            await self.deluser(message.author.id)
            automation_logger.info(f"user {message.author} ({message.author.id}) sent bad word in channel {message.channel.name}, message: \"{message.content[0:1500]}\" ")


def setup(bot):
    with open("data/badwords.txt") as f:
        badwords = [word.strip("\n\t .\"'") for word in f.readlines()]
    print(badwords)
    bw = Badwords(bot, badwords)
    bot.add_cog(bw)
