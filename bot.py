import discord
import os
import json


client = discord.Client()

commands = {}
people = {}
channels = {}

async def add_command(command, content, dictionary):
	output = " ".join(content)
	dictionary[command] = output
	return output

async def add_me_command(message, content):
	number = message.author.discriminator
	if not(number in people):
		people[number] = {}
	if (len(content) < 2):
		await message.channel.send("Usage: !add -m/--me <command> <output>")
	else:
		response = await add_command(content[0], content[1:], people[number])
		await message.channel.send("<@" + str(message.author.id) + "> Command added successfully exclusively for you!\n !" + content[0] + " " + response)

async def add_channel_content(message, content):
	number = message.channel.id
	if not(number in channels):
		channels[number] = {}
	if (len(content) < 2):
		await message.channel.send("Usage: !add -c/--channel <command> <output>")
	else:
		response = await add_command(content[0], content[1:], channels[number])
		await message.channel.send("Command added successfully exclusively for channel '" + message.channel.name + "'!\n !" + content[0] + " " + response)


async def add(message):
	content = message.content.split(" ")
	if (len(content) < 2):
		await message.channel.send("Usage: !add [options] <command> <output>")
	else:
		if (content[1][0] != '-'):
			if not(content[1] in commands):
				response = await add_command(content[1], content[2:], commands)
				await message.channel.send("Command added successfully!\n !" + content[1] + " " + response)
			else:
				await message.channel.send("Command already exists!\nUse command !change instead of !add to change")
		elif (content[1] == "--me" or content[1] == "-m"):
			await add_me_command(message, content[2:])
		elif (content[1] == "--channel" or content[1] == "-c"):
			await add_channel_content(message, content[2:])

async def change_me_command(message, content):
	number = message.author.discriminator
	if not(number in people):
		people[number] = {}
	if not(content[0] in people[number]):
		await message.channel.send("<@" + str(message.author.id) + "> personal command " + content[0]+ " doesn't exist!")
	elif(len(content) < 2):
		await message.channel.send("<@" + str(message.author.id) + "> Usage: !change -m/--me <command> <output>")
	else:
		response = await add_command(content[0], content[1:], people[number])
		await message.channel.send("<@" + str(message.author.id) + "> command changed successfully!\n !" + content[0] + " " + response)

async def change_channel_command(message, content):
	number = message.channel.id
	if not(number in channels):
		channels[number] = {}
	if not(content[0] in channels[number]):
		await message.channel.send("'" + message.channel.name + "' channel command " + content[0]+ " doesn't exist!")
	elif (len(content) < 2):
		await message.channel.send("Usage: !add -c/--channel <command> <output>")
	else:
		response = await add_command(content[0], content[1:], channels[number])
		await message.channel.send("Command changed successfully exclusively for channel '" + message.channel.name + "'!\n !" + content[0] + " " + response)


async def change(message):
	content = message.content.split(" ")
	if (len(content) < 3):
		await message.channel.send("Usage: !change <options> command output")
	else:
		if (content[1][0] != '-'):
			if (content[1] in commands):
				response = await add_command(content[1], content[2:], commands)
				await message.channel.send("Command changed successfully!\n !" + content[1] + " " + response)
			else:
				await message.channel.send("Command " + content[1]+ " doesn't exist!")
		elif (content[1] == "--me" or content[1] == "-m"):
			await change_me_command(message, content[2:])
		elif (content[1] == "--chanel" or content[1] == "-c"):
			await change_channel_command(message, content[2:])

async def check_me_command(message, content):
	number = message.author.discriminator
	if (number in people):
		if (content[0] in people[number]):
			await message.channel.send("<@" + str(message.author.id) + "> " + people[number][content[0]])
			return True
	return False

async def check_channel_command(message, content):
	number = message.channel.id
	if (number in channels):
		if (content[0] in channels[number]):
			await message.channel.send(channels[number][content[0]])
			return True
	return False

async def check_command(message):
	content = message.content.split(" ")
	content[0] = content[0][1:]
	recognized = await check_me_command(message, content)
	if not(recognized):
		recognized = await check_channel_command(message, content)
	if (not(recognized) and content[0] in commands):
		await message.channel.send(commands[content[0]])
		recognized = True
	if not(recognized):
		await message.channel.send("Command not recognized!")

async def delete(message):
	content = message.content.split(" ")
	if (len(content) < 2):
		await message.channel.send("Usage: !del [options] <command>")
	else:
		if (content[1][0] != '-'):
			if (content[1] in commands):
				commands.pop(content[1])
				await message.channel.send("Command removed successfully!\n")
			else:
				await message.channel.send("Command " + content[1]+ " doesn't exist!")
		elif (content[1] == "--me" or content[1] == "-m"):
			people[message.author.discriminator].pop(content[2])
			await message.channel.send("Personal command removed successfully!\n")
		elif (content[1] == "--chanel" or content[1] == "-c"):
			channels[message.channel.id].pop(content[2])
			await message.channel.send("Channel command removed successfully!\n")

async def save(message):
	f = open('commands.txt', 'w')
	f.write(json.dumps(commands))
	f.close()
	f = open('people.txt', 'w')
	f.write(json.dumps(people))
	f.close()
	f = open('channels.txt', 'w')
	f.write(json.dumps(channels))
	f.close()
	await message.channel.send("Saved all comands")

async def help(message):
	await message.channel.send("""BBot - Bacalhau's Bot

Usage: !<command>
Usage: !add [options] command output
Usage: !change [options] command output
Usage: !del command
Usage: !save

options:
	-m/--me: command only works with the person who created
	-c/--channel: command only works with on the channel it was created
If the same command exists for --me, --channel and without options the bot will choose based on this order: me > channel > general""")

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('!add'):
		await add(message)
	elif message.content.startswith('!change'):
		await change(message)
	elif message.content.startswith('!del'):
		await delete(message)
	elif message.content.startswith('!save'):
		await save(message)
	elif message.content.startswith('!help'):
		await help(message)
	elif message.content.startswith('!'):
		await check_command(message)

f = open("commands.txt", 'r')
commands = json.loads(f.read())
f.close()
f = open("people.txt", 'r')
people = json.loads(f.read())
f.close()
f = open("channels.txt", 'r')
channels = json.loads(f.read())
f.close()

client.run("ODE1MTgxNzU3MTYyMTkyOTA2.YDorLA.KPPHg4yrZAN61B4LvSfUnbaSrzU")