from datetime import datetime, timedelta
from time import time
from discord import Activity, ActivityType, Embed, Status, HTTPException, TextChannel
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions, CheckFailure, is_owner, group
from typing import Optional
from ..ext import check
from ..ext.utils import color
from typing import Optional
from corona_python import Country, World
from sr_api import image, Client as _client

class Utility(Cog, name='\U00002699 Utility'):
	'''Commands for config the bot and other Utils.'''
	def __init__(self, bot):
		self.bot = bot
		self._country = Country
		self._world = World()

	
	@command(name='color')
	async def _color(self, ctx, *, clr):
		'''
		returns a color by its hex
		color a773f5
		'''
		cl = _client()
		e = Embed(color=color.invis(self))
		e.set_image(url=cl.view_color(clr))
		await ctx.send(embed=e)
	
	
	@command()
	async def covid(self, ctx, *, country: Optional[str]=None):
		if country is not None:
			e = Embed(title=f"Covid stats for {country}", color=color.invis(self))
			country = self._country(country)
			if country.flag():
				e.set_image(url=country.flag())
			e.add_field(name='\U0000274c Active cases', value=country.active())
			e.add_field(name="\U0000274c Today's cases", value=country.today_cases())
			e.add_field(name='\U0000274c Total cases', value=country.total_cases())
			e.add_field(name="\U0000274c Today's deaths", value=country.today_deaths())
			e.add_field(name='\U0000274c Total deaths', value=country.total_deaths())
			e.add_field(name='\U0000274c Total criticals', value=country.critical())
			e.add_field(name='\U00002705 Total recovered', value=country.recovered())
			e.add_field(name='\U0001f30e Continent', value=country.continent())
			e.add_field(name="\U00002705 Today's recovered", value=country.today_recovered())
			await ctx.send(embed=e)
		else:
			e = Embed(title=f"Covid stats for the world. \U0001f30e", color=color.invis(self))
			e.add_field(name='\U0000274c Active cases', value=self._world.active_cases())
			e.add_field(name="\U0000274c Today's cases", value=self._world.today_cases())
			e.add_field(name='\U0000274c Total cases', value=self._world.total_cases())
			e.add_field(name='\U0000274c Last Updated', value=self._world.last_updated())
			e.add_field(name="\U0000274c Today's deaths", value=self._world.today_deaths())
			e.add_field(name='\U0000274c Total deaths', value=self._world.total_deaths())
			e.add_field(name='\U0000274c Total criticals', value=self._world.critical_cases())
			e.add_field(name='\U00002705 Total recovered', value=self._world.recovered())
			e.add_field(name="\U00002705 Today's recovered", value=self._world.today_recovered())
			e.set_footer(text=f"World Population {self._world.population()}")
			await ctx.send(embed=e)


	@command(name='ping')
	async def _ping(self, ctx):
		await ctx.message.add_reaction('\U00002705')


	@group(name="set")
	async def setter(self, ctx):
		pass


	@setter.command(name="prefix")
	@check.is_mod()
	async def change_prefix(self, ctx, prefix: Optional[str]):
		"""
		Change the bot's prefix. 
		You need the manage_guild perms to use this command.
		"""
		if len(prefix) > 6:
			await ctx.send("Prefix too long.")
			
		query = "SELECT prefix FROM prefixes WHERE id = $1"
		method = await self.bot.pool.fetchval(query, ctx.guild.id)

		if not method:
			await self.bot.pool.execute("INSERT INTO prefixes(id, prefix) VALUES ($1, $2)", ctx.guild.id, prefix)
			await ctx.send(f"Prefix changed to {prefix}")
		else:
			query = "UPDATE prefixes SET prefix = $1 WHERE id = $2"
			await self.bot.pool.execute(query, prefix, ctx.guild.id)
			await ctx.send(f"Prefix updated to {prefix}")


	@setter.command(name="sts", hidden=True)
	@is_owner()
	async def change_sts(self, ctx, stts: str):
		try:
			discord_status = ["dnd", "offline", "idle", "online"]
			
			if stts not in discord_status:
				await ctx.send(f"Couldn't change the status to `{stts}`")
			else:
				if stts == "dnd":
					await self.bot.change_presence(status=Status.dnd)
					await ctx.send(f"Status changed to `{stts}`")
				elif stts == "idle":
					await self.bot.change_presence(status=Status.idle)
					await ctx.send(f"Status changed to `{stts}`")
				elif stts == "offline":
					await self.bot.change_presence(status=Status.offline)
					await ctx.send(f"Status changed to `{stts}`")
				elif stts == "online":
					await self.bot.change_presence(status=Status.online)
					await ctx.send(f"Status changed to `{stts}`")
		except:
			raise



def setup(bot):
	bot.add_cog(Utility(bot))
