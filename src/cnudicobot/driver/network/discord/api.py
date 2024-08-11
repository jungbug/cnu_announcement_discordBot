import discord
from discord.ext import commands, tasks

from ...env.settings import *


# Create intent configuration
intents = discord.Intents.default()

# Grant permissions to read message content, presences, and members
intents.message_content = True
intents.presences = True
intents.members = True

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)


def on_ready(func):
    @bot.event
    async def wrapped():
        print(f"INFO: Logged in as {bot.user.name}")
        await func()
    return wrapped


def run():
    bot.run(TOKEN)
