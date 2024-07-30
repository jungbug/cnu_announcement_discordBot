import requests
from bs4 import BeautifulSoup
from info import url


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_html(html):
    soup = BeautifulSoup(get_html(url["board_url"]), 'html.parser')
    notices = []
    rows = soup.find_all("tr")
    for row in rows:
        number = row.find('td', class_="b-num-box")
        title_box = row.find('div', class_="b-title-box")
        date = row.find('span', class_="b-date")
        writer = row.find('span', class_="b-writer")
        views = row.find('span', class_="hit")
        notice_data = {'번호': number.get_text(strip=True) if number else '',
                       '제목': title_box.a.get_text(strip=True) if title_box and title_box.a else '',
                       "작성자": writer.get_text(strip=True) if writer else '',
                       '날짜': date.get_text(strip=True) if writer else '',
                       "조회수": views.get_text(strip=True) if views else '',
                       "본문링크": url["board_url"] + title_box.a['href'] if title_box and title_box.a else ''}
        notices.append(notice_data)
    return notices


def clean_data(notices):
    notices.pop(0)
    for notice in notices:
        view = notice["조회수"].replace("조회수", "").strip()
        notice["조회수"] = view
    return notices


if __name__ == "__main__":
    url = url["board_url"]
    html = get_html(url)
    notices = parse_html(html)
    clean_data(notices)



