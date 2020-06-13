import json
import os
from discord.ext import commands
import discord
from discord.utils import get
import logging
import re
logger = logging.getLogger('salc1bot')
automation_logger = logging.getLogger('salc1bot.automated')

g_channels = {
    "channels":[660701994549379125, 669119687530905613, 436411303351943188, 548308507636662283, 710226813808279615],
    "packchannels":[666575359411748875, 666758275504537604, 710226813808279615]
}

class RegExMessagePair:
    def __init__(self, reg, content, channels):
        self.reg = reg
        self.content = content
        self.ch = channels
        self.channels = g_channels[channels]

class FaqMessage:
    def __init__(self, name, content):
        self.name = name
        self.content = f"{content}"

    async def __call__(self, ctx):
        delete_after = None
        if len(ctx.author.roles) <= 1:
            delete_after = 30
        await ctx.send(self.content, delete_after=delete_after)


class Faq(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.PE = True
        self.regexs = []
        with open("data/faq.json") as f:
            self.json_data = json.load(f)
        for item in self.json_data:
            command = FaqMessage(item["names"][0], item["content"])
            for listitem in item["regexs"]:
                self.regexs.append(RegExMessagePair(listitem, item["content"], item["channels"]))
            #print(command.name, command.content)
            self.faq.command(item["names"][0], aliases=item["names"][1:])(command.__call__)


    @commands.group(name="faq")
    @commands.has_any_role("Member", "Private Chat Access", "OG Role That Has No Purpose", "Moderator", "Administrator")
    async def faq(self, ctx):
        if ctx.invoked_subcommand is None:
            msg = "FAQ Commands:\n```md"
            for command in self.faq.commands:
                msg += f"\n+ {command.name}"
            msg += '\n```'
            await ctx.channel.send(msg, delete_after=30)

    @faq.command(name="togglepack")
    @commands.has_any_role("Administrator", "Moderator")
    async def togglepack(self, ctx):
        self.PE = False if self.PE else True
        resp = "enabled" if self.PE else "disabled"
        await ctx.channel.send(f"Pack.png bot responses have been {resp}")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return
        if ctx.channel.id in [666575359411748875, 666758275504537604, 710226813808279615] and not self.PE:
            return
        content = ctx.content.lower()
        if len(content.split(" ")) < 2:
            return
        if len(ctx.author.roles) >= 1:
            return
        for item in self.regexs:
            try:
                #print(re.search(item.reg, content))
                if re.search(item.reg, content) and (ctx.channel.id in item.channels):
                    await ctx.channel.send(item.content, delete_after=20)
                    if item.ch == "packchannels":
                        await ctx.add_reaction("\U00002705")
                    return
            except Exception as e:
                print(e)

def setup(bot):
    bot.add_cog(Faq(bot))