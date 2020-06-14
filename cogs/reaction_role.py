from discord.ext import commands
import discord
from pathlib import Path
import json

logger = logging.getLogger('salc1bot')
data_store = Path("./data/reactionlistener.json")

class ReactionRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with data_store.open() as f:
            self.data = json.load(f)
        self.channel = self.bot.get_channel(self.data["channel_id"])
        self.guild = self.channel.guild
        self.role = self.guild.get_role(self.data["role_id"])

    def is_relevant_reaction(self, emoji_object):
        if isinstance(emoji_object, discord.PartialEmoji):
            id_ = emoji_object.id 
        if isinstance(emoji_object, discord.Reaction):
            id_ = emoji_object.emoji.id
        return id_ == self.data["emoji_id"]

    async def add_role(self, user):
        try:
            await user.add_roles(self.role)
        except Exception as e:
            logger.exception(f"Error adding role to: {user}", exc_info=True)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.data["message_id"]:
            return
        if self.is_relevant_reaction(payload.emoji):
            await self.add_role(self.guild.get_member(payload.user_id))
    
    @commands.command()
    @commands.has_any_role("Moderator", "Administrator")
    async def check_history(self, ctx):
        message = await self.channel.fetch_message(self.data["message_id"])
        for reaction in message.reactions:
            if self.is_relevant_reaction(reaction):
                async for member in reaction.users():
                    await self.add_role(member)
        
def setup(bot):
    bot.add_cog(ReactionRole(bot))