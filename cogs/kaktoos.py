from discord.ext import commands
import discord
import re
import logging
automation_logger = logging.getLogger('salc1bot.automated')

class Kaktoos(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.regexes = []
		self.cactus = None
		self.enabled = True
		with open('data/kaktoos.txt') as f:
			for line in f.readlines():
				self.regexes.append(re.compile(line.strip("\n")))

	@commands.Cog.listener()
	async def on_message(self, ctx):
		if not self.enabled:
			return
		if isinstance(ctx.channel, discord.channel.DMChannel):
			return
		if not self.cactus:
			self.cactus = self.bot.get_user(459235187469975572)
		for regex in self.regexes:
			if regex.search(ctx.content.lower()):
				await self.cactus.send(f"Alert for regex '{regex}' in channel {ctx.channel.name}")
				automation_logger.info(f"[CactusAlert] Alert for regex '{regex}' in channel {ctx.channel.name}")
				return

	@commands.has_any_role("Administrator", "Moderator")
	@commands.command(name="cactusadd")
	async def cactusadd(self, ctx):
		try:
			cmd = ctx.message.content.split(' ', 1)[1]
			with open("data/kaktoos.txt", 'a') as f:
				f.write("\n" + cmd)
			with open('data/kaktoos.txt') as f:
				for line in f.readlines():
					self.regexes.append(re.compile(line.strip("\n")))
		except Exception as e:
			print(e)

	@commands.has_any_role("Administrator", "Moderator")
	@commands.command(name='cactustoggle')
	async def cactustoggle(self, ctx):
		self.enabled = False if self.enabled else True
		await ctx.channel.send(f"Toggled CactusAlert to {self.enabled}")

def setup(bot):
	bot.add_cog(Kaktoos(bot))