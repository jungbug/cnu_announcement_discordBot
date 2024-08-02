import requests
from bs4 import BeautifulSoup
from info import urls


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def post_parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    posts = []
    rows = soup.find_all("tr")
    for row in rows:
        number = row.find('td', class_="b-num-box")
        title_box = row.find('div', class_="b-title-box")
        date = row.find('span', class_="b-date")
        writer = row.find('span', class_="b-writer")
        views = row.find('span', class_="hit")
        post_data = {'번호': number.get_text(strip=True) if number else '',
                       '제목': title_box.a.get_text(strip=True) if title_box and title_box.a else '',
                       "작성자": writer.get_text(strip=True) if writer else '',
                       '날짜': date.get_text(strip=True) if writer else '',
                       "조회수": views.get_text(strip=True) if views else '',
                       "본문링크": url + title_box.a['href'] if title_box and title_box.a else ''}
        posts.append(post_data)
    return posts


def contents_parser(posts):
    contents_list = []
    for post in posts:
        post_url = post["본문링크"]
        soup = BeautifulSoup(get_html(post_url), 'html.parser')
        trs = soup.find_all("tr")
        for tr in trs:
            contents = tr.find("div", class_="fr-view")
            contents_list.append(contents.get_text(strip=True).strip()) if contents else ''
    return contents_list


def clean_data(posts):
    posts.pop(0)
    for post in posts:
        view = post["조회수"].replace("조회수", "").strip()
        post["조회수"] = view
    return posts


def add_post_contents(posts, contents):
    for num in range(len(posts)):
        posts[num]["내용"] = contents[num]





if __name__ == "__main__":
    url = urls["board_url"]
    html = get_html(url)
    posts = post_parser(html)
    posts = clean_data(posts)
    contents = contents_parser(posts)
    add_post_contents(posts, contents)
    print(posts)



