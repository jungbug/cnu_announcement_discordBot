# 마지막 스크랩 제목
last_scraped_title = ""


# Bot TOKEN, SERVER ID, CHANNEL ID
TOKEN = 'TOEKN'  # 실제 토큰으로 교체
GUILD_ID = 1264888980684406796
CHANNEL_ID = 1264888981187858465


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    channel = discord.utils.get(guild.text_channels, id=CHANNEL_ID)
    # Start the notice scraping task
    notice_sender.start(channel)


# 1시간마다 새로운 공지사항 가져오도록 루프 돌리는 함수
@tasks.loop(minutes=60)
async def notice_sender(channel):
    global last_scraped_title
    new_scraped_notice = scrape_notice()

    if new_scraped_notice:
        new_scraped_title = new_scraped_notice["topictitle"]
        if new_scraped_title != last_scraped_title:
            print(f"[New!] {new_scraped_title}")
            await send_notice(channel, new_scraped_notice)
            last_scraped_title = new_scraped_title
        else:
            print("Keep waiting for another notice ...")
    else:
        print("No new notices found.")


# url, 제목, 내용 스크랩하는 함수
def scrape_notice():


    title = soup.select_one('#jwxe_main_content > div > div > div.bn-list-common01.type01.bn-common > table > tbody')

    if title:
        links = title.find_all('a')

        max_article_no = -1
        max_link = None

        for link in links:
            href = link.get('href')
            article_no_str = href.split('articleNo=')[1].split('&')[0]
            article_no = int(article_no_str)

            if article_no > max_article_no:
                max_article_no = article_no
                max_link = link

        if max_link:
            # https://ai.cnu.ac.kr/ai/board/notice.do?mode=view&articleNo=521598&article.offset=0&articleLimit=10
            url_result = 'https://ai.cnu.ac.kr/ai/board/notice.do' + max_link.get('href')
            data_result = requests.get(url_result, headers=headers)
            soup_result = BeautifulSoup(data_result.text, 'html.parser')
            content_div = soup_result.select_one('#jwxe_main_content > div > div > div.bn-view-common01.type01 > table > tbody > tr:nth-child(5) > td > div ')

            content = content_div.get_text(separator='\n', strip=True)
            image_url = get_image_url(soup_result)

            # 내용 포맷팅
            formatted_content = format_notice_content(content, url_result)

            return {"baseurl": url_result, "topictitle": max_link.text.strip(), "topicdesc": formatted_content, "imageurl": image_url}

    return None


def get_image_url(soup):
    # 이미지 URL 추출
    image_tag = soup.select_one('#jwxe_main_content img')
    if image_tag and image_tag.get('src'):
        return image_tag.get('src')
    return None


def format_notice_content(content, url_result):
    # 기본 내용 포맷팅
    formatted_content = content

    # 줄바꿈 및 불필요한 공백 제거
    formatted_content = formatted_content.replace('\n\n', '\n')  # 이중 줄바꿈을 단일 줄바꿈으로
    formatted_content = formatted_content.replace('\n', ' ')  # 줄바꿈을 공백으로 변경
    formatted_content = ' '.join(formatted_content.split())  # 이중 공백 제거

    # 내용 길이 제한 및 요약
    max_length = 500  # 제한 길이
    if len(formatted_content) > max_length:
        formatted_content = formatted_content[:max_length] + '... \n\n(더 보기: ' + url_result + ')'

    return formatted_content


# 디스코드로 공지사항을 보내는 함수
async def send_notice(channel, notice):
    embed = discord.Embed(
        title=notice["topictitle"],
        description=notice["topicdesc"],
        url=notice["baseurl"],
        color=discord.Color.blue()  # 임베드 색상 설정
    )

    # 이미지가 있으면 추가
    if notice["imageurl"]:
        embed.set_image(url=notice["imageurl"])

    embed.set_footer(text="충남대학교 AI 관련 공지사항")

    await channel.send(embed=embed)
