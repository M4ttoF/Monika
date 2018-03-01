#MainBot
import discord
from discord.ext import commands
import asyncio
import random
import os
import sys
from riotwatcher import RiotWatcher

bot=commands.Bot(command_prefix='!',description='This is a bot made by Matto')

watcher = RiotWatcher('RGAPI-8b67a641-0366-4c60-8a91-73a07d8764f3')


ADMIN = '131987304930738177'	        #my discord ID
COPY = '279111604384169984'#brej server
#'198220189400039425'		#Afreeca Discord

SAFE = '408832439318741004'
#'396811310722973697'#Fallout shelter
#'403296596424654859'		#Testerino





#This dictionary stores all the mod roles for the servers the bot is in
modRoles={}

#This dictionary is for the list of roles any user can assign to themselves
freeRoles={}


global chanNames
chanNames={}

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('--------------')



	with open('ModRoles.txt','r') as modRolesFile:
		file_data=modRolesFile.read()
	
	lines=file_data.split('\n')
	file_data=[]
	for i in range(len(lines)):
		file_data.append(lines[i].split())
		serv=bot.get_server(file_data[i][0])
		role=discord.utils.find(lambda m: m.id==file_data[i][1], serv.roles)
		
		#check if the role still exists
		if not role == None:
			modRoles[serv]=role



############################
#		Owner Commands
@bot.command(pass_context=True)
async def kill(ctx):
	if ctx.message.author.id==ADMIN:
		await bot.say( 'Goodbye!')
		bot.logout()
		bot.close()
		sys.exit()


@bot.command(pass_context=True)
async def servers(ctx):
	if ctx.message.author.id==ADMIN:
		msg=''
		for server in bot.servers:
			msg+= server.name+'\t'+server.id
			msg+='\n'
		await bot.say(msg)


@bot.command(pass_context=True)
async def modroles(ctx):
	if ctx.message.author.id==ADMIN:
		print(modRoles)


###################################
#		Mod commands



@bot.command(pass_context=True)
async def addFree(ctx,role : discord.Role):
	if ctx.message.channel.permissions_for(ctx.message.author).administrator:
		if not ctx.message.server in freeRoles:
			freeRoles[ctx.message.server]={}
			await bot.say('Created list')
		freeRoles[ctx.message.server][role.name.lower()]=role
		await bot.say('Added '+ role.name)
		print(freeRoles)



@bot.command(pass_context=True)
async def join(ctx):
	if not ctx.message.server in freeRoles:
		await bot.say("No free roles setup!")
		return None
	word=ctx.message.content.lower().split()[1]
	print(word)
	if word in freeRoles[ctx.message.server]:
		await bot.add_roles(ctx.message.author,freeRoles[ctx.message.server][word],ctx.message.channel)
		await bot.say(ctx.message.author.name+ ' added to '+freeRoles[ctx.message.server][word].name)

	else:
		await bot.say('Couldnt find that role!')





@bot.command(pass_context=True)
async def purge(ctx,num : int):
	if message.channel.permissions_for(ctx.message.author).manage_messages:

		if num==None or num>50:
			bot.purge_from(channel=ctx.message.channel, limit=50)
		else:
			bot.purge_from(channel=ctx.message.channel,limit=num)

@bot.command(pass_context=True)
async def setmodrole(ctx, role : discord.Role):
	message=ctx.message
	if message.channel.permissions_for(message.author).administrator:
		roles=list(message.content)
		if len(roles)<2:
			await bot.say( 'No role mentioned!')
		else:
			if message.server in modRoles:
				await bot.say('Mod role is already set!\nUse (!setmodrole) with no argument to reset it' )
			else:
				WriteLine(message,'ModRoles.txt',role.id)
				await bot.say( 'Mod role set to '+role.name)
				modRoles[message.server]=role
	else:
		await bot.say( 'Invalid Permissions')



@bot.command(pass_context=True)
async def resetmod(ctx):
	message=ctx.message
	if message.channel.permissions_for(message.author).administrator:
		del(modRoles[message.server])
		DeleteLine(message,'ModRoles.txt')
		await bot.say( 'Mod role cleared')


 
@bot.command(pass_context=True)
async def mod(ctx,member : discord.Member):
	message=ctx.message
	if message.server in modRoles:

		if message.channel.permissions_for(ctx.message.author).administrator:
			users=message.mentions
			await bot.add_roles(member,modRoles[message.server],message.channel)

		else:
			await bot.say('Invalid Permissions')
	else:
		await bot.say('No mod role set up!\nUse "!setmodrole <Role>" to set the role')


@bot.command(pass_context=True)
async def demod(ctx,member : discord.Member):

	message=ctx.message
	if message.channel.permissions_for(message.author).administrator:
		if message.server in modRoles:
			users=message.mentions
			if member==None:
				await bot.say('No users mentioned!')
			else:
				await bot.remove_roles(member,modRoles[message.server],message.channel)
		else:
			await bot.say('No mod role set up!\nUse "!modrole <Role>" to set the role')

	else:
		await bot.say('Invalid Permissions')


######################################
#		Regular Commands



@bot.command()
async def roll(num : int):
	if num==None:
		x=random.randrange(1,6);
	if num<1:
		bot.say('Invalid Number')
		return None
	else:
		x=random.randrange(1,num);
	bot.say('You rolled a ',x,'!')
		

				


def isNum(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


async def addRoles(mems,roles,chan):
	if len(mems)==0 or len(roles)==0:
		await bot.say(chan,'No user or role mentioned')
	else:
		for m in mems:
			for r in roles:
				await bot.add_roles(m,r)
		await bot.say(chan,'Roles added!')

async def removeRoles(mems,roles,chan):
	if len(mems)==0 or len(roles)==0:
		await bot.say(chan,'No user or role mentioned')
	else:
		for m in mems:
			for r in roles:
				await bot.remove_roles(m,r)
		await bot.say(chan,'Roles have been revoked!')
		print(chan.server)



def WriteLine(msg, fileName,ln):
	with open(fileName,'a') as file:
		file.write(msg.server.id+' '+ln+'\n')
	file.close()


def DeleteLine(msg,fileName):
	with open(fileName,'r+') as file:
		lines=file.readlines()
		file.seek(0)
		for line in lines:
			if not line.startswith(msg.server.id):
				file.write(line)

		file.truncate()
		file.close()

#bot.run('email','pass')
#bot.close()
bot.run('NDAyOTUzMTUwODExNzM0MDE3.DUAgKA.KCF_Vff5GKx8M7gqDyOwLTjHZeM')
