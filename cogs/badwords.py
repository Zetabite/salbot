from discord.ext import commands

class Badwords(commands.Cog):
    def __init__(self, bot, badwords):
        self.bot = bot
        self.badwords = badwords    
    

    @commands.Cog.listener()
    async def on_message(self, message):
	    if len(message.author.roles) <= 2 and any(word in message.content.lower() for word in self.badwords):
		    ### Print log in console:
		    print('Removed message - %s : %s' % (message.author, message.content))
		    ### Remove the message which triggered the bot
		    await message.delete()
		    ### Send reply/notification
		    await message.channel.send(f':eyes:')

def setup(bot):
    bw = Badwords(bot, ["nigger", "faggot", "pornhub.com", "retarded"])
    bot.add_cog(bw)
