import discord
import asyncio
import config
from discord.utils import get
import database

# Initialize discord connection
client = discord.Client()
print('discord.py v' + discord.__version__)

# Initialize database connection
database = database.Connection()

# When bot has loaded
@client.event
async def on_ready():
    print('Logged in as:', client.user.name, "(" + client.user.id + ")")
    
    # Set status
    presence = discord.Game(name=config.PREFIX + "help for help")
    await client.change_presence(game=presence)

    print('Ready.')
    print('-'*50)

    if config.STARTUP_MESSAGE is not None:
        await send_global_message(config.STARTUP_MESSAGE)

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

    # Admin commands
    if(is_admin(author)):
        if content.startswith(config.ADMIN_PREFIX + 'setwelcomechannel'):
            new_channel_name = ' '.join(content.split(' ')[1:])
            new_channel = get(author.server.channels, name=new_channel_name)
            if new_channel is None:
                await client.send_message(channel, author.mention + ": Channel with name \"" + new_channel_name + "\" was not found.")
            else:
                database.update_server(author.server.id, "welcome_channel", new_channel.id)
                await client.send_message(new_channel, author.mention + ": This channel is now the welcome channel.")
        
        if content.startswith(config.ADMIN_PREFIX + 'setbotchannel'):
            new_channel_name = ' '.join(content.split(' ')[1:])
            new_channel = get(author.server.channels, name=new_channel_name)
            if new_channel is None:
                await client.send_message(channel, "Channel with name \"" + new_channel_name + "\" was not found.")
            else:
                database.update_server(author.server.id, "bot_channel", new_channel.id)
                await client.send_message(new_channel, author.mention + ": This channel is now the bot channel.")

        if content.startswith(config.ADMIN_PREFIX + 'admin'):
            new_admin_name = ' '.join(content.split(' ')[1:])
            new_admin = get(author.server.members, name=new_admin_name)
            if new_admin is None:
                await client.send_message(channel, author.mention + ": User with name \"" + new_admin_name + "\" was not found.")
            else:
                if new_admin.bot:
                    await client.send_message(channel, author.mention + ": User with name \"" + new_admin_name + "\" is a bot.")
                else:
                database.update_server(author.server.id, "admins", new_channel.id, operation="push")

    else:
        await client.send_message(channel, author.mention + ": You do not have permission to do that.")

# Handle server join events
@client.event
async def on_member_join(member):
    server = member.server
    print("[" + server.name + "]:", member.name, "(" + member.id + ") joined")
    if config.WELCOME_MESSAGE:
        # channel = server.get_channel(config.WELCOME_CHANNEL_ID)
        channel = get_welcome_channel(server)
        if channel is not None:
            await client.send_message(channel, "Welcome to " + server.name + ", " + member.mention + "!")
        # Register user
        database.get_user(member.id)

@client.event
async def on_member_remove(member):
    # Send message notifying that a person left
    server = member.server
    channel = get_welcome_channel(server)
    if channel is not None:
        await client.send_message(channel, "Goodbye, " + member.mention + "!")

async def send_global_message(message):
    """Sends a message to the bot channels of all the servers that EnterpRyze is connected to."""
    servers = client.servers # Get servers bot is connected to
    for server in servers: # Loop through each server
        channel = get_bot_channel(server)
        if channel is not None:
            await client.send_message(channel, message) # Send the message

def get_welcome_channel(server):
    """Gets welcome channel from database. Returns default if query result is null."""
    server_db = database.get_server(server.id)
    channel = client.get_channel(server_db['welcome_channel'])
    if channel is None:
        channel = get(server.channels, name=config.DEFAULT_WELCOME_CHANNEL)
    return channel

def get_bot_channel(server):
    """Gets bot channel from database. Returns default if query result is null."""
    server_db = database.get_server(server.id)
    channel = client.get_channel(server_db['bot_channel'])
    if channel is None:
        channel = get(server.channels, name=config.DEFAULT_BOT_CHANNEL)
    return channel

def is_admin(member):
    if member.server.owner == member:
        return True
    return False


# Start bot
client.run(config.TOKEN)