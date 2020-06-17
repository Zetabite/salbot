from discord.ext import commands
import discord
from pathlib import Path
import json
import logging

logger = logging.getLogger('salc1bot')
data_store = Path("./data/reactionlistener.json")
blacklist_store = Path("./salbot-secrets/packpng_blacklist.json")

class ReactionRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with data_store.open() as f:
            self.data = json.load(f)
        with blacklist_store.open() as f:
            self.blacklist = json.load(f)
        self.channel = self.bot.get_channel(self.data["channel_id"])
        self.guild = self.channel.guild
        self.role = self.guild.get_role(self.data["role_id"])

    def add_blacklist(self, id):
        self.blacklist.append(id)
        with blacklist_store.open("w") as f:
            json.dump(self.blacklist, f)

    def is_relevant_reaction(self, emoji_object):
        if isinstance(emoji_object, discord.PartialEmoji):
            id_ = emoji_object.id 
        if isinstance(emoji_object, discord.Reaction):
            id_ = emoji_object.emoji.id
        return id_ == self.data["emoji_id"]

    async def add_role(self, member):
        try:
            await member.add_roles(self.role)
        except Exception as e:
            logger.exception(f"Error adding role to: {member}", exc_info=True)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.data["message_id"]:
            return
        if payload.user_id in self.blacklist:
            return
        if self.is_relevant_reaction(payload.emoji):
            logmessage = f"Not Member\npayload.member: {payload.member} {type(payload.member)}"
            getmember = self.guild.get_member(payload.user_id)
            logmessage += f"\nguild.get_member: {getmember} {type(getmember)}"
            if isinstance(getmember, discord.member.Member):
                await self.add_role(getmember)
            else:
                logger.error(logmessage)
            if isinstance(payload.member, discord.member.Member):
                await self.add_role(payload.member)
            else:
                logger.error(logmessage)
            print(logmessage)

    @commands.command()
    @commands.has_any_role("Moderator", "Administrator")
    async def check_history(self, ctx):
        message = await self.channel.fetch_message(self.data["message_id"])
        for reaction in message.reactions:
            if self.is_relevant_reaction(reaction):
                async for member in reaction.users():
                    if not member.id in self.blacklist:
                        await self.add_role(member)
    
    @commands.command()
    @commands.has_any_role("Moderator", "Administrator")
    async def packmute(self, ctx, member: discord.Member):
        await member.remove_roles(self.role)
        self.add_blacklist(member.id)
        await ctx.channel.send(f"Packmuted {member}")
        
def setup(bot):
    bot.add_cog(ReactionRole(bot))