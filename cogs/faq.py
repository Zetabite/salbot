import discord
import json
import inspect
import re
from discord.ext import commands

def FAQMessage_factory(bot, names, regexes, channel_whitelist, message):
    """return cog classes, needed for cog name
    
    names: List of command names this FAQ Message is known as
    regexes: list of regex r"" strings for matching non-command messages
    channel_whitelist: list of channel ids to respond to
    message: string of the message which the bot responds with
    """
    
    class FAQMessage(commands.Cog, name=names[0]):
        def __init__(self, bot, names, regexes, channel_whitelist, message,):
            self.bot = bot
            self.names = names
            self.command = commands.command(names[0], aliases=names[1:])(self.send) # create the command to be later added to the bot
            self.message = message
            self.regexes = [re.compile(reg) for reg in regexes]
            self.channel_whitelist = channel_whitelist

        @commands.Cog.listener()
        async def on_message(self, message):
            if message.author.id != self.bot.user.id: # check for the bot beign the author
                if message.channel.id in self.channel_whitelist:# check for channel in channel_whitelist
                    if any(r.search(message.content) for r in self.regexes): # check if any of the regexes are matched
                        await self.send(message.channel) # send the message using the method below

        async def send(self, channel): # this is a seperate method because of the command
            await channel.send(self.message) # simply send the message

    return FAQMessage(bot, names, regexes, channel_whitelist, message)

def setup(bot):
    channels = [666575359411748875, 666758275504537604, 666813360867770388, 660701994549379125, 669119687530905613]
    
    faq_messages = [
        FAQMessage_factory(bot, ["dream", "dreams"], [r"dream.?s?.?method",], channels, ">>> Hey, it looks like you mentioned Dream! Unfortunately we cannot use that method because we don't have enough information. But here's some other ideas: {link to a google doc}"),
        FAQMessage_factory(bot, ["seed",], [r"seed.is", r"have.?the.?seed"], channels, ">>> Hey, it looks like you mentioned what the seed is! If you actually found the seed, please message a mod. If you're saying this as a joke, please dont :)"),
        FAQMessage_factory(bot, ["supercomputer", "supercomp", "sc"], [r"super.?comput."], channels, ">>> Hey, it looks like you mentioned a supercomputer! Thankfully `@cactus uwu#0523` is dedicating several supercomputers towards this!"),
        FAQMessage_factory(bot, ["quantumcomputer", "qcomp", "qc"], [r"quantum.?comput."], channels, ">>> Hey, it looks like you mentioned a quantum computer! Unfortunately this won't help with this problem and we already have enough computing power"),
        FAQMessage_factory(bot, ["ihelp",], [r"(?:(?:can|may).?i.?help)", r"(do.?to.?help)"], channels, ">>> Hey, it looks like want to help! If you have reverse-engineering or coding experience head to <#666758275504537604>, otherwise you can help a recreation project in <#666813360867770388>"),
    ]

    for faq in faq_messages:
        bot.add_cog(faq)
        bot.add_command(faq.command)

