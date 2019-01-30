import discord
import asyncio
import config

client = discord.Client()

# When bot has loaded
@client.event
async def on_ready():
    print('Logged in as:', client.user.name, "(" + client.user.id + ")")
    
    # Update status
    presence = discord.Game(name=config.PREFIX+"help for help")
    await client.change_presence(game=presence)

    print('Ready.')

# Handle message events
@client.event
async def on_message(message):
    print(message.channel.id)
    if message.content.startswith(config.PREFIX + 'hello'):
        await client.send_message(message.channel, 'Hello, ' + message.author.mention + ".")
    
    # Count how many messages a user has sent in a channel
    if message.content.startswith(config.PREFIX + 'count'):
        
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    
    # Sleep
    elif message.content.startswith(config.PREFIX + 'sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

@client.event
async def on_member_join(member):
    if config.WELCOME_CHANNEL_ID is not None:
        server = member.server
        channel = server.get_channel(config.WELCOME_CHANNEL_ID)
        await client.send_message(channel, "Welcome to " + server.name + ", " + member.mention + "!")

# Start bot
client.run(config.TOKEN)