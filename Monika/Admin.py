#Admin.py
import asyncio
import random
import os
import sys
import subprocess
import discord
from discord.ext import commands

class Admin():

	def __init__(self, bot):
		self.bot = bot


	async def __local_check(self, ctx):
		return ctx.channel.permissions_for(ctx.author).manage_messages

	@commands.command(pass_context=True)
	async def purge(self,ctx,num : int):
		"""removes the most recent messages in the chat (limit is 50)"""
		if num>100:
			await ctx.channel.purge(limit=100)
		elif num>0:
			await ctx.channel.purge(limit=num)
		else:
			await ctx.send('Invalid Num')


#END OF CLASS



def setup(bot):
    bot.add_cog(Admin(bot))

	
