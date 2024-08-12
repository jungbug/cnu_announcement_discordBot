from enum import Enum

from ...driver.network.discord.api import Embed, Color


class ContentType(Enum):
    TEXT = "text"
    IMAGE = "image"
    EMBED = "embed"


def format_notice_content(content: str, max_length=500) -> list[str]:
    # split the content based on the max length
    if len(content) > max_length:
        formatted_content = []
        split_content = content.split('\n')
        current_content = ""
        for line in split_content:
            if len(current_content) + len(line) > max_length:
                formatted_content.append(current_content)
                current_content = ""
            current_content += line + '\n'
    else:
        formatted_content = [content]
    return formatted_content


def create_embed(
        title: str, description: str, url: str | None = None, image_url: str | None = None, footer: str | None = None
):
    embed = Embed(
        title=title,
        description=description,
        url=url,
        color=Color.greyple()
    )

    if image_url:
        embed.set_image(url=image_url)

    if footer:
        embed.set_footer(text=footer)

    return embed
