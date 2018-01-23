#MainBot
import discord
import asyncio
import random
import os
import sys
#from riotwatcher import RiotWatcher

#watcher = RiotWatcher('RGAPI-8b67a641-0366-4c60-8a91-73a07d8764f3')

client = discord.Client()

ADMIN = '131987304930738177'	#my discord ID
COPY = '198220189400039425'		#Afreeca Discord
SAFE = '403296596424654859'		#Testerino


@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
@client.event
async def on_message(message):
	global mimic, chanNames
	try:
		if mimic==None:
			print("oi")
	except NameError:
		chanNames=[]
		for s in client.servers:
			if s.id==SAFE:
				mimic=s
				break
		for c in mimic.channels:
			if c.type==discord.ChannelType.text:
				chanNames.append(c.name)
		print(mimic.id)

    
	###########################################
	#Admin commands
	auth=message.author
	if auth.id==ADMIN:
		if message.content.startswith('!servers'):
			msg=''
			for server in client.servers:
				msg+= server.name+'\t'+server.id
				msg+='\n'
			await client.send_message(message.channel, msg)
		if message.content.startswith('!kill'):
			await client.send_message(message.channel, 'Goodbye!')
			client.logout()
			client.close()
			sys.exit()

		


	##########################################
	#regular commands

	if message.content.startswith('!sleep'):
		await asyncio.sleep(5)
		await client.send_message(message.channel, 'Done sleeping')

	elif message.content.startswith('!roll'):
		line = message.content.split()
		if len(line)<2:
			await client.send_message(message.channel, 'Invalid usage')
		elif len(line)==2:
			await roll(message,1,int(line[1]))
		else:
			await roll(message,int(line[1]),int(line[2]))

	elif message.content.startswith('!purge'):
		if message.channel.permissions_for(auth).manage_messages:
			line=message.content.split()
			await purge(message,line)
		else:
			await client.send_message(message.channel, 'Invalid Permission')	
		

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
client.run('NDAyOTUzMTUwODExNzM0MDE3.DUAgKA.KCF_Vff5GKx8M7gqDyOwLTjHZeM')