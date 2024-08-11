import discord
from discord.ext import commands, tasks

TOKEN = 'TOKEN'

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # 서버 멤버 인텐트 활성화
intents.presences = True  # 프레즌스 인텐트 활성화

bot = commands.Bot(command_prefix='!', intents=intents)

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

            second_text = """
1. 목적 및 배경

     o 저학년들을 대상으로 비전 관련 인공지능 태스크를 처리해보는 경험을 가질 수 있도록 하여 인공지능 공부를 보다 더 가깝게 느낄 수 있도록 하기 위함

     o 인공지능을 공부하고 있는 학생들에게 대회를 통해 방향성을 잘 잡을 수 있도록 유도하기 위함



2. 세부내용

o 행 사 명 : dAiv AI Competition[2024] Basic (다이브 AI 컴페티션[2024] 베이직)

o 행사일시 : 최종발표회 - 2024년 08월 30일 금요일

  결과발표회 및 시상식 - 2024년 9월 중 예정

o 장 소 : 다이브 디스코드 대회 회의실, 학내 공대 5호관 강의실

o 참가대상 : 충남대학교 1, 2학년 재학생으로 이루어진 5인 이하의 팀 (단, 팀원 중 다이브 소속 회원이 한 명 이상 있어야 하며, 한 팀에서 2학년의 수는 최대 2명으로 제한)

o 참가인원 : 10팀(20명) 내외

o 진행요원 : 다이브 회장, 다이브 기획부(기획부장, 기획부 인턴)

o 지도교수 : 충남대학교 공과대학 인공지능학과 권진근 교수님

o 주 최 : 충남대학교 공과대학 인공지능학과 학술동아리 dAiv(다이브)

o 주 관 : 충남대학교 소프트웨어중심대학사업단

o 추진 일정





3. 행사 진행 방법



 가. 홍보

    o 대회 포스터 제작하여 동아리 내 공지 채널을 통해 참여 독려

    o 다이브 온라인 홈페이지에 참여 신청 페이지를 개설하여 홍보

       - https://daiv-cnu.github.io/contest/coding/ai_competition[2024]_basic.html



 나. 신청 및 접수

    o 다이브 온라인 홈페이지를 통해 신청 폼 작성

    o 익명 질문 플랫폼을 통한 대회 신청 관련 질의응답 진행



 다. 교육 내용

  o 저학년들의 대회 참여를 돕기 위해 PyTorch의 경우 베이스라인 코드가, TensorFlow의 경우 코드 생성기가 제공될 예정으로, 인공지능에 대한 경험이 적은 경우에도 대회를 참여할 수 있도록 함

  o 제공되는 AI 개발 환경과, 코드 생성기 관련 교육을 대회 OT에서 진행할 예정임



 라. 대회 방법

    o 11개의 Class가 존재하는 이미지 Classification 태스크가 주어질 예정으로, 데이터셋과 관련된 내용은 대회 오리엔테이션에서 공개될 예정임

    o 학습 과정에 필요한 연산 처리를 위한 GPU 서버가 제공될 예정임 (학과 GPU)

    o 참가자들은 제공된 BaseLine 코드를 바탕으로 모델을 수정하거나, 코드 생성기를 이용하여 모델을 설계하여 학습시킨 후, Evaluation DataSet을 대상으로 분류 작업을 수행한 .csv 파일을 대시보드에 업로드하여 결과 확인

    o Pre-Trained모델은 사용이 불가능하며, 모델 구조만 불러와 사용하는 것은 가능

    o 제공되지 않은 타 출처 DataSet을 허가 없이 사용하는 것은 불가능

    o Test DataSet을 학습에 사용하는 것은 불가능



 마. 평가 방법

    o 참가자들은 각 제출 기간(1차, 2차, 최종) 동안 다이브 홈페이지의 리더보드를 활용하여 .csv 파일을 업로드하여 자신의 실시간 등수 확인 가능

    o 최종 점수 산출 비율: 제출된 모델의 test 셋 예측 성능(30%) + 코드 가독성 및 참신함(30%) + 세미나 발표(40%) (단, 세미나는 제출 모델 test셋 예측 성능 상위 일부 팀만 진행할 예정입니다.) (동점자가 발생할 경우, 리더보드에 먼저 제출한 참가자의 등수가 높음)



 바. 시상 내역 (총 상금 50만원 / 6팀)


"""

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

bot.run(TOKEN)
