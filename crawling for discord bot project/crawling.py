import json

import pandas as pd
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
        content = soup.find("div", class_="fr-view")
        contents_list.append(content.get_text(strip=True).strip()) if content else contents_list.append('')
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


def add_post_tables(posts, dfs):
    if len(dfs) != 0:
        post["is_table"] = 1
        post["table"] = [df.to_json(orient='split') for df in dfs]
    else:
        post["is_table"] = 0
        post["table"] = None


def parse_html_table(table):
    rows = table.find_all("tr")
    table_data = []
    columns = []
    rowspan_dict = {}

    for i, row in enumerate(rows):
        tds = row.find_all(["td", "th"])
        row_data = []
        col_idx = 0
        while col_idx in rowspan_dict:
            if rowspan_dict[col_idx][1] > 0:
                row_data.append(rowspan_dict[col_idx][0])
                rowspan_dict[col_idx][1] -= 1
                if rowspan_dict[col_idx][1] == 0:
                    del rowspan_dict[col_idx]
                col_idx += 1
            else:
                del rowspan_dict[col_idx]

        for td in tds:
            spans = td.find_all("span")
            ps = td.find_all("p")
            if spans:
                cell_text = " ".join([span.get_text(strip=True) for span in spans])
            elif ps:
                cell_text = " ".join([p.get_text(strip=True) for p in ps])
            else:
                cell_text = td.get_text(strip=True)
            colspan = int(td.get("colspan", 1))
            rowspan = int(td.get("rowspan", 1))

            for _ in range(colspan):
                row_data.append(cell_text)
                if rowspan > 1:
                    rowspan_dict[col_idx] = [cell_text, rowspan - 1]
                col_idx += 1

        if i == 0:
            columns = row_data
        else:
            while len(row_data) < len(columns):
                row_data.append("")
            table_data.append(row_data)

    return pd.DataFrame(table_data, columns=columns)



def find_tables(soup):
    trs = soup.find_all("tr")
    tables = []
    seen_tables = set()
    for tr in trs:
        is_td = tr.find("td", class_="b-no-right")
        is_div = is_td.find("div", class_="fr-view") if is_td else None
        table_elements = is_div.find_all("table") if is_div else None
        if table_elements:
            for table in table_elements:
                table_str = str(table)
                if table_str not in seen_tables:
                    seen_tables.add(table_str)
                    tables.append(table)
    return tables


def table_main(post_url):
    soup = BeautifulSoup(get_html(post_url), 'html.parser')
    tables = find_tables(soup)
    dfs = []
    for table in tables:
        df = parse_html_table(table)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_columns', None)
        dfs.append(df)
    return dfs


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)







if __name__ == "__main__":
    url = urls["board_url"]
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




