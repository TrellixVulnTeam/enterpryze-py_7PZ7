import discord
import asyncio
import config
from discord.utils import get
import database

print('discord.py v' + discord.__version__)
client = discord.Client()

# When bot has loaded
@client.event
async def on_ready():
    print('Logged in as:', client.user.name, "(" + client.user.id + ")")
    
    # Set status
    presence = discord.Game(name=config.PREFIX + "help for help")
    await client.change_presence(game=presence)

    print('Ready.')

# Handle message events
@client.event
async def on_message(message):
    author = message.author

    # Don't respond to bots, includes self
    if author.bot is True:
        return

    channel = message.channel
    content = message.content

    # Active chat logging
    print(message.timestamp, '[' + message.server.name + '/' + channel.name + '/' + author.name + ']:', content)
    
    # Ping/pong 
    if content.startswith(config.PREFIX + 'ping'):
        await client.send_message(channel, author.mention + ': Pong!')
    
    # Help
    if content.startswith(config.PREFIX + 'help'):
        await client.send_message(channel, author.mention + ": A list of commands and usage instructions has been sent to you via PM.")
        await client.send_message(author, "Help")

    # Vote
    if content.startswith(config.PREFIX + 'vote'):
        topic = ' '.join(content.split(' ')[1:]) # Get every word after the command
        vote_message = await client.send_message(channel, 'A vote has been called by ' + author.mention + ': **' + topic + '**\nVote by adding reactions. Voting will close in 60 seconds.')
        await client.add_reaction(vote_message, config.AYE)
        await client.add_reaction(vote_message, config.NAY)
        await asyncio.sleep(config.DEFAULT_VOTE_TIME)
        results = vote_message.reactions
        results_aye = get(results, emoji=config.AYE)
        results_nay = get(results, emoji=config.NAY)
        print(results_aye, results_nay)
        await client.send_message(channel, "The vote by " + author.mention + " has ended.")

    # Count how many messages a user has sent in a channel
    if content.startswith(config.PREFIX + 'count'):
        
        counter = 0
        tmp = await client.send_message(channel, 'Calculating messages...')
        async for log in client.logs_from(channel, limit=100):
            if log.author == author:
                counter += 1

        await client.edit_message(tmp, author.mention + ': You have {} messages.'.format(counter))

@client.event
async def on_member_join(member):
    server = member.server
    print(message.timestamp, "[" + server.name + "]:", member.name, "joined")
    if config.WELCOME_CHANNEL is not None:
        # channel = server.get_channel(config.WELCOME_CHANNEL_ID)
        channel = get(server.channels, name=config.WELCOME_CHANNEL)
        await client.send_message(channel, "Welcome to " + server.name + ", " + member.mention + "!")

# Start bot
client.run(config.TOKEN)