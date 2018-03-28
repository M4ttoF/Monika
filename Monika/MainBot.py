#MainBot
import discord
from discord.ext import commands
import asyncio
import random
import os
import sys
#from riotwatcher import RiotWatcher


startup_extensions = ["Music","Admin","RoleManagement"]

bot=commands.Bot(command_prefix='!',description='This is a bot made by Matto')

#watcher = RiotWatcher('RGAPI-8b67a641-0366-4c60-8a91-73a07d8764f3')


ADMIN = 131987304930738177	        #my discord ID





#This dictionary stores all the mod roles for the servers the bot is in
modRoles={}




arrr=[]

global chanNames
chanNames={}

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('--------------')






############################
#		Owner Commands
@bot.command(pass_context=True,hidden=True)
async def kill(ctx):
	if ctx.author.id==ADMIN:
		await ctx.send( 'Goodbye!')
		bot.logout()
		bot.close()
		sys.exit()

@bot.command(pass_context=True,hidden=True)
async def servers(ctx):
	if ctx.author.id==ADMIN:
		msg=''
		for server in bot.servers:
			msg+= server.name+'\t'+server.id
			msg+='\n'
		await ctx.send(msg)

@bot.command(pass_context=True,hidden=True)
async def modroles(ctx):
	print(modRoles)


@bot.command(pass_context=True,hidden=True)
async def say(ctx):
	if ctx.author.id==ADMIN:
		await ctx.channel.purge(limit=1)
		await ctx.send(ctx.message.content[4:])

@bot.command(pass_context=True,hidden=True)
async def printList(ctx):
	if ctx.author.id==ADMIN:
		await ctx.send(arrr)



######################################
#		Regular Commands



@bot.command()
async def roll(ctx):
	"""Rolls a 6 sided die"""
	x=random.randrange(1,7);
	await ctx.send('You rolled a '+str(x)+'!')

@bot.command()
async def croll(ctx,num : int):
	"""Enter a number for a custom roll"""
	if num<1:
		await ctx.send('Invalid number!')
		return
	x=random.randrange(1,num);
	await ctx.send('You rolled a '+str(x)+'!')			


def isNum(s):
	try:
		int(s)
		return True
	except ValueError:
		return False






def WriteLine(msg, fileName,ln):
	with open(fileName,'a') as file:
		file.write(msg.server.id+' '+ln+'\n')
	file.close()


def AddLine(msg,fileName,ln):
	with open(fileName, 'r+') as file:
		lines=file.readlines()
		file.seek(0)
		for line in lines:
			if line.startswith(msg.server.id):
				file.write(line[:-1]+" "+ln+'\n')
			else:
				file.write(line)

def DeleteLine(msg,fileName):
	with open(fileName,'r+') as file:
		lines=file.readlines()
		file.seek(0)
		for line in lines:
			if not line.startswith(msg.server.id):
				file.write(line)

		file.truncate()
		file.close()



if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


#bot.run('email','pass')
#bot.close()
bot.run('NDAyOTUzMTUwODExNzM0MDE3.DUAgKA.KCF_Vff5GKx8M7gqDyOwLTjHZeM')
