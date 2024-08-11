TOKEN = 'TOKEN'

# 포럼 채널 ID를 여기에 입력하세요
FORUM_CHANNEL_ID = 1271636906614063258


# 주기적으로 포스트를 생성하는 태스크
@tasks.loop(hours=24)  # 24시간마다 실행
async def create_forum_post():
    channel = bot.get_channel(FORUM_CHANNEL_ID)

    if isinstance(channel, discord.ForumChannel):
        # 포스트 제목 설정
        post_title = "[dAiv ] dAiv AI Competition[2024] - Basic (다이브 AI 컴페티션 2024 - 베이직)"

        # 첫 번째 본문 텍스트
        first_text = "Tutle"
        image_url = 'https://ai.cnu.ac.kr/_attach/image/editor_image/2024/07/uMviMrJpVtiuuThtJlru0.png'

        #포럼 게시물 생성
        thread = await channel.create_thread(name=post_title, content=image_url)

        if thread:
            print(f'Thread created: {thread.name}')

            # 스레드에 두 번째 본문 텍스트 추가
            await thread.send(content=second_text)

            image_url2 = 'https://ai.cnu.ac.kr/_attach/image/editor_image/2024/07/MyOefvtNQSrBwIIpUZhn0.png'
            await thread.send(content=image_url2)
            await thread.send('https://ai.cnu.ac.kr/ai/community/free.do?mode=download2&articleNo=519913&attachNo=402544')
        else:
            print('Failed to create thread.')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    create_forum_post.start()  # 봇이 실행될 때 태스크 시작
