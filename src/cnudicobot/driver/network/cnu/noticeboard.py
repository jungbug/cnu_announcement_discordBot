from bs4 import BeautifulSoup
import aiohttp
import datetime
import pytz

from ...env.settings import *


# 이전에 가져온 값 저장 변수
previous_value = None

async def fetch_cnu_announcement():
    async with aiohttp.ClientSession() as session:
        url = cnu_base_url
        response = await session.get(url)
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        # tr:nth-child(11) 여기부분 수정해야함 지금은 공지가 10개라서 맞는데 나중에 바뀌면 문제 있음
        title = soup.select_one('#jwxe_main_content > div > div > div.bn-list-common01.type01.bn-common > table > tbody > tr:nth-child(11) > td.b-td-left > div > a')
        college_TA = soup.select_one('#jwxe_main_content > div > div > div.bn-list-common01.type01.bn-common > table > tbody > tr:nth-child(11) > td:nth-child(4)')
        date = soup.select_one('#jwxe_main_content > div > div > div.bn-list-common01.type01.bn-common > table > tbody > tr:nth-child(11) > td:nth-child(5)')
        return title.attrs['title'], f"{cnu_front_url+title.attrs['href']}#list", college_TA.text, date.text


async def send_announcement_to_channel(channel, announcement, link, college_TA, date):
    message = f"# 제목: {announcement}\n### 시간 : {date}\n### {college_TA}\n[바로가기]({link})"
    await channel.send(message)


async def my_function():
    global previous_value
    new_value = await fetch_cnu_announcement()
    if new_value != previous_value:
        announcement, link, college_TA, date = new_value
        print(announcement, link, college_TA, date)
        channel_id = int(discord_channel_id)
        channel = bot.get_channel(channel_id)
        if channel:
            await send_announcement_to_channel(channel, announcement, link, college_TA, date)
            previous_value = new_value
        else:
            print('채널을 찾을 수 없습니다.')
    else:
        print("새로운 공지가 없습니다.")

    print("Function executed at:", datetime.datetime.now(pytz.utc))
