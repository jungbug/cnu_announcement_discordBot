from ...driver.network.discord.api import create_bot, abc, ForumChannel
from ...driver.env.settings import DiscordAPISettings
from .formatter import format_notice_content, create_embed, ContentType


def setup_transmitter(task: callable | list[callable]):
    run, on_ready, loop, get_channel = create_bot()

    @loop(minutes=30)
    async def run_task():
        if not isinstance(task, list):
            await task(get_channel)  # run the task with the get_channel function
        else:
            for t in task:
                await t(get_channel)

    @on_ready
    def register_task():
        run_task.start()  # run the task when the bot is ready

    return run


def get_channel_id(board_name: str):
    return DiscordAPISettings.channel_id[board_name]


async def notify(channel: abc.GuildChannel, title: str, content_tags: list, contents: list):
    if isinstance(channel, ForumChannel):
        thread = await channel.create_thread(name=title)
        if thread:
            print(f"INFO: Thread created: {thread.name}")
            send = thread.send
        else:
            print("ERROR: Failed to create thread.")
            return
    else:
        send = channel.send
        await send(content=title)

    for content_tag, content in zip(content_tags, contents):
        match content_tag:
            case ContentType.TEXT:
                content = format_notice_content(content)
                for text in content:
                    await send(content=text)
            case ContentType.IMAGE:
                await send(content=content)
            case ContentType.EMBED:
                content = create_embed(**content)
                await send(embed=content)
            case _:
                print(f"ERROR: Invalid content tag: {content_tag}")
                continue
