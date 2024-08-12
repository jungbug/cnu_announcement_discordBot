from typing import Callable

from discord import *
from discord.ext import commands, tasks

from ...env.settings import DiscordAPISettings


# Create intent configuration
intents = Intents.default()

# Grant permissions to read message content, presences, and members
intents.message_content = True
intents.presences = True
intents.members = True


# Create a bot instance
def create_bot() -> tuple[callable, callable, callable, Callable[[int], abc.GuildChannel]]:
    bot = commands.Bot(command_prefix='!', intents=intents)

    def on_ready(func):
        @bot.event
        async def wrapped():
            print(f"INFO: Logged in as {bot.user.name}")
            func()
        return wrapped

    def run():
        bot.run(DiscordAPISettings.token)

    def get_channel(channel_id: int) -> TextChannel:
        return bot.get_channel(channel_id)

    return run, on_ready, tasks.loop, get_channel
