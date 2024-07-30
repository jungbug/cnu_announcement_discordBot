import requests
from bs4 import BeautifulSoup
from info import urls


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_html(html):
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


def clean_data(posts):
    posts.pop(0)
    for post in posts:
        view = post["조회수"].replace("조회수", "").strip()
        post["조회수"] = view
    return posts


if __name__ == "__main__":
    url = urls["board_url"]
    html = get_html(url)
    posts = parse_html(html)
    posts = clean_data(posts)
    print(posts)



