from crawling import get_html
from crawling import post_parser
from crawling import contents_parser
from crawling import clean_data
from crawling import add_post_contents
from crawling import add_post_tables
from crawling import parse_html_table
from crawling import find_tables
from crawling import table_main
from crawling import save_to_json
from info import urls

if __name__ == "__main__":
    url = urls["page2_url"]
    html = get_html(url)
    posts = post_parser(html)
    posts = clean_data(posts)
    contents = contents_parser(posts)
    add_post_contents(posts, contents)
    for post in posts:
        post_url = post["본문링크"]
        print(post["번호"])
        dfs = table_main(post_url)
        add_post_tables(posts, dfs)
        for df in dfs:
            print(df)
    save_to_json(posts,'posts_data.json')