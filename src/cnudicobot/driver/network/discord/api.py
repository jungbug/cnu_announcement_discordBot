import discord
from discord.ext import commands

from ...env.settings import *


intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


async def run_function_hourly():
    seoul = pytz.timezone('Asia/Seoul')

    while True:
        now = datetime.datetime.now(seoul)

        if now.hour >= 8 and now.hour < 18:
            await my_function()

        await asyncio.sleep(3600)


@bot.event
async def on_ready():
    print(f'{bot.user}이(가) 준비 완료되었습니다.')
    await run_function_hourly()


if __name__ == '__main__':
    bot.run(discord_token)
