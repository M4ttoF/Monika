#MainBot
import discord
import asyncio
import random
import os
import sys
from riotwatcher import RiotWatcher

watcher = RiotWatcher('RGAPI-8b67a641-0366-4c60-8a91-73a07d8764f3')

client = discord.Client()

ADMIN = '131987304930738177'	#my discord ID
COPY = '198220189400039425'		#Afreeca Discord
SAFE = '403296596424654859'		#Testerino



#Dictionaries for commands

#This dictionary stores all the mod roles for the servers the bot is in
modRoles={}

global messageCom

messageCom=None

############################
#		Owner Commands
async def killCom(message):
	if message.author.id==ADMIN:
		await client.send_message(message.channel, 'Goodbye!')
		client.logout()
		client.close()
		sys.exit()

async def serversCom(message):
	if message.author.id==ADMIN:
		msg=''
		for server in client.servers:
			msg+= server.name+'\t'+server.id
			msg+='\n'
		await client.send_message(message.channel, msg)

async def modrolesCom(self, message):
	if message.auth.id==ADMIN:
		print(modRoles)


###################################
#		Mod commands


async def purgeCom(message):
	if message.channel.permissions_for(message.author).manage_messages:
		line=message.content.split()
		await purge(message,line)
	else:
		await client.send_message(message.channel, 'Invalid Permissions')	

async def setmodroleCom(message):
	if message.channel.permissions_for(message.author).administrator:
		roles=message.role_mentions
		if len(roles)==0:
			if message.server in modRoles:
				
				del(modRoles[message.server])
				with open('ModRoles.txt','r') as modRolesFile:
					lines=modRolesFile.read()

				with open('ModRoles.txt','w') as modRolesFile:
					for line in lines:
						if not line.startswith(message.server.id) and len(line.split())==2:
							modRolesFile.write(line+'\n')

				await client.send_message(message.channel, 'Mod role cleared')

			else:
				await client.send_message(message.channel, 'No role mentioned!')
		else:
			with open('ModRoles.txt','a') as modRolesFile:
					modRolesFile.write(message.server.id+' '+roles[0].id+'\n')

			await client.send_message(message.channel, 'Mod role set to '+roles[0].name)
			modRoles[message.server]=roles[0]
	else:
		await client.send_message(message.channel, 'Invalid Permissions')



async def modCom(message):
	if message.server in modRoles:

		if message.channel.permissions_for(auth).administrator:
			users=message.mentions
			await addRoles(users,[modRoles[message.server]],message.channel)

		else:
			await client.send_message(message.channel, 'Invalid Permissions')
	else:
		await client.send_message(message.channel, 'No mod role set up!\nUse "!setmodrole <Role>" to set the role')


async def demodCom(message):
	if message.channel.permissions_for(message.author).administrator:
		if message.server in modRoles:
			users=message.mentions
			if len(users)==0:
				await client.send_message(message.channel, 'No users mentioned!')
			else:
				await removeRoles(users,[modRoles[message.server]],message.channel)
		else:
			await client.send_message(message.channel, 'No mod role set up!\nUse "!modrole <Role>" to set the role')

	else:
		await client.send_message(message.channel, 'Invalid Permissions')


######################################
#		Regular Commands

async def rollCom(message):
	line = message.content.split()
	if len(line)<1:		
		await client.send_message(message.channel, 'Invalid usage')
	elif len(line)==1:
		await roll(message,1,6)
	elif len(line)==2:
		await roll(message,1,int(line[1]))
	else:
		await roll(message,int(line[1]),int(line[2]))







commands={
	'!kill':killCom,'!servers': serversCom,'!mod':modCom,
	'!setmodrole':setmodroleCom,'!demod':demodCom,'!roll':rollCom,
	'!modroles':modrolesCom
	}







@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	with open('ModRoles.txt','r') as modRolesFile:
		file_data=modRolesFile.read()
	
	lines=file_data.split('\n')
	file_data=[]
	for i in range(len(lines)):
		file_data.append(lines[i].split())
		serv=client.get_server(file_data[i][0])
		role=discord.utils.find(lambda m: m.id==file_data[i][1], serv.roles)
		
		#check if the role still exists
		if not role == None:
			modRoles[serv]=role
		
	
	

@client.event
async def on_message(message):
	global mimic, chanNames, messageCom
	messageCom=message
	
	if message.content.startswith('!'):
		if message.content.lower().split()[0] in commands:
			await commands[message.content.lower().split()[0]](message=message)
		
	

	###############################################
	#copying messages to backup server
	elif message.server.id==COPY:
		if message.channel.name not in chanNames:
			await client.create_channel(mimic,message.channel.name,type=discord.ChannelType.text)
			
		for c in mimic.channels:
			if c.type!=discord.ChannelType.voice and c.name == message.channel.name:
				await client.send_message(c,auth.name+': '+message.content)			
async def roll(message,n,m):
	x=random.randrange(n,m+1);
	await client.send_message(message.channel,message.author.name+" rolled a "+str(x)+"!")

async def purge(message,line):
	if len(line) <2 :
		deleted = await client.purge_from(message.channel,limit=50)
		await client.send_message(message.channel,'Deleted {} message(s)'.format(len(deleted)))
	elif isNum(line[1]):
		deleted = await client.purge_from(message.channel,limit=int(line[1]))
		await client.send_message(message.channel,'Deleted {} message(s)'.format(len(deleted)))
	else:
		await client.send_message(message.channel,'Invalid usage')
def isNum(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


async def addRoles(mems,roles,chan):
	if len(mems)==0 or len(roles)==0:
		await client.send_message(chan,'No user or role mentioned')
	else:
		for m in mems:
			for r in roles:
				await client.add_roles(m,r)
		await client.send_message(chan,'Roles added!')

async def removeRoles(mems,roles,chan):
	if len(mems)==0 or len(roles)==0:
		await client.send_message(chan,'No user or role mentioned')
	else:
		for m in mems:
			for r in roles:
				await client.remove_roles(m,r)
		await client.send_message(chan,'Roles have been revoked!')
		print(chan.server)


client.run('NDAyOTUzMTUwODExNzM0MDE3.DUAgKA.KCF_Vff5GKx8M7gqDyOwLTjHZeM')