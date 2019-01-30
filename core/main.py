import discord
import asyncio
from debug import log

client = discord.Client()

# When bot has loaded
@client.event
async def on_ready():
    log('Logged in as:', client.user.name, "(" + client.user.id ")")
    log('------')

# Handle message events
@client.event
async def on_message(message):
    if message.content.startswith(config.PREFIX + 'test'):
        
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    
    elif message.content.startswith(config.PREFIX + 'sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run(config.TOKEN)