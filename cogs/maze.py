from discord.ext import commands
import discord
import random
import time

class Random:
    def __init__(self, seed=round(time.time())):
        self.seed = seed
        self.PSeed = seed

    def next(self):
        self.seed = (self.PSeed * self.seed + 11) % 2**48
        return(self.seed)

    def randint(self, max):
        return self.next() % 100

class Maze(commands.Cog):
	def __init__(self, bot):
		self.rng = Random()
		self.bot = bot
		self.enabled = True
		self.mid = [373946864531144726]

	@commands.Cog.listener()
	async def on_message(self, ctx):
		if ctx.author.id in self.mid and self.enabled:
			if self.rng.randint(100) == 43:
				await ctx.channel.send(f"Fuck you {ctx.author.mention}")
			if self.rng.randint(100) == 69:
				await ctx.channel.send(f"Do you like Alex Dillinger {ctx.author.mention}")

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
