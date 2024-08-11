import dotenv
import os

# Load environment variables
dotenv.load_dotenv()


# Discord API Settings
class DiscordAPISettings:
    discord_token = os.getenv("DISCORD_TOKEN")
    discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")


# Database settings
db_file_path = os.path.join(os.path.dirname(__file__), "log.db")
DATABASE_URL = f"sqlite:///{db_file_path}"


# Target board URLs
class TargetBoardURLS(dict):
    BASE_URL = "https://ai.cnu.ac.kr/ai/board/"

    @classmethod
    def get_url(cls, board_id: str) -> str:
        return cls.BASE_URL + board_id + ".do"

    def __init__(self):
        self.notice = self.get_url("notice")            # 학사공지
        self.news = self.get_url("news")                # 교내 일반소식
        self.job = self.get_url("job")                  # 교외 활동.인턴.취업
        self.unit_news = self.get_url("unit-news")      # 사업단소식
        self.depart_news = self.get_url("depart-news")  # 학과 News
        self.events = self.get_url("events")            # 학과주최행사

        super().__init__(
            학사공지=self.notice,
            교내일반소식=self.news,
            교외활동인턴취업=self.job,
            사업단소식=self.unit_news,
            학과News=self.depart_news,
            학과주최행사=self.events
        )

        for key, value in self.items():
            setattr(self, key, value)


TargetBoardURLS = TargetBoardURLS()  # Singleton instance
