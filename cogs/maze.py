from discord.ext import commands
import discord
import random

class Maze(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.enabled = False
		self.mid = [373946864531144726]

	@commands.Cog.listener()
	async def on_message(self, ctx):
		if ctx.author.id in self.mid and self.enabled:
			if random.randint(0,100) == 5:
				await ctx.channel.send(f"Fuck you {ctx.author.mention} >:)")

	@commands.has_any_role("Moderator", "Administrator", "Private Chat Access")
	@commands.command(name='togglemaze')
	async def togglemaze(self, ctx):
		if ctx.author.id in self.mid or ctx.author.id == 297045071457681409:
			if self.enabled:
				self.enabled = False
			else:
				self.enabled = True
			await ctx.send(f"Toggled maze responses to {self.enabled}")

def setup(bot):
	bot.add_cog(Maze(bot))