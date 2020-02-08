from discord.ext import commands
import logging
import discord
logger = logging.getLogger('salc1bot')
automation_logger = logging.getLogger('salc1bot.automated')


class Badwords(commands.Cog):
    def __init__(self, bot, badwords):
        self.bot = bot
        self.badwords = badwords

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.author, discord.User) or message.author.bot:
            return

        if len(message.author.roles) <= 2 and any(word in message.content.lower() for word in self.badwords):
            # Remove the message which triggered the bot
            await message.delete()
            # Send reply/notification
            await message.channel.send(f':eyes')
            automation_logger.info(f"user {message.author} ({message.author.id}) sent bad word in channel {message.channel.name}, message: \"{message.content[0:1500]}\" ")


def setup(bot):
    with open("data/badwords.txt") as f:
        badwords = [word.strip("\n\t .\"'") for word in f.readlines()]
    print(badwords)
    bw = Badwords(bot, badwords)
    bot.add_cog(bw)
