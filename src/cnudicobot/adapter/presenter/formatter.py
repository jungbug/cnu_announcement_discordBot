

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
