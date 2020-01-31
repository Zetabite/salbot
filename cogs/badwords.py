import discord

class WordBlacklist(cogs):
  def __init__(self, bot):
    self.bot = bot
    self.words = # your lsit of words
  
  # your on message here
def setup(bot):
  bot.add_cog(WordBlacklist(bot))
  
bad_words = ["nigger", "faggot", "pornhub.com", "discord.gg"]

@bot.event
async def on_message(message):
    message_content = message.content.strip().lower()
    for bad_word in bad_words:
        if bad_word in message.content:
            await message.delete()
