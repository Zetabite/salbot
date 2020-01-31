import asyncio
import discord
from discord.ext import commands
import typing
  
bad_words = ["nigger", "faggot", "pornhub.com", "discord.gg", "test123"]

@bot.event
async def on_message(message):
    message_content = message.content.strip().lower()
    for bad_word in bad_words:
        if bad_word in message.content:
            await message.delete()
            
def setup(bot):
    bot.add_cog(badwords(bot))
