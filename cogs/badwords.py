from discord.ext import commands
import logging
import discord
import aiosqlite
import re
import json
import io
import aiohttp

logger = logging.getLogger('salc1bot')
automation_logger = logging.getLogger('salc1bot.automated')

def is_apng(a: bytes):
    acTL = a.find(b"\x61\x63\x54\x4C")
    if acTL > 0:
        iDAT = a.find(b"\x49\x44\x41\x54")
        if acTL < iDAT:
            return True
    return False

async def message_contains_apng(message: discord.Message):
    for embed in message.embeds:
        if embed.type == "image":
            async with aiohttp.ClientSession() as session:
                async with session.get(embed.url) as r:
                    if r.status == 200:
                        raw = await r.read()
                        if is_apng(raw):
                            return True
    
    for a in message.attachments:
        f = io.BytesIO()
        await a.save(f)
        if is_apng(f.read()):
            return True
    
    return False

class Badwords(commands.Cog):
    def __init__(self, bot, badwords):
        self.bot = bot
        self.badwords = list(map(re.compile, badwords))

    async def deluser(self, id):
        await self.bot.sql_conn.execute(f"DELETE FROM messagecount WHERE user_id = {id};")
        logger.debug(f"Deleted database entry for {id}")

    def isExempt(self, author: discord.User):
        for role in ["Administrator", "Moderator"]:
            if role in map(str, author.roles):
                return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.author, discord.User) or message.author.bot:
            return

        if not self.isExempt(message.author) and any(re.search(pattern, message.content.lower()) for pattern in self.badwords):
            # Remove the message which triggered the bot
            await message.delete()
            await message.author.send("There are some words discord doesn't like, we have to filter them out.")
            await self.deluser(message.author.id)
            automation_logger.info(f"user {message.author} ({message.author.id}) sent bad word in channel {message.channel.name}, message: \"{message.content[0:1500]}\" ")

        if await message_contains_apng(message):
            await message.delete()
            await message.channel.send(f"> We do not allow the APNG format due to it being abused. {message.author.mention}")

def setup(bot):
    with open("data/badwords.json") as f:
        badwords = json.load(f)
    print(badwords)
    bw = Badwords(bot, badwords)
    bot.add_cog(bw)