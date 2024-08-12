import dotenv
import os

# Load environment variables
dotenv.load_dotenv()


# Database settings
db_file_path = os.path.join(os.path.dirname(__file__), "log.db")
DATABASE_URL = f"sqlite:///{db_file_path}"


# Target board URLs
class TargetBoardURLS(dict):
    BASE_URL = "https://ai.cnu.ac.kr/ai/board/"
    BASE_URL2 = "https://computer.cnu.ac.kr/computer/notice/"

    @classmethod
    def get_url(cls, board_id: str) -> str:
        return cls.BASE_URL + board_id + ".do"

    @classmethod
    def get_url2(cls, board_id: str) -> str:
        return cls.BASE_URL2 + board_id + ".do"

    def __init__(self):
        self.notice = self.get_url("notice")            # 학사공지
        self.news = self.get_url("news")                # 교내 일반소식
        self.job = self.get_url("job")                  # 교외 활동.인턴.취업
        self.unit_news = self.get_url("unit-news")      # 사업단소식
        self.project = self.get_url2("project")         # 사업단소식(컴융)
        self.council = self.get_url2("council")         # 동아리공지사항(컴융)

        super().__init__(
            학사공지=self.notice,
            교내일반소식=self.news,
            교외활동인턴취업=self.job,
            사업단소식=self.project,  # 컴융
            동아리공지사항=self.council  # 컴융
        )

        for key, value in self.items():
            setattr(self, key, value)


TargetBoardURLS: TargetBoardURLS = TargetBoardURLS()  # Singleton instance


# Discord API Settings
class DiscordAPISettings:
    token = os.getenv("DISCORD_TOKEN")
    channel_id = dict(
        학사공지=os.getenv("DISCORD_CHANNEL_ID0"),
        교내일반소식=os.getenv("DISCORD_CHANNEL_ID1"),
        교외활동인턴취업=os.getenv("DISCORD_CHANNEL_ID2"),
        사업단소식=os.getenv("DISCORD_CHANNEL_ID3"),
        동아리공지사항=os.getenv("DISCORD_CHANNEL_ID4")
    )
