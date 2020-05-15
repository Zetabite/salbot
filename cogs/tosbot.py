import json
import os
from discord.ext import commands
import discord
from discord.utils import get
import logging
logger = logging.getLogger('salc1bot')

termtypes = {
    "warn":"The following is banned by Discord's community guidelines and may result in account termination: ",
    "termination":"The following is banned by Discord's community guidelines and will result in immediate account deletion by Discord: ",
    "none":"",
    "nouse":"By agreeing to Discord's ToS, you agree not to use Discord in order to: "
}

class TosCommand:
    def __init__(self, name, content, typ):
        self.name = name
        self.typ = termtypes[typ]
        self.content = f"{content}"

    async def __call__(self, ctx):
        delete_after = None
        if ctx.author.top_role.name == "Member":
            delete_after = 30
        embed = discord.Embed(title=self.typ, description=self.content)
        await ctx.send(embed=embed, delete_after=delete_after)


class Tos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("data/dgl.json") as f:
            self.json_data = json.load(f)
        for item in self.json_data:
            command = TosCommand(item["names"][0], item["content"], item["info"])
            print(command.name, command.content)
            self.dgl.command(item["names"][0], aliases=item["names"][1:])(command.__call__)

        with open("data/tos.json") as f:
            self.json_data = json.load(f)
        for item in self.json_data:
            command = TosCommand(item["names"][0], item["content"], item["info"])
            print(command.name, command.content)
            self.tos.command(item["names"][0], aliases=item["names"][1:])(command.__call__)

    @commands.group(name="dgl")
    @commands.has_any_role("Member", "Private Chat Access", "OG Role That Has No Purpose", "Moderator", "Administrator")
    async def dgl(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Discord Guidelines Commands")
            for command in self.dgl.commands:
                embed.add_field(
                    name=command.name, value=f"Aliases: {', '.join(command.aliases)}", inline=True)
            await ctx.channel.send(embed=embed)

    @commands.group(name="tos")
    @commands.has_any_role("Member", "Private Chat Access", "OG Role That Has No Purpose", "Moderator", "Administrator")
    async def tos(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Discord ToS Commands")
            for command in self.tos.commands:
                embed.add_field(
                    name=command.name, value=f"Aliases: {', '.join(command.aliases)}", inline=True)
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Tos(bot))
