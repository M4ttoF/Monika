#Role Management
import asyncio
import random
import os
import sys
import subprocess
import discord
from discord.ext import commands

class RoleManagement():
	def __init__(self, bot):
		self.bot = bot

		#This dictionary is for the list of roles any user can assign to themselves
		self.freeRoles={}
		

	@commands.command(hidden=True)
	async def loadRoles(self,ctx):
		if ctx.author.id==131987304930738177:
			with open('OpenRoles.txt','r') as openRolesFile:
				file_data=openRolesFile.read()
			
			lines=file_data.split('\n')
			file_data=[]
			for line in lines:
				file_data=line.split()
				try:	
					servId=int(file_data[0]);
					serv=None
					print(servId,end='lel\n')
					serv=self.bot.get_guild(servId)
					print(serv)
					self.freeRoles[serv]={}


					for i in file_data:
						num=int(i)
						if not num==servId:
							role=discord.utils.find(lambda m: m.id==num, serv.roles)
							if not role == None:
								self.freeRoles[serv][role.name.lower()]=role
				except Exception as e:
					print(e)
					openRolesFile.close()

	@commands.command(pass_context=True)
	async def addFree(self,ctx,role : discord.Role):
		"""Adds a role to the free roles"""
		if not ctx.guild in self.freeRoles:
			#WriteLine(ctx.message,'OpenRoles.txt',role.id)
			self.freeRoles[ctx.guild]={}
			await ctx.send('Created list')
		else:
			AddLine(ctx.message,'OpenRoles.txt',role.id)
		self.freeRoles[ctx.guild][role.name.lower()]=role
		await ctx.send('Added '+ role.name)
		print(self.freeRoles)



	@commands.command(pass_context=True)
	async def roles(self,ctx):
		"""Lists the free roles any user can join"""
		if not ctx.guild in self.freeRoles:
			await ctx.send('No roles available to join!')
			return
		msg='```\n'
		array=list(self.freeRoles[ctx.guild].keys())
		for a in array:
			msg+=a
			msg+='\n'
		msg+='```'
		await ctx.send(msg)

	@commands.command(pass_context=True)
	async def joinRole(self,ctx):
		"""joins one of the free roles"""
		if not ctx.guild in self.freeRoles:
			await ctx.send("No free roles setup!")
			return None
		word=ctx.message.content.lower()[6:]
		print(word)
		if word in self.freeRoles[ctx.guild]:
			await ctx.author.add_roles(self.freeRoles[ctx.guild][word])
			await ctx.send(ctx.author.name+ ' added to '+self.freeRoles[ctx.guild][word].name)
		else:
			await ctx.send('Couldnt find that role!')

def WriteLine(msg, fileName,ln):
	with open(fileName,'a') as file:
		gID=str(msg.guild.id)
		file.write(gID+' '+ln+'\n')
	file.close()


def AddLine(msg,fileName,ln):
	with open(fileName, 'r+') as file:
		lines=file.readlines()
		file.seek(0)
		for line in lines:
			if line.startswith(msg.guild.id):
				file.write(line[:-1]+" "+ln+'\n')
			else:
				file.write(line)

def DeleteLine(msg,fileName):
	with open(fileName,'r+') as file:
		lines=file.readlines()
		file.seek(0)
		for line in lines:
			if not line.startswith(msg.guild.id):
				file.write(line)

		file.truncate()
		file.close()
def setup(bot):
    bot.add_cog(RoleManagement(bot))