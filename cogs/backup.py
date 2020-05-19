import logging
import os

import discord
from discord.ext import commands
from discord.utils import get
from io import BytesIO

class Backup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.messages_done = False
        self.source_guild: discord.Guild = self.bot.get_guild(int(os.environ["BACKUP_SOURCE_GUILD"]))
        self.destination_guild: discord.Guild = self.bot.get_guild(int(os.environ["BACKUP_DESTINATION_GUILD"]))
        self.channel_to_webhook = {}
        self.bot.loop.create_task(self.loop_message_history())
    
    async def get_webhook(self, channel:discord.TextChannel) -> discord.Webhook:
        for webhook in await channel.webhooks():
            if webhook.name == "BackupWebhookPleaseDontEdit":
                return webhook
        return await channel.create_webhook(name="BackupWebhookPleaseDontEdit")
    
    async def update_mapping(self):
        for channel in self.destination_guild.channels:
            if isinstance(channel, discord.TextChannel):
                self.channel_to_webhook[channel.name] = await self.get_webhook(channel)
    
    async def find_webhook(self, channel: discord.TextChannel) -> discord.Webhook:
        await self.update_mapping()
        if not channel.name in self.channel_to_webhook.keys():
            await self.destination_guild.create_text_channel(channel.name)
        await self.update_mapping()
        return self.channel_to_webhook[channel.name]
    

    def convert(self, message):
        parameters = {
            "content": message.content,
            "username": str(message.author)[:15],
            "avatar_url": message.author.avatar_url,
            "embeds": message.embeds
        }

        # Load files
        files = []
        for attachment in message.attachments:
            buffer = BytesIO(bytes(attachment.data))
            files.append(discord.File(fp=buffer, filename=attachment.filename, spoiler=attachment.is_spoiler))
        
        for emoji in message.emojis:
            buffer = BytesIO(bytes(emoji.data))
            files.append(discord.File(fp=buffer, filename=emoji.filename))
        
        parameters["files"] = files
        
        return parameters

    async def handle_message(self, message: discord.Message):
        channel = message.channel
        dest_webhook = await self.find_webhook(channel)
        await dest_webhook.send(**self.convert(message))

    async def loop_message_history(self):
        for channel in self.source_guild.channels:
            if isinstance(channel, discord.TextChannel):
                async for message in channel.history(limit=None, oldest_first=True):
                    await self.handle_message(message)
        self.messages_done = True
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild == self.source_guild:
            if self.messages_done:
                await self.handle_message(message)

def setup(bot):
    bot.add_cog(Backup(bot))
