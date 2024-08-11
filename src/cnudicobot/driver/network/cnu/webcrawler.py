import requests
from bs4 import BeautifulSoup

# TODO: Pretend that the crawler is a normal browser by setting the User-Agent header
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"


class Crawler:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @staticmethod
    def get_html(request_url: str) -> str | None:
        response = requests.get(request_url, headers={
            'User-Agent': USER_AGENT
        })
        if response.status_code == 200:
            return response.text
        else:
            return None

    def fetch_posts(self) -> BeautifulSoup:
        html = self.get_html(self.base_url)
        soup = BeautifulSoup(html, 'html.parser')
        return soup


class NoticeCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.crawler = Crawler(base_url)
        self.soup = self.crawler.fetch_posts()
        self.parser = Parser(self.soup)
        self.cleaner = DataCleaner(self.parser.posts)
        self.table_parser = TableParser(base_url)

    def crawl(self):
        self.parser.parse_post_list(self.base_url)
        self.cleaner.clean_data()
        self.parse_contents_and_images_and_files()

    def parse_contents_and_images_and_files(self):
        for post in self.parser.posts:
            post_url = post["본문링크"]
            content_soup = BeautifulSoup(self.crawler.get_html(post_url), 'html.parser')
            self.parser.parse_contents(post, content_soup)
            self.parser.parse_images(post, content_soup)
            self.parser.parse_files(post, content_soup)

    def parse_tables(self):
        for post in self.parser.posts:
            post_url = post["본문링크"]
            dfs = self.table_parser.table_main(post_url)
            if dfs:
                post["is_table"] = 1
                post["table"] = dfs
            else:
                post["is_table"] = 0
                post["table"] = None
